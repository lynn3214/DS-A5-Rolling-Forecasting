# Phase 5A — Student-Requested Post-hoc Descriptive Diagnostics

## Status and scope

**Overall verdict: PARTIAL.** The requested computations completed and their integrity checks passed. The observations explain much of the sparse Ridge eligibility and clarify the F2 population reversal, but they do not establish physical clock drift, historical release-time availability, or causal operating-regime explanations. This report is a post-hoc descriptive response to the student review. It does not tune/select a model, change the frozen protocol, or replace the student's review.

No forecasting model was fitted or refitted. The frozen protocol, manifest, original MetroPT-3 CSV, saved Phase 2B predictions/metrics, Phase 3 outputs, notebook, and PDF were preserved. The diagnostic script verified 48 protected files before and after its run; all hashes matched. No Phase 2B/3 result was overwritten.

## A. Historical lag matching and Ridge availability

### Student question and method

The student asked whether five-second past-only lookup tolerance, nominally about ten-second sampling, lag requests at 10/60/300 seconds, and the seven simultaneous feature requirements explain the sparse and time-varying Ridge coverage. The proposed mechanism was treated as a hypothesis, not as an established cause.

The audit loaded the original CSV timestamps and sensor values. It reused `src.temporal.construct_features` and compared its point-in-time matches with an independent scalar, past-only search on 1,246 deterministic row/feature cases. For every monthly and frozen-window feature/lag row, the audit also compared the newly decomposed eligibility with the production feature matrix. Match categories are: exact age 0; positive age `(0,5]` seconds; stale age `>5` seconds; no past observation; non-finite selected value; and a `>60` second historical gap. Non-finite and gap rejection counts are reported only after the observation satisfies the age tolerance, making the rejection categories interpretable. Successful and unsuccessful lookup age quantiles are retained in the CSV.

### Verified monthly results

The three distinct lag offsets have the following per-feature eligibility counts. Features sharing a lag have the same timestamp lookup opportunity; all original sensor fields used here are finite in this CSV, so their empirical counts match by lag. “Joint” requires all seven frozen features simultaneously. Interval gap count is the number of observed adjacent intervals over 60 seconds whose ending observation falls in that month.

| Month | Candidate issues | 10s eligible | 60s eligible | 300s eligible | All 7 eligible (rate) | >60s intervals | Interval q05 / median / q95 (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Feb | 214,850 | 196,034 | 102,048 | 0 | 0 (0.000%) | 35 | 9 / 10 / 10 |
| Mar | 230,448 | 210,248 | 109,427 | 234 | 206 (0.089%) | 43 | 9 / 10 / 10 |
| Apr | 198,734 | 182,218 | 99,008 | 10,885 | 10,011 (5.037%) | 54 | 9 / 10 / 11 |
| May | 212,800 | 195,208 | 107,129 | 12,456 | 12,136 (5.703%) | 52 | 9 / 10 / 12 |
| Jun | 216,514 | 199,542 | 113,078 | 22,970 | 21,204 (9.793%) | 38 | 9 / 10 / 12 |
| Jul | 222,638 | 203,476 | 107,563 | 4,493 | 4,122 (1.851%) | 64 | 9 / 10 / 10 |
| Aug | 220,434 | 201,098 | 104,596 | 375 | 94 (0.043%) | 43 | 9 / 10 / 10 |

The monthly 300-second TP2-lag lookup illustrates the mechanism. In August, 220,249 of 220,434 candidates had a past observation more than five seconds before the requested timestamp; only 185 had a match with age 0–5 seconds, and 60 of those otherwise timely/finite cases crossed a prohibited historical gap, leaving 125 eligible for that single lag. For the same August candidates, 10-second eligibility was 201,098 and 60-second eligibility 104,596. The median sampling interval remained 10 seconds, with q05/q95 of 9/10 seconds, but a 10-second median does not guarantee phase alignment at a 300-second historical request. February had no final 300-second-lag eligibility; March had 234. Across the months, 300-second eligibility varied from zero to 22,970 while the median interval remained 10 seconds.

Non-finite-value rejections are zero for all reported sensor lookups. Gap rejections are much smaller than the stale-lookup counts at the 300-second lag; joint gap-exclusion candidates range from 10 to 108 by month, versus roughly 199k–220k monthly candidates. Thus the directly observed bottleneck is the requested-time/past-observation age alignment at longer lags, with gaps as an additional but much smaller exclusion. This is a description of timestamps in the archive. It does **not** establish physical clock drift or its cause. The timestamp interval distribution varies (including 9-second intervals and changing 11–60 second interval counts), and cumulative timestamp irregularity can affect a 300-second requested offset; no independent clock reference exists to diagnose clock behavior.

Monthly issue-time feature eligibility is not the same population as expanding-model training eligibility. Monthly joint eligibility is zero in February, 206 in March, peaks at 21,204 in June, then falls to 94 in August. The five frozen final windows separately contain 17/28,576 (F1), 25/40,143 (F2), 9/37,069 (F3), 17/29,165 (F4), and 0/37,251 (F5) issue rows with all seven features. These feature counts do not by themselves require a valid future evaluation label, so they need not equal scored Ridge predictions.

## B. Monthly issue eligibility versus cumulative training eligibility

The monthly table above uses each month's issue-time observations as its denominator. The following expanding counts use a different population: all issue rows before each origin that satisfy the frozen feature, target, gap, and actual-label-at-origin rules. Counts were reconstructed from the original timestamp/sensor arrays and compared against saved Phase 2B `training_sample_count` for every origin.

| Phase/origin | Origin | Target/gap-eligible historical pairs | Reconstructed feature-complete training rows | Saved Phase 2B rows | Match |
|---|---|---:|---:|---:|---|
| D1 | 2020-03-01 | 212,356 | 0 | 0 | Yes |
| D2 | 2020-04-01 | 439,183 | 158 | 158 | Yes |
| D3 | 2020-05-01 | 633,965 | 9,986 | 9,986 | Yes |
| D4 | 2020-06-01 | 842,555 | 21,568 | 21,568 | Yes |
| D5 | 2020-07-01 | 1,055,970 | 42,650 | 42,650 | Yes |
| F1 | 2020-08-01 | 1,273,871 | 46,711 | 46,711 | Yes |
| F2 | 2020-08-07 | 1,310,538 | 46,728 | 46,728 | Yes |
| F3 | 2020-08-13 | 1,358,562 | 46,749 | 46,749 | Yes |
| F4 | 2020-08-19 | 1,402,887 | 46,784 | 46,784 | Yes |
| F5 | 2020-08-25 | 1,440,152 | 46,801 | 46,801 | Yes |

No discrepancy was found; the audit would stop before interpretation if any count differed. D2 is a cumulative pre-April origin training history, not a March-only sample; similarly, D5 and F1–F5 are expanding histories rather than single-month cohorts. It is therefore invalid to compare their cumulative counts as if they represented individual months. The fair period-level comparison is the monthly denominator table plus the separate frozen-window issue eligibility counts.

## C. Paired baseline error tails and population sensitivity

### Error difference and tails

For each exact shared `(origin_id, issue_row, target_row)` baseline pair, the difference is `|seasonal-naive error| − |persistence error|`; negative values favor seasonal-naive. Ties are `abs(difference) <= 1e-12` bar. The source rows were reconstructed from saved final predictions and their target identities were checked against the frozen target matcher and the existing Phase 3 paired artifact.

| Origin | n | Mean | Median | q05 | q25 | q75 | q95 | Seasonal win / tie / loss |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F1 | 8,121 | −0.2476 | 0 | −9.618 | −0.002 | 0.002 | 9.386 | 3,039 / 2,321 / 2,761 |
| F2 | 22,979 | −0.1492 | 0 | −9.574 | −0.002 | 0.002 | 9.466 | 8,305 / 7,029 / 7,645 |
| F3 | 13,743 | −0.2263 | 0 | −9.608 | −0.002 | 0.002 | 9.366 | 5,149 / 4,230 / 4,364 |
| F4 | 13,428 | −0.2556 | 0 | −9.708 | −0.002 | 0.002 | 9.447 | 5,175 / 3,232 / 5,021 |
| F5 | 18,894 | −0.4529 | 0 | −9.754 | −0.002 | 0.002 | 9.485 | 7,789 / 4,953 / 6,152 |
| Pooled | 77,165 | −0.2662 | 0 | −9.660 | −0.002 | 0.002 | 9.442 | 29,457 / 21,765 / 25,943 |

The median is zero and the interquartile range is only −0.002 to +0.002 bar, while the 5th/95th percentiles are near ±9.5 bar. Thus a median-centered boxplot with hidden fliers conceals a substantial two-sided tail. The mean advantage is not attributable to the largest 1% alone: the deterministic top-1%-by-absolute-difference set (`ceil(0.01*n)`, stable original-row order for ties) contributes −546.882 bar-units to the pooled signed difference sum, 2.66% of the net signed sum, and 5.24% of the total absolute-difference mass. The top 5% contributes −3,292.874 bar-units, 16.03% of net signed sum and 25.66% of absolute-difference mass. Positive and negative tail contributions coexist; the signed percentage is a share of a negative net and is not a causal attribution. By origin, top-5% absolute-mass shares are F1 27.84%, F2 27.53%, F3 27.01%, F4 23.82%, and F5 23.42%.

The new figure displays mean and median separately, labels exact paired counts, and reports the top-5% share of total absolute difference so the mean/tail contrast is visible. It does not replace or modify the Phase 3 figure.

### F2 population sensitivity

The baseline pair set contains exactly 22,979 matching forecast identities. On this set, Persistence MAE/RMSE is 2.0515/4.3929 bar and Seasonal-naive is 1.9023/4.2239 bar. The all-three-method intersection contains exactly 18 identical issue/target identities. On these 18, Persistence is 0.0018/0.0024 bar, Seasonal-naive 2.1004/4.4524 bar, and Ridge 0.2526/0.4829 bar. The Persistence-versus-Seasonal ranking reverses on this highly selected subset.

On those 18 identities, observed TP2 target-minus-issue change has median +0.001 bar, median absolute change 0.002 bar, and range −0.006 to +0.004 bar. This verifies that the selected 18 forecast intervals have little observed TP2 movement. It does not show that all Ridge-eligible periods are stable, nor does it establish why these observations passed the feature, training, and target filters. An 18-row intersection cannot determine the overall baseline ranking; the larger paired-baseline population and all-three intersection answer different questions and must remain separately labeled.

## Student question traceability

| Review item | Student's question/concern | Evidence produced | Follow-up status |
|---|---|---|---|
| A | Do five-second lag matching, ~10-second sampling, and seven feature requirements explain variable Ridge coverage? | `monthly_lag_alignment.csv`, `monthly_joint_feature_eligibility.csv`, scalar parity checks | Longer-lag age misalignment is supported as the dominant observed eligibility constraint; physical clock drift and historical release availability remain unknown. |
| B | Are early training counts comparable to August evaluation eligibility; why is August sparse? | `expanding_training_reconciliation.csv`, monthly/window eligibility tables | Populations are different; all saved training counts reconcile. August 300s eligibility is very low despite median interval 10s. Cause beyond timestamp alignment evidence remains unproven. |
| C | Does a zero-median paired boxplot hide meaningful error tails? | `paired_error_tail_summary.json`, `paired_error_tails.png` | Yes: median 0, IQR ±0.002, but 5th/95th percentiles near ±9.5 bar. Top-tail contribution is quantified without claiming causality. |
| C | Does F2's 18-row all-method subset reverse the baseline ranking relative to 22,979 paired baseline rows? | `f2_population_sensitivity.json` | Yes; exact identities and metrics verified. The 18-row subset is too selected/small to set broad ranking. |
| D | Could observed distribution changes represent operating-regime changes rather than sensor drift? | Existing Phase 3 descriptive report; the present audit adds no causal attribution | Unresolved; these diagnostics cannot distinguish sensor drift from changes in operating mixture. |
| E | Should the notebook explain feature coverage and tails more clearly? | This report and the new standalone figure/table artifacts | Recommend a targeted revision after student review; the notebook/PDF were intentionally not modified. |

## Verification, provenance, and execution record

Original input hashes: MetroPT-3 CSV `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`; development predictions `c53e94087feb4c2bd10cab0df0c3e08f4364f2eb97f10c22d9508575fe20d586`; development metrics `1c97599d08311a2cadca555313ee1ab87d7c3648539e34f73235c316dafde641`; final predictions `e2cdf4de6f838f8f06d241149e514d09bc33e0192ac5073b7d1e02e83a12db41`; final metrics `6af02ab6d02e491b622f66d3b0b45b62a871a6c264f917c92d519ced2f9f4d11`; Phase 3 paired pairs `bb7eda2d4eed94ecc00a698d3d896b27b9651e45510cdb38e6459ade4dcca0ee`.

The diagnostic manifest records before/after hashes for 48 protected files across the source data, frozen specifications and implementation, all Phase 2B rolling outputs, all Phase 3 analysis outputs, notebook, and submission package. All are identical. It also records a Git status checkpoint and recent log, environment, source-code hashes, commands, checks, and output hashes. No commit or push was made.

Commands executed in the required Conda environment:

```text
conda run -n nussem1 python -m py_compile scripts/verify_student_review_findings.py tests/test_student_review_diagnostics.py
conda run -n nussem1 python scripts/verify_student_review_findings.py
conda run -n nussem1 python -m pytest -q tests
```

Final outcomes: compilation passed; diagnostic status `PASS` with 1,246 scalar lookup parity cases, all 84 monthly/frozen-window feature-period decompositions, exact D1–D5/F1–F5 training-count reconciliation, exact Phase 3 paired identities, F2 n=22,979 baseline pairs, and n=18 all-three identity equality; test suite **13 passed**. One intermediate diagnostic run stopped with an `IndexError` caused by indexing the production joint-eligibility vector as a feature matrix. The diagnostic code was corrected to compare against the actual per-feature finite matrix; the final run passed, and the failed run wrote no final outputs. Matplotlib reported that its default user cache was not writable and used a temporary cache; figure generation completed successfully.

New artifacts and SHA-256 values are recorded in `results/student_review_diagnostics/diagnostic_manifest.json`. Principal output hashes:

| Artifact | SHA-256 |
|---|---|
| `scripts/verify_student_review_findings.py` | `3eb9d05842a0826f946fe4f1655c0aa864249fcb21be690841ee20527bfe1539` |
| `tests/test_student_review_diagnostics.py` | `d3b354f0da6a5e4410e0f11b6ac732e1b0f0b3d69a0dea4b8ec0a41a5ea04888` |
| `results/student_review_diagnostics/monthly_lag_alignment.csv` | `917d648cc4facda20fa2ff41dbbb480256082737efdd5103e12476a6f5340f5a` |
| `results/student_review_diagnostics/monthly_joint_feature_eligibility.csv` | `4f13aa40d9ca3a31d38a2173ddbbd0f6f8cde82ff48d79af5e09c326f05dec71` |
| `results/student_review_diagnostics/expanding_training_reconciliation.csv` | `e285250625d7ef2b27e4d383a31c561d076a4be01336845915b6af39745787d1` |
| `results/student_review_diagnostics/paired_error_tail_summary.json` | `1519e41be27448ec7e61af5036bbfd9c5276cbb9d0da156f72084f3b98254e20` |
| `results/student_review_diagnostics/f2_population_sensitivity.json` | `9cf87255e7d601cdbd3298d517bb9c71eb31f3850fec5cd8da12fac2ecbca174` |
| `results/student_review_diagnostics/paired_error_tails.png` | `9aaa45f796238fb590a7e55f4fa955f1339c2d720d261170b7f858417c69a155` |

## Interpretation limits and notebook recommendation

No timezone, physical-clock reference, or historical publication/release timestamps are available. Archive observation time therefore does not prove feature availability at a live forecast issue time. The monthly timestamp evidence supports an observed long-lag alignment explanation, not a physical clock-drift diagnosis. Overlapping forecasts are dependent; no iid significance claim is made. The F2 18-row subset is descriptive and highly selected.

Recommend a narrowly targeted notebook revision only after independent student review: explain why a 10-second median interval does not imply 300-second lookup alignment; distinguish monthly issue-feature eligibility from cumulative training rows; show the mean/median/tail figure with exact denominators; and explain the F2 22,979-versus-18 population reversal. Retain every frozen result and its limitation. No notebook or PDF edit is part of Phase 5A. New diagnostics are **pending student verification**.
