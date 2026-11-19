# Phase 2A protocol freeze review

## Verdict: FROZEN — independently approved

The user supplied approval following independent ChatGPT analysis. Evaluation Protocol v1.0 is frozen. This freezes the protocol only; no forecasting model or final evaluation has been independently verified.

## Proposed configuration

MetroPT-3 TP2 pressure, 600-second horizon; earliest observed label in `[issue+600s, issue+605s]`; issue-target gap threshold 60s. Fixed Ridge feature order: TP2 lags 10/60/300s, TP3 lags 60/300s, Motor_current lags 60/300s. Historical lookup is past-only within five seconds; all required values finite and no >60s gap from selected history through issue. Ridge alpha 1, intercept, SVD; StandardScaler fit per origin on eligible training rows only; no target scaling or tuning.

Persistence uses latest valid TP2 at/before issue. Seasonal naive references `issue+600s-24h`, selecting latest finite row at/before reference no more than five seconds old and available by issue. Its single-reference rule does not demand continuous data throughout 24 hours. Unavailable predictions remain unavailable and are never silently replaced.

Five development origins and five final candidate windows are preserved. At origin O, training issue <O, actual target timestamp <=O; evaluation issue in [O,E), target <E. Later final origins may use earlier final labels only after they become available. All models compare on the common target IDs while method-specific metrics and coverage remain reported.

## Changes in this phase

Added reusable historical and lag lookup functions in `scripts/temporal_rules.py`; added deterministic tests for seasonal reference boundaries, unavailable/nonfinite data, lag causality, tolerance, and gap crossing. Synchronized task, feature availability, rolling protocol, dataset selection, and checklist documents. Empirical diagnostic JSON and original data were not modified.

## Verification evidence

Command: `conda run -n nussem1 python -m pytest -q tests/test_timestamp_match.py` — **5 passed**. The suite includes future-only target matching, actual label-at-origin boundary, missing TP2 safety, gap crossing, seasonal historical lookup, and lag lookup. Syntax check: `conda run -n nussem1 python -m py_compile scripts/diagnose_forecast_task.py scripts/temporal_rules.py tests/test_timestamp_match.py` — passed. Full test command: `conda run -n nussem1 python -m pytest -q tests` — **5 passed**. No model training command was run.

The previously executed diagnostic JSON remains tied to its recorded input/script hashes. This phase changed neither diagnostic script nor JSON, because no empirical consistency defect was identified in those artifacts for the requested scope.

## Assumptions and limits

The archive does not document historical publication latency; zero additional latency is a retrospective assumption. Timestamps are naive, timezone/clock accuracy unknown. External failure-report windows are retrospective labels with uncertain alignment, not proven ground-truth faults. State fields are excluded from the primary model. Ridge numerical reproducibility depends partly on software and BLAS/LAPACK environment, to be recorded during execution.

## Remaining blockers

No technical ambiguity remains within this specification pass. Independent user approval was supplied for the protocol freeze. Phase 2B implementation remains pending separate authorization. Final-period label counts and model results remain uninspected by design.
