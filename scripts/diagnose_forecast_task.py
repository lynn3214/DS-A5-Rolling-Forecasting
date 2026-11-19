#!/usr/bin/env python
"""Development-only, point-in-time-safe MetroPT-3 TP2 diagnostics."""
import argparse,hashlib,json,time
from pathlib import Path
from datetime import datetime,timezone
import numpy as np,pandas as pd
VERSION='3.0.0'; CUTOFF=np.datetime64('2020-08-01T00:00:00'); HORIZONS=(10,600,3600); TOL=5.; GAP=60.
def match_future(ts,nominal,tolerance=TOL):
    ix=np.searchsorted(ts,nominal,side='left'); ok=ix<len(ts); safe=np.minimum(ix,len(ts)-1); ok &= ts[safe] <= nominal+tolerance
    return np.where(ok,ix,-1)
def reference_match(ts,nominal,tolerance=TOL):
    return np.array([next((i for i,x in enumerate(ts) if q<=x<=q+tolerance),-1) for q in nominal],dtype=int)

def label_eligible(ts,issue_idx,target_idx,origin_s):
    ok=(target_idx>=0); safe=np.maximum(target_idx,0)
    ok &= ts[safe] <= origin_s
    return ok
def gap_crossings(ts,src,dst,threshold=GAP):
    gaps=np.diff(ts); bad=np.flatnonzero(gaps>threshold)
    return np.searchsorted(bad,dst,side='left')>np.searchsorted(bad,src,side='left')
def hash_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
      for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data',type=Path,default=Path('data/raw/metropt3/MetroPT3(AirCompressor).csv')); ap.add_argument('--out',type=Path,default=Path('results/audit/forecasting_task_diagnostics.json')); a=ap.parse_args(); st=time.perf_counter()
    # Timestamp-only pass identifies the strict cutoff. Target values are loaded only for development rows.
    allts=pd.read_csv(a.data,usecols=['timestamp'],parse_dates=['timestamp']).timestamp.to_numpy(dtype='datetime64[ns]'); cut=int(np.searchsorted(allts,CUTOFF)); ts=allts[:cut].astype('int64')/1e9; dev_dt=allts[:cut]
    y=pd.read_csv(a.data,usecols=['TP2'],nrows=cut).TP2.to_numpy(float); n=len(ts); origins=[(np.datetime64(f'2020-{m:02d}-01'),np.datetime64(f'2020-{m:02d}-15')) for m in range(3,8)]; horizons={}
    for h in HORIZONS:
      nominal=ts+h; ix=match_future(ts,nominal); has=ix>=0; safe=np.maximum(ix,0); val=has & np.isfinite(y) & np.isfinite(y[safe]); gap=has & gap_crossings(ts,np.arange(n),safe); eligible=val&~gap; rows=np.flatnonzero(eligible); dst=ix[eligible]; delta=y[dst]-y[rows]
      # interval summaries over the same eligible pairs
      corr=float(np.corrcoef(y[rows],y[dst])[0,1]) if len(rows)>1 and np.std(y[rows])>0 and np.std(y[dst])>0 else None
      origins_data=[]
      for o,e in origins:
        os=o.astype('datetime64[s]').astype('int64'); es=e.astype('datetime64[s]').astype('int64')
        train=eligible & (ts<os) & (ts[ix.clip(0,n-1)]<=os)
        ev=eligible & (ts>=os)&(ts<es)&(ts[ix.clip(0,n-1)]<es)
        origins_data.append({'origin':str(o),'evaluation_end_exclusive':str(e),'training_pairs':int(train.sum()),'evaluation_pairs':int(ev.sum())})
      # strict observed target-time boundary check
      horizons[str(h)]={'issue_count':n,'target_match_count':int(has.sum()),'missing_match_count':int((~has).sum()),'eligible_pair_count':int(eligible.sum()),'gap_exclusions':int((val&gap).sum()),'invalid_issue_or_target_value_count':int((has&~val).sum()),'coverage_denominator':n,'coverage':float(eligible.sum()/n),'pair_correlation':corr,'correlation_pair_count':int(len(rows) if corr is not None else 0),'abs_change_quantiles':{str(q):float(np.quantile(np.abs(delta),q)) for q in [0,.5,.9,.99,1]},'origins':origins_data}
      if h==3600:
        nexti=np.searchsorted(ts,nominal,side='left'); exist=nexti<n; delay=np.full(n,np.nan); delay[exist]=ts[nexti[exist]]-nominal[exist]
        unmatched=~has; sample=np.flatnonzero(unmatched)[::max(1,int(unmatched.sum()/20))][:20]
        horizons[str(h)]['matching_diagnostic']={'first_subsequent_delay_quantiles_seconds':{str(q):float(np.nanquantile(delay,q)) for q in [0,.5,.9,.99,1]},'first_subsequent_within_tolerance_fraction':float(np.mean(delay[exist]<=TOL)),'unmatched_sample_issue_timestamps':[str(dev_dt[i]) for i in sample],'issue_phase_mod_3600_seconds_quantiles':{str(q):float(np.quantile(np.mod(ts[rows],3600),q)) for q in [0,.25,.5,.75,1]}}
    # final timestamps only, no final target values
    final=allts[cut:]; windows=[]
    for name,a0,b0 in [('F1','2020-08-01','2020-08-06'),('F2','2020-08-07','2020-08-12'),('F3','2020-08-13','2020-08-18'),('F4','2020-08-19','2020-08-24'),('F5','2020-08-25','2020-08-30')]:
      m=(final>=np.datetime64(a0))&(final<np.datetime64(b0)); z=final[m]; windows.append({'id':name,'start_inclusive':a0,'end_exclusive':b0,'timestamp_count':int(m.sum()),'first':str(z[0]) if len(z) else None,'last':str(z[-1]) if len(z) else None,'label_count':'NOT_INSPECTED'})
    out={'schema_version':'1.1','diagnostic_version':VERSION,'input_sha256':hash_file(a.data),'script_sha256':hash_file(Path(__file__)),'input_bytes':a.data.stat().st_size,'execution_utc':datetime.now(timezone.utc).isoformat(),'command':'conda run -n nussem1 python scripts/diagnose_forecast_task.py','development_cutoff_exclusive':'2020-08-01T00:00:00','development_rows':n,'timestamp_timezone':'naive/unknown','matching_rule':'earliest observation in [issue+horizon, issue+horizon+5s]','gap_threshold_seconds':GAP,'horizons':horizons,'final_timestamp_windows':windows,'final_target_values_loaded':False,'runtime_seconds':time.perf_counter()-st}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
