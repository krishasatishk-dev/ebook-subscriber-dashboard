## Scoring model

Subscriber Propensity Score (SPS) computed as a weighted min-max-normalised sum of three predictors:

1. **Number of Children At Home** (min-max normalised to [0,1]) × weight 0.40
2. **Avg Monthly Spend** (min-max normalised to [0,1]) × weight 0.35
3. **Annual Income** (min-max normalised to [0,1]) × weight 0.25

Normalisation formula:  x_norm = (x - min(x)) / (max(x) - min(x))

Final SPS = (w1 × x1_norm + w2 × x2_norm + w3 × x3_norm) × 100, yielding a 0–100 scale.

Weights were chosen based on absolute Pearson correlation with the eBook Subscriber Flag:
Children At Home (0.456) > Avg Monthly Spend (0.422) > Annual Income (0.287). No selected pair
has |r| > 0.8, so no collinearity penalty is applied. The weights sum to 1.0 and reflect the
relative predictive strength of each variable while avoiding double-counting correlated children
measures (e.g., Total Number of Children was excluded in favour of Children At Home).

## Segment Definitions

The dataset is partitioned into six mutually exclusive segments by combining the 'Subscriber Propensity Score' tier (Low/Medium/High) with the actual eBook Subscriber Flag (0/1).

The dataset is partitioned into six mutually exclusive segments by combining the 'Subscriber Propensity Score' tier (Low/Medium/High) with the actual eBook Subscriber Flag (0/1).

1. **Core Subscribers**   : Flag = 1 AND Tier = High
   → Customers who both subscribe and score in the top tercile.

2. **Low-fit Subscribers** : Flag = 1 AND Tier = Low
   → Customers who subscribe but have a low propensity score (possible under‑scorers or legacy accounts).

3. **High-potential Prospects** : Flag = 0 AND Tier = High
   → Non‑subscribers with a high propensity score (good targets for conversion campaigns).

4. **Low-priority** : Flag = 0 AND Tier = Low
   → Non‑subscribers with a low propensity score (low‑value targets).

5. **Mid-tier Subscribers** : Flag = 1 AND Tier = Medium
   → Subscribers in the middle tercile.

6. **Mid-tier Non-subscribers** : Flag = 0 AND Tier = Medium
   → Non‑subscribers in the middle tercile.

Segments are computed in the order listed above; each row belongs to exactly one segment.
