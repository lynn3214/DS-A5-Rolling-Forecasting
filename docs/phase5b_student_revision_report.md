# DS-A5 Phase 5B — Student-Directed Scientific Revision Report

## Verdict

**PASS — the requested evidence-based notebook and PDF revision is complete and technically verified.** This verdict applies to the Phase 5B revision and reproducibility checks only. Student review and final submission approval remain pending. Questions that the available retrospective data cannot resolve are retained as limitations rather than presented as findings.

## Scope and preservation

The revision used the student review record, Phase 5A diagnostic report and outputs, the Phase 2B evaluation artifacts, the Phase 3 drift and critical-period analysis, and the frozen protocol and feature-availability specification. It did not fit models, tune parameters, change the frozen protocol or results, alter source data, create the final assignment notebook anew, or change `docs/ai_use_log.md`.

The final notebook and its rendered PDF are the two authorized revision targets. Their Phase 5A baseline SHA-256 values were respectively `b2702150a7acefe85af3583807bfc3af6eb0c5be1d06e1922daa96866280d655` and `cf6a0b7462e1ef7bfc389ad7124668aa1308ce660c29433fc74012b2a77e9900`. All other 46 of the 48 recorded source files still match their Phase 5A hashes. All six diagnostic output hashes and both diagnostic-code hashes also match. No source, frozen-result, or Phase 5A diagnostic artifact was rewritten.

## Student-review traceability

| # | Review concern | Revision and evidence | Disposition / remaining limit |
|---:|---|---|---|
| 1 | Persistence, seasonal-naive, and Ridge have different prediction availability. | Sections 3 and 10 distinguish exact issue-time persistence lookup, tolerance-limited historical seasonal lookup, and the seven-feature Ridge requirement; monthly counts and rates are shown. | Accepted descriptively; historical publication availability is unknown. |
| 2 | Five-second tolerance, roughly ten-second sampling, seven simultaneous lags, and gap rules may interact. | Section 10 reports observed monthly lag and joint eligibility counts from the Phase 5A audit. | Observed eligibility is verified; no single mechanism is asserted as causal. |
| 3 | Ridge eligibility changes across calendar periods. | Section 10 adds monthly all-seven-feature candidate counts and rates. | Verified for these recorded periods; mechanism remains qualified. |
| 4 | Monthly eligibility and expanding training availability were difficult to compare. | Section 10 separates monthly forecast-issue eligibility from cumulative expanding training counts and reconciles D1–D5/F1–F5 to saved Phase 2B counts. | Accepted; the tables describe different populations and time constructions. |
| 5 | Aggregate MAE obscures the marginal distribution and pressure extremes. | Sections 2 and 12 report TP2 marginal summaries separately from forecast-error summaries, including the June 75th percentile and median. | Accepted descriptively; no engineering acceptability threshold is available. |
| 6 | Pressure error may vary with operating conditions or transitions. | Sections 9 and 12 add contextual evidence and explicitly distinguish distributional changes from issue-to-target changes and forecast errors. | Qualified; no causal operating-condition effect is established. |
| 7 | Overall MAE cannot establish operational acceptability. | Section 12 states that the observed MAE cannot be classified as acceptable without an engineering loss threshold. | Accepted; threshold remains unavailable. |
| 8 | Baseline and three-method comparisons use different populations. | Section 7 labels the baseline and common-method populations separately. | Accepted; no cross-population ranking is implied. |
| 9 | F2 has 22,979 paired baseline rows but only 18 all-method rows, with a ranking reversal. | Section 7 reports a population-specific comparison using the Phase 5A sensitivity results. | Accepted; the 18-row comparison is sparse and cannot establish general Ridge performance. |
| 10 | The paired-error boxplot hides tails despite a nonzero mean difference. | Section 8 embeds the Phase 5A paired-error-tail figure and reports median, IQR, and 5th/95th percentiles. | Accepted; tail summaries describe the pooled paired population and do not identify causes. |
| 11 | Pressure/current drift may instead reflect changing operating-state mixtures. | Sections 2 and 9 discuss the observed period changes alongside the recorded operating-state summaries. | Qualified; regime mixture and sensor drift cannot be separated with these data. |
| 12 | No causal mechanism has been demonstrated. | Sections 9 and 12 explicitly limit interpretation to retrospective descriptive evidence. | Accepted; causal attribution is not made. |
| 13 | The June critical period reverses the broader persistence/seasonal-naive pattern. | Section 9 reports the event-window paired comparison and a same-D4 outside-event comparison. | Accepted as an applicability boundary; it is not a general model ranking. |
| 14 | UCI failure-report timestamps may not align exactly with sensor clocks or event onset. | Section 9 labels the interval retrospective and retains timestamp and applicability uncertainty. | Qualified; independent clock alignment and causal event timing are unavailable. |
| 15 | Generic disclaimers and repeated limitations weakened the prose. | The overview, results, scope, and conclusion were edited to state the relevant evidence and limitations once in context. | Addressed editorially; limitations remain where material. |
| 16 | Imperative or developer-facing wording appeared in research prose. | Research sections were rewritten as descriptive reporting; implementation assertions remain in code. | Addressed in the revised notebook narrative. |
| 17 | Machine status strings, repeated PASS messages, and a dense overview distracted from findings. | The overview is organized around question, approach, findings, and scope; narrative status strings were removed while executable checks remain. | Addressed; machine-readable checks remain in code. |
| 18 | The paired-error figure and governance-heavy vocabulary needed clearer scientific framing. | Section 8 explains typical versus tail behavior; Section 11 uses retrospective-replay language in the display while retaining the underlying assertion. | Addressed editorially; no live deployment or governance capability is claimed. |

## Reproducibility and verification

The final notebook has 31 cells, including 16 executable code cells. A clean-kernel execution completed with execution counts 1–16, no cell errors, no stderr warnings, and no personal absolute paths in the notebook. Its embedded Phase 5A integrity check passed for the 46 unchanged protected source files and all diagnostic outputs/code.

The PDF was regenerated from the revised notebook with the existing WebPDF exporter. Ghostscript rendered 29 page images for visual review. The complete contact sheet was reviewed, and the final data-table, conclusion, and disclosure pages were inspected at full page size. No clipped table labels, truncated conclusions, or orphaned disclosure text were observed. No browser or Python dependency was added.

Commands executed (Python commands were run in the `nussem1` Conda environment):

```text
MPLCONFIGDIR=/tmp/ds-a5-mpl-phase5b IPYTHONDIR=/tmp/ds-a5-ipython-phase5b conda run -n nussem1 python -m nbconvert --to notebook --execute notebooks/DS_A5_rolling_forecasting.ipynb --output /tmp/DS_A5_rolling_forecasting.phase5b.executed.ipynb --ExecutePreprocessor.timeout=900
MPLCONFIGDIR=/tmp/ds-a5-mpl-phase5b IPYTHONDIR=/tmp/ds-a5-ipython-phase5b conda run -n nussem1 python -m nbconvert --to webpdf notebooks/DS_A5_rolling_forecasting.ipynb --output-dir submission --output DS_A5_rolling_forecasting
gs -q -dNOPAUSE -dBATCH -sDEVICE=txtwrite -sOutputFile=/tmp/ds-a5-phase5b-final2.txt submission/DS_A5_rolling_forecasting.pdf
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r72 -sOutputFile=/tmp/ds-a5-phase5b-qa2/page-%02d.png submission/DS_A5_rolling_forecasting.pdf
conda run -n nussem1 python -m pytest -q tests
git diff --check
```

Verification outputs:

```text
13 passed in 21.45s
Notebook: 31 cells; 16 code cells executed; 0 cell errors; 0 stderr warnings
PDF: 29 pages rendered by Ghostscript and visually reviewed
Phase 5A manifest: PASS; 46 unchanged source hashes, 6 diagnostic output hashes, and 2 diagnostic-code hashes verified; no mismatches
```

Phase 5B artifact hashes at that phase checkpoint:

| Artifact | SHA-256 |
|---|---|
| `notebooks/DS_A5_rolling_forecasting.ipynb` | `6699e7e92c5070b0cdec038ede6ff198e997fb73e86fa6f562677869095863c9` |
| `submission/DS_A5_rolling_forecasting.pdf` | `87cad8e15c369870d4a6d9adc02dc506adc17a5df2962570574b9f636f9c528e` |

The one-time notebook revision helper is `scripts/revise_notebook_phase5b.py`; the finished notebook was then clean-kernel executed and the PDF rendered from that result. It is a revision aid, not part of the frozen forecasting evaluation.

## Remaining limitations and next action

Forecasts are evaluated retrospectively. Independent device-clock evidence and historical publication-availability timestamps are absent. The June 5–7 UCI interval may not align exactly with sensor event timing; observed operating-state shifts do not establish sensor drift or a cause. Sparse Ridge coverage and the 18-row F2 common-method subset do not support broad comparative claims. No operational error threshold was supplied.

At the Phase 5B checkpoint, student review and final submission approval were pending. The student subsequently requested and accepted a final Section 9 clarification; the current hashes and acceptance status are recorded in `docs/phase5c_review_closeout.md`. No commit, push, or submission action was performed.
