# AI use log

This is a factual summary of assistance in the DS-A5 repository. It does not reconstruct verbatim prompts or claim manual review of final assignment results.

| Work | AI assistance | Human review/status |
|---|---|---|
| Dataset feasibility | Codex inspected official NOAA/UCI sources, audited supplied local MetroPT-3 and UR3 data, and recorded access limitations and provenance. | User supplied local files and reviewed dataset-selection recommendations. NOAA ERDDAP access remained blocked. |
| Temporal protocol | Codex developed timestamp matching, gap, origin, availability, and leakage specifications and diagnostics. | ChatGPT independent analysis was reviewed by the user; the user explicitly approved freezing Evaluation Protocol v1.0 in the supplied request. |
| Code review and tests | Codex implemented non-modeling diagnostics and deterministic timestamp tests. | Tests and local integrity checks were executed and recorded; forecasting models were not trained. |
| Protocol freeze | Codex prepared the freeze manifest and repository commit. | User authorization was provided for protocol freezing and a local first commit. No GitHub push was performed. |

No final forecasting results exist in this phase. No claim is made that such results or a final notebook were manually reviewed.

## Phase 2B execution

Codex implemented reusable feature construction, baselines, expanding rolling-origin Ridge evaluation, leakage assertions, raw prediction outputs, and independent output verification. Debugging included two import-path failures, an empty Ridge inference batch, and an omitted candidate-row issue for a failed development origin; failed logs and intermediate outputs were preserved under `results/rolling/`. Final test run: 10 passed. Development and final evaluations ran; D1 had no eligible Ridge training rows, Ridge prediction coverage was sparse, and F5 had no Ridge predictions. At the time of the initial Phase 2B run, no separate implementation commit or push had been made. An independent reviewer accepted the Phase 2B/3 documented artifacts for submission preparation, but did not rerun the full raw-data analysis. No complete independent replication or final scientific validation is claimed.

## Phase 3 descriptive analysis

Codex added `scripts/analyze_phase3.py` and generated paired Persistence/Seasonal-naive comparison tables, exact issue/target-pair error differences, daily and per-origin error/coverage summaries, monthly and frozen-window sensor/state/gap summaries, a retrospective UCI critical-period subgroup table, figures, an explicitly labeled offline Ridge-to-Persistence replay, and an analysis manifest. The analysis verified the original data and four prediction/metric file hashes, paired baselines by `origin_id + issue_row + actual target_row`, and recomputed development/final per-origin and pooled metrics (72 checks). It did not fit, refit, tune, or select forecasting models, modify the frozen protocol, or change saved predictions/metrics. The explicit fallback replay followed the frozen protocol's allowed retrospective diagnostic and is not described as deployed or validated. The user-provided constraints to avoid causal claims, final-period tuning, iid uncertainty claims, and false zero-error imputation were followed. No model/feature/horizon or deployment-threshold changes were implemented. Verification results and unresolved timestamp/publication-time limitations are documented in the Phase 3 report and manifest. An independent review accepted the Phase 3 artifacts for submission preparation; it did not independently rerun the complete raw-data analysis. No claim is made that the Phase 3 analyses were fully independently replicated or that final assignment results received complete human review.
