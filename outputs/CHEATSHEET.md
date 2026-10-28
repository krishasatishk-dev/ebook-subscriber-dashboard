# CHEATSHEET — eBook Subscriber Propensity & Segmentation
*One page. Every number verified against the repo (2026-10-10). Companion file: `outputs/EXPLAINER.md`.*

---

## 30-second pitch
> "I scored 16,404 customers 0–100 on subscription likelihood using the three features that
> actually correlate with the flag — children at home (r 0.46), monthly spend (r 0.42),
> income (r 0.29) — weighted 40/35/25, min-max normalised. The score works: subscriber rate
> rises 13.0% → 25.8% → 61.1% across score thirds (4.7× lift). Crossing tier × real flag
> gives six segments, none over 29%: protect 3,308 Core Subscribers, convert 2,103
> High-potential Prospects ($104K income, no subscription), watch 699 Low-fit Subscribers.
> It all runs in a Streamlit dashboard with live filters, per-customer lookup, and full
> methodology. Caveat: no usage data — association, not causation; weights judged, not fitted."

## The one formula
```
SPS = (0.40 × children_norm + 0.35 × spend_norm + 0.25 × income_norm) × 100
x_norm = (x − min) / (max − min)        ranges: children 0–5 · spend $22–$176 · income $9,482–$196,511
```
Tiers by terciles: **Low** ≤16.7 · **Medium** 16.7–29.2 · **High** >29.2
(boundaries 16.7463 / 29.1834). Human approves weights in `03_score.py` before anything is written.

## Headline numbers

| What | Number |
|---|---|
| Raw data | 16,519 rows × 21 cols; 16,404 unique IDs; **115 duplicates** |
| Analysis base | **16,404** customers (dedup in `04_segment.py`) |
| Overall subscriber rate | **33.2%** (5,451 / 16,404) |
| Mean income / mean spend | **$78,129** / **$72.4 per month** (middle 50% spend $52–$84) |
| Top correlations with flag | children **0.4564** · spend **0.4218** · income **0.2871** |
| Input collinearity (max pair) | children–spend **0.73** (all pairs < 0.8 threshold) |
| Score distribution | mean **28.6** · median **21.6** · max **98.4** |
| Tier validation | Low **13.0%** → Medium **25.8%** → High **61.1%** = **4.7× lift** |
| Worked example (cust 11001) | 3 kids, $117 spend, $101,141 income → **score 57.84 → High → Core** |

## The six segments (share of 16,404)

| Segment | Rule | n | Share | Story |
|---|---|---|---|---|
| Core Subscribers | flag 1, High | 3,308 | 20.2% | $107,799 · $105.6/mo · 3.1 kids · 71% Prof/Mgmt · **protect** |
| Low-fit Subscribers | flag 1, Low | 699 | 4.3% | 96% childless · $51.1/mo · score 12.4 · **retention risk** |
| High-potential Prospects | flag 0, High | 2,103 | 12.8% | $103,736 income, $91.4 spend · 71% Prof/Mgmt · **convert** |
| Low-priority | flag 0, Low | 4,712 | 28.7% | $44,228 · lowest score · **minimal effort** |
| Mid-tier Subscribers | flag 1, Medium | 1,444 | 8.8% | upsell pool |
| Mid-tier Non-subscribers | flag 0, Medium | 4,138 | 25.2% | secondary conversion pool |

Largest segment 28.7% — no segment exceeds the 60% warning threshold.

## Best patterns to show
- **Children staircase:** 19.4% → 24.7% → 59.0% → 69.3% → 72.5% → **83.9%** (0→5 kids)
- **Age:** 1960s-born **51.6%** vs base 33.2%; oldest cohort just 13.3%
- **Job:** Professional **44.3%** / Management 37.4% vs Manual 23.7%
- **Education:** Bachelors **39.3%** highest · Partial HS 23.2% lowest
- **State spread (top 15):** only NJ 36.8% → AZ 31.1% — geography is a weak lever

## Files map
- Scripts: `src/02_eda.py` (charts/pivots/takeaways) → `03_score.py` (score, interactive approval) → `04_segment.py` (dedup + 6 segments) → `app.py` (Streamlit: Intro + Dashboard, 5 tabs, 5 filters, CSV download)
- Data: `data/processed/clean.csv` (16,519×23) → `scored.csv` (16,519×10) → `segmented.csv` (16,404×11)
- Outputs: `outputs/charts/` 11 PNGs · `outputs/pivots/` 2 XLSX · `methodology.md` · `insights.md` (all figures re-verified ✓) · `eda_takeaways.md` (⚠ stale — see below)

## ⚠ Not verified / missing
- **`outputs/BUILD_LOG.md` does not exist** (checked twice; no file matching `*build*` in repo). Never cite it.
- **No cleaning script exists** — git history has only `02/03/04/app.py`. Cleaning produced `clean.csv` but that code was never committed.
- Raw CSV provenance unverified (course-provided file).

## ❌ Do not say
| Wrong claim | Verified truth |
|---|---|
| "clean.csv has 16,404 rows" | 16,519 rows, 16,404 unique IDs |
| "Core is ~33% of customers" | Core = **20.2%**; 33.2% is the overall subscriber rate |
| "Core earns ~$104K, spends ~$88" (from `eda_takeaways.md`) | **$107,799, $105.6/mo, 3.1 kids** |
| "HPP ~$101K / ~$77" | **$103,736 / $91.4** |
| "Low-priority ~$74K / ~$57 / 0.4 kids" | **$44,228 / $50.4 / 0.0 kids** |
| "We predicted churn / used ML / measured accuracy" | No churn labels, no classifier, no held-out test |
| "More spend *causes* subscribing" | Association only — never causation |
| "We modelled reading/engagement behaviour" | Dataset has **zero** usage columns |
| "The cleaning script / build log is in the repo" | Neither exists |

## Answers to the 5 hardest questions
1. **"Is this ML?"** → Transparent weighted index, weights from correlations, human-approved. Explainability over accuracy; a fitted model with a test split is the next step.
2. **"How do you know it works?"** → Tiers: 13.0 → 25.8 → 61.1%, monotonic, 4.7× lift; score never sees the flag. Limit: in-sample.
3. **"Why children as top weight?"** → Strongest measured association in this data (r 0.4564), proxy for household use. Not a belief — a correlation we report.
4. **"Is it circular?"** → Score inputs = children, spend, income only. Flag used afterwards for tier test and segment labels.
5. **"Biggest weakness?"** → No behaviour data (profile-based segments only) + judgement-based weights validated in-sample. Both are stated in the dashboard itself.

## Next steps (honest)
1. Commit the missing cleaning script + write `BUILD_LOG.md` (reproducibility).
2. Refresh stale `eda_takeaways.md` and de-dup the doubled sentence in `methodology.md`.
3. Get usage data → fit logistic regression/GBM with train/test split and real metrics.
4. Calibrate tiers into probabilities; A/B test the Low-fit and High-potential offers.
