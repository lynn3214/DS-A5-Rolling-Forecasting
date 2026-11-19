# Evaluation Protocol v1.0 — FROZEN after independent user review

Protocol approval was provided by the user after independent ChatGPT analysis. This freezes the experimental design only; it does not verify any trained model or final evaluation result.

## Task, boundaries, and availability

Forecast MetroPT-3 `TP2` pressure (bar) 600 elapsed seconds ahead. For issue time `t`, select the earliest observation in `[t+600s, t+605s]`. Earlier or later observations are unavailable; never interpolate. All calendar intervals are left-closed/right-open. Source timestamps are naive. Historical feature and label availability is assumed to have zero additional archive latency for retrospective replay only; this is unverified and does not establish live availability.

A valid issue-target pair requires finite TP2 at both issue and matched target and no adjacent source timestamp gap greater than 60 seconds between the issue and target rows. Labels used for training at origin `O` must have their actual matched timestamp `<= O`. Training issues are `< O`. Evaluation issues are in `[O,E)` and matched targets must be `< E`.

## Feature construction

Fixed ordered Ridge features: `TP2_lag_10s`, `TP2_lag_60s`, `TP2_lag_300s`, `TP3_lag_60s`, `TP3_lag_300s`, `Motor_current_lag_60s`, `Motor_current_lag_300s`. For each requested time `t-L`, select latest recorded row at or before it; require age from row to requested time in `[0,5s]`, finite value, and no >60-second adjacent gap from the selected row through the latest observed row at/before issue time. No future-looking matching, centered windows, or interpolation. If any required feature is missing/invalid, Ridge prediction is unavailable. Digital state and calendar features are excluded.

## Baselines

Persistence: latest finite TP2 observation at or before issue, age <=5 seconds, with no >60-second gap on that observation-to-issue segment. Seasonal naive: `reference_time = issue_time + 600s - 24h`; select the latest observation at or before reference time, requiring age `reference_time - observed_time` in `[0,5s]`, finite TP2, and timestamp <= issue. It must be available by issue under the retrospective assumption. No interpolation or persistence substitution. The historical lookup validates that single observation only; it does not require continuous samples across all 24 hours. The separate common gap rule applies to issue-to-target pairs.

## Rolling origins and retraining

Development origins: 2020-03-01, 04-01, 05-01, 06-01, 07-01; each evaluation window is `[O,O+14d)`. Final candidate windows: F1 `[2020-08-01,2020-08-06)`, F2 `[2020-08-07,2020-08-12)`, F3 `[2020-08-13,2020-08-18)`, F4 `[2020-08-19,2020-08-24)`, F5 `[2020-08-25,2020-08-30)`. At every origin expand training from the beginning, using training issues `<O`, actual labels `<=O`, and only point-in-time-valid features. Refit `StandardScaler` on eligible training X only. Later final origins may use earlier final observations only after their labels would have become available by that later origin. This is prequential retraining; it does not permit changing the frozen recipe based on earlier final errors.

## Model and reproducibility

Candidate: `sklearn.linear_model.Ridge(alpha=1.0, fit_intercept=True, solver="svd")`. No target scaling, tuning, random split, shuffle, or model fit during protocol preparation. Keep identical feature names/order in fit and predict. Capture Python, numpy, pandas, scikit-learn versions, BLAS/LAPACK configuration, platform, input hash, script hash, and seed (no stochastic estimator seed is used). Numerical results may vary slightly across BLAS/platform builds.

## Populations, metrics, and reporting

For every origin report candidate issue timestamps; valid issue-target pairs; persistence-, seasonal-naive-, and Ridge-available predictions; each method's count and fraction over candidate issues; method-specific MAE/RMSE; and common timestamp count and MAE/RMSE. Primary comparison is on the intersection of target timestamps predicted by every compared method. Also retain method-specific results to expose coverage selection. Unavailable predictions are not zero errors. Do not choose periods based on final performance.

## Drift, critical periods, and fallback

Summarize by origin the distributions (median, IQR, 5th/95th percentiles) of TP2, TP3, Motor_current, and frequencies of missingness/gaps; report available operating-state transition frequencies descriptively, without causal claims. Plot timestamp-ordered errors with origin boundaries. Predefine critical-period comparison using UCI-listed external failure-report windows (2020-04-18; 2020-05-29 to 2020-05-30; 2020-06-05 to 2020-06-07; 2020-07-15) versus other eligible times; timestamp alignment and event truth are uncertain, so this is retrospective subgrouping only. Negative results include no common predictions, no improvement over persistence on common timestamps, unstable origin effects, or insufficient coverage. Retrospective fallback simulation may use persistence when Ridge features are unavailable and report the triggered fraction; do not silently impute. Input staleness, gap rates, and delayed rolling errors are hypothetical monitoring signals, not validated operational thresholds.

## Assertions for implementation

Assert feature timestamps <= requested lag time <= issue; finite required values; no prohibited gap on required feature segments; target is future-only and in tolerance; issue/target values finite; training actual label time <= origin; eval target time < E; scaler fit indices subset of eligible training rows; fixed feature names/order; no final metrics used for selection; method comparison populations intersect by target ID. Archive timestamps cannot verify actual publication latency or clock timezone.
