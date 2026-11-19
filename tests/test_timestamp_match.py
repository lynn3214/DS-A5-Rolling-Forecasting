import numpy as np
from scripts.diagnose_forecast_task import match_future, reference_match

def test_future_match_edges_gaps_boundaries_and_duplicates():
    # Missing timestamps and a long gap are represented by absent observations.
    ts=np.array([0,10,20,40,100,110],float)
    nominal=np.array([0,5,15,35,94,95,96,105,106,110,111],float)
    got=match_future(ts,nominal,5)
    assert np.array_equal(got,reference_match(ts,nominal,5))
    assert got.tolist()==[0,1,2,3,-1,4,4,5,5,5,-1]
    assert np.all((got<0)|(ts[np.maximum(got,0)]>=nominal))
    # Development/final split: an observation exactly at the final boundary is excluded
    # when the caller supplies development timestamps only.
    dev=np.array([0,10,20],float)
    assert match_future(dev,np.array([20.]),5).tolist()==[2]
    assert match_future(dev,np.array([21.]),5).tolist()==[-1]
from scripts.diagnose_forecast_task import label_eligible, gap_crossings

def test_actual_label_availability_boundary():
    ts=np.array([0.,600.,603.,610.])
    # nominal target is exactly origin (600), matched label at 600; also label at 603
    matched=np.array([1,2,-1])
    issues=np.array([0,0,0])
    assert label_eligible(ts,issues,matched,600.).tolist()==[True,False,False]
    assert label_eligible(ts,issues,matched,603.).tolist()==[True,True,False]

def test_missing_issue_and_target_values_and_gap_crossing():
    values=np.array([1.,np.nan,3.])
    idx=np.array([0,1,2,-1]); safe=np.maximum(idx,0)
    issues=np.array([0,1,2,0]); valid=(idx>=0)&np.isfinite(values[issues])&np.isfinite(values[safe])
    assert valid.tolist()==[True,False,True,False]
    ts=np.array([0.,10.,100.,110.])
    assert gap_crossings(ts,np.array([0,0,2]),np.array([1,2,3]),60.).tolist()==[False,True,False]
from scripts.temporal_rules import seasonal_reference_index, lag_feature_index

def test_seasonal_reference_lookup():
    t=np.array([80.,90.,100.,105.,110.]); v=np.array([1.,2.,3.,4.,5.])
    assert seasonal_reference_index(t,v,issue_time=110.,reference_time=100.)==2 # exact
    assert seasonal_reference_index(t,v,110.,100.5)==2 # 0.5s before ref
    assert seasonal_reference_index(t,v,110.,96.)==-1 # latest prior is >5s old
    assert seasonal_reference_index(t,v,110.,89.)==-1 # no history
    assert seasonal_reference_index(t,v,110.,111.)==-1 # after issue
    v[2]=np.nan
    assert seasonal_reference_index(t,v,110.,100.)==-1 # non-finite reference

def test_lag_lookup_is_past_only_and_gap_bounded():
    t=np.array([0.,10.,20.,30.,100.]); v=np.array([1.,2.,3.,4.,5.])
    assert lag_feature_index(t,v,issue_time=30.,lag_seconds=10.)==2
    assert lag_feature_index(t,v,30.,lag_seconds=4.)==-1 # chosen sample is too old from requested time
    assert lag_feature_index(t,v,issue_time=100.,lag_seconds=60.)==-1 # no sample in tolerance
    assert lag_feature_index(t,v,issue_time=100.,lag_seconds=80.)==-1 # long gap crosses required history
