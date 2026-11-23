# DS-A5 Final Submission Inventory

This inventory separates the GitHub package, recommended Drive materials, SPAIQ fields, and local-only data. The final project package was committed and pushed to `origin main` in commit `fe7dda6c34e0d38c291fcb780e366381585a08e0`. GitHub publication is separate from Google Drive and SPAIQ course submission, which remain pending. The `Current state` column records the package status.

## A. GitHub deliverables

### Core tracked repository

These files are already tracked in the local Git history and should remain in the repository:

- Root/configuration: `README.md`, `TASK.md`, `.gitignore`, `requirements.txt`, and `data/manifest.json`.
- Implementation: `src/__init__.py`, `src/metrics.py`, `src/rolling_evaluation.py`, `src/temporal.py`; `scripts/audit_alternatives.py`, `scripts/audit_noaa.py`, `scripts/audit_phase2b_outputs.py`, `scripts/analyze_phase3.py`, `scripts/diagnose_forecast_task.py`, `scripts/run_rolling_evaluation.py`, `scripts/temporal_rules.py`, and `scripts/verify_rolling_outputs.py`.
- Existing tests: `tests/test_timestamp_match.py` and `tests/test_rolling_integration.py`.
- Core documents: `docs/alternative_dataset_audit.md`, `docs/candidate_comparison.md`, `docs/dataset_selection.md`, `docs/feasibility_audit.md`, `docs/sources.md`, `docs/artifact_registry.md`, `docs/forecasting_task_definition.md`, `docs/evaluation_protocol_v1.md`, `docs/evaluation_protocol_freeze_manifest.json`, `docs/feature_availability.md`, `docs/protocol_freeze_checklist.md`, `docs/protocol_freeze_review.md`, `docs/phase2b_execution_report.md`, `docs/phase2b_technical_audit.md`, `docs/phase3_drift_failure_analysis.md`, `docs/monitoring_fallback_plan.md`, and `docs/ai_use_log.md`.
- Compact results: `results/audit/` summary tables/JSON; `results/analysis/` compact tables, manifest, summaries, and figures; and `results/rolling/` metrics, manifests, execution logs, and verification records. Large row-level prediction CSVs are excluded.

### Final package and post-freeze evidence

| File or group | Purpose | Current state |
|---|---|---|
| `notebooks/DS_A5_rolling_forecasting.ipynb` | Executable, clean-kernel-reviewed assignment notebook | Committed and pushed in `fe7dda6` |
| `submission/DS_A5_rolling_forecasting.pdf` | Rendered assignment report | Committed and pushed in `fe7dda6` |
| `submission/spaiq_submission_draft.md` | Platform summary draft; contains an intentional Drive placeholder | Committed and pushed in `fe7dda6`; draft only, not submitted |
| `docs/phase4a_notebook_review.md`, `docs/phase4b_submission_review.md` | Historical construction and packaging checks | Committed and pushed in `fe7dda6` |
| `docs/student_independent_review.md`, `docs/student_review_diagnostic_report.md` | Student-originated review record and post-hoc diagnostic report | Committed and pushed in `fe7dda6` |
| `docs/phase5b_student_revision_report.md`, `docs/phase5c_review_closeout.md` | Scientific revision and student-review closeout | Committed and pushed in `fe7dda6` |
| `docs/phase6a_final_repository_audit.md`, `docs/final_submission_inventory.md` | Final pre-submission audit and inventory | Committed and pushed in `fe7dda6` |
| `scripts/verify_student_review_findings.py`, `tests/test_student_review_diagnostics.py`, `results/student_review_diagnostics/` | Reproducible Phase 5A post-hoc checks, tests, compact outputs, and manifest | Committed and pushed in `fe7dda6` |
| `scripts/revise_notebook_phase5b.py` | One-time Notebook revision helper; not required to run the final Notebook | Optional local helper; excluded from the final package and remains untracked |

The final package excludes `data/raw/` and ignored row-level prediction exports. The optional one-time revision helper is not part of the package. Review `git status` before any later repository changes.

## B. Google Drive written materials

The official submission guide requests Markdown source files, PDF versions of written work, and supporting evidence. Recommended folder contents:

### Required primary material

- `submission/DS_A5_rolling_forecasting.pdf` — final PDF report.
- `docs/evaluation_protocol_v1.md` — frozen protocol source.
- `docs/feature_availability.md` — point-in-time feature and label map.
- `docs/phase2b_execution_report.md` — rolling evaluation methods and results.
- `docs/phase2b_technical_audit.md` — independent implementation/scoring audit.
- `docs/phase3_drift_failure_analysis.md` — drift, critical-period, and monitoring analysis.
- `docs/ai_use_log.md` — AI assistance, student review, acceptance, and verification attribution.
- `docs/sources.md` — source and provenance record.

The executable report source is `notebooks/DS_A5_rolling_forecasting.ipynb` in GitHub. Upload it to Drive as supplementary material if desired. The course guide does not specify a separate standalone Markdown export of Notebook cells; confirm with the instructor if one is expected in addition to the notebook source and related Markdown records.

### Supplementary evidence (upload selectively)

- `docs/phase5b_student_revision_report.md`, `docs/phase5c_review_closeout.md`, and `docs/student_independent_review.md` if review provenance is useful to the instructor.
- Compact figures and summaries from `results/analysis/` if they are not already legible in the PDF.
- `docs/artifact_registry.md` if the instructor needs local-data and excluded-output provenance.

Do not upload the entire internal audit history or large row-level predictions unless specifically requested. Keep the raw MetroPT-3 CSV out of Drive unless the course/instructor explicitly requests it and its license/handling is confirmed.

Create the course folder, share it with `tiejianluo@gmail.com` as Viewer according to the current guide, and verify every intended file is accessible. No Drive link has been supplied and no upload has occurred.

## C. SPAIQ submission fields

| Field | Draft value / required manual action |
|---|---|
| Assignment | DS-A5 (W10, according to the current assignment catalog) |
| Submission type | Homework assignment |
| Title | Retrospective Rolling-Origin Forecasting of MetroPT-3 Compressor TP2 Pressure |
| Summary | Use the English summary in `submission/spaiq_submission_draft.md`; 206 whitespace-delimited words excluding the GitHub/Drive lines. The official catalog calls for a brief summary and publishes no numeric word range. |
| GitHub URL | `https://github.com/lynn3214/DS-A5-Rolling-Forecasting` |
| Google Drive URL | `[USER ACTION REQUIRED: paste the shared Google Drive folder link]` — placeholder only |
| Student full name | Not supplied; enter manually on the course platform |
| Student ID | Not supplied; enter manually on the course platform |

The final project package was pushed to the configured GitHub repository in commit `fe7dda6c34e0d38c291fcb780e366381585a08e0`. This records the GitHub code push only; it does not indicate a Google Drive upload or SPAIQ submission.

## D. Local-only excluded artifacts

The following remain intentionally outside Git. Their exact sizes, hashes, sources, and reproduction details are recorded in `docs/artifact_registry.md`.

| Local-only artifact | Registry reference | Handling |
|---|---|---|
| `data/raw/metropt3/MetroPT3(AirCompressor).csv` (218,300,507 bytes) | Original UCI source; SHA-256 `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24` | Required for Notebook Layer A and experimental reproduction; Git-ignored under `data/raw/` |
| `data/raw/metropt3/Data Description_Metro.pdf` (81,208 bytes) | Official UCI archive companion document | Source evidence; Git-ignored under `data/raw/` |
| `data/raw/ur3/dataset_02052023.xlsx` (1,771,022 bytes) | Official UCI UR3 source inspected during dataset selection | Retained as audit evidence; not required for the selected MetroPT-3 study |
| `results/rolling/development_predictions.csv`, `results/rolling/final_predictions.csv` | Artifact registry entries; large reproducible Phase 2B row-level exports | Excluded from Git; regenerate only through the documented frozen commands |
| `results/rolling/attempt_1/*_predictions.csv`, `results/rolling/attempt_2/*_predictions.csv` | Historical attempt hashes, sizes, manifests, and logs in artifact registry | Excluded from Git; preserve locally as historical evidence |

The MetroPT-3 CSV and prediction files are present locally. `.gitignore` excludes the raw-data tree and prediction patterns; a bare Git clone does not contain them and cannot run the standard Notebook review or full experimental reproduction without obtaining them separately.

## E. Student submission verification checklist

### Before submission

- [ ] Before any later repository changes, review the diff and untracked files; continue excluding raw data and large prediction exports.
- [ ] Verify the local Notebook/PDF SHA-256 values against the current audit report.
- [x] Final project package committed as `fe7dda6c34e0d38c291fcb780e366381585a08e0` and pushed to `origin main`.
- [ ] Create the Drive folder and upload the selected PDF and Markdown/supporting materials.
- [ ] Share the folder with `tiejianluo@gmail.com` as Viewer and personally verify instructor access.
- [ ] Enter the student's full name and ID, assignment number/type, title, summary, Drive link, and GitHub link in the course platform.
- [ ] Check the platform's displayed deadline and submission fields; the platform timestamp is authoritative.

### After submission

- [ ] Verify the platform record and both links are accessible and point to the intended versions.
- [ ] Preserve the platform confirmation/receipt and final Git commit identifier.
- [ ] Recheck that uploaded PDF and repository Notebook correspond to the reviewed hashes; record any later changes explicitly.

The final project commit and GitHub push are complete. Google Drive upload and SPAIQ submission remain pending student action.
