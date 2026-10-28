# EXPLAINER — eBook Subscriber Propensity & Segmentation Dashboard

**How to read this file.** It explains the whole project in plain language so you can talk
about it confidently. Every number here was checked against the actual files in this repo.
If something could not be verified, it says **"not verified"** — never fill such a gap with a
guess.

**Where this sits:** `outputs/EXPLAINER.md`. Its one-page companion is
`outputs/CHEATSHEET.md`.

---

## PART A — What this project is (the big picture)

**In one sentence:** we took a customer list from an eBook subscription business, measured
what makes a person likely to subscribe, gave every customer a score from 0 to 100, split
the customer base into six groups, and built an interactive dashboard to show it all.

**The two questions the project answers:**

1. Which customers are most likely to subscribe?
2. How should the business treat each group differently?

**The raw material.** One CSV file: `Customer Data - Customer Data.csv`.
Verified facts about it:

| Fact | Value |
|---|---|
| Rows (customers) | 16,519 |
| Columns | 21 |
| Unique Customer IDs | 16,404 |
| Duplicate Customer IDs | 115 (same ID appears more than once) |
| Column names include | Customer ID, Birth Date, Education Level, Occupation, Gender, Marital Status, Home Owner Status, Number of Cars Owned, Number of Children At Home, Total Number of Children, Annual Income, Avg Monthly Spend, **eBook Subscriber Flag** |

The **eBook Subscriber Flag** is the answer key: `1` means the person subscribes,
`0` means they do not. Overall, **33.2%** of customers are subscribers
(5,451 of 16,404 after de-duplication; 5,489 of 16,519 before it — both round to 33.2%).

**What is NOT in the data (important and verified):** there are no usage columns — no
logins, sessions, reads, clicks, churn labels, or engagement metrics. A keyword scan of all
21 column names found none. Everything in this project is built from demographics
(age, education, job), money (income, monthly spend), household (children, cars, home
ownership), and the flag. The dashboard shows this warning on every page.

**Honest note on provenance:** where the raw CSV originally came from is **not verified**.
It arrived with the course materials (the `reregardingprojectreportpptanddatasetebooksubscr/`
folder holds the project report and proposal). Treat it as a provided practice dataset.

---

## PART B — How the project is built (the pipeline)

A **pipeline** is a chain of steps where each step's output becomes the next step's input.

```
raw CSV  →  [cleaning]  →  clean.csv  →  02_eda.py  →  charts + pivots + takeaways
                             │
                             └→ 03_score.py (you type "y") → scored.csv + methodology.md
                                        │
                                        └→ 04_segment.py → segmented.csv + 2 more charts
                                               │
                                               └→ app.py (Streamlit dashboard)
```

### Stage 1 — Cleaning → `data/processed/clean.csv`

| Check | Verified result |
|---|---|
| Shape | 16,519 rows × 23 columns |
| New columns vs raw | `AgeGroup`, `IncomeBand` (21 → 23) |
| Duplicate IDs removed here? | **No** — clean.csv still has all 16,519 rows (16,404 unique IDs) |
| Birth dates | Raw is `M/D/YY` with 2-digit years (tokens 10–80, i.e. 1910–1980); clean.csv stores ISO dates with the 1900s added (`4/8/66` → `1966-04-08`). All 16,519 rows converted. |
| AgeGroup bins | `1910-1949` (2,930), `1950-1959` (3,997), `1960-1969` (5,609), `1970-1979` (3,982), plus **1 blank** |
| The 1 blank AgeGroup | Customer 12725, born `8/13/10` → 1910-08-13; 1910 falls just outside the first bin, so it was left empty. One row in 16,519. |
| IncomeBand | Five equally sized buckets `Q1`–`Q5` (3,304 each, one has 3,303) — a **quintile** split of income |
| State | Not a raw column. Derived from `City-ZipCode-State` (format `City-ZipCode-State`, e.g. `Oakland-94601-California`) by taking the text after the last hyphen. Full state names. 0 blanks in the final data. Top states by count: California 3,192, Texas 1,946, Ohio 874, Florida 850, North Carolina 840. |
| Nearly empty columns excluded | `Title` 99.5% missing (16,431 rows), `Street Address2` 98.3% missing (16,243 rows) |

**⚠️ Not verified — the cleaning script does not exist.** Git history shows only four files
were ever committed under `src/`: `02_eda.py`, `03_score.py`, `04_segment.py`, `app.py`.
No `01_clean.py` (or similar) has ever been committed. The cleaning was done before the
committed scripts, and the code that produced `clean.csv` is **not in the repo**. If asked,
say honestly: *"The cleaning steps are documented in the README and visible by comparing
raw vs clean CSVs, but the script itself was not committed — that's a gap I'd fix first."*

**⚠️ Not verified — `outputs/BUILD_LOG.md` does not exist.** Checked twice: the file is
absent from `outputs/`, and a repo-wide search for `*build*` returned nothing. If your
brief says to cite a build log, report it as missing. Do not describe it.

### Stage 2 — EDA → `src/02_eda.py`

**EDA** means Exploratory Data Analysis: looking at the data with charts and numbers before
modeling, to find patterns and avoid dumb mistakes.

- Reads `clean.csv`, derives `State` in memory, writes **9 charts** to `outputs/charts/`
  (2 histograms, 5 rate bar charts, 1 pie, 1 correlation heatmap).
- Writes **2 pivot tables** to `outputs/pivots/` (`.xlsx`): age × occupation subscription
  rate, and income band × education average income. A **pivot table** is a spreadsheet-style
  grid that summarises many rows into one cell per combination.
- Rewrites `outputs/eda_takeaways.md` from scratch, then appends a one-line takeaway under
  every chart.
- Prints correlations with the flag and runs a collinearity check (see Part F).

### Stage 3 — Scoring → `src/03_score.py`

Interactive on purpose: it prints candidate inputs, correlations, and proposed weights, then
pauses at `Approve these weights and proceed? (y/n):` and **only continues if you type `y`**.
Typing anything else prints `Aborted. No changes saved.` and exits without writing files.
This forces a human decision before the model is applied.

Outputs:

- `outputs/methodology.md` — appended with the scoring model (this text is shown live in the
  dashboard's Methodology tab).
- `data/processed/scored.csv` — 16,519 rows × 10 columns: Customer ID, Title, First/Last
  Name, the three score inputs, `Subscriber_Propensity_Score`, `Tier`, and the flag.

### Stage 4 — Segmentation → `src/04_segment.py`

- **Removes the 115 duplicate IDs here** (`drop_duplicates(subset="Customer ID", keep="first")`),
  so the working set becomes 16,404 customers.
- Writes the six segment rules into `outputs/methodology.md` **before** computing anything —
  the rules are fixed first, then applied (no fitting to get a nicer result).
- Assigns each customer to exactly one of six segments (Part F).
- Outputs `data/processed/segmented.csv` (16,404 × 11), a pie chart, a 3-panel profile bar
  chart, and appends 2 takeaways to `eda_takeaways.md`.
- Prints a warning if any segment exceeds 60% of the base. **None does** (largest is 28.7%).

### Stage 5 — Dashboard → `src/app.py`

A **Streamlit** app (Streamlit is a Python library that turns scripts into web pages).

Run from the repo root: `streamlit run src/app.py` (data is read with relative paths).
Python environment used here: `/Users/krishasatishkadam/ebook-prototype/.venv` (Streamlit 1.64.0);
system Python 3.14.6 runs the pipeline scripts.

Structure (verified in code):

- **Two pages** switched by sidebar buttons: **Intro** and **Dashboard**.
- **Intro page:** just the hero banner (gradient art with an open-book picture on the
  right), a centered "📚 Welcome to the eBook Subscriber Intelligence Dashboard" heading,
  and a single **Open the Dashboard** button. All earlier explainer text, the six segment
  cards, and the intro data note were removed from this page (the data note still appears
  in the dashboard sidebar).
- **Dashboard:** sidebar filters (State, Occupation, Education Level, AgeGroup, Segment),
  a 4-KPI row (customers in view, subscriber rate vs 33.2% overall, average propensity
  score, average monthly spend), then **5 tabs**:
  1. Overview — segment donut, subscriber rate by occupation and by age group (red dashed
     average line), score histogram with the two tier boundary lines drawn on it.
  2. Correlation Heatmap — Pearson r between income, spend, children, and the flag.
  3. Segment Profiles — table + 3 bar charts (income, spend, children) per segment.
  4. Customer Lookup — type a Customer ID, get score, tier, segment, flag, and the three
     inputs used in the score.
  5. Methodology — renders `outputs/methodology.md` exactly as stored.
- **Download button** exports the currently filtered rows as `segmented_filtered.csv`.
- Data loads through `@st.cache_data` (Streamlit's memoisation: the data is read once and
  kept in memory, so filter changes recompute charts without re-reading files).
- Every filter recomputes KPIs and all five tabs live.

### Repository contents (verified with git)

One commit, 30 tracked files: 4 scripts (`src/`), 3 CSVs (`data/processed/`), 11 chart PNGs,
2 pivot XLSX, 3 markdown outputs (`methodology.md`, `eda_takeaways.md`, `insights.md`),
README, requirements.txt, .gitignore, the raw CSV, and the 3 report/PPT files in
`reregardingprojectreportpptanddatasetebooksubscr/`.

**Known cosmetic quirks (verified, harmless):**

- `outputs/methodology.md` repeats one sentence twice (the "The dataset is partitioned into
  six mutually exclusive segments…" line). Because `03_score.py` and `04_segment.py` *append*
  to methodology.md, re-running them adds copies; the file currently shows this one doubled
  line. It is visible in the dashboard's Methodology tab.
- README's project-structure comment calls `clean.csv` "16,404 unique customers", but the file
  itself has 16,519 rows (with 16,404 unique IDs). The dedup happens later, in `04_segment.py`.
- README's tier table rounds to 12.9% / 25.9% / 61.1%; the actual values are 12.95% / 25.83% /
  61.13%, which the dashboard states as 13.0% / 25.8% / 61.1%. Both are the same data —
  just rounding. Prefer 13.0 / 25.8 / 61.1 when you speak.

---

## PART C — Every technical term, defined

*(Definitions are also given inline at first use; this is the consolidated list.)*

- **Dataset / CSV** — a table of data saved as one file; each row is one record (here, one
  customer), each column is one property.
- **Column / variable / field** — the same thing: one measured property, e.g. `Annual Income`.
- **Missing data (null / NaN)** — a cell with no value. `% missing` = blank cells ÷ rows.
- **De-duplication (dedup)** — removing repeated records so each ID appears once.
- **Mean (average)** — sum of values ÷ count of values.
- **Median** — the middle value when you sort all values; less affected by extremes than the mean.
- **Quartile / percentile** — cut the sorted data into 4 equal parts (quartiles) or 100 equal
  parts (percentiles). 25th percentile = first quartile = the value 25% of rows sit below.
- **Skewed (right-skewed)** — most values are low with a long tail of high values; the mean
  sits above the median. Both income and monthly spend look like this.
- **Correlation (Pearson r)** — a number from −1 to +1 saying how two numeric columns move
  together. `+1` = rise together perfectly, `0` = no linear relationship, `−1` = opposite
  directions. It measures **association, not causation**: two things can travel together
  without one causing the other.
- **Collinearity** — when two input variables are highly correlated with each other (usually
  a red flag at |r| > 0.8), because the model would count the same signal twice.
- **Normalisation (min-max)** — rescaling a column so its smallest value becomes 0 and its
  largest becomes 1: `x_norm = (x − min) / (max − min)`. It makes columns with different
  units (dollars vs counts of children) comparable.
- **Weight** — how much each input matters in the final sum; here weights must add up to 1.0.
- **Weighted sum** — multiply each input by its weight, then add the results.
- **Propensity score** — a single number estimating how likely a customer is to do the thing
  we care about (here, subscribing). Ours is the **Subscriber Propensity Score (SPS)**, 0–100.
- **Quantile** — a cut point that splits data into equal-sized groups; `quantile(0.33)` is
  the value with 33% of rows below it.
- **Tercile** — cut into three equal parts (33rd and 67th percentile). We use terciles to
  build tiers.
- **Tier** — our Low / Medium / High banding of the score. It is **relative to this dataset**
  (a customer's tier would change if the customer base changed).
- **Lift** — how much better one group performs than another: 61.1% ÷ 13.0% ≈ **4.7×**.
- **Segment** — a named group of customers treated as one audience. Ours are **mutually
  exclusive**: every customer belongs to exactly one segment.
- **Profile-based vs behaviour-based segmentation** — we group by *who people are*
  (demographics, money) not by *what they do* (reading, logins), because behaviour data
  doesn't exist here.
- **EDA** — Exploratory Data Analysis; chart-first exploration before modeling.
- **Pivot table** — a grid that aggregates many rows into one number per row/column combination.
- **KPI** — Key Performance Indicator; the headline numbers shown at the top of the dashboard.
- **Dashboard / filter** — a visual summary page; a filter narrows which rows are counted.
- **Pipeline / stage / script** — the ordered chain of processing steps; each step; a runnable
  program file (e.g. `03_score.py`).
- **Commit / repository (repo)** — one saved snapshot of the project; the project's storage
  (here on GitHub: `krishasatishk-dev/ebook-subscriber-dashboard`, private).
- **Streamlit / cache** — the web-app framework used; `cache` = keep loaded data in memory
  so the app reacts instantly to filters.

---

## PART D — Worked example: customer 11001

Use this to show that every score in the dashboard can be reproduced by hand.

**Step 0 — Who is this customer (from `clean.csv`):**

| Field | Value |
|---|---|
| Customer ID | 11001 |
| Number of Children At Home | 3 |
| Avg Monthly Spend | $117 |
| Annual Income | $101,141 |
| AgeGroup / Occupation / Education | 1960-1969 / Professional / Bachelors |

**Step 1 — Normalise each input to 0–1** using the dataset's min and max
(children 0–5, spend $22–$176, income $9,482–$196,511):

- Children: (3 − 0) / (5 − 0) = **0.6000**
- Spend: (117 − 22) / (176 − 22) = 95 / 154 = **0.6169**
- Income: (101,141 − 9,482) / (196,511 − 9,482) = 91,659 / 187,029 = **0.4900**

**Step 2 — Weighted sum × 100:**

```
SPS = (0.40 × 0.6000 + 0.35 × 0.6169 + 0.25 × 0.4900) × 100
    = (0.2400 + 0.2159 + 0.1225) × 100
    = 57.84
```

Hand-computed 57.84 — **exactly matches** the stored `Subscriber_Propensity_Score` of 57.84.

**Step 3 — Tier:** tercile boundaries are 16.7463 and 29.1834 (call them 16.7 and 29.2).
57.84 > 29.2 → **High tier**.

**Step 4 — Segment:** the flag for 11001 is `1` (a subscriber), and the tier is High →
**Core Subscribers** (rule: flag = 1 AND Tier = High).

You can repeat this in the dashboard: tab **④ Customer Lookup** → type `11000` or `11001`
→ the app shows the same score, tier, segment, and the three inputs.

---

## PART E — The charts, one by one

All 11 PNGs live in `outputs/charts/`. Numbers below are verified from the CSVs.

| # | File | What it shows | The one-line story (verified) |
|---|---|---|---|
| 1 | `hist_avg_monthly_spend.png` | Distribution of monthly spend | Right-skewed: mean **$72.4/mo**, middle 50% spend **$52–$84**. |
| 2 | `hist_annual_income.png` | Distribution of income | Right-skewed: mean **$78,123**, median **$76,120**, tail to $196,511. |
| 3 | `bar_sub_by_occupation.png` | Subscriber rate by job | **Professional 44.3%** and **Management 37.4%** top the chart; **Manual 23.7%** and **Clerical 23.7%** bottom; base rate 33.2%. |
| 4 | `bar_sub_by_education.png` | Subscriber rate by education | **Bachelors 39.3%** highest; **Partial High School 23.2%** lowest; Graduate Degree sits mid-table at 30.0%. |
| 5 | `bar_sub_by_age.png` | Subscriber rate by birth cohort | **1960–1969: 51.6%** — far above the 33.2% base; **1910–1949: 13.3%** lowest; 1970–1979: 26.4%; 1950–1959: 28.8%. |
| 6 | `bar_sub_by_state.png` | Rate for the 15 largest states | Real but modest regional spread: **New Jersey 36.8%** (highest of the 15) down to **Arizona 31.1%** (lowest) — a ~6-point band, so geography is a weak lever. |
| 7 | `bar_sub_by_children.png` | Rate by children at home | Steepest pattern in the project: **19.4% (0 kids) → 24.7% → 59.0% → 69.3% → 72.5% → 83.9% (5 kids)**. |
| 8 | `pie_subscriber_dist.png` | Subscribers vs not | **33.2% subscribe** (5,489 of 16,519; on the deduped base 5,451 of 16,404 — both 33.2%). |
| 9 | `heatmap_corr_numeric.png` | Income vs spend vs flag | Income–spend move together at **r = 0.61**; both relate more weakly to the flag (0.29 and 0.42). |
| 10 | `pie_segment_distribution.png` | The six segments | Core 20.2%, Low-fit 4.3%, High-potential 12.8%, Low-priority 28.7%, Mid-tier Subs 8.8%, Mid-tier Non-subs 25.2%; no slice above 60%. |
| 11 | `bar_segment_profiles.png` | Income / spend / children per segment | Core leads every panel ($107,799, $105.6, 3.1 kids); High-potential runs close ($103,736, $91.4, 2.0 kids); Low-priority trails ($44,228, $50.4, 0.0 kids). |

Pivot tables: `outputs/pivots/pivot_age_occupation.xlsx` (subscription rate by age × job) and
`outputs/pivots/pivot_income_education.xlsx` (average income by income band × education).

**Dashboard tabs mirror these charts** (Overview = donut + rate bars + score histogram;
tab ② = heatmap; tab ③ = profile table + bars), with every chart recomputing under the
sidebar filters.

---

## PART F — The scoring model and segment rules (and why)

### F.1 Input selection — evidence first

`03_score.py` prints correlations of every candidate numeric column with the flag
(verified on `clean.csv`):

| Candidate input | \|r\| with flag | Chosen? |
|---|---|---|
| Number of Children At Home | **0.4564** | ✅ weight 0.40 |
| Avg Monthly Spend | **0.4218** | ✅ weight 0.35 |
| Annual Income | **0.2871** | ✅ weight 0.25 |
| Total Number of Children | 0.2335 | ❌ dropped — double-counts family size alongside children at home |
| Number of Cars Owned | 0.1648 | ❌ too weak |
| Home Owner Status | 0.0006 | ❌ essentially zero |

**Collinearity check** (collinearity = inputs being redundant with each other). All three
pairs among the chosen inputs are below the 0.8 threshold (verified):
children–spend **0.73**, spend–income **0.61**, children–income **0.37**. So all three were
kept, and no pair is double-counted.

### F.2 The formula

```
SPS = (0.40 × children_norm + 0.35 × spend_norm + 0.25 × income_norm) × 100
```

where `norm` = min-max normalisation (Part C). Ranges used: children 0–5, spend $22–$176,
income $9,482–$196,511. Weights sum to 1.0 and follow the correlation ranking
(strongest predictor gets the biggest weight). They were set **by judgement from these
correlations** — they were not fitted by an algorithm and not tested on held-out data.

Score shape (verified): mean **28.6**, median **21.6**, maximum **98.4**.

### F.3 Tiers and the validation test

Tercile cuts on the score: **16.7463** and **29.1834** → Low / Medium / High
(computed on the 16,519-row scored file).

| Tier | Score range | Customers | Subscriber rate |
|---|---|---|---|
| Low | 0.1 – 16.7 | 5,451 | **12.95%** (≈13.0%) |
| Medium | 16.7 – 29.2 | 5,617 | **25.83%** (≈25.8%) |
| High | 29.2 – 98.4 | 5,451 | **61.13%** (≈61.1%) |

**Why this is the key validation:** subscription rate climbs monotonically (always upward)
Low → Medium → High, and the top third converts **4.7×** better than the bottom third
(61.1 ÷ 13.0). A score that failed would show flat or jumpy rates. Note the score never
touches the flag as an input — the flag is only used afterwards to test it.

### F.4 The six segments (rules written before computing)

**Segment = score tier × actual flag.** Six mutually exclusive combinations:

| # | Segment | Rule | Customers | Share | Mean score | Mean income | Mean spend | Mean kids |
|---|---|---|---|---|---|---|---|---|
| 1 | Core Subscribers | flag=1, tier=High | 3,308 | 20.2% | 57.1 | $107,799 | $105.6 | 3.1 |
| 2 | Low-fit Subscribers | flag=1, tier=Low | 699 | 4.3% | 12.4 | $50,397 | $51.1 | 0.0 |
| 3 | High-potential Prospects | flag=0, tier=High | 2,103 | 12.8% | 44.5 | $103,736 | $91.4 | 2.0 |
| 4 | Low-priority | flag=0, tier=Low | 4,712 | 28.7% | 11.4 | $44,228 | $50.4 | 0.0 |
| 5 | Mid-tier Subscribers | flag=1, tier=Medium | 1,444 | 8.8% | 22.8 | $84,519 | $68.1 | 0.3 |
| 6 | Mid-tier Non-subscribers | flag=0, tier=Medium | 4,138 | 25.2% | 21.9 | $82,453 | $66.3 | 0.3 |

(Counts and shares computed on 16,404 deduped customers; they sum to 100%. Largest segment
is 28.7% — comfortably under the 60% warning line.)

**Profiles of the two segments that matter most (verified):**

- **Core Subscribers (keep them):** income $107,799 (median $110,866), spend $105.6/mo,
  3.1 children; **71% (2,340)** are Professional/Management; **58% (1,906)** born 1960s;
  **42% (1,393)** have 4+ children; top state California; mean score 57.1.
- **Low-fit Subscribers (retention risk):** they *do* subscribe, yet score in the bottom
  third (mean 12.4, range 3.5–16.7). **96% (669 of 699) have zero children** — family size
  is what drags their score down; mean spend $51.1 (below the $52 bottom quartile), mean
  income $50,397; **52% (360)** born 1970s, a cohort that subscribes at only 26.4% overall.
- **High-potential Prospects (conversion pool):** they look like Core in every measurable
  way but haven't subscribed. Income $103,736 (only $4,063 below Core), spend $91.4 (a $14.3
  gap to Core's $105.6); **71% (1,494)** Professional/Management (912 are Professional, the
  largest single job cell); **51% (1,078)** born 1910–1949 or 1950–1959 — the two
  lowest-converting cohorts (13.3% and 28.8%) despite high income. Mean score 44.5.

### F.5 Recommended actions (from `outputs/insights.md`, all figures verified)

- **Low-fit (699):** protect with loyalty/grandfathered pricing (they are the most
  price-exposed subscribers); market *individual* value, not family bundles (96% childless);
  start retention monitoring with the 1970s subgroup (360 of 699).
- **High-potential (2,103):** run job-targeted campaigns (professional peers convert at
  44.3% / 37.4%); push premium trials rather than discounts (income is already there — the
  gap is spend, $91.4 vs $105.6); explicitly target the 55+ high-income block (1,078 people).

---

## PART G — Caveats, limitations, and what NOT to say

### G.1 The limitations (say these yourself, before anyone asks)

1. **No behaviour data.** Verified: zero engagement columns in the raw file. No logins,
   sessions, reads or churn labels. Engagement can only be *inferred* from demographics.
   Nothing here models churn directly.
2. **Profile-based, not behaviour-based segments.** Core vs High-potential differ only by
   the flag; we cannot claim a prospect would behave like a Core subscriber after converting.
3. **Association, not causation.** The score shows variables travel together with
   subscribing. It does NOT show that raising someone's spend or income would cause them to
   subscribe, and no recommendation is guaranteed to work.
4. **Not a fitted/validated model.** Weights come from correlation magnitudes applied by
   judgement — no algorithm fitting, no train/test split, no accuracy metric (no AUC,
   no precision/recall). The tier test (13.0 → 25.8 → 61.1) is an in-sample check, on the
   same data the weights were read from. Honest framing: *"transparent index, validated
   in-sample, would need hold-out validation in production."*
5. **Tiers are relative.** Terciles are computed from this dataset; a different customer
   base would produce different boundaries.
6. **Data caveats.** 115 duplicate IDs (deduped only at the segmentation stage);
   two-digit birth years needed century inference (raw years span 1910–1980);
   1 row (Customer 12725) has no AgeGroup; `Title` 99.5% and `Street Address2` 98.3% missing
   and were excluded; State is parsed from a concatenated `City-ZipCode-State` string;
   provenance of the raw file is unverified.
7. **Mixed rows-counts.** `clean.csv` and `scored.csv` have 16,519 rows (dedup happens in
   `04_segment.py`); `segmented.csv` and the dashboard use 16,404. Tier rates come from the
   16,519-row file; segment counts from the 16,404-row file.

### G.2 Numbers that exist in output files but are WRONG — do not quote them

`outputs/eda_takeaways.md` was appended by earlier script runs and contains stale text.
Checked against current data:

| Don't say (it's in eda_takeaways.md) | Verified truth |
|---|---|
| "a core of ~33% High-tier subscribers (Core Subscribers)" | Core Subscribers = **20.2%** (3,308). 33.2% is the *overall subscriber rate*, a different number. |
| "Core … income (~$104K) and spend (~$88), most children (~1.3)" | Core = **$107,799**, **$105.6/mo**, **3.1 children**. |
| "High-potential … (~$101K and ~$77)" | HPP = **$103,736**, **$91.4/mo**. |
| "Low-priority … (income ~$74K, spend ~$57, children ~0.4)" | Low-priority = **$44,228**, **$50.4/mo**, **0.0 children**. |
| "Mid-tier Subscribers, ~25.8% subscriber rate / Non-subscribers ~13.0%" | Incoherent: by construction Mid-tier Subscribers are 100% subscribers and Mid-tier Non-subscribers 0%. The 25.8% figure is the *Medium tier's* overall rate. |

**Safe sources to quote:** `outputs/insights.md` (every figure in it was re-verified), the
README's score/segment tables, `outputs/methodology.md`, and this EXPLAINER.

### G.3 Do-not-say checklist

- ❌ "The cleaning script is in the repo." → No such script exists (never committed).
- ❌ "There's a build log." → `outputs/BUILD_LOG.md` does not exist — **not verified / missing**.
- ❌ "clean.csv has 16,404 rows." → It has 16,519 rows with 16,404 unique IDs.
- ❌ "We predicted churn / used ML classifiers / measured accuracy." → No churn labels, no
  classifier, no held-out test. It's a transparent weighted index.
- ❌ "More spend *causes* subscription." → Association only.
- ❌ "We modelled engagement/reading behaviour." → No behaviour data exists.
- ❌ "The segments prove how customers behave." → They show who customers are, not what they do.
- ❌ Quoting any G.2 figure from `eda_takeaways.md`.

---

## PART H — What could come next (honest options, not promises)

1. **Fix the reproducibility gap first:** write and commit the missing cleaning script so
   `clean.csv` can be rebuilt from raw; add a build log (`outputs/BUILD_LOG.md`) that records
   what ran, when, and with what results; de-duplicate inside the cleaning stage so all three
   processed CSVs agree on row counts.
2. **Clean the outputs:** de-duplicate the doubled sentence in `methodology.md`, and rewrite
   the stale takeaways flagged in G.2 so every output file matches the data.
3. **Behaviour data** (needs a new source): reading logs, logins, session length, content
   categories — enabling real engagement and churn models like the report's literature themes.
4. **Fit and validate a model:** logistic regression or gradient boosting on the same inputs,
   with a train/test split and proper metrics (AUC, precision/recall), then compare its
   lift against the hand-set score.
5. **Calibrate the score:** convert propensity to an actual probability per tier
   (High tier ≈ 61% base rate), so sales can expect counts, not just rankings.
6. **Operational follow-through:** A/B test the Low-fit pricing offer and the High-potential
   trial offer, and measure whether lift survives contact with reality.

---

## PART I — Presentation scripts

### I.1 The 3-minute script

> **[0:00–0:30 — the problem]**
> "This project starts from one question: with a list of 16,404 customers and a 33.2%
> subscription rate, who should we talk to first? The dataset has demographics, income,
> monthly spend, and a subscription flag — but, importantly, **no usage data**: no logins,
> no reads, no churn labels. So everything I show is built from customer profiles."
>
> **[0:30–1:15 — the method]**
> "I ran exploratory analysis first. The three signals that relate most to subscription are
> **children at home, r = 0.46; monthly spend, r = 0.42; and income, r = 0.29**. I checked
> those inputs against each other for redundancy — no pair exceeded the 0.8 collinearity
> threshold — then combined them into one **0-to-100 Subscriber Propensity Score**: 40% of
> the weight on children, 35% on spend, 25% on income, each min-max normalised first so
> dollars and child counts are comparable. The script prints the proposed weights and
> **waits for my approval before it writes anything** — a human decision point."
>
> **[1:15–2:00 — does it work?]**
> "I cut the score into thirds: Low, Medium, High. If the score means anything, subscribers
> should concentrate at the top — and they do: **13.0%, then 25.8%, then 61.1%** — a
> monotonic rise and **4.7 times** the conversion rate between bottom and top third. One
> worked example: customer 11001 has 3 children, spends $117 a month, earns $101,141. The
> formula gives **57.84** — High tier — a subscriber — **Core Segment**. You can reproduce
> that by hand."
>
> **[2:00–2:40 — the six segments and what to do]**
> "Crossing the tier with the actual flag gives **six mutually exclusive segments**, none
> bigger than 29%. **Core Subscribers, 3,308 (20.2%)** — high income, high spend, large
> families: protect them. **High-potential Prospects, 2,103 (12.8%)** — they score like Core
> but haven't subscribed: income $103,736 against Core's $107,799, so affordability isn't the
> barrier — run premium trials and job-targeted campaigns. **Low-fit Subscribers, 699 (4.3%)**
> — they subscribe despite bottom-third scores, 96% childless, spending $51 a month: they are
> the real retention risk, so lock their pricing. **Low-priority, 4,712 (28.7%)**: minimal
> spend. The mid-tier groups are upsell pools."
>
> **[2:40–3:00 — the dashboard and honesty]**
> "All of it runs in a Streamlit dashboard: filters for state, job, education, age and
> segment update every KPI live; there's a customer lookup that returns anyone's score, tier
> and inputs; and a Methodology tab showing the exact formulas. And the honest limits: this
> is **association, not causation** — no behaviour data exists, the weights were set by
> judgement rather than fitted on held-out data, and the tier validation is in-sample. The
> next step is behaviour logging and a fitted, validated model. Thank you."

### I.2 The 1-minute script

> "I scored 16,404 customers from 0 to 100 on how likely they are to subscribe, using the
> three features that actually correlate with the flag — children at home (r 0.46), monthly
> spend (r 0.42), and income (r 0.29) — weighted 40/35/25 and min-max normalised. The score
> works: subscriber rates rise monotonically from 13.0% in the bottom third, to 25.8%, to
> 61.1% in the top third — 4.7 times the lift. Crossing that tier with the real subscription
> flag gives six segments, none larger than 29%: protect the 3,308 Core Subscribers, convert
> the 2,103 High-potential Prospects who already earn $104K but haven't subscribed, and watch
> the 699 Low-fit Subscribers who subscribe despite profiles that predict they shouldn't.
> Everything is in a Streamlit dashboard with live filters, per-customer lookup, and the full
> methodology. The honest caveat: there is no usage data, so this measures association, not
> causation, and the weights are judgement-based, not fitted on held-out data."

### I.3 Likely questions and verified answers

**Q: Why put the biggest weight on children at home? Isn't that a strange predictor?**
A: Because in *this* data it has the strongest association with the flag (r = 0.4564,
beating spend at 0.4218). It's a proxy for household use — a family at home is a plausible
multi-user audience for eBooks. We report the correlation, not a belief, and we say clearly
that association ≠ causation.

**Q: Is this machine learning?**
A: It's a transparent weighted index, not a fitted model. No algorithm learned these weights;
we set them from correlation magnitudes, and a human approves them interactively. The
trade-off: we gain explainability (anyone can recompute a score by hand) and lose the
accuracy tuning a fitted model would give. Fitting a logistic regression with a train/test
split is the listed next step.

**Q: How do you know the score is any good?**
A: Tier validation: subscriber rate rises 13.0% → 25.8% → 61.1% across score thirds, a 4.7×
lift, and the score never sees the flag as an input. Honest limit: that check is in-sample.

**Q: Why terciles — why not fixed thresholds?**
A: Terciles split *this* customer base into equal thirds, so every tier is big enough to act
on and the ranking is internal to the dataset. Fixed thresholds would need an external
benchmark we don't have.

**Q: Isn't it circular — High tier predicts subscribing, and segments use the flag?**
A: The score uses only children, spend, income — never the flag. The flag enters only when
building segments (tier × flag). So High-potential Prospects are genuinely "profile says yes,
flag says no".

**Q: Why not logistic regression / a classifier?**
A: Time and transparency for a first version, plus no hyperparameters to tune on a course
dataset. The limitation and the upgrade path are both documented.

**Q: Where did the data come from?**
A: It came with the course materials alongside the project report. Exact provenance is not
verified — I treat it as a provided practice dataset.

**Q: You removed 115 rows — did that bias anything?**
A: They were duplicate Customer IDs, keeping the first occurrence — a standard dedup, not a
selection. It takes 16,519 rows to 16,404. Note: the dedup happens at the segmentation
stage, so scored.csv still has 16,519 rows.

**Q: What's the business takeaway in one line?**
A: Treat the 3,308 Core Subscribers as the base to protect, target the 2,103 High-potential
Prospects for conversion (their income matches Core — the gap is spend), and hold pricing for
the 699 Low-fit Subscribers whose loyalty the data can't explain.

**Q: What's the biggest weakness?**
A: No behaviour data at all, so segments are profile-based; and the weights are
judgement-based and validated only in-sample. Both are stated in the dashboard itself.

**Q: What would you do next?**
A: Fix reproducibility first (commit the missing cleaning script, add a build log), then
collect usage data, then fit and validate a model with a held-out test set.

---

*Verification basis: raw CSV, `data/processed/*.csv`, `src/*.py`, `outputs/*.md`,
`outputs/charts/`, `outputs/pivots/`, git history, and direct pandas computations run on
2026-10-10. Unverified items are explicitly labeled above.*
