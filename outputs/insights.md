# Insights: eBook Subscriber Propensity Analysis

All figures below are drawn from `outputs/` (charts, takeaways, methodology, pivots) and
`data/processed/` (clean.csv, scored.csv, segmented.csv; 16,404 unique customers after
removing 115 duplicate Customer IDs from the original 16,519 rows).

---

## (a) The High-Value Subscriber Profile

**Who is the ideal subscriber in this dataset? The "Core Subscribers" segment — flag = 1 and
Top-tercile score — 3,308 customers, 20.2% of the base.**

In plain language: a Core Subscriber is a 1960s-born professional living in California with a
Bachelors degree, earning well above average, spending heavily each month, and raising a
large family at home.

The numbers behind the profile:

- **Money**: mean annual income **$107,799** (median $110,866) versus the dataset mean of
  $78,129 — about **$29,670 richer** than average. Mean average monthly spend **$105.6**
  (median $99) versus the dataset mean of $72.4 — **46% more** than average, and well above
  the 75th percentile of $84.
- **Family**: mean **3.1 children at home**; **42% (1,393 of 3,308)** have 4 or more children.
  Children at home is the single strongest correlate of subscription in the dataset
  (r = 0.456): subscriber rates climb from **19.4%** for customers with no children at home
  to **83.9%** for those with five.
- **Career and education**: **71% (2,340 of 3,308)** are Professional or Management.
  Professionally employed customers subscribe at **44.3%**, versus 23.7% for Manual and
  Clerical workers. Bachelors degree holders show the highest uptake of any education level
  at **39.3%**.
- **Age and geography**: **58% (1,906 of 3,308)** were born 1960–1969 — the strongest cohort
  overall, subscribing at **51.6%** versus 33.2% for the full base. California is the top
  state by count.
- **Score**: mean Subscriber Propensity Score **57.1** (segment range 29.2–97.7). Validation:
  subscription rates rise monotonically across score terciles — **Low tier 13.0%, Medium tier
  25.8%, High tier 61.1%**.

In short: the high-value subscriber is a high-income, high-spend, large-household,
college-educated professional in their late 40s–50s. Every one of the three score inputs
(income, spend, children) sits well above its dataset average for this segment.

---

## (b) Recommendations

### Retention recommendations for Low-fit Subscribers (699 customers, 4.3%)

Low-fit Subscribers are flag = 1 but score in the bottom tercile: mean score **12.4**
(range 3.5–16.7). They subscribe despite a profile that predicts non-subscription — the
segment most at risk of unexplained churn, because the factors we can see do not explain
why they stay.

1. **Protect them with grandfathered/loyalty pricing — they are the most price-exposed
   subscribers we have.** Finding: their mean monthly spend is **$51.1**, which sits below
   the dataset's bottom quartile ($52) and is **$54.5 less** than Core Subscribers' $105.6;
   their mean income is **$50,397**, a **$57,401 gap** versus Core Subscribers. Any price
   increase hits this group's affordability hardest, so hold their current rates and offer
   annual lock-ins at the entry price.
2. **Lead with household-independent value messaging, not family-oriented offers.**
   Finding: **96% (669 of 699) have zero children at home**, and children at home is the
   score's top-weighted input (weight 0.40, r = 0.456) — their low score is driven almost
   entirely by family structure. Marketing that assumes household or family use (the pattern
   that works for Core Subscribers, 42% of whom have 4+ children) will miss them; instead
   emphasise individual, commute-length, or solo-reading value at their $51 price point.
3. **Prioritise the 1970–1979 subgroup for retention monitoring.** Finding: **360 of 699
   (52%)** of Low-fit Subscribers were born 1970–1979 — and this cohort's overall subscriber
   rate is only **26.4%**, below the 33.2% base rate. They are the largest concentration of
   low-propensity subscribers and belong to a below-average-uptake cohort, so churn outreach
   for this segment should start here rather than spreading effort evenly.

### Conversion recommendations for High-potential Prospects (2,103 customers, 12.8%)

High-potential Prospects are flag = 0 but score in the top tercile: mean score **44.5**
(range 29.2–98.4). They look like subscribers in every measurable way except that they have
not subscribed.

1. **Run an occupation-targeted conversion campaign — their professional peers already
   subscribe at above-average rates.** Finding: **1,494 of 2,103 (71%)** are Professional or
   Management, occupations that subscribe at **44.3%** and **37.4%** respectively, both above
   the 33.2% base rate; 912 are Professional, the single largest occupational cell in the
   segment. Occupational peer proof and role-relevant offers target the group most likely to
   convert.
2. **Push premium trials rather than discounts — affordability is not the barrier.**
   Finding: their mean income is **$103,736**, only **$4,063 below** Core Subscribers, yet
   their mean spend is **$91.4**, a **$14.3 gap** versus Core Subscribers' $105.6. The income
   is already there; the spend step-up is not. Trial periods and bundle upgrades that move
   them from $91 toward $106 close the widest gap between this segment and Core status.
3. **Target the 55+ high-income block explicitly.** Finding: **1,078 of 2,103 (51%)** were
   born 1910–1949 or 1950–1959 — cohorts whose subscriber rates are just **13.3%** and
   **28.8%**, the two lowest of any age group, despite this segment's $103,736 mean income.
   This is the largest under-subscribed, high-affordability pool in the data: half of all
   High-potential Prospects belong to age groups that are least represented among current
   subscribers.

---

## (c) Limitations

1. **No usage metrics exist in the source dataset.** The dataset contains demographics,
   address, income, spend and the subscription flag only. There are no reads, sessions,
   logins, page-navigation or content-consumption events of the kind the literature (e.g.,
   Theme 2 and Theme 4 studies using reading logs) relies on. Engagement and churn-behaviour
   cannot be observed or modelled directly — only inferred from proxies.
2. **Segments are profile-based, not behaviour-based.** The six segments are built from
   demographic and spend fields combined with the subscription flag. "Core" versus
   "High-potential" is distinguished by the flag alone, not by any difference in how the two
   groups use the service. We cannot say whether a High-potential Prospect would behave like
   a Core Subscriber after converting — only that they resemble one demographically.
3. **The score reflects association, not causation.** The Subscriber Propensity Score is a
   weighted sum of three correlates (children at home r = 0.456, monthly spend r = 0.422,
   income r = 0.287). It shows that these variables travel together with subscription status;
   it does not show that raising a customer's spend or income would cause them to subscribe,
   nor that any recommendation in section (b) will produce the predicted effect. The weights
   were assigned from correlation magnitudes by judgement, not fitted or validated on held-out
   data, and the tercile tiers are relative to this dataset only.
4. **Minor data caveats.** The original file had 115 duplicate Customer IDs (removed,
   16,519 → 16,404 rows); Title is 99.5% missing and Street Address2 is 98.3% missing, so
   neither was used; two-digit birth years required century inference; and City-ZipCode-State
   is a single concatenated field, so state extraction depends on its hyphen format.

---

## (d) Mapping of Findings to Report Literature Themes

| Report theme | This analysis's corresponding finding |
|---|---|
| **Segmentation** (Theme 3: "subscribers are not a uniform population"; Majid et al. 2019; Foasberg 2011) | The six-segment scheme operationalises multi-variable segmentation: the same base splits into 20.2% Core, 4.3% Low-fit, 12.8% High-potential, 28.7% Low-priority and 34.0% mid-tier — no segment exceeds 60%. Subscriber rates vary sharply by every profile dimension tested (children: 19.4% → 83.9%; occupation: 23.7% → 44.3%; age cohort: 13.3% → 51.6%), empirically confirming that the subscriber population is not uniform and that single-average strategies would misfire. |
| **Segment-specific strategies** (Theme 3's argument that what drives one reader's engagement can be reversed for another) | The Low-fit and High-potential recommendations in section (b) are deliberately opposed: retention for Low-fit hinges on price protection ($51.1 spend, $50,397 income, 96% childless) and household-independent messaging, while conversion for High-potential hinges on premium trials and peer-proof targeting (71% Professional/Management, $103,736 income). Identical treatment of the two segments — both large, one a retention risk, one a conversion pool — would waste effort in opposite directions. |
| **Personalization** (Theme 5: personalized recommendations; Zielnicki et al. 2025's ~12% engagement drop without personalization; Hennig-Thurau et al. 2010 on channel-fit) | The per-customer Subscriber Propensity Score (0–100) plus the Segment label provide the individual-level inputs personalization requires; the dashboard's customer lookup returns score, tier, segment and inputs for any Customer ID, enabling one-to-one rather than segment-average decisions. The score-tier validation (13.0% / 25.8% / 61.1%) shows tiers are precise enough to calibrate offer intensity by individual propensity. |
| **EDA as precursor** (Theme 4: explore the data before modelling) | The project followed the literature's sequence — correlation and collinearity checks first (no predictor pair |r| > 0.8; Total Children excluded in favour of Children At Home to avoid double-counting), then score, then segmentation — so weights were chosen from observed evidence rather than assumption. |
| **Behavioural signals unavailable** (Theme 2: churn prediction from consumption patterns) | The report's Theme 2 research relies on login frequency, session duration and content-consumption depletion signals; none exist here (see Limitations). Our profile-based score is the closest possible proxy, and this gap should be stated explicitly wherever churn claims are made — the dashboard footer note serves this purpose. |
