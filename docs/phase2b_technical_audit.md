# Phase 2B Independent Technical Audit

## Verdict

**PASS — the saved Phase 2B implementation and scoring populations satisfy the frozen protocol checks.** The very low Ridge coverage is reproduced by the frozen feature-availability rules, including zero eligible D1 training rows and zero F5 evaluation rows. No material implementation defect was found in the audited paths.

This technical verdict does not upgrade the Phase 2B execution/scientific status: `docs/phase2b_execution_report.md` remains **PARTIAL** because coverage is extremely sparse and the results do not support broad comparative or scientific conclusions. This audit did not train/refit models, rerun evaluation, or alter frozen rules or historical outputs.

## Scope and preservation

The audit checked frozen commit `ca83f0a295a68337aebc070cfd481645418cda13`, the freeze manifest's committed document/source/diagnostic hashes, the MetroPT-3 input hash, saved prediction records and metrics, and the implementation in `src/temporal.py` and `src/rolling_evaluation.py`. Audit reconstruction reads the original raw data and saved result files only.

The original MetroPT-3 CSV SHA-256 is `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`. The audited top-level Phase 2B outputs remain:

| File | SHA-256 |
|---|---|
| `results/rolling/development_predictions.csv` | `c53e94087feb4c2bd10cab0df0c3e08f4364f2eb97f10c22d9508575fe20d586` |
| `results/rolling/development_metrics.json` | `1c97599d08311a2cadca555313ee1ab87d7c3648539e34f73235c316dafde641` |
| `results/rolling/development_manifest.json` | `6db45bc36a7166ce9baa81612eb42d112ad26cb030db88d889aec4a52789a012` |
| `results/rolling/final_predictions.csv` | `e2cdf4de6f838f8f06d241149e514d09bc33e0192ac5073b7d1e02e83a12db41` |
| `results/rolling/final_metrics.json` | `6af02ab6d02e491b622f66d3b0b45b62a871a6c264f917c92d519ced2f9f4d11` |
| `results/rolling/final_manifest.json` | `aa1d53ae76b8bb8942d1dc67511cb699f4184b065aa9c01edd8bcbbbd622f169` |
| `results/rolling/logs/development_verification.json` | `fe17b0a3c41fd5541b9f9ecb702f46d8d0015f3bafdfc8779630958c5b127d3b` |
| `results/rolling/logs/final_verification.json` | `a1de3a364a7812ec590584b614547b65444cd2a36427fa626527adbd9ce171dc` |

Earlier failed attempts and runner logs remain under `results/rolling/attempt_1/`, `attempt_2/`, and `logs/`. The audit generated separate files under `results/audit/`; it did not replace predictions, metrics, manifests, or execution logs. No Git commit or push was made.

## Count reconciliation and scoring

For every development/final origin and all three methods, the audit independently reconstructed candidate issue rows, valid target pairs, available forecasts, forecasts with valid labels, scored rows, exclusion reasons, and issue/target uniqueness. All invariants held:

- `scored_predictions <= valid_target_pairs`
- `scored_predictions <= available_predictions`
- No duplicate `(issue_row, target_row)` prediction identities were found within an origin-method.
- Every scored row has a finite, eligible target pair and an available finite prediction.

Prediction availability is evaluated independently of whether a future label is valid. Thus a method can emit a forecast for an issue whose target is later missing, non-finite, across a prohibited gap, or outside the evaluation window. Those rows are retained in the raw predictions but excluded from scoring. This explains the apparent F1 discrepancy: persistence has 28,576 available predictions, while only 28,036 valid target pairs exist; all 28,036 eligible pairs are scored, and the other 540 available predictions have invalid/ineligible labels. This is a count-definition/reporting ambiguity, not a scoring defect. The same rule is consistently enforced for every origin and method.

The audit recomputed method-specific and common-population MAE/RMSE from individual saved predictions and errors. All per-origin and pooled results matched the saved metrics JSON. Development and final output verifiers independently confirmed target row IDs and observed labels against the original data, future-only target matching within `[issue+600s, issue+605s]`, complete method rows per issue, fold/scaler counts, fixed Ridge parameters, common flags, and pooled metrics.

## Ridge eligibility diagnosis

The sequential funnel is in `results/audit/phase2b_coverage_funnel.csv`; independent per-feature failure counts are in `results/audit/phase2b_feature_failures.csv`. Sequential exclusions depend on the frozen feature order and must not be interpreted as unique causal contributions.

For D1 training, 214,850 issue rows reduce to 212,356 after valid targets and issue-target gap checks. `TP2_lag_10s` leaves 194,139, `TP2_lag_60s` leaves 101,085, and `TP2_lag_300s` leaves zero. Independently, 212,346 of the 212,356 base rows have no acceptable 300-second TP2 lag observation; the remaining 10 fail the historical-gap rule. The other two 300-second features have the same availability pattern. Thus zero Ridge training rows is the expected result of the frozen requirement for all seven complete features, not a skipped origin or fit crash. The recorded `FAILED_NO_TRAINING_ROWS` status is correct.

For F5 evaluation, 37,251 candidate issues reduce to 36,725 after future target/gap eligibility. The 10-second TP2 lag leaves 33,584, the 60-second lag leaves 17,532, and the 300-second TP2 lag has zero eligible rows: all 36,725 base rows lack an acceptable 300-second lookup. The 300-second TP3 and motor-current features are likewise unavailable for the whole base population. Therefore F5's zero Ridge forecasts are correctly produced by strict features; no fallback was silently substituted.

Across final origins, Ridge has only 64 scored forecasts total (F1 17, F2 21, F3 9, F4 17, F5 0). Sparse method-specific metrics and especially their tiny common intersections are not reliable evidence of comparative generalization.

## Common populations and timestamp identity

The protocol identity used was `(origin_id, original issue_row, actual target_row)`, not target timestamp alone. Final common counts were F1=0, F2=18, F3=9, F4=0, F5=0; pooled final common count was **27**, matching the saved results. Development common counts were D1=0, D2=155, D3=0, D4=2,428, D5=23 (pooled 2,606).

The audit separately intersected actual target timestamps and checked, for every shared timestamp, whether all methods also shared the same issue row. Final timestamp-only counts were 0, 18, 9, 0, 0 by F1–F5; pooled count was 27. No common target timestamp lacked a shared issue identity. Therefore, in these saved populations, timestamp-only intersection did not inflate the reported common count; issue-row plus matched-target identity remains the safer protocol key.

## Implementation review and limitations

Inspected implementation paths enforce expanding training windows, training issues strictly before origin, actual matched training-label timestamp at or before origin, evaluation target strictly before window end, finite target eligibility, issue-to-target gap exclusions, per-origin StandardScaler fitting on eligible training features only, fixed seven-feature order, and frozen Ridge parameters (`alpha=1`, intercept enabled, `solver='svd'`). Historical features use the latest recorded observation at or before requested lag time, reject stale/non-finite values, and reject prohibited gaps. No future-looking lookup or interpolation was found in the inspected code.

Deterministic parity checks compared production vectorized feature lookups with a scalar reference at 100 sampled rows across archive start/end for each of seven features (700 checks), and target matching at 200 deterministic sampled rows. Every match/exclusion agreed. Spot-check files preserve source issue row, issue/request time, matched row/time, and exclusion reason.

Remaining methodological limitations are not resolved by this audit:

- Source timestamps are naive; timezone and any duplicate-timestamp observation-order semantics remain unverified.
- The archive contains no historical publication/release timestamps. The frozen retrospective assumption of zero additional release latency is not evidence that features were available live at issue time.
- Coverage is highly selected and sparse for Ridge. Several final origins have no all-method common population.
- No scientific, causal, drift, production, or monitoring-threshold conclusion is established.

## Reproducible commands and verification

Commands executed in the `nussem1` Conda environment:

```text
conda run -n nussem1 python scripts/audit_phase2b_outputs.py
conda run -n nussem1 python -m py_compile src/*.py scripts/*.py tests/*.py
conda run -n nussem1 python -m pytest -q tests
conda run -n nussem1 python scripts/verify_rolling_outputs.py --phase development
conda run -n nussem1 python scripts/verify_rolling_outputs.py --phase final
```

Results: audit `PASS` (270 funnel rows, 30 origin-method count rows, 700 feature lookup checks, 200 target matcher checks); compilation passed; test suite **10 passed**; development and final verifiers both `PASS` (1,470,153 and 516,612 saved prediction rows, respectively). The first rerun after correcting the timestamp-only intersection calculation was interrupted while optimizing the scalar gap-reference check; it did not change historical results. The optimized read-only audit rerun completed with `PASS`.

Audit artifact hashes after the completed run:

| File | SHA-256 |
|---|---|
| `scripts/audit_phase2b_outputs.py` | `d0915ad8df69d8b6471670bc3989ccc38e24675f34dd36d1d8567692db14528d` |
| `results/audit/phase2b_coverage_funnel.csv` | `2d9d5877188b6b4ddc847e37b5e9894a11ba9e4b155907fbe06034366bb6b70b` |
| `results/audit/phase2b_count_reconciliation.csv` | `c143e8b673a5fa867d219d7911420a466266ff7f5abf0d8126aadcf9f0b9d681` |
| `results/audit/phase2b_feature_failures.csv` | `74ded8fe872d37ff3e34ab7835e678d1c3063b2f8f5498b357913856be49ba64` |
| `results/audit/phase2b_lookup_spot_checks.csv` | `35758b2ff63bae62aff5540ab1ef093e702985b68b2f8cbb9e4bdf0a39cc95f7` |
| `results/audit/phase2b_target_spot_checks.csv` | `40ec33cec469f563547bc6e4a2bf18f425f3b1da8efc284068b987a7c899cfab` |
| `results/audit/phase2b_metric_recalculation.json` | `fc13f90f9b8db35d836e22d803ac06e07d2633e1e2e8d80738abe366b420cc87` |

The checkout remains on `main` at the frozen commit with pre-existing uncommitted Phase 2B work and new audit artifacts. The existing `docs/ai_use_log.md` modification predates this audit; this audit made no AI-use-log edit or claim of independent human approval. The technical audit is complete for independent review; Phase 2B scientific interpretation remains provisional.
