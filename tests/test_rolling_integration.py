import numpy as np,pandas as pd
from src.temporal import match_target,target_eligibility,construct_features,FEATURES
from src.rolling_evaluation import run_origins

def test_adversarial_target_and_origin_boundaries():
    base=np.datetime64('2020-01-01T00:00:00','ns').astype('int64')
    base_sec=base//1_000_000_000
    rel=np.r_[np.arange(0,600,10),603,613]
    ts=base_sec*1_000_000_000+rel.astype('int64')*1_000_000_000
    got=match_target(ts,np.array([0]))
    assert got.tolist()==[60] # nominal 600s, actual observation +3s
    y=np.ones(len(ts)); idx,valid=target_eligibility(ts,y,np.array([0]))
    assert valid.tolist()==[True]
    origin=base_sec*1_000_000_000+600*1_000_000_000
    assert ts[idx[0]]>origin # label unavailable at origin despite nominal time == origin

def test_feature_construction_order_causality_and_nan():
    ts=np.arange(1000,dtype='int64')*1_000_000_000
    arr={'TP2':np.arange(1000,dtype=float),'TP3':np.arange(1000,dtype=float)+1,'Motor_current':np.arange(1000,dtype=float)+2}
    X,prov,ok=construct_features(ts,arr)
    assert X.shape==(1000,7) and len(FEATURES)==7
    i=500
    assert ok[i]
    assert np.all(ts[prov[i]]<=ts[i])
    arr['TP3'][440]=np.nan
    X2,_,ok2=construct_features(ts,arr)
    assert not ok2[500] # requested 60s TP3 selects exactly row 440

def test_gap_and_rolling_origin_integration():
    n=3600; base=np.datetime64('2020-01-01T00:00:00','ns').astype('int64'); ts=base+np.arange(n,dtype='int64')*1_000_000_000
    frame=pd.DataFrame({'timestamp':pd.to_datetime(ts),'TP2':np.sin(np.arange(n)/20)+8,'TP3':np.arange(n,dtype=float),'Motor_current':np.arange(n,dtype=float)/10})
    O='2020-01-01T00:20:00'; E='2020-01-01T00:50:00'
    raw,summary=run_origins(frame,[('T1',O,E)])
    assert summary[0]['status']=='COMPLETED' and summary[0]['training_sample_count']>0
    assert summary[0]['scaler_fit_row_count']==summary[0]['training_sample_count']
    assert summary[0]['common_target_count']<=summary[0]['valid_target_pair_count']
    paired=raw[raw['target_pair_eligible']]
    assert paired['actual_target_timestamp'].gt(paired['issue_timestamp']).all()
    assert (raw['method']!='ridge').any()

def test_empty_ridge_prediction_batch_is_explicitly_unavailable():
    base=np.datetime64('2020-01-01T00:00:00','ns').astype('int64')
    rel=np.r_[np.arange(0,3000),np.arange(5000,5011),5600]
    ts=base+rel.astype('int64')*1_000_000_000; n=len(ts)
    frame=pd.DataFrame({'timestamp':pd.to_datetime(ts),'TP2':np.sin(np.arange(n)/20)+8,'TP3':np.arange(n,dtype=float),'Motor_current':np.arange(n,dtype=float)/10})
    raw,summary=run_origins(frame,[('T1','2020-01-01T01:23:20','2020-01-01T01:23:30')])
    assert summary[0]['status']=='COMPLETED'
    ridge=raw[raw.method=='ridge']
    assert not ridge.prediction_available.any()
    assert (ridge.missing_reason=='incomplete_or_invalid_required_features').all()
    assert summary[0]['valid_target_pair_count']==0

def test_feature_gap_invalidates_history_segment():
    ts=np.arange(20,dtype='int64')*10_000_000_000
    ts[10:]+=100_000_000_000
    arr={'TP2':np.arange(20,dtype=float),'TP3':np.arange(20,dtype=float),'Motor_current':np.arange(20,dtype=float)}
    _,_,ok=construct_features(ts,arr)
    # Issues soon after redeployment lack complete lag history across the >60s boundary.
    assert not ok[10]
