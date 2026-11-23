# DS-A5 — Student Independent Review Record

**Status at initial review:** Completed core reproducibility and model-evaluation checks; scientific interpretation and presentation revisions under review. This file is a sequential record: later dated addenda update review status without replacing the student's earlier statements.

## 1. Independent checks completed

I independently reviewed the final notebook and repository using a structured checklist.

The following checks passed:

- A1 — Final artifact and version consistency
- A2 — Clean-kernel notebook execution
- A3 — Dataset hashes and execution environment
- A4 — Git history and reproducibility of excluded large artifacts
- B2 — Data quality and empirical sampling intervals
- B3 — Forecast horizon, target matching, and temporal boundaries
- B4 — Seven lag features and historical availability
- C1 — Rolling-origin temporal separation
- C2 — Ridge preprocessing and training isolation
- C3 — D1 training failure and Ridge prediction coverage
- C4 — Metric counts and independent MAE/RMSE calculation
- C5 — Fair paired comparison
- C6 — Negative results and unavailable-prediction handling

**B1 — Dataset suitability:** PARTIAL. The dataset supports the implemented retrospective time-series evaluation, but questions about the suitability of the sampling/availability constraints and their effects on forecasting coverage require further interpretation.

The scientific interpretation, visualization, and reporting items were also critically reviewed. Their checklist categories do not align exactly with the issues identified below; they should not be recorded as unexamined solely because the corresponding original checklist labels were left as TODO.

## 2. Scientific questions raised during manual review

### A. Timestamp alignment and model coverage

I questioned whether the extreme differences in prediction availability were sufficiently explained.

Persistence is available at essentially every evaluated issue, whereas seasonal-naive and Ridge have substantially lower coverage.

I identified the interaction between the five-second historical matching tolerance, approximately ten-second empirical sampling interval, seven simultaneous lag requirements, and gap eligibility as a possible explanation.

I also observed that Ridge feature eligibility varies substantially across periods. The cumulative training availability and the sparse final-window availability require a comparable time-period analysis before attributing the difference to timestamp behavior.

I propose a focused retrospective audit of lag-lookup ages, timestamp alignment, gap exclusions, and joint feature eligibility by calendar period.

These mechanisms are **hypotheses to verify**, not established causes.

### B. Interpretation of forecasting errors

I questioned whether aggregate MAE adequately represents performance across different compressor operating conditions.

TP2 has a highly uneven empirical distribution, with a median close to zero but much larger pressure observations in some periods.

I recommend explaining the target distribution and, if supported by a limited descriptive analysis, reporting how large errors vary across operating conditions or transitions.

I do not consider the existing overall MAE sufficient to determine whether forecasting performance would be operationally acceptable.

### C. Population selection and model comparison

I verified that baseline and three-method comparisons refer to different evaluation populations.

In F2, the Persistence/Seasonal-naive paired population contains 22,979 forecasts, whereas the three-method common population contains only 18. The resulting relative model ranking changes substantially.

I recommend explaining this specific selection effect rather than relying only on a general warning that population sizes differ.

I also questioned why the paired-error boxplot shows very small typical differences even though the paired mean error difference is appreciable. The plot hides outliers, and a tail-sensitive summary is needed before explaining which observations drive the aggregate MAE difference.

### D. Drift and critical periods

I questioned whether observed pressure and current distribution changes reflect changes in compressor operating regimes rather than sensor drift.

The existing descriptive evidence is consistent with a changing operating-state mixture, but this explanation has not been causally established.

I also identified a retrospective UCI-reported critical period in which Persistence performs substantially better than Seasonal-naive, in contrast with their broader final-period paired comparison.

This should be discussed as an applicability boundary, with uncertainty about source-report timing and clock alignment retained.

### E. Scientific writing and presentation

I identified several presentation weaknesses in the AI-generated notebook:

- Repeated generic disclaimers and conclusions
- Imperative or developer-facing text in research prose
- Excessive repetition of Ridge coverage and timestamp limitations
- Machine-readable status strings embedded in narrative paragraphs
- Repeated PASS/verification messages
- An overly dense executive overview
- A paired-error figure that does not adequately explain the difference between typical and mean error behavior
- Operational governance terminology that is too prominent for a course research report

I recommend revising these sections into concise, evidence-specific academic prose while retaining essential limitations and reproducibility checks.

## 3. Decisions

**Accepted:**

- The frozen target, feature, and rolling-origin definitions
- The reported D1 and F5 failures
- Explicit unavailable predictions and coverage reporting
- The independent scoring-audit approach
- Exact paired baseline comparisons
- Retention of sparse Ridge results as negative evidence
- Restrained causal and deployment claims

**Qualified or challenged:**

- Whether the five-second tolerance explains the observed feature-availability patterns
- Whether the observed period-to-period coverage changes indicate timestamp alignment effects
- Whether aggregate MAE adequately describes pressure-transition errors
- Whether drift terminology sufficiently distinguishes operating-regime changes from sensor behavior
- Whether the boxplot and common-target tables are clearly interpreted

**Proposed revisions:**

1. Clarify the observed availability mechanisms, avoiding unverified probability arguments.
2. Explain evaluation-population sensitivity using the F2 example.
3. Improve error-distribution interpretation and figure captions.
4. Add operating-condition context where supported.
5. Refine the executive overview, conclusions, and repetitive language.
6. Preserve all frozen model results and explicitly label any additional diagnostics as exploratory.

## 4. Verification boundaries

The completed PASS checks were performed by the student as reported in the manual checklist.

The proposed timestamp-phase, operating-regime, and error-tail explanations remain hypotheses unless supported by additional executed diagnostics.

No new model fitting, hyperparameter tuning, or changes to the frozen evaluation protocol are authorized by this review.

**Final student submission approval:** Pending targeted clarification and review of any resulting revisions.

## AI-assisted follow-up diagnostics — pending student verification

Codex completed the student-requested Phase 5A descriptive follow-up in `docs/student_review_diagnostic_report.md` and `results/student_review_diagnostics/`. The follow-up investigates the timestamp-lag and Ridge-availability question in Section 2.A, the monthly-versus-expanding population concern in Sections 2.A/2.C, the paired-error-tail question in Section 2.C, the F2 population sensitivity in Section 2.C, and the presentation questions in Section 2.E. It also records that the operating-regime versus sensor-drift concern in Section 2.D remains unresolved.

The diagnostic script reports PASS for its computational integrity checks: original source and saved result hashes were checked; all D1–D5/F1–F5 reconstructed training counts matched saved Phase 2B counts; paired issue/target identities matched the saved Phase 3 baseline artifact; and the F2 baseline and all-three populations were verified as 22,979 and 18 rows. The complete repository test suite reported 13 passed after adding three focused diagnostic tests. These results were generated by Codex and have **not** been independently verified by the student.

At the time of this Phase 5A entry, the existing student-reported checklist statuses and decisions above were unchanged. No new student PASS/PARTIAL status was asserted, no final submission approval was implied, and the notebook/PDF had not yet been revised. These were point-in-time statements; later entries record the Phase 5B revision and subsequent student review.

## AI-assisted Phase 5B scientific revision — pending student verification

Codex revised the notebook and regenerated the PDF in response to the Phase 5A findings and the student review concerns above. The revision traceability, evidence sources, execution checks, and remaining limitations are recorded in `docs/phase5b_student_revision_report.md`. The notebook and PDF hashes changed as authorized revision outputs; the other 46 Phase 5A protected source hashes, six diagnostic-output hashes, and two diagnostic-code hashes remain unchanged. The repository tests reported 13 passed and the revised notebook completed a clean-kernel execution. These are implementation and reproducibility results, not student approval. Student verification and final submission approval remain pending.

## Student-requested critical-period clarification — verification pending

The student independently reviewed the Phase 5B notebook and PDF, accepted four of the five review dimensions, and requested one additional clarification of the opposite Persistence and Seasonal-naive paired-error pattern in the retrospective June 5–7 window. The request concerns the interpretation in Section 9 and came from the student's independent review. At that point, acceptance of the requested clarification was pending.

## Phase 5C — Final student review closure (2026-11-23)

The student explicitly confirmed that the new revision meets the requirements and is accepted. This confirms acceptance of the final Section 9 clarification. Together with the student's prior acceptance, the review dispositions are:

| Review dimension | Student disposition |
|---|---|
| Timestamp alignment and Ridge coverage explanation | ACCEPTED |
| Paired-error distributions and F2 population-selection analysis | ACCEPTED |
| Executive overview and scientific conclusions | ACCEPTED |
| Notebook/PDF presentation and consistency | ACCEPTED |
| Critical-period interpretation | ACCEPTED after the requested Section 9 clarification |

The student-originated questions, Codex follow-up evidence, and disposition mapping are retained in `docs/student_review_diagnostic_report.md` and `docs/phase5b_student_revision_report.md`. The final clarification remains scientifically bounded: the June 5–7 comparison is retrospective and paired; its reversal relative to the five final origins is observed, its cause is unknown, and UCI report-time alignment is uncertain.

The student reported independent review of the Notebook and PDF and explicitly accepted the clarification. The student did **not** report personally rerunning the Phase 5A diagnostic script, the 13-test suite, the final clean-kernel run, the PDF exporter, or the latest PDF page-rendering/hash checks. Those technical checks are attributed to Codex in the Phase 5C closeout and AI-use log. No exact student-run command, terminal log, or recalculation trace was supplied. The acceptance recorded here applies to the reviewed content; it does not claim independent student execution of those technical checks or that the student personally inspected the regenerated PDF's page rendering after the final export.

**Student acceptance of Phase 5B revisions, including the Section 9 clarification: ACCEPTED.** This does not certify that repository documentation/testing has a scientific PASS verdict, authorize an external submission, or imply a Git commit/push, Drive upload, or SPAIQ submission. The scientific interpretation remains **PARTIAL**, and those external actions remain unperformed.
