# SPAIQ Submission Draft

**Assignment:** DS-A5<br>
**Title:** Retrospective Rolling-Origin Forecasting of MetroPT-3 Compressor TP2 Pressure

## English summary

This study evaluates whether MetroPT-3 compressor pressure (`TP2`, in bar) can be forecast 600 elapsed seconds ahead under a frozen, chronological rolling-origin protocol. The target is the earliest recorded observation in the five-second interval beginning 600 seconds after each issue time. Persistence, a 24-hour seasonal-naive baseline, and a fixed Ridge model are assessed using expanding training windows, future-only target matching, point-in-time lag rules, and explicit gap and finite-value eligibility checks.

The original UCI CSV contains 1,516,948 timestamp-ordered records with a 10-second median interval, 331 adjacent gaps longer than 60 seconds, and no missing sensor cells. Its timestamps are timezone-naive, and historical publication latency is undocumented. Seasonal-naive has lower MAE and RMSE than Persistence on 77,165 shared final forecasts across all five final origins, although its prediction availability is lower. Ridge has only 64 scored final forecasts, F5 has none, and the all-method common population contains 27 forecasts. These sparse, selected populations do not establish Ridge superiority or broad predictive reliability. Development origin D1 also has no eligible Ridge training rows. The analysis is retrospective and descriptive: overlapping forecasts are serially dependent, failure-event clock alignment is uncertain, and no live availability or production fallback has been validated. Coverage and point-in-time validity must accompany accuracy when judging reliability.

**GitHub repository:** https://github.com/lynn3214/DS-A5-Rolling-Forecasting<br>
**Google Drive folder:** `[USER ACTION REQUIRED: paste the shared Google Drive folder link]`

## Final manual submission checklist

- [ ] Review the Notebook and PDF personally; confirm the methods, tables, limitations, and AI-use disclosure are understood.
- [ ] Add the student's full name and student ID to the course-platform record; none are supplied in this draft.
- [ ] Upload the PDF, Markdown report/source, and relevant supporting evidence to the Google Drive course folder.
- [ ] Share the Drive folder with the instructor using the access level specified by the official submission guide and verify access.
- [ ] Confirm the GitHub repository contains the reviewed files and the locally excluded raw dataset is not mistakenly represented as included.
- [ ] Replace the Drive placeholder above with the actual shared link.
- [ ] Submit the DS-A5 record on the course platform with assignment number, title, brief summary, Drive link, and GitHub link.
- [ ] Verify the platform record and uploaded files are accessible; this draft has not been submitted.
