# DS-A5 Phase 6A — Final Repository Audit and Submission Readiness

## Executive verdict

**PARTIAL for final course submission readiness; READY for a reviewed local final Git commit after explicit student authorization.** The local Notebook/PDF, frozen evidence, tests, and documentation are internally consistent. External submission is not complete: the changes are not committed or pushed, GitHub remote state could not be read because DNS resolution failed, no Google Drive folder/link or upload exists, and no SPAIQ record has been submitted. The scientific conclusion remains **PARTIAL**; this repository audit does not change that verdict.

No model was retrained, no rolling evaluation or experiment was rerun, and no frozen results were changed. The only Phase 6A repository edits were a direct SciPy version pin, README navigation/environment clarifications, and the two requested audit deliverables.

## 1. Official requirements and current-source verification

The following official pages were accessed on 2026-11-23:

- [UCAS Data Science course homepage](https://tjluo-ucas.github.io/ds/)
- [Assignments and labs catalog](https://tjluo-ucas.github.io/ds/en/assignments/)
- [Course Submission Guide](https://tjluo-ucas.github.io/ds/en/submission-guide/)

The local `TASK.md` is the original Phase 1 feasibility-audit specification, not a separate final-assignment handout. The frozen protocol and later phase reports define the implemented DS-A5 task. No additional assignment PDF/handout was present in the repository.

| Requirement | Official/current evidence | Repository evidence and status |
|---|---|---|
| DS-A5 academic evidence | The catalog lists time order, rolling origin, leakage checks, drift, and failure cases. Its minimum standard calls for an executable Notebook or equivalent, PDF and reproduction commands; provenance/environment; assumptions, baselines, metrics, output and failure analysis; an applicability boundary; AI-use record; and no fabricated work. | Notebook, frozen protocol, audit reports, Phase 3 analysis, applicability examples, and AI-use log are present locally. **Locally verified; not yet pushed.** |
| GitHub code package | The guide calls for runnable source, README with dependencies/setup/run instructions, and relevant configuration/sample inputs. It requires instructor access; private repos should invite the instructor with read-only access where supported. | Repository has source, tests, README, requirements, protocol/configuration, and compact evidence. Origin is configured. **Remote visibility/content was not verified.** |
| Google Drive written materials | The guide requests Markdown source files, PDF versions of written work, and supporting evidence, organized by course folder. It says to share with `tiejianluo@gmail.com` as Viewer and verify access. | Final PDF and Markdown evidence exist locally; no Drive folder/link or upload was supplied. **Pending.** See `docs/final_submission_inventory.md` for a selective file list. |
| Course-platform record | The guide requires full name, student ID, submission type/title/assignment, brief summary, Drive link, and GitHub link. | Draft exists at `submission/spaiq_submission_draft.md`; identity fields and Drive URL remain intentionally blank/placeholder. No platform record was submitted. **Pending.** |
| Summary word limit | The official assignment catalog says “brief summary” and specifies no numeric range. | The draft summary is 206 whitespace-delimited words, excluding the GitHub and Drive lines. The placeholder is explicit. |
| Deadline | The current catalog lists DS-A5 as W10, released 2026-11-18 16:30 and due 2026-11-25 16:30 Asia/Shanghai. It states that the `learn.spaiq.ai` timestamp is authoritative. | Catalog deadline was independently reverified. The live course-platform deadline/state was not accessed; confirm it on the platform. At the audit date, the catalog deadline is still in the future. |

The homepage describes the course's evidence-first and responsible-interpretation approach; assignment-specific requirements above are taken from the assignment catalog and submission guide. No grading rule, Drive permission beyond the guide's stated Viewer instruction, or platform status was inferred.

## 2. Repository and Git state

Latest local commit is `104117942c170705c9c460525015f2c4b1a851e7` (`DS-A5: analyze drift, failures, and fallback`). The configured remote is `https://github.com/lynn3214/DS-A5-Rolling-Forecasting.git`.

The three milestone commits are present in the local history and each is an ancestor of `HEAD`:

- Freeze: `ca83f0a295a68337aebc070cfd481645418cda13`
- Phase 2B: `17e8a3440697af3773300e5475fdf136999a9e39`
- Phase 3: `104117942c170705c9c460525015f2c4b1a851e7`

The current tracked working-tree modifications are `README.md`, `requirements.txt`, and `docs/ai_use_log.md`. `git diff --stat` reports tracked changes only; it omits the untracked Notebook, PDF, review records, diagnostics, and Phase 6A documents. The full status is recorded in the execution record and `docs/final_submission_inventory.md`. No file was staged, committed, reset, or cleaned.

Core frozen protocol documents and core evaluation/analysis source files are unchanged relative to their relevant freeze/Phase 3 commits. The freeze manifest is `FROZEN`; its recorded document, source-script, diagnostic, and original dataset hashes match the current files. The Phase 5A manifest is `PASS`: all 46 non-revision-target source hashes, six diagnostic output hashes, and two diagnostic-code hashes match; the Notebook/PDF are its expected later revision targets. The latest Notebook and PDF match the expected Phase 5C hashes listed below. Phase 2B/3 outputs and the original data are unchanged.

The `.gitignore` rules match the intended exclusions. The MetroPT-3 source at `data/raw/metropt3/MetroPT3(AirCompressor).csv` and the large top-level and historical attempt prediction CSVs are ignored and not tracked. Their expected sizes and hashes are preserved in `docs/artifact_registry.md`. A bare clone does not contain the source CSV or row-level predictions; the README says this explicitly.

No credentials or personal absolute paths were found in the submitted Notebook/PDF text. No unintended large generated artifact was found in the Git candidate list. Local files over 100 MB are limited to the documented raw source and ignored row-level predictions.

## 3. Frozen protocol and artifact integrity

The freeze manifest records:

- Protocol document SHA-256: `3cce2f55892e8355c27e5fa1721d4d81a8f3dd70b883e00d45501bc94725d6b3`
- Feature availability document SHA-256: `389354c89c5855573343c211873571eb7502e145d764eca5682caae178ca3b34`
- Forecast task definition SHA-256: `5c2d10ec670f0ebcd09166f75c9e8c8ba9cbf1e90451d9c00a4ff98696540d49`
- Freeze diagnostic SHA-256: `bf6ae08b38233a50575cf502847d470edc6ca70bec39e8605ce8a338a9d83ef0`
- MetroPT-3 source SHA-256: `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`

The manifest also matches its four frozen source-script hashes. A direct read-only comparison found no frozen protocol or core evaluation/Phase 3 source changes in the commit ancestry. Phase 5A hash verification found no changed protected Phase 2B/3 result, source, or diagnostic file. The Notebook and PDF changes are authorized Phase 5B/Section 9 presentation deliverables; their old Phase 5A hashes are historical, not expected current hashes.

## 4. Notebook integrity and critical results

Notebook: `notebooks/DS_A5_rolling_forecasting.ipynb`; SHA-256: `a23e9ada33d0df82e6a800ce9ee10cd06ac2e6c7e159ebedb8e329a6a05d16dc`.

The expected hash matches. `nbformat` validation passed. The saved Notebook has 31 cells, 16 code cells, consecutive execution counts 1–16, no saved cell errors or stderr warnings, no personal absolute paths, no shell/magic markers indicating hidden-state execution, and no unresolved Notebook placeholders. The final P5B/Section 9 text is present. A prior fresh-kernel execution completed successfully; this Phase 6A audit inspected its saved execution record rather than rerunning the Notebook.

The saved outputs and underlying compact results agree on the critical checks:

- D1 has zero Ridge training rows; F5 has zero Ridge predictions.
- Final Ridge scored count is 64; the three-method final common population is 27.
- Final baseline-paired population is 77,165, and Seasonal-naive paired MAE/RMSE is lower than Persistence on each of F1–F5 shared targets.
- The August TP2 300-second lookup decomposition is 220,434 candidates; 220,249 stale lookups; 185 within 0–5 seconds; 60 further gap rejections; 125 lag-eligible lookups; 94 all-seven-feature issue times.
- F2 population sensitivity labels 22,979 baseline pairs separately from 18 selected all-method targets.
- The June 5–7 paired subgroup remains n=14,274 with Persistence MAE 0.6332893 bar and Seasonal-naive MAE 4.4586442 bar. The Notebook states that the reversal's reason is unknown, possible mechanisms were not isolated or causally tested, and event-time alignment is uncertain.

These are verified retrospective observations, not evidence of physical clock drift, historical publication availability, fault causality, broad Ridge superiority, or live performance. The late lag lookup explanation is post-hoc Phase 5A evidence. The core conclusion and scientific status remain restrained.

## 5. PDF integrity and visual inspection

PDF: `submission/DS_A5_rolling_forecasting.pdf`; SHA-256: `a55da1929dbcb0bf76f53e7af1a1cfa344bb93cd7bd9c2d0de273fb03285f9ed`.

The expected hash matches. Ghostscript opened and rendered the PDF into 29 page images, and text extraction succeeded. A complete 29-page contact sheet was visually reviewed; detailed pages containing the availability table, paired-error figures, critical-period table, monthly eligibility tables, conclusion, and disclosure were inspected. Figures are present and labeled, tables fit within the page, text is not clipped or overlapped, and no page is blank. No private local paths or secret-like strings were found in extracted PDF text. The critical Section 9 clarification matches the Notebook and saved metrics.

One non-blocking layout note: the final page contains only the short AI/review-status disclosure paragraph. It is readable and complete, not a blank page or a clipped paragraph, but the sparse last page could be cosmetically consolidated if a later authorized PDF revision is desired. The PDF was not regenerated during Phase 6A.

## 6. AI-use log and student-review attribution

`docs/ai_use_log.md`, `docs/student_independent_review.md`, `docs/student_review_diagnostic_report.md`, `docs/phase5b_student_revision_report.md`, and `docs/phase5c_review_closeout.md` agree on the sequence and attribution:

- The student reported independent checks A1–A4, B2–B4, C1–C6 as passed and B1 as PARTIAL. No exact student-run command logs or numeric recalculation traces were supplied.
- The 18 scientific/presentation concerns originated from the student's independent review. Phase 5A diagnostics and Phase 5B edits were executed by Codex in response; they are not attributed as student-run analyses.
- The student accepted the five review dimensions, including the last Section 9 clarification. The current record does not claim that the student reran Codex's latest tests/hashes or personally inspected the final PDF page render.
- The scientific status remains PARTIAL. The records retain sparse Ridge coverage, D1/F5 failures, 27 all-method targets, naive timestamps, unknown publication latency and physical clock behavior, uncertain UCI event alignment, serial dependence, noncausal drift/event interpretation, and offline-only fallback validation.
- AI is described as materially involved in planning, implementation, analysis, debugging, technical review, and document production—not merely copyediting. Earlier failed attempts and historical status statements remain preserved and time-qualified.

Phase 4/5 historical reports contain point-in-time hashes/statuses; their later follow-ups identify current artifacts. The SPAIQ draft remains a draft with an explicit Drive placeholder; no text falsely claims a push, upload, platform submission, or complete public review.

## 7. SPAIQ draft verification

`submission/spaiq_submission_draft.md` identifies DS-A5 and the research accurately. Its title matches the Notebook. Its English summary is 206 whitespace-delimited words when counting the summary body only, excluding the GitHub/Drive lines; no numeric word range appears on the official assignment pages. The Phase 4B report recorded 209 words under an unspecified counting convention; the current count differs by three and is non-material because the official requirement is only a brief summary.

The summary's frozen horizon, target, five-origin comparison, 77,165 paired forecasts, 64 Ridge scored forecasts, 27 all-method targets, and stated limitations agree with the Notebook. It does not claim general Ridge superiority or causal failure effects. The GitHub URL matches the configured remote URL without the `.git` suffix. The Drive link remains visibly marked as a user action. Student identity is not fabricated. The SPAIQ draft was not changed in Phase 6A.

## 8. README, reproducibility, and dependencies

README paths and reproduction commands resolve to local scripts/docs. The standard Notebook review (Layer A) requires the local hash-verified MetroPT-3 CSV and compact result artifacts; it does not retrain models. Full reproduction (Layer B) additionally regenerates large prediction CSVs and runs the documented audits. These commands are documented with overwrite warnings; they were not run in this audit. Phase 5A has its own command and report. The source CSV and ignored predictions are not represented as included in a bare clone.

`requirements.txt` pins the direct dependencies; review found that the rolling runner imports SciPy directly although only scikit-learn had been pinned. Phase 2B records SciPy 1.15.2, and the current `nussem1` environment reports that version. Phase 6A added `scipy==1.15.2` and updated the README to state the verified Python 3.10.18 environment and link the current inventory/audit. No package installation was run. `pip check` reported no broken requirements. The documented WebPDF command also explains the Playwright Chromium installation step. No unused direct dependency was identified: openpyxl supports the alternative XLSX audit, while pytest/nbconvert/IPython support tests and Notebook/PDF workflows.

The English SPAIQ summary count and missing external fields are documented above. Current platform access, instructor permissions, and a Google Drive folder cannot be verified without the student's account/link.

## 9. Findings by severity

### BLOCKER — before actual course submission

1. **External submission is incomplete.** No commit/push, Drive upload/link, instructor-access verification, or SPAIQ record exists. Student name and ID remain manual fields. These are required external actions, not missing scientific results.
2. **GitHub remote state is unverified.** `git remote -v` confirms the configured URL, but `git ls-remote` first failed with `Could not resolve host: github.com`; a permitted read-only retry did not complete and was stopped. A web fetch of the repository URL returned a cache-miss error. Do not infer that the remote is unavailable or that its branches are empty; verify after network access returns.

### IMPORTANT — resolve before external submission

1. Confirm the live `learn.spaiq.ai` deadline and required fields; the official catalog lists 2026-11-25 16:30 Asia/Shanghai and says the platform timestamp is authoritative.
2. Review the final local Git diff and untracked inventory before staging. The local commit is ready for that review, but `git diff --stat` alone omits untracked deliverables.
3. The course guide requests Markdown source files in Drive. The project has relevant Markdown protocol/results/review sources and a Notebook source in GitHub, but no separate full-report Markdown export. The guide does not explicitly require converting an executable Notebook to standalone `.md`; ask the instructor only if that distinction is material to the course submission.

### OPTIONAL — non-blocking polish

1. The PDF's last page has only the complete short review-status paragraph; it is readable and not blank or clipped.
2. Phase 4B's old 209-word count differs by three from the current 206 whitespace-delimited count; no numeric word range is published, and the summary is still brief.
3. `scripts/revise_notebook_phase5b.py` is a one-time mutation helper, not needed for normal reproduction. Decide whether to include it as provenance or omit it from a future commit after inspecting its contents; do not run it again without a separate review.

No protocol, frozen metric, prediction, source data, or summary correction is required by this audit. No file was removed or rewritten as historical evidence.

## 10. Verification commands and outcomes

Commands actually executed in this audit (all Python commands used `conda run -n nussem1`):

```text
git status --short
git diff --stat
git ls-files
git log -5 --oneline
git remote -v
git ls-remote origin HEAD refs/heads/main refs/heads/master
git merge-base --is-ancestor ca83f0a295a68337aebc070cfd481645418cda13 HEAD
git merge-base --is-ancestor 17e8a3440697af3773300e5475fdf136999a9e39 HEAD
git merge-base --is-ancestor 104117942c170705c9c460525015f2c4b1a851e7 HEAD
git diff --exit-code ca83f0a295a68337aebc070cfd481645418cda13 HEAD -- docs/evaluation_protocol_v1.md docs/evaluation_protocol_freeze_manifest.json docs/feature_availability.md
git diff --exit-code 104117942c170705c9c460525015f2c4b1a851e7 HEAD -- src/rolling_evaluation.py src/temporal.py scripts/run_rolling_evaluation.py scripts/verify_rolling_outputs.py scripts/analyze_phase3.py
git check-ignore -v data/raw/metropt3/MetroPT3(AirCompressor).csv results/rolling/development_predictions.csv results/rolling/final_predictions.csv
conda run -n nussem1 python -m pytest -q tests
conda run -n nussem1 python -m py_compile src/*.py scripts/*.py tests/*.py
conda run -n nussem1 python -m pip check
git diff --check
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r75 -sOutputFile=/tmp/ds-a5-phase6a-pdf/page-%02d.png submission/DS_A5_rolling_forecasting.pdf
gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=/tmp/ds-a5-phase6a-pdf.txt submission/DS_A5_rolling_forecasting.pdf
```

Results: three commit ancestry checks passed; frozen documents/core scripts had no diff; all current freeze-manifest and Phase 5A protected hashes matched; Notebook static checks passed; Ghostscript rendered 29 PDF pages and extracted text; no PDF private-path/secret marker was found; tests **13 passed**; Python syntax compilation passed; `pip check` reported no broken requirements; `git diff --check` passed; Markdown relative-link checks passed on 26 files after the report and inventory were present. An initial link scan before report creation found only the expected not-yet-created README target; the final scan found no broken relative links. The sandboxed `git ls-remote` failed with `Could not resolve host: github.com`; an escalated read-only retry stalled without refs and was stopped, so remote state remains unknown.

## 11. Commit and submission readiness

**Local final Git commit: READY for student diff review and explicit authorization.** Do not stage or commit until authorized. Include the Notebook/PDF and intended review records; exclude ignored raw data and large row-level prediction CSVs. The new Phase 6A audit and inventory are part of the candidate deliverables.

**Push and course submission: NOT READY / UNVERIFIED.** Remote access could not be checked, and the required Drive and SPAIQ actions are incomplete. After authorization, commit locally, restore network connectivity, verify the remote and pushed commit on GitHub, finish the Drive folder and permissions, verify the platform deadline/identity fields, then submit and confirm the course-platform record. No commit, push, upload, or submission was performed here.
