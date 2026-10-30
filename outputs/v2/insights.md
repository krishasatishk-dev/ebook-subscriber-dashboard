# Phase 2 Insights — Engagement

Every number below comes from `outputs/v2/` (tables, significance_checks.csv, status_summary.csv)
or `data/processed/v2/` (scored.csv, merged.csv). Nothing else.

---

## Multiple-comparison caution (applies to this whole document)

The high-value comparisons ran **9 tests**; with Bonferroni correction the bar is
**0.05 / 9 ≈ 0.0056**. What clears it: Annual Income (p≈1.1e-08), Avg Monthly Spend (p≈1.6e-16),
Age (p≈1.9e-06), Children At Home (p≈4.5e-08), Management (p≈0.0041), Graduate Degree
(p≈0.0017) and AgeGroup 1960-1969 (p≈6.2e-06). What does **not** clear it: **Genre: Fantasy
(p≈0.037) — it is not presented as a finding anywhere below.**

Two summary statements that frame everything: **demographic effects are small** (Cohen's d
0.20-0.33, Cramér's V 0.05-0.09 — practically modest even when significant) and **behaviour
carries the larger separation** — with the honest caveat that the behavioural gap is **partly
by construction**, because status is defined on recency and the score carries recency at 40%.

---

## (a) The high-value subscriber profile

High-value = Active subscribers in the High score tier: **1,803 people**, compared here with
the **901 Churned**.

In plain language: the typical high-value subscriber is a somewhat **wealthier, slightly
younger, married-with-kids household reader** — earning about **$99,810** a year versus
$90,337 for churned subscribers (+10%), spending **$94.1/month versus $83.5** (+13%), with
**2.15 versus 1.74** children at home, at **62.2 versus 63.8** years of age. They are a little
more likely to work in **Management (21.5% vs 16.8%)**, hold a **Graduate Degree (18.0% vs
13.2%)** and be born in the **1960s (55.1% vs 45.8%)** — all of these survive the Bonferroni
bar.

Honesty about size: every one of these differences is **statistically solid but modest in
practice** — d between 0.20 and 0.33, V at or below 0.09 (a 9-point share gap is the largest).
The profile describes a *tendency*, not a dividing line, and everything here is an
**association, not a cause**. Fantasy (13.3% vs 10.4%) looked like a fourth category signal
but fails the corrected threshold, so it is **not** part of the profile.

---

## (b) What separates Active from Churned

**Behavioural differences (larger — but partly by construction).**
Active subscribers average **11.69 logins and 29.14 session minutes** per month; Churned
average **1.54 logins and 14.15 minutes** — a 7.6x gap in visits and a 2x gap in time. Last
activity median: **5 days (Active) versus 152 days (Churned)**. These gaps look dramatic, but
they are not independent evidence: **status is defined on recency** (Active ≤30 days, Churned
>90 days), so the recency gap is true by definition, and logins/session minutes are score
inputs, so score-based splits restate them. The near-independent part: logins and session
minutes are only a *guard* in the status rule, so their means across statuses are informative
but still expected to move with recency.

**Demographic differences (smaller — but valid independent evidence).**
Churned subscribers are modestly poorer, older and smaller-household: income −$9,473,
spend −$10.6/month, children −0.4, age +1.6 years, fewer Management and Graduate-Degree
members, fewer born in the 1960s — all surviving p<0.0056, all with small effect sizes
(d 0.20-0.33, V≤0.09). Descriptively, churned rates run highest in the **Q1 income band
(19.2%)**, **Manual work (20.9%)**, the **1910-1949 (25.3%) and 1950-1959 (20.5%) cohorts**,
and **1-child or childless households (19.7% / 18.4%)**. These demographic patterns are
consistent with the tested effects but were not themselves part of the test battery, so treat
them as supportive description, not proof.

**The independent check that behaviour means something:** Books Accessed and Subscription
Tenure are **not** score inputs, yet books rise **4.1 → 9.1 → 20.2** from Low to High tier and
tenure rises **16.7 → 19.9 → 20.6 months**. A score built from recency, logins and session
minutes still lines up with two inputs it never saw — that is the real validation.

---

## (c) Null findings: genre and tenure

**Genre does not separate statuses.** Active rates span only **52.0% (Fiction) to 58.0%
(Self Help)** and churned rates **14.4% to 19.4%** across the eight named genres (the small
Unknown group, n=54, sits at 13.0%) — bands of about six points, with genre composition
nearly identical per status (Fiction is about a fifth of every status: 18.5% of Active,
20.0% of Churned). Fantasy's apparent
edge fails the Bonferroni bar (p≈0.037 > 0.0056), so **no genre finding survives**.
*Implication:* no recommendation in this project rests on genre. The file also contains only
each subscriber's single most-read genre, so content diversity cannot even be tested.

**Tenure does not reliably separate churn.** Churned rates by band are **16.5% (0-6 mo),
22.4% (7-12), 16.5% (13-24), 12.1% (25-48), 12.0% (49+)** — non-monotone and overlapping;
there is no clean "longer tenure = safer" story for churn. One cross-sectional gradient does
show Active share rising 42.7% → 68.4% across the bands, but that is a single snapshot of
different people, not tracked customers: it was not part of the tested battery, it moves with
age and cohort, and **the data has no cancellation dates**, so it cannot be read as retention.
*Implication:* no recommendation rests on tenure, and no retention curve is claimed anywhere.

---

## (d) Recommendations

### Inactive (1,520 subscribers — 31-90 days since activity, or 30 days or fewer with fewer than 1 login a month; median 58 days: the win-back window before day 90)

1. **Trigger a re-engagement message the day a subscriber passes 30 days of silence**
   *(theme: early warning signs).* Finding: recency is the single strongest signal in the
   project (40% of the score; Active median 5 days vs Inactive median 58), and every Inactive
   subscriber is by definition inside the window — act at day 31, not day 80.
2. **Send usage-based "pick up where you left off" nudges, not generic blasts**
   *(theme: personalised recommendations).* Finding: Inactive subscribers still average
   **3.31 logins and 20.1 session minutes** — real residual habit, far above Churned
   (1.54 / 14.2) — so reminders built from their own recent reading volume and activity are
   the highest-probability conversion.
3. **Prioritise the lower-Active segments inside Inactive**
   *(themes: segment-specific strategies, relevant communication).* Finding: Active rates
   lowest in **Q1 income (51.0%)**, **1-child households (50.6%)** and the older cohorts —
   all consistent with the surviving income/children/age effects (p<0.0056, though small) —
   so effort concentrates where Inactive is thickest, with messaging matched to each group
   rather than one campaign for all.

### Churned (901 subscribers — over 90 days, median 152)

1. **Run win-back sequences keyed to declining login frequency**
   *(theme: declining login frequency).* Finding: Churned average **1.54 logins/month vs
   Active 11.69** — the decline is steep and long before day 90, so reopen contact using
   their historical reading pattern ("you used to read weekly") rather than a price offer.
2. **Flag Low-tier subscribers approaching day 90 and intervene before churn happens**
   *(theme: early warning signs).* Expected by design: all 901 Churned sit in the Low tier
   because recency is 40% of the score and also defines Churned status, so this is not an
   independent finding. The practical point stands: a Low-tier subscriber entering the
   31-90 day band is the pre-churn population to catch while still Inactive.
3. **Give higher-value churned subscribers relevant, value-based reactivation**
   *(themes: relevant communication, personalised recommendations).* Finding: churned
   subscribers still average **$90,337 income and $83.5 monthly spend**, and the income/spend
   gaps to high-value survive correction (p<0.0056, small d) — the Q5 band alone holds
   **270 churned** — so approach them with the value and quality of the reading experience
   they once used, not blanket discounts.

*(No recommendation rests on genre or tenure, per the null findings in (c).)*

---

## (e) Limitations

1. **Association, not causation.** Every relationship described here is co-movement in one
   dataset; nothing shows that acting on a factor will change status or score.
2. **No cancellation reasons — we show who leaves, not why.** The files record behaviour and
   demographics, never a reason for cancelling, so every churn statement describes when people
   stopped showing up, not what made them leave.
3. **Status is recency-based by definition.** Active/Inactive/Churned are thresholds on Days
   Since Last Activity (plus a ≥1-login guard for Active), so behavioural and score
   differences against status are partly built in — independent evidence comes only from
   inputs outside that definition (books, tenure, demographics).
4. **No cancellation dates → no true retention curves.** The tenure view is cross-sectional;
   it compares different people at one moment, never the same cohort over time.
5. **Only the single most-read genre per subscriber** is recorded, so content diversity,
   genre breadth and multi-genre reading behaviour cannot be tested at all.
6. **The dataset is synthetic**, so conclusions illustrate method on this file — they are not
   market claims about real subscribers.
7. **33 Unclassified rows** (missing or invalid recency) are never imputed for recency: they
   are excluded from tier charts and status shares, shown separately (32 Low / 0 Medium /
   1 High tier) and scored only from logins + session with renormalised weights.
