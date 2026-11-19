"""Frozen MetroPT-3 temporal eligibility and feature construction."""
import numpy as np
FEATURES=('TP2_lag_10s','TP2_lag_60s','TP2_lag_300s','TP3_lag_60s','TP3_lag_300s','Motor_current_lag_60s','Motor_current_lag_300s')
SPEC=(('TP2',10),('TP2',60),('TP2',300),('TP3',60),('TP3',300),('Motor_current',60),('Motor_current',300))
HORIZON=600; TOL_NS=5_000_000_000; GAP_NS=60_000_000_000

def match_target(ts_ns, issue_idx, horizon=HORIZON, tolerance_ns=TOL_NS):
    nominal=ts_ns[issue_idx]+horizon*1_000_000_000
    idx=np.searchsorted(ts_ns,nominal,side='left'); ok=idx<len(ts_ns)
    safe=np.minimum(idx,len(ts_ns)-1)
    ok &= ts_ns[safe] <= nominal+tolerance_ns
    return np.where(ok,idx,-1)

def latest_past(ts_ns, query_ns, max_age_ns=TOL_NS):
    idx=np.searchsorted(ts_ns,query_ns,side='right')-1
    if idx<0 or query_ns-ts_ns[idx]>max_age_ns: return -1
    return int(idx)

def gap_ok(bad_prefix, start_idx, end_idx):
    """No >60s gap on source intervals [start_idx,end_idx)."""
    if start_idx<0 or end_idx<start_idx: return False
    return bad_prefix[end_idx]-bad_prefix[start_idx]==0

def construct_features(ts_ns, arrays):
    n=len(ts_ns); issue_idx=np.arange(n); latest=np.searchsorted(ts_ns,ts_ns,side='right')-1
    gaps=np.diff(ts_ns); bad=(gaps>GAP_NS).astype(np.int64); prefix=np.r_[0,np.cumsum(bad)]
    X=np.full((n,len(SPEC)),np.nan); provenance=np.full((n,len(SPEC)),-1,dtype=np.int64)
    for j,(col,lag) in enumerate(SPEC):
        requested=ts_ns-lag*1_000_000_000; ix=np.searchsorted(ts_ns,requested,side='right')-1
        valid=(ix>=0)&(requested<=ts_ns); safe=np.maximum(ix,0)
        valid &= (requested-ts_ns[safe] <= TOL_NS)
        valid &= np.isfinite(arrays[col][safe])
        # Segment from selected lag observation through latest observed row at/before issue.
        rows=np.flatnonzero(valid)
        valid[rows] &= (prefix[latest[rows]]-prefix[ix[rows]])==0
        X[valid,j]=arrays[col][ix[valid]]; provenance[valid,j]=ix[valid]
    eligible=np.isfinite(X).all(axis=1)
    return X,provenance,eligible

def target_eligibility(ts_ns, y, issue_idx):
    idx=match_target(ts_ns,issue_idx); has=idx>=0; safe=np.maximum(idx,0)
    valid=has & np.isfinite(y[issue_idx]) & np.isfinite(y[safe])
    bad=(np.diff(ts_ns)>GAP_NS).astype(np.int64); prefix=np.r_[0,np.cumsum(bad)]
    rows=np.flatnonzero(valid); valid[rows] &= (prefix[idx[rows]]-prefix[issue_idx[rows]])==0
    return idx,valid

def persistence(ts_ns,y,issue_idx):
    out=np.full(len(issue_idx),np.nan); reason=np.full(len(issue_idx),'',dtype=object)
    hist=np.searchsorted(ts_ns,ts_ns[issue_idx],side='right')-1; ok=hist>=0; safe=np.maximum(hist,0)
    age=ts_ns[issue_idx]-ts_ns[safe]; ok &= age<=TOL_NS
    reason[~ok]='no_recent_history'
    finite=np.isfinite(y[safe]); reason[ok&~finite]='nonfinite_history'; ok &= finite
    bad=(np.diff(ts_ns)>GAP_NS).astype(np.int64); pref=np.r_[0,np.cumsum(bad)]
    no_gap=(pref[issue_idx]-pref[safe])==0; reason[ok&~no_gap]='history_gap'; ok &= no_gap
    out[ok]=y[safe[ok]]
    return out,reason

def seasonal_naive(ts_ns,y,issue_idx):
    out=np.full(len(issue_idx),np.nan); reason=np.full(len(issue_idx),'',dtype=object)
    ref=ts_ns[issue_idx]+(HORIZON-86400)*1_000_000_000
    hist=np.searchsorted(ts_ns,ref,side='right')-1; ok=hist>=0; safe=np.maximum(hist,0)
    age=ref-ts_ns[safe]; ok &= age<=TOL_NS
    reason[~ok]='reference_missing_or_stale'
    finite=np.isfinite(y[safe]); reason[ok&~finite]='nonfinite_reference'; ok &= finite
    before=ts_ns[safe]<=ts_ns[issue_idx]; reason[ok&~before]='reference_after_issue'; ok &= before
    out[ok]=y[safe[ok]]
    return out,reason
