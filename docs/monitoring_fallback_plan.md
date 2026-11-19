# Monitoring and Fallback Plan — Proposal

## Status and scope

This is a prospective monitoring design proposal derived from the Phase 3 archive analysis. It is **not implemented, deployed, or operationally validated**. The frozen evaluation protocol and its `5 s` historical lookup tolerance, `60 s` gap rule, `600 s` forecast horizon, and `600–605 s` target matching interval remain unchanged. No additional threshold is calibrated from final-period outcomes.

The source archive has naive timestamps and no historical publication times. Before any live claim, deployment must capture both event time and system-received time for each observation. The existing retrospective zero-additional-latency assumption is unverified.

## Event and data contract

For each scheduled issue, persist an immutable record containing:

- Model and protocol version, issue timestamp, issue receive timestamp, and source observation watermark.
- For every required lag feature: requested time, selected source row/time, value, age, and availability/exclusion reason.
- Gap/duplicate/out-of-order checks, finite-value checks, and the exact feature-eligibility result.
- Ridge prediction status/value, Persistence status/value, fallback status, and reason.
- When labels arrive: matched target row/time, label receive time, target-pair validity, and the scored error.

Keep source observations, predictions, delayed labels, and metric updates append-only. Never represent unavailable predictions as zero. Never calculate an error until the target label is actually available.

## Monitoring signals and responses

| Signal | Calculation and cadence | Action or trigger | Evidence and limitation |
|---|---|---|---|
| Timestamp integrity | On each batch: monotonicity, duplicate count, event-time interval median/quantiles, latest event-time and receive-time watermarks | Quarantine out-of-order/duplicate input from scoring until resolved; expose stale watermark as unavailable input | The archive is monotonic with no duplicate timestamps and median 10 s sampling, but production transport latency is unknown |
| Required feature freshness | At every issue, apply the frozen latest-at-or-before requested lag rule; record age and selected row for all seven features | Age over 5 s makes that feature unavailable under v1.0; Ridge is unavailable if any required feature fails | This is the frozen protocol rule, not a newly tuned production threshold |
| History continuity | For each required feature segment, check any adjacent timestamp gap greater than 60 s | Any prohibited gap makes the corresponding feature/forecast unavailable; report gap count and duration distribution | 331 such gaps occurred in the audited archive; all can be described but cannot establish live release availability |
| Feature and prediction coverage | Per origin/day and per method, report `available predictions / candidate issues`, `scored / valid targets`, unavailable reason counts, and zero-coverage intervals | If Ridge is unavailable and a valid Persistence forecast exists, proposed fallback may issue Persistence and mark `fallback=true`; if both are unavailable, issue no value and raise a service-availability event if the product contract requires a forecast | Ridge scored only 64 valid final rows; F5 had no Ridge predictions. Persistence scored all 169,215 valid final targets in the retrospective archive. Fallback itself is not implemented |
| Delayed label availability | Match the earliest observed target in `[issue+600 s, issue+605 s]`; record when it was first received | Keep issue-time prediction metrics pending until the matched label arrives; exclude invalid/gapped labels | Archive time is not release time. A live metric can only use recorded receipt time |
| Rolling forecast error | Daily MAE/RMSE and coverage with exact `n`; additionally aggregate errors by non-overlapping 10-minute issue blocks and show block counts | Display error/coverage trends after label arrival. Treat persistent changes as a review signal; do not apply an automatic performance action until a separate prospective calibration is approved | A 10-minute block reduces direct horizon overlap within a block but does not make adjacent blocks independent |
| Baseline comparison | Compare Ridge/fallback with Persistence on exact `(issue, actual target)` pairs; track paired MAE difference, wins/ties/losses, and paired count | Report only when paired sample support exists; otherwise show “insufficient paired coverage” | Final Ridge common population was only 27 for all three methods; no broad comparative conclusion is supported |
| Sensor/state distribution | Daily or weekly median, IQR, 5th/95th percentiles, missingness, `COMP` and selected state frequencies/transitions; keep a predeployment reference versioned | Flag changes for engineering investigation and annotation; do not infer a fault or retrain from the signal alone | Motor_current and state distributions changed materially by month; the archive does not establish cause |
| External failure records | Store UCI/company failure notices as retrospective annotation with source, original text, naive time, and alignment status | Do not use as real-time input or treat as exact ground truth without verified clock mapping | One UCI maintenance note is chronologically inconsistent with its associated failure window; timezone is absent |

## Persistence fallback: what is and is not supported

The v1.0 evaluator already computes Persistence as a baseline. It does **not** implement a Ridge-to-Persistence serving fallback. The Phase 3 script performed a separate retrospective replay using only saved predictions: use Ridge if present, otherwise Persistence. In the final archive this proposed rule triggered 169,151 times among 169,215 valid target pairs (99.962%), issued a replay forecast for every valid target, and yielded MAE/RMSE `2.1852 / 4.5285` bar. Persistence alone yielded `2.1852 / 4.5287` on its own scored population. Only 64 valid Ridge predictions replaced the fallback.

This result supports Persistence as a **candidate availability fallback for further review**, not as an empirically validated deployment policy. It says nothing about live freshness, transport delay, alert lead time, operational costs, or whether Persistence is safe for a train compressor. A future implementation must test fallback state transitions, dual-unavailability behavior, logging, and delay-aware scoring in a separate prospective/shadow evaluation.

## Threshold governance

Use only the frozen v1.0 `5 s`, `60 s`, and `600–605 s` rules as deterministic data/eligibility checks. Do not set a live error alarm from the August final errors or pick a coverage service-level threshold from observed final coverage. Before deployment, an independent engineering/operations owner must set service requirements and approve a calibration plan using data not used in this audit. Until then:

1. Report availability, coverage, error, and sample counts without automatically declaring degradation.
2. Distinguish a forecast that is unavailable or was not issued from a valid numerical prediction of `0`. Do not score an unavailable prediction as zero error or silently substitute Persistence; retain a valid zero-valued prediction as an ordinary forecast.
3. If the product requires a value and persistence is valid, use the explicitly approved fallback only after its implementation is separately reviewed; otherwise report no forecast.
4. Preserve every trigger and decision so offline replay can reconstruct exactly what the system knew at issue time.

## Reproduction and source evidence

Reproduce Phase 3 analysis using:

```text
conda run -n nussem1 python scripts/analyze_phase3.py
```

The script and machine-readable analysis manifest are `scripts/analyze_phase3.py` and `results/analysis/analysis_manifest.json`. The official event report source is the [UCI MetroPT-3 dataset page](https://archive.ics.uci.edu/dataset/791/metropt%2B3%2Bdataset). This plan does not modify or extend frozen evaluation rules, train a model, validate a live fallback, or claim any causal or production result.
