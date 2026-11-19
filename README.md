# DS-A5 Rolling Forecasting

This repository contains the DS-A5 feasibility investigation, frozen Evaluation Protocol v1.0, completed Phase 2B rolling evaluation and technical audit, and Phase 3 descriptive analysis. The Phase 2B technical audit passed its implementation checks, while Phase 2B/3 scientific status remains **PARTIAL** because Ridge coverage is extremely sparse, critical-period alignment is uncertain, and archive timestamps do not establish historical publication availability. No final submission notebook or PDF is included.

## Frozen protocol

The frozen protocol predicts MetroPT-3 `TP2` pressure (bar) 600 elapsed seconds ahead using the committed expanding rolling-origin design. Exact matching, feature-eligibility, baseline, and evaluation rules are in [`docs/evaluation_protocol_v1.md`](docs/evaluation_protocol_v1.md); the freeze record is [`docs/evaluation_protocol_freeze_manifest.json`](docs/evaluation_protocol_freeze_manifest.json). The initial freeze commit is `ca83f0a295a68337aebc070cfd481645418cda13`.

## Data and excluded artifacts

Original source data and large row-level rolling prediction CSVs are excluded from Git. Official UCI source pages, local expected hashes, prediction hashes, sizes, and regeneration instructions are documented in [`docs/artifact_registry.md`](docs/artifact_registry.md). The MetroPT-3 source CSV hash is:

`db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`

The official UCI dataset pages and provenance are recorded in [`docs/sources.md`](docs/sources.md). Place the source CSV at `data/raw/metropt3/MetroPT3(AirCompressor).csv` before running the rolling evaluation or Phase 3 script.

## Environment

Use the `nussem1` Conda environment. Dependency versions used for the audit are listed in `requirements.txt`.

```sh
conda activate nussem1
```

## Reproduce Phase 2B

The evaluation commands below execute the frozen rolling protocol and produce large prediction CSVs that remain ignored by Git. Manifests, metrics, logs, verification, and audit tables are retained in the repository.

```sh
conda run -n nussem1 python scripts/run_rolling_evaluation.py --phase development
conda run -n nussem1 python scripts/verify_rolling_outputs.py --phase development
conda run -n nussem1 python scripts/run_rolling_evaluation.py --phase final
conda run -n nussem1 python scripts/verify_rolling_outputs.py --phase final
conda run -n nussem1 python scripts/audit_phase2b_outputs.py
```

The rolling runner fits the frozen Ridge estimator per origin as specified by the protocol. Re-running it overwrites the current top-level phase outputs; preserve any local evidence before intentionally reproducing the run.

## Reproduce Phase 3

Phase 3 reads the original MetroPT-3 source and the saved Phase 2B predictions. It does not train or refit a model.

```sh
conda run -n nussem1 python scripts/analyze_phase3.py
```

The reports are [`docs/phase2b_execution_report.md`](docs/phase2b_execution_report.md), [`docs/phase2b_technical_audit.md`](docs/phase2b_technical_audit.md), [`docs/phase3_drift_failure_analysis.md`](docs/phase3_drift_failure_analysis.md), and [`docs/monitoring_fallback_plan.md`](docs/monitoring_fallback_plan.md). Reproduction commands, verified hashes, aggregate results, and figures are documented in each report and under `results/analysis/analysis_manifest.json`.

## Tests and syntax checks

```sh
conda run -n nussem1 python -m py_compile src/*.py scripts/*.py tests/*.py
conda run -n nussem1 python -m pytest -q tests
```

## Audit history and AI-use disclosure

Earlier NOAA access failures, dataset feasibility audits, and failed rolling-evaluation attempts are preserved as documented evidence. See [`docs/sources.md`](docs/sources.md), the reports under `docs/`, and the logs/manifests under `results/rolling/`. [`docs/ai_use_log.md`](docs/ai_use_log.md) records assistance, verification, and review status without claiming scientific certainty.
