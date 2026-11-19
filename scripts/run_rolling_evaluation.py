#!/usr/bin/env python
"""Execute frozen development or final rolling evaluation."""
import argparse,json,hashlib,platform,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np,pandas as pd,scipy,sklearn
from src.rolling_evaluation import run_origins,DEV,FINAL
DATA=Path('data/raw/metropt3/MetroPT3(AirCompressor).csv')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 started=time.perf_counter()
 ap=argparse.ArgumentParser(); ap.add_argument('--phase',choices=['development','final'],required=True); a=ap.parse_args()
 # Development command loads only rows before cutoff; final command reads the full source after development gates.
 if a.phase=='development':
  ts=pd.read_csv(DATA,usecols=['timestamp'],parse_dates=['timestamp']).timestamp; count=int((ts<'2020-08-01').sum()); df=pd.read_csv(DATA,nrows=count,parse_dates=['timestamp'])
  windows=[(f'D{i+1}',o,e) for i,(_,o,e) in enumerate(DEV)]
 else:
  df=pd.read_csv(DATA,parse_dates=['timestamp']); windows=FINAL
 raw,summary=run_origins(df,windows); out=Path('results/rolling');out.mkdir(parents=True,exist_ok=True)
 raw_path=out/f'{a.phase}_predictions.csv'; raw.to_csv(raw_path,index=False)
 # Pooled results are computed from individual saved-error rows, not an unweighted mean of fold metrics.
 pooled={}
 eligible=raw[raw.target_pair_eligible & raw.prediction_available]
 for method,g in eligible.groupby('method'):
  err=g.prediction.to_numpy()-g.observed_tp2.to_numpy(); pooled[method]={'count':int(len(g)),'mae':float(np.mean(np.abs(err))),'rmse':float(np.sqrt(np.mean(err**2)))}
 wide=eligible.pivot_table(index=['origin_id','issue_row','target_row'],columns='method',values='prediction',aggfunc='first')
 common_ids=wide.dropna().index
 common={}
 if len(common_ids):
  labels=raw[(raw.method=='persistence')].set_index(['origin_id','issue_row','target_row']).loc[common_ids].observed_tp2.to_numpy()
  for method in wide.columns:
   err=wide.loc[common_ids,method].to_numpy()-labels; common[method]={'count':len(err),'mae':float(np.mean(np.abs(err))),'rmse':float(np.sqrt(np.mean(err**2)))}
 metrics_path=out/f'{a.phase}_metrics.json'; metrics_path.write_text(json.dumps({'origins':summary,'pooled_method_specific':pooled,'pooled_common_targets':common},indent=2))
 manifest={'phase':a.phase,'protocol':'DS-A5-Evaluation-Protocol-v1.0','freeze_commit':'ca83f0a295a68337aebc070cfd481645418cda13','dataset_sha256':sha(DATA),'source_code_sha256':{p:sha(Path(p)) for p in ['scripts/run_rolling_evaluation.py','src/temporal.py','src/rolling_evaluation.py','src/metrics.py']},'rows_loaded':len(df),'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__,'numpy_config':str(np.__config__.show(mode='dicts')),'command':f'conda run -n nussem1 python scripts/run_rolling_evaluation.py --phase {a.phase}','windows':summary,'raw_predictions_sha256':sha(raw_path),'metrics_sha256':sha(metrics_path),'runtime_seconds':time.perf_counter()-started,'run_status':'COMPLETED' if all(x['status']=='COMPLETED' for x in summary) else 'PARTIAL'}
 (out/f'{a.phase}_manifest.json').write_text(json.dumps(manifest,indent=2,default=str));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
