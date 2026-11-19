# Forecasting task definition — protocol proposal

## Selected task

MetroPT-3 TP2 pressure (bar), 600-second elapsed-time horizon. The future label is the earliest observation in `[issue_time + 600s, issue_time + 605s]`. No earlier observation, interpolation, or out-of-window substitution is allowed. Pair validity requires finite TP2 at both issue and label rows and no adjacent timestamp gap >60s between them. Development-only valid coverage is 98.2937% of 1,295,984 issue rows after the gap rule; correlation on the same valid pairs is 0.25466. This is descriptive, not a forecast score.

## Frozen feature/model specification

Use elapsed-time TP2 lags at 10s, 60s, and 300s; small exogenous history set TP3 and Motor_current at 60s and 300s. For each desired lag time, take the latest observation at or before issue-minus-lag, only if its age is <=5s. Require all selected features finite; otherwise exclude the issue. Any crossed >60s gap invalidates the feature history. Exclude state variables in the minimal model because their operational availability timing is undocumented and their event transition semantics add complexity. No calendar features in the primary specification.

Candidate estimator: sklearn Ridge, `alpha=1.0`, `fit_intercept=True`, solver `svd`, no randomization; no hyperparameter search. Apply `StandardScaler` fitted on each training fold only to continuous inputs; target remains in bar units. Determinism is expected on fixed software/hardware, though floating point libraries may differ. Record package versions and BLAS details at implementation time. No fit has occurred in Phase 2A.

Missing history: no imputation; drop that prediction and report coverage. Persistence predicts the latest finite TP2 at/before issue, max age 5s, with no >60s gap crossing. Seasonal naive reference is `issue + 600s - 24h`; select the latest observation at/before reference, requiring reference minus observation in [0,5s], finite TP2, and timestamp <= issue; otherwise unavailable (never substitute persistence). Do not require continuity over the full 24-hour interval: only the reference row must be valid, while the issue-target gap rule is independent.

Historical availability is an unverified retrospective assumption. Source timestamps are naive and do not prove publication latency.
