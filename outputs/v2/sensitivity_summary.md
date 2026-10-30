# Engagement-score sensitivity — do the tiers depend on the weights?

Recomputed the 0-100 engagement score on the **5,422 classified subscribers** (the 33 Unclassified rows are excluded throughout, as they were from the tercile basis).
Inputs are min-max normalised exactly as `src/v2_score.py` does and are held fixed; only the weights change, with recency always entered inverted. Tiers are re-cut from each set's own terciles.

## Sanity check — baseline reproduces the shipped tiers

- Tercile cuts recomputed: Low <= 40.80 < Medium <= 51.25 < High (methodology.md records 40.80 / 51.25).
- Max |recomputed - shipped| engagement score: 0.0000 (rows off by more than 0.01: 0).
- **Tier mismatches vs the `Tier` column in scored.csv: 0 of 5,422 (0.00%).**
- The baseline therefore reproduces the shipped Tier column exactly, so every comparison below is against a verified baseline.

## Status is unaffected

Status is defined on Days Since Last Activity (<= 30 days AND >= 1 login -> Active; > 90 days -> Churned; else Inactive) and reads no score term, so reweighting cannot move anyone between Active / Inactive / Churned. Counts held constant throughout: **Active 3,001**, **Inactive 1,520**, **Churned 901** (total 5,422).

## Alternatives vs baseline (weights: recency / logins / sessions)

| Set | Weights | Same tier | Spearman rho | Moved >1 tier | Active in Low |
|---|---|---|---|---|---|
| baseline | 0.40 / 0.35 / 0.25 | 100.0% | 1.000 | 0 | 11 |
| equal | 0.33 / 0.33 / 0.33 | 95.4% | 0.997 | 0 | 21 |
| recency_light | 0.25 / 0.45 / 0.30 | 95.6% | 0.997 | 0 | 29 |
| recency_heavy | 0.50 / 0.30 / 0.20 | 96.6% | 0.999 | 0 | 2 |

### equal — recency 0.33 / logins 0.33 / sessions 0.33

- Same tier as baseline: **95.4%**
- Spearman rank correlation of scores: **0.9967**
- Moved more than one tier: **0** (0.0%)
- Active subscribers in the Low tier: **21** (baseline 11)

Tier migration (rows = baseline tier, columns = this set):

| baseline \ equal | Low | Medium | High |
|---|---|---|---|
| Low | 1761 | 49 | 0 |
| Medium | 48 | 1683 | 75 |
| High | 0 | 75 | 1731 |

Interpretation: Moving weight toward logins and sessions (recency 0.33) leaves the ranking essentially intact — Spearman rho = 0.997 — and re-sorts only 4.6% of subscribers (247 of 5,422), with 0 moving more than one tier, so the three tiers as a whole are robust to this change. The Active-in-Low early-warning watchlist, however, grows from 11 to 21 (+10, +91%) — so although the tiers barely move, the group the project flags as 'still Active but already Low-engagement' is not stable and should not be quoted as a fixed number.

### recency_light — recency 0.25 / logins 0.45 / sessions 0.30

- Same tier as baseline: **95.6%**
- Spearman rank correlation of scores: **0.9967**
- Moved more than one tier: **0** (0.0%)
- Active subscribers in the Low tier: **29** (baseline 11)

Tier migration (rows = baseline tier, columns = this set):

| baseline \ recency_light | Low | Medium | High |
|---|---|---|---|
| Low | 1742 | 68 | 0 |
| Medium | 66 | 1689 | 51 |
| High | 0 | 51 | 1755 |

Interpretation: Moving weight toward logins and sessions (recency 0.25) leaves the ranking essentially intact — Spearman rho = 0.997 — and re-sorts only 4.4% of subscribers (236 of 5,422), with 0 moving more than one tier, so the three tiers as a whole are robust to this change. The Active-in-Low early-warning watchlist, however, grows from 11 to 29 (+18, +164%) — so although the tiers barely move, the group the project flags as 'still Active but already Low-engagement' is not stable and should not be quoted as a fixed number.

### recency_heavy — recency 0.50 / logins 0.30 / sessions 0.20

- Same tier as baseline: **96.6%**
- Spearman rank correlation of scores: **0.9986**
- Moved more than one tier: **0** (0.0%)
- Active subscribers in the Low tier: **2** (baseline 11)

Tier migration (rows = baseline tier, columns = this set):

| baseline \ recency_heavy | Low | Medium | High |
|---|---|---|---|
| Low | 1751 | 59 | 0 |
| Medium | 60 | 1715 | 31 |
| High | 0 | 32 | 1774 |

Interpretation: Moving weight toward recency (recency 0.50) leaves the ranking essentially intact — Spearman rho = 0.999 — and re-sorts only 3.4% of subscribers (182 of 5,422), with 0 moving more than one tier, so the three tiers as a whole are robust to this change. The Active-in-Low early-warning watchlist, however, shrinks from 11 to 2 (-9, -82%) — so although the tiers barely move, the group the project flags as 'still Active but already Low-engagement' is not stable and should not be quoted as a fixed number.

## Bottom line

Per-subscriber scores and tiers for every set are in `outputs/v2/sensitivity.csv` (`tier_move_*` is +1 for moved up, -1 for moved down, 0 for unchanged). Status is carried through untouched.
