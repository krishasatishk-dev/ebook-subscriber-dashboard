# v2 Engagement Methodology — APPROVED (23 Oct 2026)

Cleaning rules C1–C10 and the Active/Inactive/Churned thresholds below were proposed here first
and approved by Tridha on 23 Oct 2026, including the exact rationales quoted in section 2.
These are the only rules the v2 pipeline may apply.

Data: `data/raw/eBook_Engagement.csv` (5,500 rows, 7 columns, copied unmodified — raw is never edited).

---

## 1. Cleaning rules (proposed)

| # | Rule | Why (one line) |
|---|------|----------------|
| C1 | Drop 45 exact duplicate rows, keep first → 5,455 unique IDs | Same rule as v1 segment dedupe; duplicates would double-count behaviour. |
| C2 | Genre → trim, lowercase, canonical-map to exactly 8 genres: Business, Fantasy, Fiction, Mystery, Non Fiction, Romance, Sci-Fi, Self Help (26 raw spelling variants (23 after trimming spaces and ignoring case) collapse to these 8 genres) | Case/hyphen variants are the same genre; keeping 26 would split every genre stat. |
| C3 | Genre missing (54 rows) → label "Unknown", keep the row | A missing label doesn't invalidate the behaviour numbers; dropping them loses real subscribers. |
| C4 | Days Since Last Activity negative (6 rows, −24 to −2) → treat as invalid, set to missing | A negative "days since" is a date error; inventing a value would be synthetic data. |
| C5 | Days Since Last Activity missing or invalid (27 + 6 = 33 rows) → status "Unclassified", excluded from Active/Inactive/Churned counts | No recency means no honest way to place the row in any of the three buckets. |
| C6 | Implausible values — Avg Logins > 60 (7 rows, up to 860), Avg Session Minutes > 180 (8 rows, up to 912), Books Accessed > 60 (7 rows, up to 86) → set to missing, count logged | A month has 30 days/1,440 minutes; numbers this high are decimal-shift errors, not behaviour. |
| C7 | Avg Logins = 0 (416 unique rows) → keep as genuine zeros | Genuinely logged-in-nothing subscribers are exactly who "Inactive" should catch. |
| C8 | Days Since Last Activity > 365 (11 rows, several exactly 400) → keep as-is | Looks like a capture cap at 400; they are still clearly the least-recent group either way. |
| C9 | Remaining missing values (Avg Session Minutes 81, Books Accessed 43) → leave empty, exclude from any average, no imputation | Averaging only real observations keeps every reported number traceable to the raw file. |
| C10 | Join to `data/processed/clean.csv` on Customer ID, subscribers only (flag = 1) | Engagement file covers only subscribers; the join reattaches profile/score columns. |

## 2. Active / Inactive / Churned thresholds — APPROVED 23 Oct 2026

Computed only from these definitions. Rationales in quotes are the approver's own words.

| Status | Rule | Why |
|--------|------|-----|
| **Active** | Days Since Last Activity ≤ 30 **AND** Avg Logins Per Month ≥ 1 | "30 days = one monthly subscription cycle, so someone who has not opened the app in a full cycle is not currently active; the ≥1 login/month condition is a data-consistency guard for rows with recent activity but zero average logins." |
| **Inactive** | 31-90 days since last activity, OR 30 days or fewer with fewer than 1 login per month (in practice 0 logins: 10 subscribers) | Between one and three cycles — the habit has lapsed but it is not yet a sustained lapse. |
| **Churned** | Days Since Last Activity > 90 | "90 days = three cycles, a sustained lapse." |
| **Unclassified** | Days Since Last Activity missing or invalid (33 rows) | "Recency decides the segment and I will not guess it." |

Edge notes:
- A row ≤30 days with 0 logins lands in **Inactive**, not Active — the ≥1 login condition is required, not optional.
- Tenure is deliberately **not** used in the status rule — a 72-month subscriber can churn this month, and a 1-month subscriber can be active.

### Why status is not defined on the score

Status is defined on recency (plus a minimum-1-login guard), not on the score, because (1) the rules had to be written and approved before the score existed, (2) the score already contains recency at 40%, so using both would count recency twice, and (3) recency is the most direct and easily explained signal of leaving. The score is used afterwards to rank engagement and in the status-by-tier table.

**Watchlist — Active subscribers in the Low tier** (early-warning group: they are still Active today but their score says their engagement is already Low; the individual rows are saved in `outputs/v2/watchlist.csv`):

| Group | Count | Mean recency (days) | Mean logins | Mean session minutes | Mean books |
|---|---|---|---|---|---|
| Active subscribers in the Low tier (early-warning group) | 11 | 29.1 | 1.45 | 11.3 | 4.4 |


## 3. Outputs (staged)

- `data/processed/v2/engagement_clean.csv` — cleaned rows (stage 1)
- `data/processed/v2/engagement_status.csv` + `outputs/v2/status_summary.csv` — classification (stage 2)
- `src/v2_clean.py`, `src/v2_status.py` — pipeline (mirrors v1's numbered scripts)
- `outputs/v2/BUILD_LOG.md` — one plain-English note appended after every stage

## 4. Merging (stage 3 — run 23 Oct 2026)

Script: `src/v2_merge.py`. Inner join on `Customer ID`:

- **Left**: `data/processed/v2/engagement_status.csv` — cleaned engagement + Status column (stage-1 file with the stage-2 status; `engagement_clean.csv` itself has no status column).
- **Right**: `data/processed/clean.csv` (v1), de-duplicated keep-first first — the same rule v1 applied in `src/04_segment.py:27-28` — because 115 Customer IDs appear twice there and keeping both breaks one-row-per-customer.
- **Counts**: 5,455 unique engagement IDs; 16,404 unique customer IDs (16,519 raw rows); 5,455 matched; 0 unmatched on the engagement side; 10,949 unmatched on the customer side (subscribers without engagement rows — expected, the engagement file is a subset).
- **Assertions passed**: 5,455 rows out, one row per Customer ID.
- **Caveat found while merging**: of the 115 doubled customer IDs, 38 also appear in the engagement file, and their two rows are *not* exact duplicates — 6 differ in Annual Income/Avg Monthly Spend and 4 have opposite subscriber flags (same ID, different address/city, one row flag=0 and one flag=1). Keep-first picked the flag=1 variant for 34 of the 38 and the flag=0 variant for 4. Flagged for review; no rule changed.
- **Columns kept**: Birth Date + AgeGroup (clean.csv has no `Age` column), Education Level, Occupation, Gender, Marital Status, Home Owner Status, Number of Cars Owned, Number of Children At Home, Annual Income, IncomeBand, Avg Monthly Spend, State (parsed from `City-ZipCode-State` as the text after the last hyphen), plus all engagement columns and Status.
- **Output**: `data/processed/v2/merged.csv` — Active 2,995 / Inactive 1,526 / Churned 901 / Unclassified 33, unchanged by the join. *(These are the counts at merge time, before decision D1; section 5 below records the +6/−6 move, and every current file on disk contains the post-D1 counts 3,001 / 1,520 / 901 / 33.)*

## 5. Decisions taken 23 Oct 2026 (approved)

### D1 — Median-fill for behaviour columns (amends C9)
- **Rule**: blank Avg Logins Per Month, Avg Session Minutes and Books Accessed are filled with that column's median — medians used: **logins 6.00, session 21.80, books 9.00** (5,455-row cleaned file; covers original blanks 7/81/43 plus C6-blanked outliers 7/8/7; 7+89+50 fills, 144 rows touched, none double-counted across columns). An `Imputed` flag column (1/0) marks every row where at least one value was filled.
- **Why**: "Median-fill keeps every subscriber in behaviour summaries using a real observed value from the same column, instead of dropping them or inventing an extreme number."
- **Not imputed**: Days Since Last Activity — blank/invalid recency stays blank, those 33 rows stay **Unclassified**. Why: "Recency decides Active/Inactive/Churned and I will not guess it."
- Effect on status: 6 rows moved Inactive→Active (blank-login rows with recent activity now carry the login median of 6 ≥ 1). New counts: **Active 3,001 / Inactive 1,520 / Churned 901 / Unclassified 33**.

### D2 — Duplicate Customer IDs: prefer the subscriber record (amends §4 dedupe note)
- **Rule**: when one Customer ID has two records in `clean.csv`, keep the flag=1 record; if the flags are equal, keep the first (v1's rule, `src/04_segment.py:27-28`).
- **Counts**: 115 doubled IDs overall; **4 differ specifically on the subscriber flag** (same ID, opposite flag). 38 of the 115 also appear in the engagement file — my earlier "38 conflicting" counted every doubled engagement ID whose two rows differ in *any* column (city, address, income…), not just the flag; the flag-specific count is 4, matching the raw-file count.
- **Why**: "The engagement file contains subscribers only, so when two records disagree, the flag=1 record is the one that matches reality; equal flags keep v1's first-record rule."
- **Confirmation**: after the merge, **all 5,455 of 5,455** engagement IDs matched a flag=1 subscriber record (asserted in `src/v2_merge.py`).

## 6. Standing rules (v2)

1. Never modify anything in `data/raw/`.
2. Never add synthetic or random data.
3. Every weight or threshold is defined in this file **before** it runs, each with a one-line rationale.
4. You approve before the pipeline runs; I do not pick thresholds on my own.
5. Review-1 outputs and code are untouched; v2 lives only under `outputs/v2/`, `data/processed/v2/`, `src/v2_*.py`.

## 7. Engagement score — APPROVED WEIGHTS

Inputs min-max normalised to 0-1 on the classified population (rows with valid recency); recency inverted as `1 - scaled` so fresh activity scores high; weighted sum x 100; tiers by terciles (Low <= 40.80 < Medium <= 51.25 < High).

| Input | Weight | Why |
|---|---|---|
| Days Since Last Activity (inverted) | 0.40 | How recently someone last showed up is the clearest sign a subscription is still in use, so it carries the largest share. |
| Avg Logins Per Month | 0.35 | Login frequency is the direct measure of habit — just under recency because it averages across months rather than showing right now. |
| Avg Session Minutes | 0.25 | Time spent adds depth beyond visit counts but is the noisiest input (r=0.38 with logins), so it gets the smallest share. |
| Books Accessed | 0.00 (excluded) | r=0.88 with logins (0.90 before imputation) — would double-count usage frequency; descriptive only |

Unclassified rows (33): scored from logins+session only with those weights renormalised, reported separately.

Construction-overlap warning: status is defined on recency, so tier-vs-status agreement is partly by construction, not independent validation.

**Validity note (§7).** Tier-by-status agreement and tier differences in logins and session minutes are partly by construction: recency defines status and carries 40% of the score, and logins and session minutes are score inputs. Books Accessed and Subscription Tenure are NOT score inputs, so they are the independent checks. Unclassified rows are excluded from tier-based charts and tables and shown separately.

### Why status is not defined on the score

Status is defined on recency (plus a minimum-1-login guard), not on the score, because (1) the rules had to be written and approved before the score existed, (2) the score already contains recency at 40%, so using both would count recency twice, and (3) recency is the most direct and easily explained signal of leaving. The score is used afterwards to rank engagement and in the status-by-tier table.

**Status x tier (subscribers; computed from `data/processed/v2/scored.csv`):**

| Status | Low | Medium | High | Total |
|---|---|---|---|---|
| Active | 11 | 1187 | 1803 | 3001 |
| Inactive | 898 | 619 | 3 | 1520 |
| Churned | 901 | 0 | 0 | 901 |
| Unclassified | 32 | 0 | 1 | 33 |

### Tier cutoffs — why terciles

Tiers use terciles of the engagement score (Low up to the lower cut (40.80), Medium up to the upper cut (51.25), High above). Reasons: fixed numbers such as 33/66 would be arbitrary; equal-sized thirds guarantee no lopsided tier; cutoffs come from the data rather than numbers we chose. Limitation: tiers are relative to this subscriber population, not absolute standards.

**Behaviour by tier chart** — `outputs/v2/charts/bar_behaviour_by_tier.png` (four panels: mean recency, logins, session minutes, books by tier, Unclassified excluded). Caption: books and tenure are independent of the score while recency, logins and session minutes are score inputs, so the gradient in those three is partly by construction.


## 8. Segment views and significance checks (23 Oct 2026)

- **Age** in the high-value profile: `data/processed/clean.csv` has no literal Age column, so Age is derived once from its Birth Date at reference date **2026-10-02** (the date specified for the report) and reused by every segment output so all charts, tables and printed numbers agree.
- **`outputs/v2/significance_checks.csv`** — High-value (Active+High, n=1,803) vs Churned (n=901): numeric rows (Annual Income, Avg Monthly Spend, Age, Children At Home) carry both means, the difference, Welch t-test p-value and Cohen's d; categorical rows (Management, Graduate Degree, AgeGroup 1960-1969, Fantasy) carry both shares, difference in percentage points and chi-square p-value with Cramér's V.
- **Reading rule** (also written as the CSV's note row): with these sample sizes small gaps can be significant while still being practically small — read the effect size (d/V: 0.2 small, 0.5 medium, 0.8 large), not just the p-value. Current result: income/spend/children are small effects (d 0.22-0.33), age borderline small (d -0.20), and all four category gaps negligible (V <= 0.09) despite p < 0.05.
