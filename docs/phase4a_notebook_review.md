# Phase 4A — Final Notebook Construction and Verification

> Historical Phase 4A record. The Notebook was subsequently revised during Phase 4B for submission formatting and privacy corrections; the current Notebook/PDF hashes are recorded in `docs/phase4b_submission_review.md`.

## Verdict

**PASS for Phase 4A notebook construction and verification.** The notebook was executed from a fresh `nussem1` Jupyter kernel with all 12 code cells completing, no cell errors or captured warnings, and four rendered PNG outputs. Its standard review path verifies frozen protocol/source hashes, loads the original MetroPT-3 observations and audited compact result artifacts, recreates the core tables/figures, and does not retrain models. This verdict does not upgrade the scientific status of the saved evaluation: Ridge coverage remains extremely sparse and historical publication latency remains unknown. PDF creation and final submission packaging were explicitly out of scope.

## Notebook outline

`notebooks/DS_A5_rolling_forecasting.ipynb` presents:

1. Executive overview and research question
2. Dataset provenance and empirical temporal audit
3. Forecast definition and feature/label availability map
4. Frozen evaluation protocol and rolling windows
5. Reproducible implementation and two execution layers
6. Development/final results and method-specific coverage
7. Exact paired Persistence versus Seasonal-naive comparison
8. Daily error/coverage and per-origin diagnostics
9. Sensor/operating-state drift and June 5–7 retrospective subgroup
10. Ridge feature-availability failure diagnosis
11. Monitoring and offline fallback replay
12. Limitations, conclusions, reproduction, and AI-use disclosure

The notebook narrative is English, links to the detailed repository records, and uses reusable source modules and saved audited summaries instead of duplicating the rolling evaluator.

## Assignment requirements checked

The official course assignment catalog was consulted on 2026-11-19 at <https://tjluo-ucas.github.io/ds/en/assignments/>. It lists DS-A5 evidence for time order, rolling origin, leakage checks, drift, and failure cases. The minimum standard calls for an executable notebook or equivalent, exported PDF and reproduction commands; data provenance and environment; assumptions, baseline, metrics, actual output and failure analysis; a counterexample/sensitivity/applicability boundary; and an AI-use record. The official submission guide at <https://tjluo-ucas.github.io/ds/en/submission-guide/> describes GitHub code/README, Drive written materials, and a course-platform record. The notebook covers the evidence relevant to this phase. PDF/platform packaging is not performed here, per task scope. The current platform-specific submission record and access settings could not be verified from this repository.

## Important design decisions

- **Standard review (Layer A):** reads the original data file for empirical source checks; verifies the frozen documents, diagnostic, source scripts, Phase 2B metric files, Phase 3 manifest outputs, protocol commit ancestry, and summary invariants; regenerates review tables/plots. It does not read the large row-level prediction CSVs or refit models.
- **Full reproduction (Layer B):** remains an explicit route through the README commands to regenerate Phase 2B predictions, run the independent output verifier and audit, and rerun Phase 3. This path is not triggered by an ordinary notebook run.
- Project-root discovery uses the notebook working directory and its parents, looking for `TASK.md` and the frozen protocol document. No private absolute path is embedded.
- The notebook preserves zero-coverage days with missing MAE and separates candidate issues, valid labels, available predictions, and scored records.
- It retains the retrospective zero-additional-latency assumption and naive timestamps as limitations; issue time is not treated as proof of historical feature publication time.
- No model, feature, horizon, baseline, rolling window, hyperparameter, or saved historical result was changed.

## Executed verification

Execution environment: Conda environment `nussem1`, Python 3.10.18, pandas 2.3.1, NumPy 2.2.6, scikit-learn 1.7.1, matplotlib 3.10.5, IPython 8.37.0, ipykernel 6.30.1, nbformat 5.10.4, nbclient 0.10.2, and nbconvert 7.16.6.

Commands executed:

```sh
conda run -n nussem1 python -c 'import nbformat; n=nbformat.read("notebooks/DS_A5_rolling_forecasting.ipynb",as_version=4); nbformat.validate(n)'
MPLCONFIGDIR=/tmp/ds-a5-mpl IPYTHONDIR=/tmp/ds-a5-ipython conda run -n nussem1 python -m nbconvert --to notebook --execute notebooks/DS_A5_rolling_forecasting.ipynb --output /tmp/DS_A5_rolling_forecasting.executed.ipynb --ExecutePreprocessor.timeout=900
conda run -n nussem1 python -m pytest -q tests
conda run -n nussem1 python -m py_compile src/*.py scripts/*.py tests/*.py
```

Results:

- Notebook format validation: PASS.
- Fresh-kernel run: PASS; 28 total cells, 13 code cells executed in order; zero cell errors, zero captured notebook warnings, four PNG outputs rendered. The executed notebook was copied back to the deliverable.
- Repository tests: **10 passed**.
- Python syntax compilation: PASS.
- `git diff --check`: PASS.

The first fresh-kernel run exposed an incorrect assumption about the Phase 2B manifest schema (`outputs.metrics_sha256` was not a field). The notebook check was corrected to compare the actual metric hashes recorded in the Phase 2B execution report and to verify each run manifest's frozen commit. The completed final run passed. One initial format-check command used a nonexistent `nbformat.__main__` entry point; the supported nbformat Python API was used successfully afterward.

## Integrity and consistency checks

The clean-kernel notebook verified:

- Freeze protocol document SHA-256: `3cce2f55892e8355c27e5fa1721d4d81a8f3dd70b883e00d45501bc94725d6b3`.
- Feature availability document SHA-256: `389354c89c5855573343c211873571eb7502e145d764eca5682caae178ca3b34`.
- Forecast task document SHA-256: `5c2d10ec670f0ebcd09166f75c9e8c8ba9cbf1e90451d9c00a4ff98696540d49`.
- Freeze diagnostic SHA-256: `bf6ae08b38233a50575cf502847d470edc6ca70bec39e8605ce8a338a9d83ef0`.
- Original MetroPT-3 CSV SHA-256: `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`.
- Development/final metric SHA-256 values: `1c97599d08311a2cadca555313ee1ab87d7c3648539e34f73235c316dafde641` / `6af02ab6d02e491b622f66d3b0b45b62a871a6c264f917c92d519ced2f9f4d11`.
- Phase 3 manifest output hashes, source dataset hash, Phase 3 script hash, and the frozen protocol commit reference.
- The freeze commit is an ancestor of the current HEAD.

Notebook assertions also confirmed the five development and five final origin records, D1's failed Ridge fit with zero eligible training rows, zero F5 Ridge predictions, the final Ridge scored count of 64, and the all-three-method common final population of 27. The notebook displays development status and the final common-target comparison separately. It rechecked final paired baseline counts `[8121, 22979, 13743, 13428, 18894]` (77,165 total) and verified that seasonal-naive paired MAE and RMSE are lower in each origin. It preserves method-specific denominators and unavailable results rather than assigning zero error. It verifies the offline fallback replay summary against its saved status and counts.

No protocol file, historical metric, prediction file, source data, or frozen configuration was edited. Git history still contains the protocol freeze (`ca83f0a295a68337aebc070cfd481645418cda13`), Phase 2B (`17e8a3440697af3773300e5475fdf136999a9e39`), and Phase 3 (`104117942c170705c9c460525015f2c4b1a851e7`) commits in order.

## Artifact dependencies and unresolved issues

- The original MetroPT-3 CSV is excluded from Git and required by Layer A at `data/raw/metropt3/MetroPT3(AirCompressor).csv`; its expected hash and reproduction instructions are recorded in `docs/artifact_registry.md`.
- Large Phase 2B prediction CSVs are excluded from Git. Layer A uses committed audited summaries and hashed Phase 3 outputs; Layer B requires regenerating the prediction files using the documented commands.
- NOAA ERDDAP access remains PARTIAL because official observation requests were blocked; this is not evidence the source dataset is unavailable.
- The archive has naive event timestamps and no historical publication timestamps. The retrospective availability assumption cannot support claims of real-time performance.
- Ridge and three-method common coverage are too sparse for a robust Ridge comparison. Failure-report alignment is uncertain, and error observations are serially dependent.
- Student review remains pending. This notebook is not the final PDF or completed submission record.

## Notebook artifact

- Path: `notebooks/DS_A5_rolling_forecasting.ipynb`
- Size: 497,780 bytes
- SHA-256: `2b62c7a8654a6fc510823d9f94f2bc8af8002a04df0da9776c9beb8fefedae58`

No commit or push was created.
