#!/usr/bin/env python
"""Read-only reconstruction of Phase 2B coverage, features, and metrics."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from src.temporal import match_target,construct_features,FEATURES,SPEC,HORIZON,TOL_NS,GAP_NS
DATA=Path('data/raw/metropt3/MetroPT3(AirCompressor).csv')
DEV=[('D1','2020-03-01','2020-03-15'),('D2','2020-04-01','2020-04-15'),('D3','2020-05-01','2020-05-15'),('D4','2020-06-01','2020-06-15'),('D5','2020-07-01','2020-07-15')]
FINAL=[('F1','2020-08-01','2020-08-06'),('F2','2020-08-07','2020-08-12'),('F3','2020-08-13','2020-08-18'),('F4','2020-08-19','2020-08-24'),('F5','2020-08-25','2020-08-30')]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def metrics(e):
 return {'count':int(len(e)),'mae':float(np.mean(np.abs(e))) if len(e) else None,'rmse':float(np.sqrt(np.mean(e*e))) if len(e) else None}
def scalar_feature_lookup(ts,values,issue_idx,lag_seconds,gap_rows):
 req=int(ts[issue_idx]-lag_seconds*1_000_000_000); j=int(np.searchsorted(ts,req,side='right')-1)
 if j<0: return -1,'no_past_observation'
 if req-ts[j]>TOL_NS: return -1,'stale_observation_over_5s'
 if not np.isfinite(values[j]): return -1,'nonfinite_feature'
 # Independently inspect whether any >60s interval index lies in [j, issue_idx).
 left=int(np.searchsorted(gap_rows,j,side='left')); right=int(np.searchsorted(gap_rows,issue_idx,side='left'))
 if right>left: return -1,'prohibited_history_gap'
 return j,None
def main():
 m=json.loads(Path('docs/evaluation_protocol_freeze_manifest.json').read_text()); d=json.loads(Path('results/audit/forecasting_task_diagnostics.json').read_text()); c='ca83f0a295a68337aebc070cfd481645418cda13'
 for p,h in {**m['document_sha256'],m['diagnostics']['path']:m['diagnostics']['sha256'],**m['source_script_sha256']}.items(): assert hashlib.sha256(subprocess.check_output(['git','show',f'{c}:{p}'])).hexdigest()==h
 assert sha(DATA)==m['dataset']['sha256']==d['input_sha256']
 df=pd.read_csv(DATA,usecols=['timestamp','TP2','TP3','Motor_current'],parse_dates=['timestamp']); ts=df.timestamp.to_numpy(dtype='datetime64[ns]').astype('int64'); y=df.TP2.to_numpy(float); arrays={k:df[k].to_numpy(float) for k in ['TP2','TP3','Motor_current']}; assert np.all(np.diff(ts)>=0)
 X,prov,feat_ok=construct_features(ts,arrays); gap_idx=np.flatnonzero(np.diff(ts)>GAP_NS); funnels=[]; counts=[]; feature_failures=[]; recalcs={}; spots=[]; target_spots=[]
 def funnel(issue,role,oid,O,B):
  nominal=ts[issue]+HORIZON*1_000_000_000; target=match_target(ts,issue); matched=target>=0; safe=np.maximum(target,0)
  finite=matched&np.isfinite(y[issue])&np.isfinite(y[safe]); tg=np.zeros(len(issue),bool); q=np.flatnonzero(finite); tg[q]=np.searchsorted(gap_idx,target[q],side='left')>np.searchsorted(gap_idx,issue[q],side='left'); no_gap=finite&~tg
  av=np.zeros((len(issue),len(SPEC)),bool); fg=np.zeros_like(av)
  for j,(col,lag) in enumerate(SPEC):
   req=ts[issue]-lag*1_000_000_000; ix=np.searchsorted(ts,req,side='right')-1; has=ix>=0; sf=np.maximum(ix,0)
   av[:,j]=has&(req>=ts[sf])&((req-ts[sf])<=TOL_NS)&np.isfinite(arrays[col][sf])
   z=np.flatnonzero(av[:,j]); fg[z,j]=np.searchsorted(gap_idx,issue[z],side='left')>np.searchsorted(gap_idx,ix[z],side='left')
  cum=no_gap.copy(); steps=[('candidate_issues',np.ones(len(issue),bool)),('valid_future_target_match',matched),('finite_issue_and_target_tp2',finite),('issue_target_gap_pass',no_gap)]
  independent={}
  for j,name in enumerate(FEATURES):
   independent[name]={'unavailable_without_gap_test':int((no_gap&~av[:,j]).sum()),'gap_failure_when_value_available':int((no_gap&av[:,j]&fg[:,j]).sum())}
   cum &= av[:,j]; steps.append((f'{name}_available',cum.copy()))
  after_gaps=cum&~fg.any(axis=1); steps.append(('all_feature_history_gaps_pass',after_gaps))
  if role=='training':
   label_ok=matched&(ts[safe]<=O); final=after_gaps&label_ok; steps.append(('actual_label_available_by_origin',final))
  else:
   target_window=matched&(ts[safe]<B); steps.append(('target_inside_evaluation_window',no_gap&target_window)); final=after_gaps&target_window; steps.append(('all_features_and_eval_boundary',final))
  prev=np.ones(len(issue),bool)
  for name,mask in steps:
   funnels.append({'origin_id':oid,'role':role,'stage':name,'remaining_count':int(mask.sum()),'excluded_since_prior_stage':int((prev&~mask).sum())});prev=mask
  for j,name in enumerate(FEATURES): feature_failures.append({'origin_id':oid,'role':role,'feature':name,'base_population_after_target_gap':int(no_gap.sum()),'unavailable_independent':int((no_gap&~av[:,j]).sum()),'gap_failure_when_feature_value_available':int((no_gap&av[:,j]&fg[:,j]).sum()),'eligible_independent_after_own_gap':int((no_gap&av[:,j]&~fg[:,j]).sum())})
  valid_eval=no_gap&matched&(ts[safe]<B) if role=='evaluation' else None
  return {'issue_count':len(issue),'target_match_count':int(matched.sum()),'finite_issue_target_count':int(finite.sum()),'issue_target_gap_exclusions':int((finite&tg).sum()),'valid_evaluation_target_pair_count':int(valid_eval.sum()) if role=='evaluation' else None,'valid_evaluation_issue_rows':issue[valid_eval].astype(int).tolist() if role=='evaluation' else None,'feature_history_eligible_count':int(after_gaps.sum()),'final_eligible_count':int(final.sum()),'independent_feature_failures':independent}
 for phase,windows in [('development',DEV),('final',FINAL)]:
  raw=pd.read_csv(f'results/rolling/{phase}_predictions.csv'); summ=json.loads(Path(f'results/rolling/{phase}_metrics.json').read_text()); recalcs[phase]={}
  for fold in summ['origins']:
   oid=fold['origin_id']; _,sa,sb=next(w for w in windows if w[0]==oid); O=int(np.datetime64(sa).astype('datetime64[ns]').astype('int64')); B=int(np.datetime64(sb).astype('datetime64[ns]').astype('int64'))
   train_issue=np.flatnonzero(ts<O); eval_issue=np.flatnonzero((ts>=O)&(ts<B)); tf=funnel(train_issue,'training',oid,O,B); ef=funnel(eval_issue,'evaluation',oid,O,B)
   g=raw[raw.origin_id==oid]; assert g.issue_row.nunique()==len(eval_issue); persistence_rows=g[g.method=='persistence']; assert int(persistence_rows.target_pair_eligible.sum())==ef['valid_evaluation_target_pair_count']; assert set(persistence_rows.loc[persistence_rows.target_pair_eligible,'issue_row'].astype(int))==set(ef['valid_evaluation_issue_rows'])
   assert g.groupby('issue_row').target_pair_eligible.nunique().max()==1
   ridge_rows=g[g.method=='ridge']; assert not (ridge_rows.prediction_available & ~ridge_rows.feature_eligible).any(); assert np.array_equal(ridge_rows.prediction_available.to_numpy(bool),ridge_rows.feature_eligible.to_numpy(bool) if fold.get('status')=='COMPLETED' else np.zeros(len(ridge_rows),dtype=bool))
   rec={'phase':phase,'origin_id':oid,'candidate_issue_count':len(eval_issue),'valid_target_pairs':int(g[g.method=='persistence'].target_pair_eligible.sum()),'training_target_eligible_from_funnel':int(tf['final_eligible_count']),'training_feature_complete_after_actual_label_boundary':int(tf['final_eligible_count']),'methods':{},'common_identity':'(origin_id, issue_row, matched_target_row)' }
   for method,gm in g.groupby('method'):
    avail=gm.prediction_available.to_numpy(bool); label=gm.target_pair_eligible.to_numpy(bool); score=avail&label; e=gm.loc[score,'prediction'].to_numpy()-gm.loc[score,'observed_tp2'].to_numpy(); tid=gm.loc[score,'target_row'].dropna().astype(int)
    mrec={'phase':phase,'origin_id':oid,'method':method,'candidate_issue_count':len(eval_issue),'valid_target_pair_count':int(gm.target_pair_eligible.sum()),'available_prediction_count':int(avail.sum()),'available_with_valid_target':int(score.sum()),'scored_prediction_count':int(score.sum()),'missing_or_invalid_target_count':int((~label).sum()),'no_future_match_count':int((gm.target_pair_reason=='no_future_match_within_tolerance').sum()),'nonfinite_target_count':int((gm.target_pair_reason=='nonfinite_issue_or_target').sum()),'issue_target_gap_exclusion_count':int((gm.target_pair_reason=='prohibited_issue_target_gap').sum()),'target_outside_eval_boundary_count':int((gm.target_pair_reason=='target_outside_evaluation_window').sum()),'missing_prediction_count':int((~avail).sum()),'unique_issue_ids':int(gm.issue_row.nunique()),'unique_target_ids':int(tid.nunique()),'duplicate_prediction_ids':int(gm.duplicated(['issue_row','target_row']).sum()),**metrics(e)}
    rec['methods'][method]=mrec
    counts.append(mrec)
    assert score.sum()<=label.sum() and score.sum()<=avail.sum()
    fm=fold.get('method_metrics',{}).get(method,{})
    assert fm.get('count',0)==len(e) and ((fm.get('mae') is None and not len(e)) or np.isclose(fm['mae'],metrics(e)['mae'])) and ((fm.get('rmse') is None and not len(e)) or np.isclose(fm['rmse'],metrics(e)['rmse']))
   pivot=g[g.target_pair_eligible&g.prediction_available].pivot_table(index=['issue_row','target_row'],columns='method',values='prediction',aggfunc='first').reindex(columns=['persistence','seasonal_naive','ridge']); common=pivot.dropna(); rec['common_identity']='(origin_id, original issue_row, actual target_row)'; rec['common_count']=len(common)
   timestamp_sets=[set(g[(g.method==z)&g.target_pair_eligible&g.prediction_available].actual_target_timestamp.dropna().astype(str)) for z in ['persistence','seasonal_naive','ridge']]; common_timestamps=set.intersection(*timestamp_sets); rec['common_target_timestamp_only_count']=len(common_timestamps)
   rec['common_timestamp_without_shared_issue_count']=sum(not set.intersection(*[set(g.loc[(g.actual_target_timestamp.astype(str)==stamp)&(g.method==z)&g.target_pair_eligible&g.prediction_available,'issue_row'].astype(int)) for z in ['persistence','seasonal_naive','ridge']]) for stamp in common_timestamps)
   for mr in counts[-3:]: mr['common_issue_target_count']=len(common); mr['common_target_timestamp_only_count']=len(common_timestamps); mr['common_timestamp_without_shared_issue_count']=rec['common_timestamp_without_shared_issue_count']
   common_metrics={}
   lab=g[(g.method=='persistence')&g.target_pair_eligible&g.prediction_available].set_index(['issue_row','target_row']).observed_tp2
   for method in ['persistence','seasonal_naive','ridge']:
    e=common[method].to_numpy()-lab.loc[common.index].to_numpy() if len(common) else np.array([]); common_metrics[method]=metrics(e)
   fm=fold.get('common_target_count'); assert fm==len(common)
   rec['common_metrics']=common_metrics;recalcs[phase][oid]={'method_specific':{k:{'count':v['scored_prediction_count'],'mae':v['mae'],'rmse':v['rmse']} for k,v in rec['methods'].items()},'common_count':len(common),'common_metrics':common_metrics}
 # deterministic scalar/vectorized parity; sampled rows across beginning/end of archive, no outcome-based selection
 rng=np.random.default_rng(20261119); ids=np.unique(np.r_[rng.choice(min(100000,len(ts)),min(50,len(ts)),replace=False),rng.choice(np.arange(max(0,len(ts)-100000),len(ts)),min(50,len(ts)),replace=False)])
 for i in ids:
  for j,(col,lag) in enumerate(SPEC):
   q,reason=scalar_feature_lookup(ts,arrays[col],int(i),lag,gap_idx); v=int(prov[i,j]); assert q==v
   spots.append({'issue_row':int(i),'issue_timestamp_ns':int(ts[i]),'feature':FEATURES[j],'requested_timestamp_ns':int(ts[i]-lag*1_000_000_000),'matched_row':q if q>=0 else None,'matched_timestamp_ns':int(ts[q]) if q>=0 else None,'exclusion_reason':reason})
 # Scalar target matcher parity over deterministic timestamps spread across the archive.
 target_ids=np.unique(np.r_[rng.choice(min(200000,len(ts)),min(100,len(ts)),replace=False),rng.choice(np.arange(max(0,len(ts)-200000),len(ts)),min(100,len(ts)),replace=False)])
 for i in target_ids:
  req=int(ts[i]+HORIZON*1_000_000_000); first=int(np.searchsorted(ts,req,side='left')); scalar=first if first<len(ts) and ts[first]<=req+5_000_000_000 else -1; vec=int(match_target(ts,np.array([i]))[0]); assert (scalar if scalar>=0 else -1)==vec
  target_spots.append({'issue_row':int(i),'issue_timestamp_ns':int(ts[i]),'nominal_target_ns':req,'first_future_row':first if first<len(ts) else None,'first_future_timestamp_ns':int(ts[first]) if first<len(ts) else None,'matched_row':vec if vec>=0 else None,'matched_timestamp_ns':int(ts[vec]) if vec>=0 else None,'exclusion_reason':None if vec>=0 else 'no_observation_in_future_5s_tolerance'})
 out=Path('results/audit');out.mkdir(parents=True,exist_ok=True);pd.DataFrame(funnels).to_csv(out/'phase2b_coverage_funnel.csv',index=False);pd.DataFrame(counts).to_csv(out/'phase2b_count_reconciliation.csv',index=False);pd.DataFrame(feature_failures).to_csv(out/'phase2b_feature_failures.csv',index=False);pd.DataFrame(spots).to_csv(out/'phase2b_lookup_spot_checks.csv',index=False);pd.DataFrame(target_spots).to_csv(out/'phase2b_target_spot_checks.csv',index=False)
 pooled={}
 for phase in ['development','final']:
  raw=pd.read_csv(f'results/rolling/{phase}_predictions.csv'); summary=json.loads(Path(f'results/rolling/{phase}_metrics.json').read_text())
  valid=raw[raw.target_pair_eligible&raw.prediction_available]; pm={}
  for method,g in valid.groupby('method'):
   e=g.prediction.to_numpy()-g.observed_tp2.to_numpy(); pm[method]=metrics(e)
   ref=summary['pooled_method_specific'][method]; assert pm[method]['count']==ref['count'] and ((pm[method]['mae'] is None and ref['mae'] is None) or np.isclose(pm[method]['mae'],ref['mae'])) and ((pm[method]['rmse'] is None and ref['rmse'] is None) or np.isclose(pm[method]['rmse'],ref['rmse']))
  piv=valid.pivot_table(index=['origin_id','issue_row','target_row'],columns='method',values='prediction',aggfunc='first').reindex(columns=['persistence','seasonal_naive','ridge']).dropna(); common={}
  lab=valid[valid.method=='persistence'].set_index(['origin_id','issue_row','target_row']).observed_tp2
  for method in ['persistence','seasonal_naive','ridge']:
   e=piv[method].to_numpy()-lab.loc[piv.index].to_numpy() if len(piv) else np.array([]); common[method]=metrics(e)
   ref=summary['pooled_common_targets'][method]; assert common[method]['count']==ref['count'] and ((common[method]['mae'] is None and ref['mae'] is None) or np.isclose(common[method]['mae'],ref['mae'])) and ((common[method]['rmse'] is None and ref['rmse'] is None) or np.isclose(common[method]['rmse'],ref['rmse']))
  pooled[phase]={'method_specific':pm,'common_population_count':len(piv),'common_metrics':common}
 Path(out/'phase2b_metric_recalculation.json').write_text(json.dumps({'status':'PASS','identity':'origin_id + original issue_row + actual target_row','recalculated':recalcs,'pooled_recalculation':pooled,'hashes':{p:sha(Path(p)) for p in ['data/raw/metropt3/MetroPT3(AirCompressor).csv','results/rolling/development_predictions.csv','results/rolling/development_metrics.json','results/rolling/final_predictions.csv','results/rolling/final_metrics.json']}},indent=2))
 print(json.dumps({'status':'PASS','funnel_rows':len(funnels),'origin_rows':len(counts),'feature_spot_checks':len(spots),'target_spot_checks':len(target_spots)},indent=2))
if __name__=='__main__':main()
