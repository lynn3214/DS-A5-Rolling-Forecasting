"""Protocol-v1 expanding rolling fit/evaluation."""
import numpy as np,pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from .temporal import construct_features,target_eligibility,persistence,seasonal_naive,FEATURES
from .metrics import summarize
DEV=[('D1','2020-03-01','2020-03-15'),('D2','2020-04-01','2020-04-15'),('D3','2020-05-01','2020-05-15'),('D4','2020-06-01','2020-06-15'),('D5','2020-07-01','2020-07-15')]
FINAL=[('F1','2020-08-01','2020-08-06'),('F2','2020-08-07','2020-08-12'),('F3','2020-08-13','2020-08-18'),('F4','2020-08-19','2020-08-24'),('F5','2020-08-25','2020-08-30')]

def run_origins(df, windows):
    ts=pd.to_datetime(df.timestamp).to_numpy(dtype='datetime64[ns]').astype('int64'); y=df.TP2.to_numpy(float)
    arrays={c:df[c].to_numpy(float) for c in ['TP2','TP3','Motor_current']}
    X,prov,feat_ok=construct_features(ts,arrays); target_idx,target_ok=target_eligibility(ts,y,np.arange(len(ts)))
    rows=[]; summaries=[]; feature_names=list(FEATURES)
    for oid,start,end in windows:
        O=int(np.datetime64(start).astype('datetime64[ns]').astype('int64')); E=int(np.datetime64(end).astype('datetime64[ns]').astype('int64'))
        candidate=(ts>=O)&(ts<E); ci=np.flatnonzero(candidate)
        safe_target=np.maximum(target_idx,0); target_in_eval=target_ok&(ts[safe_target]<E)
        pair_reason=np.full(len(ts),'',dtype=object); pair_reason[target_idx<0]='no_future_match_within_tolerance'
        matched=target_idx>=0; pair_reason[matched&~(np.isfinite(y)&np.isfinite(y[safe_target]))]='nonfinite_issue_or_target'
        pair_reason[matched&~target_ok&(pair_reason=='')]='prohibited_issue_target_gap'
        pair_reason[target_ok&(ts[safe_target]>=E)]='target_outside_evaluation_window'
        train_target=(ts<O)&target_ok&(ts[safe_target]<=O)
        train_features=train_target&feat_ok
        train=train_features
        tr=np.flatnonzero(train); valid_eval=target_in_eval[ci]; ei=ci[valid_eval]
        # Mechanical boundary and provenance assertions.
        assert np.all(ts[tr]<O)
        assert np.all(ts[target_idx[tr]]<=O)
        assert np.all(ts[ei]>=O)&np.all(ts[ei]<E)&np.all(ts[target_idx[ei]]<E)
        assert np.all(np.isfinite(y[tr])) and np.all(np.isfinite(y[target_idx[tr]]))
        assert np.isfinite(X[tr]).all()
        failed=not len(ci) or not len(tr)
        model=None; scaler=None
        if not failed:
            scaler=StandardScaler(); Xtr=scaler.fit_transform(X[tr]); model=Ridge(alpha=1.,fit_intercept=True,solver='svd'); model.fit(Xtr,y[target_idx[tr]])
        ridge=np.full(len(ci),np.nan); ridge_ok=feat_ok[ci] if model is not None else np.zeros(len(ci),dtype=bool)
        if model is not None and ridge_ok.any(): ridge[ridge_ok]=model.predict(scaler.transform(X[ci[ridge_ok]]))
        pers,pr=persistence(ts,y,ci); seas,sr=seasonal_naive(ts,y,ci)
        preds={'persistence':pers,'seasonal_naive':seas,'ridge':ridge}; reasons={'persistence':pr,'seasonal_naive':sr,'ridge':np.where(ridge_ok,'','no_training_rows' if model is None else 'incomplete_or_invalid_required_features')}
        actual=np.full(len(ci),np.nan); actual[valid_eval]=y[target_idx[ei]]
        common=valid_eval.copy()
        for p in preds.values(): common &= np.isfinite(p)
        for k,i in enumerate(ci):
            for method,p in preds.items():
                available=bool(np.isfinite(p[k])); label_ok=bool(valid_eval[k]); err=float(p[k]-actual[k]) if available and label_ok else None
                rows.append({'origin_id':oid,'issue_row':int(i),'issue_timestamp':str(pd.Timestamp(ts[i])),'nominal_target_timestamp':str(pd.Timestamp(ts[i]+600_000_000_000)),'target_row':int(target_idx[i]) if label_ok else None,'actual_target_timestamp':str(pd.Timestamp(ts[target_idx[i]])) if label_ok else None,'observed_tp2':float(actual[k]) if label_ok else None,'method':method,'prediction':float(p[k]) if available else None,'prediction_available':available,'missing_reason':None if available else str(reasons[method][k]),'target_pair_eligible':label_ok,'target_pair_reason':None if label_ok else str(pair_reason[i]),'feature_eligible':bool(feat_ok[i]),'absolute_error':abs(err) if err is not None else None,'squared_error':err*err if err is not None else None,'training_sample_count':len(tr),'evaluation_candidate_count':len(ci),'common_target':bool(common[k]),'feature_names':feature_names if method=='ridge' else None})
        metrics={}
        for method,p in preds.items():
            met=valid_eval&np.isfinite(p); metrics[method]={'prediction_count':int(np.isfinite(p).sum()),'coverage_candidate_issues':float(np.isfinite(p).mean()),'valid_scored_count':int(met.sum()),**summarize(actual[met],p[met])}
        cm={m:summarize(actual[common],p[common]) for m,p in preds.items()}
        summaries.append({'origin_id':oid,'status':'FAILED_NO_TRAINING_ROWS' if model is None else 'COMPLETED','failure_reason':'No issue rows met all frozen label/feature eligibility rules before origin.' if model is None else None,'training_target_eligible_count':int(train_target.sum()),'training_feature_eligible_count':int(train_features.sum()),'start_inclusive':start,'end_exclusive':end,'candidate_issue_count':len(ci),'valid_target_pair_count':int(valid_eval.sum()),'training_target_eligible_count':int(train_target.sum()),'training_feature_eligible_count':int(train_features.sum()),'training_sample_count':len(tr),'scaler_fit_row_count':int(scaler.n_samples_seen_) if scaler is not None else 0,'ridge_features':feature_names,'ridge_params':{'alpha':1.0,'fit_intercept':True,'solver':'svd'},'method_metrics':metrics,'common_target_count':int(common.sum()),'common_target_metrics':cm})
    return pd.DataFrame(rows),summaries
