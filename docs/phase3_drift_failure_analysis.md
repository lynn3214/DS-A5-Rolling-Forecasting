# Phase 3 — Drift, Failure, and Monitoring Analysis

## Verdict

**PARTIAL.** The descriptive analysis, exact paired baseline comparison, error/coverage tables, figures, and reproducibility checks completed. Evidence supports substantial changes in observed operating regimes, but it does not establish why they occurred or that they caused prediction errors. Only one of the four UCI-listed failure windows intersects a saved evaluation window. Naive timestamps and the extremely sparse Ridge population limit conclusions.

This is an analysis of the frozen v1.0 evaluation records, not a new model-development phase. The protocol, input data, configurations, windows, predictions, and metrics were not changed. No forecasting model was fitted, refitted, tuned, or selected.

## Evidence and provenance

The script verifies these exact input hashes before analysis:

| Input | SHA-256 |
|---|---|
| `data/raw/metropt3/MetroPT3(AirCompressor).csv` | `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24` |
| `results/rolling/development_predictions.csv` | `c53e94087feb4c2bd10cab0df0c3e08f4364f2eb97f10c22d9508575fe20d586` |
| `results/rolling/development_metrics.json` | `1c97599d08311a2cadca555313ee1ab87d7c3648539e34f73235c316dafde641` |
| `results/rolling/final_predictions.csv` | `e2cdf4de6f838f8f06d241149e514d09bc33e0192ac5073b7d1e02e83a12db41` |
| `results/rolling/final_metrics.json` | `6af02ab6d02e491b622f66d3b0b45b62a871a6c264f917c92d519ced2f9f4d11` |

The official [UCI MetroPT-3 record](https://archive.ics.uci.edu/dataset/791/metropt%2B3%2Bdataset) describes 1,516,948 records, 15 sensor signals, a nominal 0.1 Hz attribute entry, and a separate statement that the onboard logger recorded at 1 Hz. It also publishes four air-leak/high-stress report windows, with the first two rows both labeled Report #1. The local CSV contains 1,516,948 rows, sorted naive timestamps from `2020-02-01 00:00:00` through `2020-09-01 03:59:50`, no duplicate timestamps, and no missing values in its 15 sensor fields. Its timestamp intervals have median 10 seconds, 5th percentile 9 seconds, and 95th percentile 10 seconds, empirically supporting 0.1 Hz sampling for this file. The CSV's `Unnamed: 0` index was not used as elapsed time.

There are 331 adjacent intervals greater than 60 seconds (0.0218% of intervals). These are observed timestamp discontinuities; the archive does not establish whether they reflect acquisition downtime, preprocessing, or another cause. The sensor cells themselves have no missing values. September 2020 is only partially observed: the file contains 530 September observations through 03:59:50. This partial month extends beyond the UCI page's broad February–August description and must not be interpreted as a directly comparable complete monthly regime.

## Fair final baseline comparison

Metrics in each method's separate scored population are descriptive and are not a paired superiority comparison. The exact paired population uses `origin_id + issue_row + actual target_row`, with both baselines available and the same valid target. The row-level absolute-error difference is `seasonal-naive absolute error − persistence absolute error`; negative values favor seasonal-naive on that individual pair. Ties use an absolute difference tolerance of `1e-12` bar.

| Final origin | Separate Persistence n; MAE / RMSE | Separate Seasonal n; MAE / RMSE | Paired n | Paired Persistence MAE / RMSE | Paired Seasonal MAE / RMSE | Paired MAE difference (S−P) | Seasonal win / tie / loss |
|---|---:|---:|---:|---:|---:|---:|---:|
| F1 | 28,036; 2.0003 / 4.3333 | 8,121; 1.8838 / 4.2075 | 8,121 | 2.1314 / 4.4831 | 1.8838 / 4.2075 | −0.2476 | 3,039 / 2,321 / 2,761 |
| F2 | 39,519; 2.0273 / 4.3683 | 22,979; 1.9023 / 4.2239 | 22,979 | 2.0515 / 4.3929 | 1.9023 / 4.2239 | −0.1492 | 8,305 / 7,029 / 7,645 |
| F3 | 36,435; 2.2032 / 4.5425 | 13,743; 1.8803 / 4.1836 | 13,743 | 2.1066 / 4.4435 | 1.8803 / 4.1836 | −0.2263 | 5,149 / 4,230 / 4,364 |
| F4 | 28,560; 2.3919 / 4.7278 | 13,428; 2.2188 / 4.5538 | 13,428 | 2.4744 / 4.8108 | 2.2188 / 4.5538 | −0.2556 | 5,175 / 3,232 / 5,021 |
| F5 | 36,665; 2.3181 / 4.6702 | 18,894; 1.9757 / 4.2866 | 18,894 | 2.4286 / 4.7821 | 1.9757 / 4.2866 | −0.4529 | 7,789 / 4,953 / 6,152 |

Persistence has predictions for every candidate issue and every valid target pair in all five final windows. Seasonal-naive has lower scored coverage: 29.0%, 58.1%, 37.7%, 47.0%, and 51.5% of candidate issues in F1–F5, respectively. Its scored population equals the paired population here because persistence is available for every valid target pair. On the paired samples, seasonal-naive has lower MAE and RMSE in every origin; the sign is consistent with its separate-population MAE, while the paired Persistence error is higher than its method-specific error because it is restricted to the times Seasonal-naive can score. This population selection materially changes the Persistence estimate and the magnitude of the difference.

Across the 77,165 paired final rows pooled descriptively, Persistence has MAE/RMSE `2.2356 / 4.5831`, Seasonal-naive `1.9695 / 4.2897`, and the mean per-pair absolute-error difference is `−0.2662` bar. The raw counts are not independent replicates: issue times are sampled about every ten seconds while the target horizon is ten minutes, so forecast windows overlap and errors are serially dependent. No iid standard errors, row bootstrap intervals, or significance claims are reported. Origin-level and paired per-row values are retained in `results/analysis/paired_baseline_comparison.csv` and `paired_baseline_pairs.csv`.

## Error over time and coverage

Daily values use forecast issue dates. MAE/RMSE include only available predictions with a valid target pair; unavailable forecasts and invalid labels do not become zero errors. Calendar days with no saved evaluation issues are represented in the daily table with zero candidate count and missing metrics, and plotted lines break across those dates. Days with candidates but zero Ridge predictions have zero coverage and missing MAE/RMSE. Figures annotate scored counts for daily errors and available/candidate counts for coverage; machine-readable denominators are in `error_coverage_by_day.csv`.

In final evaluation, Persistence daily MAE ranges from 1.8872 bar (F2, Aug 8, n=7,781) to 2.8782 bar (F4, Aug 23, n=1,803). Seasonal-naive daily MAE ranges from 0.0018 bar (Aug 23, n=66) to 2.4171 bar (Aug 19, n=6,366); the extremely low Aug 23 value has only 66 scores from 1,871 candidates and should not be generalized. The Ridge daily points have n=3–17, and numerous candidate days have n=0. Those points are shown with explicit counts only; they are not evidence of a daily performance trend.

Figures:

- [Daily final MAE](../results/analysis/figures/phase3_daily_mae_final.png)
- [Daily final prediction coverage](../results/analysis/figures/phase3_daily_coverage_final.png)
- [Final per-origin MAE/RMSE](../results/analysis/figures/phase3_final_origin_metrics.png)
- [Final method-specific absolute-error distributions](../results/analysis/figures/phase3_final_error_distributions.png)
- [Monthly sensor and continuity overview](../results/analysis/figures/phase3_monthly_drift_overview.png)
- [Paired baseline error differences](../results/analysis/figures/phase3_paired_baseline_error_difference.png)

All displayed Ridge error and coverage points carry scored or available sample counts. The method-specific distribution plot is explicitly not paired; its populations differ.

## Observed distribution changes and forecasting outcomes

`results/analysis/drift_summary.csv` reports monthly and exact frozen-window distributions, missing rates, quantiles, time intervals, gaps, and state-signal transitions. These are descriptive population summaries; no independence-based hypothesis tests are used.

Observed examples across calendar months:

- Median Motor_current is about 0.04 A in February–May, rises to 3.715 A in June and 3.633 A in July, then returns to 0.045 A in August.
- `COMP=1` frequency is 93.9% in February, 71.9% in June, and 87.3% in August; monthly COMP transition frequency also varies.
- TP2's June 75th percentile is 7.348 bar, versus approximately −0.01 bar in most surrounding months. This indicates a substantial change in the empirical operating-value mixture; it is not, by itself, proof of a fault or a cause of forecast error.
- Median oil temperature rises from 56.6 °C in February to 67.0 °C in July and is 65.2 °C in August.
- The median sampling interval remains 10 seconds by month. The number of >60-second gaps ranges from 35 (February) to 64 (July), with 43 in August.

Observed forecast outcomes also vary by origin. Development Persistence MAE ranges from 1.3913 (D3) to 2.4864 (D5), while final Persistence MAE ranges from 2.0003 (F1) to 2.3919 (F4). Seasonal-naive and Ridge outcomes vary as well. These performance changes are observations from different windows and, for Seasonal-naive/Ridge, different selected scoring populations; they do not identify a causal drift mechanism. The month-level sensor shifts and origin-level errors are reported separately so that an observed distribution change is not conflated with a causal explanation.

Ridge's seven required lag features and strict continuity rules are unchanged. D1 has zero eligible Ridge training rows; F5 has zero Ridge predictions; only 64 final Ridge predictions have valid targets, and the all-three-method final common population is 27. The existing independent per-feature failure evidence in `results/audit/phase2b_feature_failures.csv` shows the 300-second lag lookups as the primary availability bottleneck. The sequential funnel in `phase2b_coverage_funnel.csv` is order-dependent and cumulative; its separate independent condition counts in `phase2b_feature_failures.csv` are not additional sequential filters and must not be added to infer unique exclusions.

Final Ridge forecasts are temporally concentrated: F1 17 scored rows, F2 21, F3 9, F4 17, F5 0. They occur on only seven issue dates in August, with n=3–17 per date. By issue-time COMP state, eligibility is very low in both COMP=0 and COMP=1 strata and changes direction across origins; a simple state association is not consistent. A >60-second gap in the prior 300-second issue-time lookback appears in only 20 F2 and 26 F3 candidate rows and none are feature-eligible; however, eligibility remains extremely low even among the much larger no-gap populations. Thus observed sparse Ridge coverage is not explained by those few recent-gap cases alone. COMP is used only for retrospective stratification, not added to the frozen model.

## Critical-period analysis

Event timestamps and descriptions are taken from the failure table on the [official UCI dataset page](https://archive.ics.uci.edu/dataset/791/metropt%2B3%2Bdataset). UCI's table gives these naive times: Apr 18 00:00–23:59; May 29 23:30–May 30 06:00; Jun 5 10:00–Jun 7 14:30; and Jul 15 14:30–19:00. It calls the first two rows “Report #1”; the second row also carries “Maintenance on 30Apr at 12:00”, which predates its May 29 failure window. This source inconsistency is preserved and unresolved. The page does not identify a timezone, and MetroPT timestamps are naive; exact event-to-observation alignment is therefore unknown.

Issue timestamp is used for retrospective group membership, with inclusive reported start/end. The first, second, and fourth event periods contain 8,657, 2,360, and 1,622 raw observations respectively, but none intersects a saved evaluation window; no forecast error comparison is supported for those events. The June 5–7 event intersects development origin D4 and contains 17,315 candidate issue timestamps, with 17,031 Persistence scores, 14,274 Seasonal-naive scores, and only 9 Ridge scores. On the exact paired Persistence/Seasonal subset (n=14,274), event-window MAE is 0.6333 vs 4.4586 bar; outside the event but within the same D4 origin (n=44,691), it is 2.0455 vs 1.9012 bar. This exploratory reversal is not a causal failure effect: event timing is uncertain, groups are selected by issue time, the event labels are not sensor-clock truth, and samples are dependent. Details and unsupported windows are in `critical_period_summary.csv`.

## Monitoring and fallback

The operational proposal is in [`monitoring_fallback_plan.md`](monitoring_fallback_plan.md). In brief: record input freshness, duplicate/out-of-order timestamps, interval gaps, each required lag's availability reason, and per-method prediction availability; never replace a missing prediction with zero. Score only after the actual matched label is available, report daily counts with MAE/RMSE, and compare methods on identical issue/target identities. Track sensor/state quantiles and transition/gap rates against an explicitly documented reference period, but do not use the current final results to tune a threshold.

An explicitly permitted retrospective replay uses the saved Ridge prediction when available and saved Persistence otherwise. On valid final target pairs it triggers fallback on 169,151 of 169,215 cases (99.962%), produces 100% scored coverage in this archive replay, and has MAE/RMSE `2.1852 / 4.5285` bar. This is essentially the Persistence result (`2.1852 / 4.5287`); it only substitutes 64 valid Ridge predictions. This is offline evidence that a Persistence fallback could fill archive replay gaps, not an implemented, live-tested, or validated deployment policy. The zero-additional-publication-latency assumption remains unverified.

## Reproducibility and limits

Run with:

```text
conda run -n nussem1 python scripts/analyze_phase3.py
```

The script verifies all five input hashes, checks one record per method and issue, rejects invalid labels from scoring, pairs by the frozen issue/target identity, independently recomputes all development/final per-origin and pooled metrics (72 metric checks), and reconciles daily counts to per-origin counts. The `analysis_manifest.json` records command, software versions, source hashes, output hashes, definitions, and limitations. Figures are generated from the saved machine-readable summaries. No model fitting or protocol modification occurred.

Executed verification: `conda run -n nussem1 python -m py_compile scripts/analyze_phase3.py` passed; `conda run -n nussem1 python scripts/analyze_phase3.py` completed with `PASS_WITH_LIMITATIONS`; `conda run -n nussem1 python -m pytest -q tests` reported **10 passed**. All 14 listed generated output hashes and the script hash were independently checked against `analysis_manifest.json`; no mismatch was found. The manifest SHA-256 is `ff37fe5933b41d1ebc144f1a45d375c050739377dae9307b2d830d2f2b8a3e9f`.

Important limitations: timestamps and failure reports lack verified timezone/publication semantics; source sensor values do not establish when they were historically released; dense forecasts overlap and are serially dependent; critical labels are uncertain; Ridge metrics are extremely sparse; and no cause, validated threshold, production performance, or scientific conclusion is established. **Phase 3 is complete for independent review with a PARTIAL verdict.**
