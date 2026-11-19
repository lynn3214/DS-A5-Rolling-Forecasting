#!/usr/bin/env python
"""Vectorized independent integrity checks for rolling outputs."""
import argparse,json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd
from src.temporal import match_target

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['development','final'],required=True);a=ap.parse_args();base=Path('results/rolling'); rawp=base/f'{a.phase}_predictions.csv'; metp=base/f'{a.phase}_metrics.json'; dat=Path('data/raw/metropt3/MetroPT3(AirCompressor).csv')
 d=pd.read_csv(dat,usecols=['timestamp','TP2'],parse_dates=['timestamp']); ts=d.timestamp.to_numpy(dtype='datetime64[ns]').astype('int64'); y=d.TP2.to_numpy(float); raw=pd.read_csv(rawp); summary=json.loads(metp.read_text()); checks=[]
 assert len(raw)%3==0 and set(raw.method.unique())=={'persistence','seasonal_naive','ridge'}; checks.append('three methods per candidate issue')
 assert (raw.groupby(['origin_id','issue_row']).method.nunique()==3).all(); checks.append('method row completeness')
 valid=raw[raw.target_pair_eligible].drop_duplicates(['origin_id','issue_row']); issues=valid.issue_row.to_numpy(dtype=int); targets=valid.target_row.to_numpy(dtype=int); expected=match_target(ts,issues); assert np.array_equal(targets,expected)
 assert np.all(ts[targets]>=ts[issues]+600_000_000_000)&np.all(ts[targets]<=ts[issues]+605_000_000_000)
 assert np.allclose(valid.observed_tp2.to_numpy(),y[targets]); checks.append('target indices, labels, future-only tolerance independently match original data')
 assert raw.loc[raw.prediction_available,'prediction'].notna().all() and raw.loc[~raw.prediction_available,'prediction'].isna().all(); checks.append('prediction finite/unavailable consistency')
 for fold in summary['origins']:
  oid=fold['origin_id']; g=raw[raw.origin_id==oid]
  assert len(g)==fold['candidate_issue_count']*3
  if fold['status']=='COMPLETED':
   assert fold['scaler_fit_row_count']==fold['training_sample_count']
   assert fold['ridge_params']=={'alpha':1.0,'fit_intercept':True,'solver':'svd'}
   assert fold['common_target_count']==int(g[g.common_target].issue_row.nunique())
 checks.append('fold counts, scaler rows, fixed Ridge params, common target IDs')
 eligible=raw[raw.target_pair_eligible & raw.prediction_available]
 for method,g in eligible.groupby('method'):
  e=g.prediction.to_numpy()-g.observed_tp2.to_numpy(); v=summary['pooled_method_specific'][method]
  assert len(e)==v['count'] and np.isclose(np.mean(np.abs(e)),v['mae']) and np.isclose(np.sqrt(np.mean(e*e)),v['rmse'])
 checks.append('pooled MAE/RMSE independently recomputed from saved prediction rows')
 out={'phase':a.phase,'status':'PASS','checks':checks,'prediction_file_sha256':sha(rawp),'metrics_file_sha256':sha(metp),'rows':len(raw)}; print(json.dumps(out,indent=2))
if __name__=='__main__':main()
