# Phase 4B — Final Submission Preparation Review

## Verdict

**PASS for local submission preparation.** The revised Notebook completed a clean-kernel run, the WebPDF export passed visual and text checks, repository tests passed, and the SPAIQ record is prepared as a draft. This is not a claim that anything was pushed, uploaded, submitted, or personally reviewed by the student. Those final actions remain outstanding.

## Official requirements and destinations

The official [DS-A5 assignment catalog](https://tjluo-ucas.github.io/ds/en/assignments/) and [course submission guide](https://tjluo-ucas.github.io/ds/en/submission-guide/) were rechecked on 2026-11-22.

| Official requirement | Evidence in this repository | Status |
|---|---|---|
| Executable notebook and exported PDF | Executed `notebooks/DS_A5_rolling_forecasting.ipynb`; WebPDF at `submission/DS_A5_rolling_forecasting.pdf` | Verified locally |
| Reproduction commands and environment | `README.md`, pinned `requirements.txt`, frozen protocol and manifests | Verified locally; raw CSV remains a separately obtained input |
| Data source, license, split/protocol, assumptions, metrics and outputs | UCI source and CC BY 4.0 provenance, source hash, frozen protocol, actual saved summaries, failure analysis | Documented; source file is excluded from Git |
| Error/failure and applicability-boundary evidence | Sparse Ridge coverage, D1 failed fit, F5 zero predictions, low common-target count, retrospective event alignment limitations | Included in Notebook |
| AI-use record and independent verification | `docs/ai_use_log.md`, notebook/hash assertions, test results | Updated; student final review is pending |
| GitHub code and README | Repository remote is configured; latest local Phase 4B changes are not committed or pushed | **Not uploaded/pushed** |
| Google Drive written materials and supporting PDF | Drive folder/link is not supplied; SPAIQ draft includes a conspicuous placeholder | **No upload; user action required** |
| Course-platform submission record | Draft created at `submission/spaiq_submission_draft.md` | **Not submitted** |

The course guide requires the student's name and student ID on the platform record, a Drive link, and a GitHub link. No identity or Drive link was invented. The platform-specific submission state/access permissions and its authoritative deadline were not checked. No external service was accessed to upload or submit these files.

## Files created or changed

- Created `submission/DS_A5_rolling_forecasting.pdf`.
- Created `submission/spaiq_submission_draft.md` with a 209-word English summary and manual checklist.
- Created this review report.
- Updated `notebooks/DS_A5_rolling_forecasting.ipynb` to exclude the `Unnamed: 0` file index from the 15 sensor/state fields and sensor-missingness count, avoid personal absolute paths in saved outputs, clarify Layer A/Layer B local-data dependencies, show actual 300-second lag-funnel stages, and provide accessible embedded figure captions. The experiment and saved historical metrics were not changed.
- Updated `README.md` with the question and main findings, repository layout, UCI source/license/hash, setup, standard and full reproduction routes, PDF export, technical checks, excluded artifacts, and limitations.
- Updated `requirements.txt` with pinned notebook/PDF-rendering dependencies, including Playwright.
- Updated `docs/ai_use_log.md` with factual research-planning and Phase 4B activity and pending human review status.

NOAA and previous alternative-dataset audits, protocol freeze, evaluation metrics, predictions, and Phase 3 analysis artifacts were preserved.

## Notebook execution and integrity

The final executed Notebook contains 28 cells, including 13 code cells; all 13 have execution counts from the fresh-kernel run. There are zero cell errors. Notebook schema validation passed. The standard path checked the local original dataset, frozen document/script/diagnostic hashes, Phase 2B metrics hashes, Phase 3 manifest output hashes, and frozen-commit ancestry.

The latest execution verified:

- The source CSV has 17 raw fields: one `Unnamed: 0` file-index field, one timestamp field, and 15 sensor/state fields. Missing sensor cells are **0 across the 15 actual sensor/state columns**; the index is excluded from the sensor missingness summary.
- The verified source CSV has 1,516,948 rows, monotone naive timestamps, no duplicate timestamps, 10-second median sampling interval, and 331 adjacent gaps longer than 60 seconds.
- D1 remains a failed Ridge origin with zero eligible training rows; F5 has zero Ridge forecasts; final Ridge scored count is 64; and the common population across all three methods is 27.
- Final Persistence/Seasonal-naive paired counts remain 8,121, 22,979, 13,743, 13,428, and 18,894 (77,165 total). Seasonal-naive paired MAE and RMSE remain lower in all five final origins, with lower availability.
- The feature-availability table now uses verified saved audit stage names and exposes the 300-second lag counts by development origin.
- Saved Notebook output contains no `/Users/` or `/private/` path. No model was fitted, and no frozen configuration or historical prediction/metric file was modified.

## PDF generation and visual QA

The LaTeX PDF route was tested first but did not preserve Pandas Styler outputs as tables; its output was discarded. The delivered PDF was exported with `nbconvert --to webpdf` using the existing local Playwright Chromium. The final export completed with no exporter warning.

The PDF was rendered page by page with Ghostscript to 23 PNG pages. A contact sheet of all pages and selected full-resolution pages were reviewed. The research narrative, result tables, error/coverage plots, drift plots, Ridge-availability evidence, and fallback table are present. No blank pages, missing figures, clipped tables, overlapping text, `Styler` object descriptions, or personal absolute paths were found. The compact tables wrap within the page; code is included and wraps in print layout. Some long code/output cell pairs begin on adjacent pages, but their content is present and readable.

Executed PDF verification commands:

```sh
conda run -n nussem1 python -m nbconvert --to webpdf notebooks/DS_A5_rolling_forecasting.ipynb --output-dir submission --output DS_A5_rolling_forecasting
gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=/tmp/DS_A5_final_pdf.txt submission/DS_A5_rolling_forecasting.pdf
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r75 -sOutputFile=/tmp/DS_A5_pdfpage-%02d.png submission/DS_A5_rolling_forecasting.pdf
```

## Commands and verification results

Environment: Conda `nussem1`, Python 3.10.18, pandas 2.3.1, NumPy 2.2.6, scikit-learn 1.7.1, matplotlib 3.10.5, IPython 8.37.0, nbformat 5.10.4, nbclient 0.10.2, nbconvert 7.16.6, Playwright 1.64.1.

```sh
MPLCONFIGDIR=/tmp/ds-a5-mpl IPYTHONDIR=/tmp/ds-a5-ipython conda run -n nussem1 python -m nbconvert --to notebook --execute notebooks/DS_A5_rolling_forecasting.ipynb --output /tmp/DS_A5_rolling_forecasting.executed.ipynb --ExecutePreprocessor.timeout=900
conda run -n nussem1 python -m pytest -q tests
conda run -n nussem1 python -m py_compile src/*.py scripts/*.py tests/*.py
git diff --check
```

- Fresh-kernel execution: **PASS**, 13/13 code cells, no cell error.
- PDF WebPDF generation: **PASS**, 23 rendered pages, no export warning in the final run.
- Repository tests: **10 passed**.
- Python syntax compilation: **PASS**.
- `git diff --check`: **PASS**.
- Frozen protocol and historical metrics: unchanged; freeze commit remains an ancestor. All three milestone commits are present in order.

## Reproduction dependencies and scientific limits

Layer A requires the locally obtained source CSV at `data/raw/metropt3/MetroPT3(AirCompressor).csv` plus the committed compact metrics, audit summaries, analysis outputs, manifest, and figures. Cloning the GitHub repository alone does not provide that raw CSV. Its expected SHA-256 is `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`; source retrieval and all large excluded prediction-file hashes are recorded in `docs/artifact_registry.md`.

Layer B additionally requires locally regenerated large development/final prediction CSVs and runs the frozen evaluation verifier, Phase 2B audit, and Phase 3 analysis. The runner overwrites top-level phase outputs when intentionally rerun; the README documents that limitation.

Scientific interpretation remains **PARTIAL**: Ridge coverage is extremely sparse; the common three-model set is small; overlapping forecasts are serially dependent; timestamps are naive; historical data publication latency is unknown; UCI failure windows are retrospective and their clock alignment is unverified; and the fallback replay is not deployed or live-tested. The notebook makes no causal or production-performance claim.

## File hashes and Git status

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| `notebooks/DS_A5_rolling_forecasting.ipynb` | 624,462 | `051ad0f6df1289bbf962013ce9d2e00a655f686497543c4d75c0281b76518034` |
| `submission/DS_A5_rolling_forecasting.pdf` | 772,514 | `cf6a0b7462e1ef7bfc389ad7124668aa1308ce660c29433fc74012b2a77e9900` |

The initial freeze, Phase 2B, and Phase 3 commits remain `ca83f0a295a68337aebc070cfd481645418cda13`, `17e8a3440697af3773300e5475fdf136999a9e39`, and `104117942c170705c9c460525015f2c4b1a851e7`, respectively. No commit or push was made for Phase 4B. The working tree intentionally contains local Phase 4A/4B edits and new Notebook/submission artifacts; GitHub therefore may not contain this final package.

## Remaining user actions

1. Independently review the Notebook and PDF and confirm understanding of the scientific limitations.
2. Supply a Google Drive shared-folder link, upload/share the required Markdown/PDF/evidence, and verify access.
3. Review/publish the repository changes when ready; this phase did not push them.
4. Replace the Drive placeholder, add student identity details in the platform form, and submit the SPAIQ record manually.

The SPAIQ file is a draft only; no external upload or submission has been performed.
