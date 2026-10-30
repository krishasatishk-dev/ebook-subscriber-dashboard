# v2 Build Log (plain English)

## Stage 0 — 23 Oct 2026
- Copied the raw engagement file to `data/raw/eBook_Engagement.csv` without changing it.
- Checked it: 5,500 rows, 5,455 unique customers (45 exact duplicates), 8 real genres hiding behind 26 raw spellings (23 after tidying), some impossible numbers (logins up to 860 in a month, 6 negative "days since activity" values).
- Wrote the proposed cleaning rules and Active/Inactive/Churned thresholds in `outputs/v2/methodology.md`.
- Status: WAITING for approval of those thresholds before writing or running any v2 code.

## Stage 1 — 23 Oct 2026 (cleaning)
- Wrote `src/v2_clean.py` and ran it on the raw file; the raw file was only read, never changed.
- Dropped 45 exact duplicate rows, collapsed 23 genre spellings into the 8 real genres (+54 "Unknown" for missing), turned 6 negative recency values and 22 impossible behaviour numbers into blanks, and kept all 416 genuine zero-login rows and the 11 recency values above 365.
- Checked the join key: all 5,455 unique engagement customer IDs match subscribers in the v1 customer file.
- Saved the cleaned table to `data/processed/v2/engagement_clean.csv`.

## Stage 2 — 23 Oct 2026 (status classification)
- Wrote `src/v2_status.py` using only the thresholds you approved in `outputs/v2/methodology.md` (Active ≤30 days and ≥1 login; Churned >90 days; everything between = Inactive; missing recency = Unclassified, never guessed).
- Result on 5,455 unique subscribers: 2,995 Active (55.2%), 1,526 Inactive (28.1%), 901 Churned (16.6%), 33 Unclassified — median days-since-activity 5 / 58 / 152, exactly as the rules imply.
- Saved row-level statuses to `data/processed/v2/engagement_status.csv` and the counts to `outputs/v2/status_summary.csv`.
- Stopped here for your review. Next stage (not started): join statuses to the v1 customer profiles and build segment-level views.

## Stage 3 — 23 Oct 2026 (merge)
- Wrote `src/v2_merge.py`: joined the status file to the v1 customer file on Customer ID, keeping demographics (age info, education, occupation, income band, state, etc.) plus all engagement columns and status.
- Checked the keys first: all 5,455 engagement IDs found a customer row, 10,949 customers have no engagement row (expected — engagement covers only a subset of subscribers). The join kept exactly one row per customer, as asserted by the script.
- Found a data quirk worth your eyes: 115 customer IDs appear twice in the v1 file with *different* content (different city, sometimes different income, even opposite subscriber flags); 38 of them are in the engagement file, and keep-first (v1's rule) picked the subscriber variant for 34 and the non-subscriber variant for 4. Details in `outputs/v2/methodology.md` §4.
- Saved `data/processed/v2/merged.csv` (5,455 rows; Active 2,995 / Inactive 1,526 / Churned 901 / Unclassified 33). Stopped for review.

## Stage 4 — 23 Oct 2026 (EDA)
- Wrote `src/v2_eda.py` and produced 9 charts in `outputs/v2/charts/`, each with a title and a one-line takeaway caption; all takeaways also collected in `outputs/v2/eda_takeaways.md`.
- What the data says: logins and books are strongly related (r = 0.90) — they both measure how often someone uses the service, so putting both in one score would count that behaviour twice; nothing else among the engagement metrics correlates above 0.8, and tenure barely correlates with anything.
- Behaviour separates the status groups (Active mean 11.7 logins/month vs Churned much lower) but tenure is almost identical across Active/Inactive/Churned — how long someone has subscribed does not tell you whether they still use it.
- No weights or thresholds were chosen in this stage. Stopped for review.

## Stage 5a — 23 Oct 2026 (two approved decisions, pipeline re-run)
- Decision D1: blank logins/session/books are now filled with their column medians (6.00 / 21.80 / 9.00), with an Imputed flag on the 144 rows touched; recency is never filled — the 33 blank-recency rows stay Unclassified.
- Decision D2: when a customer ID has two records, the subscriber (flag=1) one now wins; exactly 4 IDs differ on the flag (my earlier 38 just meant "doubled IDs that also have engagement data and differ in some column"). All 5,455 engagement IDs still match a flag=1 record.
- Status after D1: Active 3,001 (+6), Inactive 1,520 (−6), Churned 901, Unclassified 33. Both decisions logged in methodology.md section 5.

## Stage 5b — 23 Oct 2026 (score proposal, Step A — STOPPED for approval)
- Wrote `src/v2_score.py`; it printed the candidate correlations and proposed weights 0.40 inverted recency / 0.35 logins / 0.25 session (books out — r=0.88 with logins would double-count usage frequency).
- Showed the tier-by-status table under recency 0.45 and recency 0.25 as well, and warned that status is defined on recency so tier-status agreement is partly by construction.
- Script stopped before writing anything: no scored.csv, no methodology score section — waiting for weight approval.

## Stage 5c — engagement score (Step B, weights approved 0.40/0.35/0.25)
- Weighted 0-100 score from inverted recency 0.40, logins 0.35, session minutes 0.25 (books excluded, r=0.88 with logins).
- Tiers by terciles: Low <= 40.80 < Medium <= 51.25 < High; scored.csv has all rows, Unclassified handled separately.
- Documented in methodology.md under 'Engagement score'.

## Stage 6 — segment views
- Wrote `src/v2_segments.py`: rate-by-demographic charts + tables, genre mix and rates, tenure-band status mix (labelled cross-sectional, not a retention curve), the Active+High vs Churned profile, and the validation section (books/tenure by tier, logins/session by status).
- The 33 Unclassified rows are out of every tier/status chart and have their own small table; the only group under 100 subscribers is Genre 'Unknown' (54), which is table-only and marked small.
- Every caption carries the associations-not-causes line; methodology.md section 7 now states which comparisons are circular and which are the independent checks.
- Biggest gaps printed: high-value vs churned differ most on money (income/spend), age and occupation share.

## Stage 7 — 23 Oct 2026 (two fixes to segment views)
- Age now uses reference date 2026-10-02 (from clean.csv's Birth Date — clean.csv has no literal Age column, so Age is derived once at that date) and every segment output was regenerated so the numbers agree.
- Added `outputs/v2/significance_checks.csv`: high-value vs Churned gaps with Welch t-test p-values and Cohen's d for income/spend/age/children, and chi-square p-values with Cramér's V for Management, Graduate Degree, AgeGroup 1960-1969 and Fantasy.
- Reading: income/spend/children are small effects (d≈0.22-0.33), age is a boundary small effect (d=-0.20), and all four category gaps are negligible (V≤0.09) — each row carries a plain-English effect line, plus a note that with n=1,803 vs 901 a small gap can be significant yet practically small.

## Stage 8 — 23 Oct 2026 (written docs)
- Wrote `outputs/v2/insights.md`: high-value profile, Active-vs-Churned split (behaviour partly by construction, demographics valid but small), the genre/tenure null findings, six recommendations tied to surviving findings and the literature themes, and the limitations list.
- Applied the multiple-comparison caution across the document: 9 tests, Bonferroni bar 0.0056 — Fantasy (p≈0.037) is excluded everywhere; all recommended actions rest on income/spend/age/children/Management/Graduate/1960s effects or on behavioural facts.
- Wrote `outputs/v2/CHEATSHEET.md`: 5-line summary, key numbers, approved weights and status rules with sizes, tier cuts, and the 5 likely viva questions with short answers.
- All figures traced to outputs/v2 and data/processed/v2 only — nothing from Phase 1 files.

## Stage 9 — 23 Oct 23:59 (number audit)
- Re-derived every figure in insights.md and CHEATSHEET.md straight from scored.csv, status_summary, significance_checks and the table folder — all match (status 3,001/1,520/901/33, medians 5/58/152, tier cuts 40.80/51.25, tier sizes 1,810/1,806/1,806, all 901 Churned in Low, Unclassified 32/0/1, r=0.88, r=0.37, 26 raw spellings (23 after tidying)).
- Flagged that methodology section 4 still showed the pre-D1 counts (2,995/1,526) and added a pointer to section 5, which records the +6/−6 move to the current 3,001/1,520 — no numbers on disk disagree.
- Tightened two genre sentences in insights.md so the churned-rate band explicitly excludes the small Unknown group (n=54, 13.0%) and the Fiction mix uses its real shares (18.5-20.0%).

## Stage 10 — 23 Oct (Final Report page + standalone HTML)
- New `src/v2_report.py` reads only scored.csv, status_summary.csv, significance_checks.csv, insights.md and methodology.md — no number or recommendation text is hardcoded — and writes the self-contained `outputs/v2/final_report.html` (embedded pie PNG, no external links, opens offline).
- The same payload now renders as the first Phase 2 tab ("⓪ Final Report") in src/app.py: title/summary, 4 KPI cards + 33 Unclassified note, status pie with takeaway, 6 findings quoted from insights.md, tier table with the by-construction note, significance table with the Bonferroni/association note, three strategy cards, 7 limitations, 3 method lines, and a download button serving the identical HTML file.
- Page is unfiltered: verified that setting the sidebar Status filter to Churned leaves the tab showing all 5,455 / 55.3% / 28.0% / 16.6%; other Phase 2 tabs unaffected (indices shifted for the new first tab).
- Fixed four text-parsing bugs found on first run (14.15 false-matching "4.1", missing ".** " sentence split, bold lead ending in a comma, association sentence pulled from wrong paragraph); final Playwright run: 30/30 checks pass, zero page/console/server errors.

## Stage 11 — 23 Oct (gap-closer: rationale, justification, watchlist, tier chart)
- Backed up the app first: `src/app_backup_before_redesign.py` (56,990 bytes) before any redesign work; this stage touched no app code, no thresholds, no weights and no number in scored.csv.
- methodology.md gained: the tier-cutoff rationale (terciles; cuts 40.80/51.25 read from scored.csv, not typed), the explicit "why status is not defined on the score" justification in both section 2 and section 7, a status x tier table (11/1,187/1,803 Active; 898/619/3 Inactive; 901/0/0 Churned; 32/0/1 Unclassified), and the Active-Low watchlist table.
- New outputs: `outputs/v2/watchlist.csv` — 11 Active subscribers in the Low tier (mean recency 29.1 days, 1.45 logins, 11.3 session minutes, 4.4 books), the early-warning group; and `outputs/v2/charts/bar_behaviour_by_tier.png` — four panels of tier means with the by-construction caption.
- `outputs/v2/final_report.html` regenerated (109,958 bytes, still offline/self-contained — 2 embedded PNGs, zero external links) and now includes the tier chart, the cutoff rationale and the watchlist block; produced by the new idempotent `src/v2_tier_docs.py`.

## Stage 12 — Presentation deck (PDF + PPTX) with live app screenshots
Captured 24 screenshots of the running Streamlit app (all 7 pages, all 7 Explore
sub-tabs, a Churned+Professional filter combo, and a Customer ID lookup) with
Playwright at 2x resolution into outputs/v2/screenshots/. Built a 27-slide deck in
the app's indigo/lavender theme: title, project overview, 5-step method, score
formula, status rules, a 18-slide app walkthrough (every slide carries a takeaway
line), four key findings, three strategy cards, and an honest-limitations closer.
Delivered as outputs/v2/deck/ebook_subscriber_insights.pdf and .pptx; every number
is loaded from the report payload (no hardcoding), and the findings-slide layout
and clipped tab screenshots were fixed and re-verified by rendering PDF pages back
to images.

## Stage 13 — 30 Oct 2026 (reviewer feedback: alignment, full Inactive rule, weight sensitivity)
- Aligned the three numbers the reviewer saw disagreeing across email/poster/site: genre is now "26 raw spellings (23 after tidying)" everywhere, children at home is "2.15 vs 1.74", and recency above 365 days is "kept as-is (capture cap 400)". Reframed the all-901-Churned-in-Low observation as "expected by design" (recency is 40% of the score and also defines Churned) in `insights.md` and `CHEATSHEET.md`, and regenerated `final_report.html` from the corrected sources.
- Stated the full Inactive rule (31-90 days, or 30 days or fewer with fewer than 1 login) everywhere the old "31-90 days" shorthand had crept in, including three hardcoded strings in `src/app.py` (status tooltip, Start Here hero card, KPI help) — the Methodology page and Glossary already had it.
- New `src/v2_sensitivity_standalone.py`: re-scored the 5,422 classified subscribers under equal-thirds, recency-light (0.25) and recency-heavy (0.50) weights, re-cutting tiers from each set's own terciles. Baseline reproduces the shipped Tier column exactly (0 of 5,422 mismatches); alternatives keep 95.4-96.6% in the same tier, Spearman rho >= 0.997, and nobody moves more than one tier — but the Active-in-Low watchlist swings 29/11/2, so that count is not robust. Status is confirmed unaffected (3,001/1,520/901 constant) because it reads recency only.
- Surfaced the sensitivity check on the Final Report page as section 5b (overview table, per-alternative migration tables, and the honest caveat that the watchlist count depends on the weights); outputs in `outputs/v2/sensitivity.csv` and `sensitivity_summary.md`.
- Fix after first deployment: section 5b failed on Streamlit Cloud with "No module named 'scipy'", because pandas' Series.corr(method="spearman") calls scipy, which that environment does not ship. Replaced it with the textbook equivalent — Pearson correlation of the ranks (base_score.rank().corr(alt.rank())), which needs only numpy/pandas. Verified the two agree on the real data to a max absolute difference of 1.1e-16, and re-ran the standalone script to confirm sensitivity.csv and sensitivity_summary.md are unchanged. Re-tested the app with scipy deliberately blocked: the panel now renders with no error.
