# DS-A5 Rolling Forecasting

This repository studies retrospective forecasting of MetroPT-3 air-compressor `TP2` pressure 600 elapsed seconds ahead. MetroPT-3 was selected over UR3 CobotOps because UR3's local record covered only about seven hours and had many invalid timestamps; official NOAA SanctSound observations remained PARTIAL after HTTP 403, which did not establish that NOAA data were unavailable. The final rolling results show lower Persistence-versus-Seasonal-naive paired MAE/RMSE for Seasonal-naive on 77,165 shared forecasts, but lower forecast availability. Ridge has only 64 scored final forecasts and just 27 all-method common targets. Its sparse coverage prevents a robust model comparison. The Phase 2B technical audit passed its implementation checks; the scientific status remains **PARTIAL** because coverage is sparse, critical-period alignment is uncertain, and archive timestamps do not establish historical publication availability. The executed Notebook and local submission PDF are under `notebooks/` and `submission/`.

## Repository layout

- `docs/`: frozen protocol, provenance, audits, scientific analysis, monitoring plan, AI-use log, and Phase 4–6 review and submission records.
- `src/`: reusable temporal matching, feature construction, evaluation, and metric code.
- `scripts/`: evaluation, verification, audit, and descriptive analysis entry points.
- `tests/`: timestamp and rolling-integration checks.
- `results/audit/`: compact machine-readable audit results.
- `results/rolling/`: metrics, manifests, logs, and audit summaries; large raw prediction CSVs are excluded from Git.
- `results/analysis/`: compact Phase 3 summaries and figures.
- `notebooks/`: executed standard-review notebook.
- `submission/`: local PDF and SPAIQ submission draft.

## Frozen protocol

The frozen protocol predicts MetroPT-3 `TP2` pressure (bar) 600 elapsed seconds ahead using the committed expanding rolling-origin design. Exact matching, feature-eligibility, baseline, and evaluation rules are in [`docs/evaluation_protocol_v1.md`](docs/evaluation_protocol_v1.md); the freeze record is [`docs/evaluation_protocol_freeze_manifest.json`](docs/evaluation_protocol_freeze_manifest.json). The initial freeze commit is `ca83f0a295a68337aebc070cfd481645418cda13`. Evaluation windows are chronological, and the fixed Ridge solver uses no stochastic split or randomized fitting; no random seed is applicable.

## Data and excluded artifacts

The original MetroPT-3 data are from the [official UCI dataset page](https://archive.ics.uci.edu/dataset/791/metropt3%2Bdataset), under CC BY 4.0. The original CSV is excluded from Git; cloning the repository alone does **not** provide the source data required to execute the Notebook or reproduce the experiment. Download the official archive and place `MetroPT3(AirCompressor).csv` at `data/raw/metropt3/MetroPT3(AirCompressor).csv`. Verify its SHA-256 before use. Large row-level rolling prediction CSVs are also excluded from Git. Source/output hashes, sizes, and regeneration instructions are documented in [`docs/artifact_registry.md`](docs/artifact_registry.md). The MetroPT-3 source CSV hash is:

`db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`

The official UCI dataset pages and provenance are recorded in [`docs/sources.md`](docs/sources.md). The source SHA-256 pins the local dataset version. Place the source CSV at `data/raw/metropt3/MetroPT3(AirCompressor).csv` before running the rolling evaluation or Phase 3 script.

## Environment

Use the `nussem1` Conda environment. The verified environment uses Python 3.10.18; direct dependency versions are listed in `requirements.txt`.

```sh
conda activate nussem1
```

Install the pinned Python dependencies with `conda run -n nussem1 python -m pip install -r requirements.txt`. PDF export uses Playwright Chromium; if Chromium is not already installed, run `conda run -n nussem1 python -m playwright install chromium` once.

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

## Review the final research notebook

The executed, standard-review notebook is [`notebooks/DS_A5_rolling_forecasting.ipynb`](notebooks/DS_A5_rolling_forecasting.ipynb). Layer A verifies frozen/source/summary hashes, reads and audits the original MetroPT-3 CSV, rebuilds compact tables and figures, and does not retrain models. It requires the locally obtained, hash-verified raw CSV and committed metrics/audit summaries/analysis figures. Run it from a clean kernel with:

```sh
MPLCONFIGDIR=/tmp/ds-a5-mpl IPYTHONDIR=/tmp/ds-a5-ipython conda run -n nussem1 python -m nbconvert --to notebook --execute notebooks/DS_A5_rolling_forecasting.ipynb --output /tmp/DS_A5_rolling_forecasting.executed.ipynb --ExecutePreprocessor.timeout=900
conda run -n nussem1 python -m nbconvert --to webpdf notebooks/DS_A5_rolling_forecasting.ipynb --output-dir submission --output DS_A5_rolling_forecasting
```

Layer B is a separate full experimental reproduction path; it requires the same local raw CSV and locally regenerated large prediction CSVs. Follow the exact Phase 2B and Phase 3 commands above and below. The Phase 2B runner overwrites current top-level prediction/metric outputs; preserve local evidence before rerunning it. The notebook is not a substitute for the original raw file.

See [`docs/phase4b_submission_review.md`](docs/phase4b_submission_review.md) for the PDF visual-QA result, artifact hashes, and unresolved submission actions.

The final pre-submission audit and file-by-file packaging checklist are [`docs/phase6a_final_repository_audit.md`](docs/phase6a_final_repository_audit.md) and [`docs/final_submission_inventory.md`](docs/final_submission_inventory.md). External submission is not complete until the student supplies the Drive link and identity fields, verifies access, and records the submission on the course platform.

## Tests and syntax checks

```sh
conda run -n nussem1 python -m py_compile src/*.py scripts/*.py tests/*.py
conda run -n nussem1 python -m pytest -q tests
```

## Audit history and AI-use disclosure

Earlier NOAA access failures, dataset feasibility audits, and failed rolling-evaluation attempts are preserved as documented evidence. See [`docs/sources.md`](docs/sources.md), the reports under `docs/`, and the logs/manifests under `results/rolling/`. [`docs/ai_use_log.md`](docs/ai_use_log.md) records assistance, verification, and review status without claiming scientific certainty.
