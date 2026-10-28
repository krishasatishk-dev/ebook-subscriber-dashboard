# Phase 2 Cheatsheet — Engagement (v2)

## The project in 5 lines
1. Phase 2 adds usage data: 5,500 engagement rows joined to the subscriber file on Customer ID → 5,455 unique subscribers, every one matching a flag=1 record.
2. We cleaned it with approved rules (45 exact duplicates removed, 23 genre spellings collapsed to 8, impossible values blanked then median-filled with an Imputed flag; recency never imputed).
3. Each subscriber gets an **Active / Inactive / Churned / Unclassified** status from approved recency thresholds, and a 0-100 **engagement score** from approved weights.
4. Scores sort into **Low / Medium / High** tiers by terciles; everything is compared against two independent checks (books, tenure) that are not score inputs.
5. Every result is an association in a synthetic dataset — no causation, no retention curve (no cancellation dates).

## Key numbers
- Engagement file: 5,500 rows → **5,455 unique subscribers** (45 exact duplicates dropped); 0 unmatched IDs.
- Classified: **5,422** = Active **3,001 (55.3%)** · Inactive **1,520 (28.0%)** · Churned **901 (16.6%)**; plus **33 Unclassified**.
- Median days since activity: Active **5** · Inactive **58** · Churned **152**.
- Mean logins / session minutes by status: Active **11.69 / 29.14** · Inactive **3.31 / 20.12** · Churned **1.54 / 14.15**.
- High-value (Active + High tier): **1,803** vs Churned **901** — income **$99,810 vs $90,337**, spend **$94.1 vs $83.5**, age **62.2 vs 63.8**, children **2.1 vs 1.7** (all p<0.0056, but small: d 0.20-0.33, V≤0.09).
- Independent checks by tier: Books **4.1 → 9.1 → 20.2** and Tenure **16.7 → 19.9 → 20.6 months** (Low → High).
- Null findings: genre Active rates span only **52.0-58.0%** (Fantasy p≈0.037 fails Bonferroni 0.0056); churned rate by tenure band is non-monotone (**16.5 / 22.4 / 16.5 / 12.1 / 12.0%**).

## Final weights (approved 23 Oct 2026)
| Input | Weight | Rationale |
|---|---|---|
| Days Since Last Activity, **inverted** (1 − min-max scaled) | **0.40** | Most direct sign a subscription is still in use — fresh activity scores high, long silence scores low. |
| Avg Logins Per Month | **0.35** | Direct measure of habit; just under recency because it averages months rather than showing right now. |
| Avg Session Minutes | **0.25** | Adds depth beyond visit counts but is the noisiest input (r≈0.37 with logins). |
| Books Accessed | **0.00 (excluded)** | r=0.88 with logins — both would count usage frequency twice; kept descriptive only. |

Score = weighted sum of the 0-1 inputs × 100. Unclassified rows use logins + session only with those two weights renormalised.

## Exact status rules (approved) with sizes
| Status | Rule | Size |
|---|---|---|
| **Active** | Days Since Last Activity ≤ 30 **AND** Avg Logins ≥ 1 ("one monthly cycle") | 3,001 |
| **Inactive** | Everything between: 31-90 days, or ≤30 days with 0 logins | 1,520 |
| **Churned** | Days Since Last Activity > 90 ("three cycles, a sustained lapse") | 901 |
| **Unclassified** | Recency missing/invalid — "recency decides the segment and I will not guess it" | 33 |

## Tier cut points (terciles on classified rows)
**Low ≤ 40.80 < Medium ≤ 51.25 < High** — sizes among classified: 1,810 / 1,806 / 1,806.
All 901 Churned sit in the Low tier; Unclassified (scored separately) split 32 Low / 0 / 1 High.

## The 5 questions you are most likely to be asked

1. **"Why these three inputs and these weights? Why not books?"**
   Recency 0.40 / logins 0.35 / session 0.25, each approved in writing before running with a one-line rationale; books is excluded because it correlates 0.88 with logins and would double-count usage frequency — it stays in as a descriptive metric instead.

2. **"Doesn't the score just re-say the status? How is that validation?"**
   Partly yes, by construction: recency defines status and carries 40% of the score, and logins/session are score inputs. The real checks are the inputs the score never saw — books rises 4.1→20.2 and tenure 16.7→20.6 months from Low to High tier.

3. **"Which genre or tenure group should we target?"**
   Neither: genre barely moves with status (6-point band, Fantasy fails the Bonferroni 0.0056 bar) and tenure's churn pattern is non-monotone and cross-sectional with no cancellation dates. No recommendation rests on them.

4. **"Is this a retention analysis?"**
   No — one snapshot of different people; no cancellation dates, so no cohort retention curve is possible. The tenure view is labelled cross-sectional everywhere it appears.

5. **"Why are 33 rows Unclassified — why not fill in the missing recency?"**
   Recency decides status, so we never guess it (approved rule). They are excluded from tier/status charts, reported separately (32/0/1 tiers) and scored only from logins + session with renormalised weights.
