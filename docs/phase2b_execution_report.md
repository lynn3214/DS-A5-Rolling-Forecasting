# Phase 2B Execution Report

## Status

**PARTIAL.** All five final windows were executed under the frozen protocol and technical row/metric checks passed. However, development origin D1 had no training rows with complete required features, Ridge prediction coverage was extremely low, and F5 had no Ridge predictions. No protocol rule was relaxed. These are material execution limitations requiring independent review before scientific interpretation.

## Frozen integrity and implementation

The evaluator used the frozen protocol commit `ca83f0a295a68337aebc070cfd481645418cda13` and input MetroPT-3 CSV SHA-256 `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`. The original file was not changed.

Implementation modules: `src/temporal.py` (future target, gap and lag feature rules), `src/metrics.py`, `src/rolling_evaluation.py`; runners/checker: `scripts/run_rolling_evaluation.py`, `scripts/verify_rolling_outputs.py`. The Ridge feature order and parameters match the manifest. StandardScaler is refit per origin on eligible training rows only. No target scaling or tuning was used.

## Verification

- `conda run -n nussem1 python -m py_compile src/*.py scripts/*.py tests/*.py`: passed.
- `conda run -n nussem1 python -m pytest -q tests`: **10 passed**.
- `conda run -n nussem1 python scripts/run_rolling_evaluation.py --phase development`: completed with D1 recorded as `FAILED_NO_TRAINING_ROWS`; D2–D5 completed.
- `conda run -n nussem1 python scripts/run_rolling_evaluation.py --phase final`: all F1–F5 windows executed; five origins completed as execution jobs. F5 Ridge prediction count is zero and remains explicit.
- `conda run -n nussem1 python scripts/verify_rolling_outputs.py --phase development` and `--phase final`: both PASS. Checks independently confirmed three method rows per issue, target row/label matching against original timestamps, the future-only 600–605 second rule, fold/scaler counts, fixed Ridge parameters, common target IDs, and pooled MAE/RMSE from saved predictions.
- Earlier failed runner attempts and the first successful but incomplete output versions are retained under `results/rolling/logs/`, `attempt_1/`, and `attempt_2/`; current complete outputs are at the top of `results/rolling/`.

Environment: Python 3.10.18; NumPy 2.2.6; pandas 2.3.1; SciPy 1.15.2; scikit-learn 1.7.1. BLAS/LAPACK configuration is recorded in each execution manifest.

## Development execution

| Origin | Candidate issues | Valid target pairs | Eligible training rows | Persistence / Seasonal / Ridge predictions | Common targets |
|---|---:|---:|---:|---:|---:|
| D1 | 103,456 | 101,251 | 0 | 103,456 / 56,117 / 0 | 0 |
| D2 | 94,505 | 92,351 | 158 | 94,505 / 33,639 / 303 | 155 |
| D3 | 95,834 | 94,352 | 9,986 | 95,834 / 51,873 / 9 | 0 |
| D4 | 103,774 | 102,327 | 21,568 | 103,774 / 59,543 / 4,096 | 2,428 |
| D5 | 92,482 | 90,357 | 42,650 | 92,482 / 46,086 / 47 | 23 |

D1 had 212,356 training rows with valid targets, but zero rows also met the frozen complete-feature and gap rules. D1 is preserved as a failed Ridge origin; baseline predictions and candidate rows remain in raw output.

## Final execution (metrics are reported for auditability, not interpreted scientifically)

Method-specific MAE/RMSE are computed only where that method has a prediction and the common valid target pair exists. Coverage denominators are candidate issues. Common metrics use target IDs with predictions from all three methods.

| Origin | Valid target pairs | Persistence coverage; MAE / RMSE | Seasonal coverage; MAE / RMSE | Ridge coverage; MAE / RMSE | Common n |
|---|---:|---|---|---|---:|
| F1 | 28,036 | 100.00%; 2.0003 / 4.3333 | 28.95%; 1.8838 / 4.2075 | 0.06%; 2.4597 / 3.6893 | 0 |
| F2 | 39,519 | 100.00%; 2.0273 / 4.3683 | 58.09%; 1.9023 / 4.2239 | 0.06%; 0.2331 / 0.4493 | 18 |
| F3 | 36,435 | 100.00%; 2.2032 / 4.5425 | 37.71%; 1.8803 / 4.1836 | 0.02%; 1.7841 / 2.9443 | 9 |
| F4 | 28,560 | 100.00%; 2.3919 / 4.7278 | 46.79%; 2.2188 / 4.5538 | 0.06%; 0.7365 / 1.1007 | 0 |
| F5 | 36,665 | 100.00%; 2.3181 / 4.6702 | 51.54%; 1.9757 / 4.2866 | 0.00%; unavailable | 0 |

Pooled method-specific final results: persistence n=169,215, MAE 2.1852, RMSE 4.5287; seasonal naive n=77,165, MAE 1.9695, RMSE 4.2897; Ridge n=64, MAE 1.1764, RMSE 2.2853. The pooled all-method common set has only 27 targets: persistence MAE/RMSE 1.0674/3.1972, seasonal naive 1.4009/3.6354, Ridge 0.7631/1.7450. These sparse Ridge/common populations do not support broad performance conclusions.

## Outputs and hashes

- Development raw predictions: `results/rolling/development_predictions.csv` (SHA-256 `c53e94087feb4c2bd10cab0df0c3e08f4364f2eb97f10c22d9508575fe20d586`); metrics SHA-256 `1c97599d08311a2cadca555313ee1ab87d7c3648539e34f73235c316dafde641`.
- Final raw predictions: `results/rolling/final_predictions.csv` (SHA-256 `e2cdf4de6f838f8f06d241149e514d09bc33e0192ac5073b7d1e02e83a12db41`); metrics SHA-256 `6af02ab6d02e491b622f66d3b0b45b62a871a6c264f917c92d519ced2f9f4d11`.
- Each phase has an execution manifest with freeze commit, input/code/output hashes, package and BLAS/LAPACK details, command, fold counts and status.

## Limitations and handoff

The strict seven-feature, five-second lookup and continuous-history rules make Ridge coverage very low in these data. This report does not change or relax them. D1 could not fit Ridge; F5 produced no Ridge predictions; common-target populations are sparse or empty in several final origins. Seasonal-naive is also unavailable for a substantial share of rows. Historical publication latency and timestamp timezone remain unverified. Final metrics have not received independent human review. No scientific conclusion, drift diagnosis, production claim, or monitoring threshold is asserted.

Next action: independently review the technical outputs and decide whether the frozen protocol execution is acceptable as-is; any proposed protocol change requires a separately reviewed deviation before further experiments. No commit or push was made.
