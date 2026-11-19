#!/usr/bin/env python
"""Local-only integrity and temporal audit for original UCI MetroPT-3 and UR3 files."""
import argparse, hashlib, json, zipfile
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd

def file_record(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''): h.update(chunk)
 return {'path':str(path),'bytes':path.stat().st_size,'sha256':h.hexdigest()}
def temporal(df, column):
 if column not in df: return {'status':'NO_TIMESTAMP_COLUMN'}
 t=pd.to_datetime(df[column],errors='coerce')
 valid=t.dropna(); d=valid.diff().dropna(); vc=d.value_counts()
 gaps=d[d>pd.Timedelta(seconds=1)]
 return {'parseable':int(valid.size),'invalid':int(t.isna().sum()),'min':str(valid.min()) if len(valid) else None,'max':str(valid.max()) if len(valid) else None,'timezone':str(valid.dt.tz) if len(valid) else None,'monotonic_non_decreasing':bool(valid.is_monotonic_increasing),'duplicate_timestamps':int(valid.duplicated().sum()),'top_intervals_seconds':{str(k.total_seconds()):int(v) for k,v in vc.head(10).items()},'interval_count':int(len(d)),'gaps_over_1s':int(len(gaps)),'longest_gap_seconds':float(gaps.max().total_seconds()) if len(gaps) else 0}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--metro',type=Path,default=Path('data/raw/metropt3/MetroPT3(AirCompressor).csv')); ap.add_argument('--ur3',type=Path,default=Path('data/raw/ur3/dataset_02052023.xlsx')); ap.add_argument('--out',type=Path,default=Path('results/audit/alternative_audit.json')); a=ap.parse_args()
 out={'run_utc':datetime.now(timezone.utc).isoformat(),'method':'Read-only local files; no imputation, sorting, or source modification.','prior_download_failures':{'MetroPT-3':{'url':'https://archive.ics.uci.edu/static/public/791/metropt%2B3%2Bdataset.zip','attempted_bytes':172032,'complete':False},'UR3-CobotOps':{'url':'https://archive.ics.uci.edu/static/public/963/ur3%2Bcobotops.zip','attempted_bytes':16246,'complete':False}},'datasets':{}}
 if a.metro.exists():
  df=pd.read_csv(a.metro,low_memory=False); numeric=df.select_dtypes('number');
  out['datasets']['MetroPT-3']={**file_record(a.metro),'status':'READABLE','format':'CSV','rows':len(df),'columns':list(df.columns),'dtypes':{k:str(v) for k,v in df.dtypes.items()},'missing_by_column':{k:int(v) for k,v in df.isna().sum().items()},'timestamp':temporal(df,'timestamp'),'numeric_summary':numeric.describe(percentiles=[.01,.5,.99]).to_dict(),'sample_state_counts':{k:{str(x):int(n) for x,n in df[k].value_counts(dropna=False).head(20).items()} for k in ['COMP','DV_electric','TOWERS','LPS','Pressure_switch','Oil_level'] if k in df}}
 else: out['datasets']['MetroPT-3']={'status':'MISSING'}
 if a.ur3.exists():
  with zipfile.ZipFile(a.ur3) as z: bad=z.testzip(); members=[{'name':i.filename,'bytes':i.file_size,'crc':i.CRC} for i in z.infolist()]
  xl=pd.ExcelFile(a.ur3); sheets={};
  for sn in xl.sheet_names:
   df=pd.read_excel(a.ur3,sheet_name=sn); tscol=next((c for c in df.columns if 'time' in str(c).lower() or 'date' in str(c).lower()),None)
   sheets[sn]={'rows':len(df),'columns':list(map(str,df.columns)),'dtypes':{str(k):str(v) for k,v in df.dtypes.items()},'missing_by_column':{str(k):int(v) for k,v in df.isna().sum().items()},'timestamp_column':str(tscol) if tscol is not None else None,'timestamp':temporal(df,str(tscol)) if tscol is not None else {'status':'NO_TIMESTAMP_COLUMN'}}
  out['datasets']['UR3-CobotOps']={**file_record(a.ur3),'status':'READABLE','format':'XLSX','zip_testzip_error':bad,'zip_members':members,'sheets':sheets}
 else: out['datasets']['UR3-CobotOps']={'status':'MISSING'}
 a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(out,indent=2,default=str)); print(json.dumps(out,indent=2,default=str))
if __name__=='__main__': main()
