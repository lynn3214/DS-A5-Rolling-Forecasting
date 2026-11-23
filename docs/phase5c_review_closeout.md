# DS-A5 Phase 5C — Student Review Closure and AI-use Closeout

## Documentation verdict

**PASS — the student review and AI-use records distinguish student-reported checks, student-originated questions and acceptance, and Codex-executed follow-up work.** This is a documentation-integrity verdict only. The scientific interpretation remains **PARTIAL**; documentation PASS is not a claim of scientific PASS or external submission approval.

## Scope and evidence examined

This closeout reconciles `TASK.md`, the existing AI-use log, the sequential student review record, Phase 5A diagnostic report and manifest, Phase 5B revision report, Phase 4A/4B review reports, frozen evaluation protocol and feature-availability map, artifact registry, current Notebook, SPAIQ submission draft, Git history, and working-tree status. It preserves the earlier phase records and their point-in-time verdicts.

Primary evidence files:

- Student statements and review history: `docs/student_independent_review.md`
- Phase 5A post-hoc computations and attribution: `docs/student_review_diagnostic_report.md`
- Phase 5A machine-readable provenance and hashes: `results/student_review_diagnostics/diagnostic_manifest.json`
- Phase 5B revision and 18-item mapping: `docs/phase5b_student_revision_report.md`
- Frozen protocol and availability semantics: `docs/evaluation_protocol_v1.md`, `docs/feature_availability.md`
- Source/large-artifact provenance: `docs/artifact_registry.md`
- Latest content under review: `notebooks/DS_A5_rolling_forecasting.ipynb`, `submission/DS_A5_rolling_forecasting.pdf`
- Submission checklist (left unchanged): `submission/spaiq_submission_draft.md`

## Verification attribution

### Student-reported independent checks

The student reported personally checking A1–A4, B2–B4, and C1–C6: final artifact/version consistency; clean-kernel execution; dataset hashes/environment; Git history and excluded-large-artifact reproducibility; data quality and empirical sampling; forecast horizon, target matching and time boundaries; lag features and availability; temporal origin separation; Ridge preprocessing and training isolation; D1/Ridge coverage; counts and independent MAE/RMSE; paired comparison; and negative/unavailable-prediction handling. The student reported B1 dataset suitability as **PARTIAL**.

These statements remain attributed as student reports. No exact student commands, execution dates/logs, or numeric recalculation traces were supplied. The student separately reviewed the Phase 5B Notebook/PDF, accepted four review dimensions, requested the Section 9 critical-period clarification, and then explicitly accepted that clarification. The acceptance is recorded as acceptance of the revision content. The student has not reported rerunning Codex's diagnostic script, the 13-test suite, clean-kernel execution, PDF export, or latest rendered-page/hash checks.

### Student-originated findings and decisions

All 18 questions originated in the student's independent review. Codex's later computations are responses to those questions, not independent discoveries attributed to Codex. The traceability table below connects each concern to the response and preserves unresolved scientific boundaries.

| # | Student-originated concern | Follow-up or disposition | Remaining boundary |
|---:|---|---|---|
| 1 | Method prediction availability differs substantially. | Phase 5A decomposed lookup and joint-feature eligibility; the revised Notebook explains method-specific rules. | Archive issue time does not establish historical publication availability. |
| 2 | Five-second tolerance interacts with approximately ten-second sampling. | Observed lag age and eligibility were measured from source timestamps. | Median interval does not determine phase alignment at each lag. |
| 3 | Timestamp alignment may vary. | Lookup-age diagnostics support historical age misalignment as the primary observed long-lag eligibility bottleneck. | No independent clock reference; physical clock drift is not established. |
| 4 | Training and evaluation feature-eligibility populations differ. | All ten expanding training counts were reconstructed and matched Phase 2B; monthly and origin-window issue eligibility are reported separately. | Expanding training rows are not single-month samples. |
| 5 | Ridge eligibility is sparse and varies by period. | Monthly and frozen-window all-seven-feature counts are reported in Phase 5A and the revised Notebook. | This is eligibility evidence, not proof of live availability or broad Ridge capability. |
| 6 | TP2 marginal distribution and forecast MAE need separate interpretation. | Revised Notebook separates target-distribution summaries from forecast-error summaries. | No engineering loss threshold establishes operational acceptability. |
| 7 | June 5–7 baseline-error direction reverses the broader final-origin pattern. | Section 9 now reports the 14,274-pair event comparison and the five-origin paired direction; the student accepted the clarification. | Reversal cause is unknown; event-report/sensor-clock alignment is uncertain. |
| 8 | Paired-error boxplot hides tails despite a mean difference. | Phase 5A reports paired median, IQR, quantiles, and tail mass; Phase 5B revised the figure discussion. | Tail summaries do not establish cause; a few rows are not claimed to explain the entire advantage. |
| 9 | F2 ranking reverses on a selected 18-row all-method population versus 22,979 baseline pairs. | Phase 5A verified the population counts and metrics; revised Notebook labels the populations separately. | The 18-row set cannot establish general model superiority. |
| 10 | Operating-state mixture may look like physical sensor drift. | The discussion contextualizes pressure/current shifts with recorded state summaries. | Drift and regime mixture cannot be separated causally with these data. |
| 11 | Generic disclaimers were repetitive. | Phase 5B replaced repeated boilerplate with evidence-specific limitations. | Material limits remain in the report. |
| 12 | Imperative/developer-facing text was unsuitable for research prose. | Research narrative was revised; executable assertions remain in code. | No substantive limitation. |
| 13 | Conclusions should be evidence-specific rather than generic. | Overview/results/conclusion were revised to distinguish observed comparisons, selected populations, and limits. | Conclusions remain retrospective. |
| 14 | MLOps/governance vocabulary was too prominent. | Phase 5B revised presentation language and retained retrospective-replay status in the output label. | No live capability is claimed. |
| 15 | Verification messages and wording were repetitive. | Narrative status strings were removed or reduced; programmatic assertions remain. | Technical checks are still recorded in documentation. |
| 16 | Sparse-Ridge caveats were repeated. | Coverage caveats were consolidated around the relevant results and limitations. | Sparse Ridge evidence remains scientifically material. |
| 17 | Timestamp-availability disclaimers were repeated. | Availability limitations are placed with the point-in-time interpretation and final scope. | Historical release latency remains unknown. |
| 18 | Executive overview was overly dense. | Phase 5B reorganized it around question, approach, findings, and scope. | No scientific limitation removed. |

### Codex-executed post-hoc verification

Phase 5A was executed by Codex at the student's request through `scripts/verify_student_review_findings.py`; it is post-hoc descriptive verification, not an independent student execution and not a protocol revision. Its final manifest records PASS for deterministic lookup parity, monthly/window feature decomposition, exact training-count reconciliation, paired identity checks, and F2 population identities. The report also preserves an intermediate `IndexError` and its correction; the failed run did not write final outputs.

Key verified observations:

- August had 220,434 candidate issues. TP2 300-second lookup: 220,249 older than five seconds; 185 within the 0–5 second age tolerance; 60 of those rejected by the historical-gap rule; 125 eligible. Only 94 issue times had all seven lag features eligible. This is an observed archive lookup-age bottleneck, not evidence of physical clock drift.
- The ten D1–D5/F1–F5 expanding training sample counts reconstructed exactly against saved Phase 2B metrics.
- Across 77,165 final paired baseline forecasts, the seasonal-minus-persistence absolute-error difference had mean about −0.2662 bar, median 0, and IQR about −0.002 to +0.002 bar. Tails materially affect aggregate summaries; the analysis does not assert that a tiny number of rows wholly explains the advantage.
- F2 has 22,979 baseline-paired forecasts where Seasonal-naive has lower MAE than Persistence; on 18 selected all-method common forecasts the ordering reverses. This is a selected-population effect, not general model superiority.
- For the retrospectively assigned June 5–7 issue-time subgroup, paired n is 14,274, Persistence MAE is 0.6333 bar, and Seasonal-naive MAE is 4.4586 bar. Across F1–F5, Seasonal-naive paired MAE is lower on each origin's shared targets. The event-window reversal is observed; its cause is unresolved. Possible operating-condition, short-term pressure-dynamic, or daily-pattern explanations were not isolated or causally tested. UCI report-time alignment remains uncertain.

The student rejected presenting a fixed 50% historical matching probability as fact. The preserved written review records the broader request to avoid unverified probability arguments; no 50% value is treated as an empirical measurement. The student did not accept physical clock drift as an established cause. After reviewing the Phase 5A evidence, the student accepted the revised lag-lookup-age explanation, the paired-tail/F2 explanations, the overview/conclusion and presentation revisions, and the requested Section 9 clarification. Acceptance of interpretation is not attribution of diagnostic execution to the student.

## Scientific status and limitations

Scientific interpretation remains **PARTIAL**. The documentation and student acceptance do not change the frozen experiment or upgrade its scientific verdict. Limitations preserved in the Notebook and reports include:

- Extremely sparse Ridge coverage: 64 final scored forecasts, D1 has no eligible Ridge training rows, F5 has zero Ridge predictions, and only 27 final targets are common to all three methods.
- Source timestamps are timezone-naive; historical publication latency and physical clock behavior are unknown.
- UCI failure periods are retrospective; failure truth and alignment to sensor-clock time are uncertain.
- Overlapping forecasts are serially dependent; iid interpretation is not justified.
- Drift and critical-period explanations are descriptive and noncausal.
- The fallback replay is offline and has not been validated live.
- The 18-row F2 all-method subset is highly selected; no operational acceptability threshold was supplied.

## Artifact integrity and consistency

The Phase 5A manifest contains 48 before/after source hashes. The two expected revision targets (Notebook and PDF) were updated in Phase 5B and in the final Section 9 clarification, so their historical Phase 5A hashes are not expected to match current bytes. The other 46 source hashes match; all six Phase 5A output hashes and both diagnostic-code hashes match. Frozen protocol, feature availability, original CSV, Phase 2B outputs, Phase 3 outputs, and source scripts remain protected by that comparison. The latest notebook/PDF hashes are:

| Artifact | SHA-256 |
|---|---|
| `notebooks/DS_A5_rolling_forecasting.ipynb` | `a23e9ada33d0df82e6a800ce9ee10cd06ac2e6c7e159ebedb8e329a6a05d16dc` |
| `submission/DS_A5_rolling_forecasting.pdf` | `a55da1929dbcb0bf76f53e7af1a1cfa344bb93cd7bd9c2d0de273fb03285f9ed` |

The Section 9 revision is present in both artifacts. The current Notebook has 31 cells and 16 code cells. Codex's latest clean-kernel run completed without cell errors; all existing assertions passed. The existing test suite reported 13 passed. Codex regenerated the WebPDF and visually inspected the affected Section 9 page and its adjacent page; the full added paragraph fits on page 20 without a page-break split. These are Codex verification results. The student accepted the content but did not report independently inspecting the final regenerated page rendering.

Historical PASS/PARTIAL/PENDING entries in Phase 4A, Phase 4B, Phase 5A, and Phase 5B reports are point-in-time records. The Phase 5C acceptance addendum supersedes the earlier pending acceptance of Phase 5B revisions and the final Section 9 wording; it does not supersede the scientific PARTIAL verdict or imply external submission completion. The SPAIQ draft remains unchanged and its manual checklist remains unticked. Its Notebook/PDF review item may be updated to reflect the student's later review only if the student confirms that the checklist's bundled understanding statement is also complete; no such checkbox edit was made here.

## Current readiness and remaining pending items

- **Revision-content review:** ACCEPTED by the student, including Section 9.
- **Student repetition of the latest technical checks:** NOT REPORTED. The clean-kernel run, test run, hash verification, PDF export, and render inspection are Codex-executed.
- **Student visual inspection of the final regenerated PDF pages:** NOT REPORTED. Codex verified the affected pages; student acceptance of Section 9 wording is recorded separately.
- **Scientific conclusion:** PARTIAL; uncertainties above remain substantive and are not project-integrity failures.
- **Submission:** Not submitted. No commit/push, Drive upload, or SPAIQ submission occurred. The SPAIQ draft still has a Drive placeholder; student identity/Drive details and platform submission remain outstanding. The MetroPT-3 source CSV remains locally required and excluded from Git as documented in the artifact registry.

The repository working tree contains the previously accumulated local phase artifacts and modifications. No commit or push was created in Phase 5C. No protocol, Notebook/PDF, experimental output, Phase 5A diagnostic, or final submission summary was changed in this documentation closeout.

## Verification performed for this closeout

The final checks use existing evidence and do not rerun the rolling evaluation or the expensive Phase 5A diagnostic. Manifest comparisons, artifact hashes, link checks, test output, and whitespace checks are recorded in this closeout and its execution history:

```text
git status --short
git log -5 --oneline
git remote -v
shasum -a 256 notebooks/DS_A5_rolling_forecasting.ipynb submission/DS_A5_rolling_forecasting.pdf results/student_review_diagnostics/diagnostic_manifest.json docs/evaluation_protocol_v1.md docs/feature_availability.md
conda run -n nussem1 python -m pytest -q tests
git diff --check
```

The existing test suite reported **13 passed**; it is not a new forecasting experiment. The Phase 5A manifest comparison returned PASS with 46 non-target source hashes, six diagnostic output hashes, and two diagnostic-code hashes matching; latest Notebook/PDF hashes matched the values above. Notebook schema and Section 9 content checks passed. Repository-relative references resolved in the four checked Markdown documents, with no CJK characters or trailing whitespace. `git diff --check` returned exit status 0.
