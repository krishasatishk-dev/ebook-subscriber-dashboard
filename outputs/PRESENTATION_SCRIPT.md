# PRESENTATION SCRIPT — 5 Speakers · Target 6–7 minutes (hard limit 10)

**Speaker order:** Ayana → Kasturi → Tridha → Vidushi → Krisha (Krisha closes with the live demo).
**Deck:** `outputs/eBook_Presentation.pptx` (18 slides — mapping below).
**Every number in these scripts is verified** against the project files. Say them exactly.

---

## Slide map & time plan

| # | Speaker | Slides | Time | Job |
|---|---|---|---|---|
| 1 | **Ayana** | 1–2 | ~0:50 | Hook + theory: what the problem is, in plain words |
| 2 | **Kasturi** | stays on 2 | ~0:50 | Bridge: why a prototype, how this is a business problem |
| 3 | **Tridha** | 3 | ~1:00 | The dataset — and the data we were NEVER given |
| 4 | **Vidushi** | 4–5 | ~1:00 | The plan (pipeline) + how we cleaned the data |
| 5 | **Krisha** | 6–17 fast, 18 + live app | ~2:30–3:00 | The analysis, the proof, the demo, what's missing, what's next |
| | | | **≈ 6:30–7:20** | + transitions ≈ 7 min total |

**Golden rules for ALL five speakers**
- ❌ Never say: "AI", "the model learned", "we trained it", "causes subscription".
- ✅ Always say: "weighted score/index", "correlation/association", "human-approved weights", "hand-checkable".
- If you don't know an answer: "That's a good question — from the data we have, the honest answer is X; beyond that we'd be guessing." Never invent.

**Handoff lines** (say them — smooth handoffs impress):
Ayana → Kasturi: *"So we know the question. Kasturi will tell you what we decided to build, and why."*
Kasturi → Tridha: *"But what can a prototype only as good as its data — Tridha shows what we actually received."*
Tridha → Vidushi: *"Given that, here's how we prepared the data — Vidushi?"*
Vidushi → Krisha: *"The data is ready. Now the actual analysis, and the live prototype — Krisha?"*

---

# SPEAKER 1 — AYANA  ·  slides 1–2  ·  ~0:50

*[SLIDE 1 — title up while people settle. Speak over it.]*

"Good morning, ma'am. Our project is about **eBook subscriptions** — predicting which customers will subscribe, and understanding that not all customers are the same.

Think of any subscription business — Netflix, Kindle Unlimited, anything. The company has a list of thousands of customers. Treating every one of them identically wastes money: some will never subscribe no matter what you offer, some already love the product, and — the valuable ones — **some look exactly like your best customers but haven't subscribed yet.**

So the business question is really two questions:
**One — who is most likely to subscribe?**
**Two — how should we treat each group differently?**

Two words we'll use a lot:
**'Propensity'** just means *likelihood* — how likely someone is to do something.
**'Segmentation'** means *grouping customers who share traits*, so we can act on each group with the right strategy.

*[CLICK → SLIDE 2]*

Our dataset even gives us an **answer key** — a column that says whether each person actually subscribed. That lets us work backwards: look at what real subscribers have in common, learn the pattern, and rank everyone else by how closely they match it.

That's the problem we tackled. Kasturi will now tell you what we decided to build for it."

⏱ *Keep to ~120 words per minute. Don't rush, don't read the slide.*

---

# SPEAKER 2 — KASTURI  ·  stays on slide 2  ·  ~0:50

"Thank you, Ayana. So the question is set. Now — **what did we decide to build, and why a prototype instead of just a report?**

First, how is this a **business** problem? Because every decision has a cost. A company that emails all 16,000 customers the same offer burns its budget on people who will never convert — and worse, it treats its most valuable subscribers like strangers. Money is lost in both directions: missed conversions, and unnecessary discounting of people who'd have stayed anyway. So the business needs **priorities**: who to protect, who to convert, and who to leave alone.

Second — **why a prototype, not a report?** A report answers one question, once. A prototype lets the person who actually makes decisions — a marketing manager, not a programmer — **ask their own questions**: *show me all Professionals in California… now show me this one customer's score… now download that list.* Decisions, not slides.

So what we built, in one sentence: **a working dashboard where every customer gets a 0-to-100 subscription-likelihood score, gets placed into one of six segments, and anyone can filter, look up, and see exactly how the number was calculated.**

And one promise we made to ourselves about it: it is **deliberately not a black box**. Everything — the formula, the weights, the rules — is visible inside the app itself. You will never have to take our word for a number.

But a prototype is only as good as the data it's fed — so let's look at what we actually received. Tridha?"

---

# SPEAKER 3 — TRIDHA  ·  slide 3  ·  ~1:00

*[SLIDE 3]*

"Here's our raw material. One file: **16,519 rows and 21 columns** — one row per customer record. But 115 Customer IDs are duplicated, so the real number of unique customers is **16,404**. About a third of them — **33.2%** — actually subscribed.

The columns fall into four groups: **demographics** — age, education, job, gender; **money** — annual income, average monthly spend; **household** — children at home, cars, home ownership; and the **subscription flag**: one means subscribed, zero means not.

Mean income is about **$78,000**; mean spend **$72 a month**. Two columns are almost completely empty — Title is **99.5% missing** and Street Address2 is **98.3% missing** — so they're useless and we excluded them.

Now — the important part: **what this dataset does NOT contain.**

The data we were directed to was supposed to include **login frequency, session duration, books accessed, recency, genre, and subscription tenure**. *None of those columns exist in the file.* The only subscription-related field is the 0/1 flag — which tells us **whether** someone subscribed, not whether they are **Active, Inactive, or Churned**. And the closest thing to behaviour, Average Monthly Spend — is *spend*, not engagement.

That has real consequences, and we want to be upfront: with this file we **cannot** build recency-based scoring, **cannot** classify Active/Inactive/Churned, and **cannot** draw retention curves — those all need the missing engagement columns. What we *could* build is a **profile-based** analysis — using demographics, spend, and the flag — and that's exactly what we did, within those honest limits. Krisha will return to this at the end with our plan for if and when we get that data.

So: given the data we have — Vidushi shows how we prepared it."

---

# SPEAKER 4 — VIDUSHI  ·  slides 4–5  ·  ~1:00

*[SLIDE 4]*

"We processed the data in **five steps, using Python** — pandas for data work, matplotlib for charts, and Streamlit to turn it all into the dashboard you'll see live.

**Step one, clean the data. Step two, explore it** — charts and correlation, to find which attributes actually relate to subscription. **Step three, score** every customer from 0 to 100. **Step four, validate** — does the score actually work? **Step five, segment** — group the customers — and then the dashboard sits on top of all of it.

One thing to stress: this is **statistics and arithmetic, not AI**. There is no training, no hidden model. At step three, the script even **pauses and asks a human** — *'Approve these weights? y or n'* — before it computes anything. The computer proposes; we decide.

*[CLICK → SLIDE 5]*

Step one in detail. Three problems in the raw file, three fixes:

**Duplicates** — 115 repeated Customer IDs. We keep the first occurrence of each → 16,404 unique customers.

**Birth years** — the file stores dates like `4/8/66`. Two-digit years are dangerous: 66 should be 1966, not 2066. We inferred the century — tokens 10 to 80 map to 1910 through 1980 — so every date became unambiguous, like 1966-04-08.

**Missing context columns** — we *derived* three new ones: **AgeGroup** — four birth cohorts; **IncomeBand** — income split into five equally sized groups, Q1 to Q5; and **State** — pulled out of the combined field, so 'Oakland-94601-California' gives us California.

After cleaning: 16,404 clean rows, ready for analysis. And with that — Krisha takes you through the analysis and the live prototype."

---

# SPEAKER 5 — KRISHA  ·  slides 6–18 + LIVE DEMO  ·  ~2:30–3:00

## Part A — The analysis (slides 6–17, ~1:40 — move fast, linger where marked)

*[SLIDE 6]*

"Step two: finding the signals. **Correlation** — you've seen the term — is a number from **−1 to +1** that measures how two columns move together. We measured every numeric column **against the flag** — the answer key.

Three signals stood out: **children at home, r equals 0.46** — the strongest; **monthly spend, 0.42**; **income, 0.29**. Home ownership? **0.001** — literally nothing, so we dropped it. Cars, 0.16 — too weak. We also checked the three chosen inputs *against each other* — nothing above 0.8 — so we're not counting the same fact twice.

⚠️ *If she probes here, this is your first defence: r measures association, not cause — see Q&A 1–3.*

*[CLICK → SLIDE 7 — linger]*

"Here's the strongest signal, visually. Subscriber rate by children at home: **19.4% with zero children — climbing to 83.9% with five**. A clean staircase. This is why children got the biggest weight. And we say it carefully: this is an **association** in the data — not a claim that having children *causes* anyone to buy eBooks."

*[CLICK → SLIDE 8]*

"Step three — the score. The three inputs have different units, so we **min-max normalise** each to 0-to-1, multiply by weights that follow the correlation ranking, and multiply by 100:

**Score = 0.40 × children + 0.35 × spend + 0.25 × income, normalised, times 100.**

Weights sum to 1.0 — and the script pauses for human approval before running. Result: a 0-to-100 score for every customer."

*[CLICK → SLIDE 9 — linger, this is your credibility slide]*

"Let me prove it's that simple. Customer **11001**: three children, $117 a month, income $101,141.
Children normalise to 3/5 = **0.6000**. Spend: (117−22)/(176−22) = **0.6169**. Income: (101,141−9,482)/(196,511−9,482) = **0.4900**.
Score = 0.40×0.60 + 0.35×0.617 + 0.25×0.49 × 100 = **57.84**.
Above 29.2 — so **High tier**. Flag is 1 — a subscriber. Segment: **Core Subscribers**. That is the entire 'model' — division, multiplication, addition. Next slide shows the app computing the same thing."

*[CLICK → SLIDE 10 — linger]*

"Same customer, in the live prototype's lookup tab: **57.8, High, Core Subscribers** — and the three inputs below. Identical to the hand calculation. Works for **any** of the 16,404 IDs — nothing is hard-coded. I'll do it live in two minutes."

*[CLICK → SLIDE 11]*

"Step four — does the score work? We split scores into equal thirds. Subscriber rate by tier: **Low 13.0%, Medium 25.8%, High 61.1%** — always rising, and the top third converts **4.7 times** the bottom third. And note: the score never sees the flag as an input — the flag is only used afterwards to check it. Honest limit: this validation is in-sample; a held-out test is the planned upgrade."

*[CLICK → SLIDE 12]*

"Step five — six segments. Tier **times** the real flag: six combinations, every customer in exactly one. Largest is 28.7% — well balanced. The interesting one: **High-potential Prospects** — top-tier scores, but haven't subscribed."

*[CLICK → SLIDE 13]*

"What they look like — Core: **$108K income, $106 a month, 3.1 kids** → protect them. Prospects: earn almost the same — **$104K** — but spend $91, not $106 → the barrier isn't money, so: **convert with trials, not discounts**. Low-fit Subscribers: they *do* subscribe, yet score bottom-third — **96% have no children** — we can't explain their loyalty, so we **protect their pricing**. That's the analysis. Now — the proof that it all works."

## Part B — Live demo (slide 18 → browser, ~1:10)

*[CLICK → SLIDE 18, then switch to the browser — the app is already open at localhost:8501]*

"This is the live prototype.

*[Intro page]* — banner, one button, nothing to read — in.

*[Dashboard]* — top row: **16,404 customers, 33.2% subscriber rate, average score 28.6**. Five tabs below.

*[Tab ④ — Customer Lookup]* — ma'am, **name any Customer ID and I'll look it up**. *(Backup: type 11001.)* There: **57.8, High tier, Core Subscribers**, the three inputs, and the profile. The same 57.84 from slide 9 — computed live.

*[Sidebar filter — Occupation = Professional]* — watch the top row: **4,922 customers, subscriber rate 44.3% versus 33.2% overall** — every chart and segment just recomputed. Add California — it narrows again. Anyone can do this. And the filtered list **downloads as CSV**.

*[Tab ⑤ — Methodology]* — and nothing is hidden: the formula, the weights, the reasons, the segment rules — all inside the app.

## Part C — What's missing & what's next (~0:40)

"One honest closing. Our original data brief promised **login frequency, session duration, books accessed, recency, genre, and subscription tenure** — none of those exist in the file we got. So churn states, recency scoring, and retention curves **cannot** be built from this data — and we didn't pretend otherwise. What we built is the strongest **profile-based** analysis the available data supports.

Next steps, in order: **one** — if we get the engagement columns, we rebuild properly: recency-based risk scoring, Active/Inactive/Churned classification, retention curves, tenure analysis. **Two** — fit a real predictive model with a train/test split and proper accuracy metrics, and compare it against our score. **Three** — production hygiene: a committed cleaning script and a build log, so every number is reproducible from scratch.

Thank you — we're happy to take questions."

---

# KRISHA'S IN-DEPTH Q&A BANK
*(Ma'am will drill into whatever she finds on screen. These are the answers — rehearse, don't read.)*

## A. Correlation & statistics

**Q1. What exactly does r = 0.46 mean?**
"It's a linear association on a −1 to +1 scale. 0.46 is moderate-to-strong positive: as children-at-home values rise, the flag tends to be 1 more often. It's not a probability, and it doesn't mean 46% of anything."

**Q2. Does correlation mean causation?**
"No. Two things can travel together for a third reason — income, habit, household size. We never claim changing a variable would change subscription. Causation would need controlled experiments, which we don't have."

**Q3. Why Pearson specifically? Why the 0.8 threshold?**
"Pearson is the standard linear-correlation measure and our inputs are numeric. 0.8 is the conventional red line for collinearity — two inputs so correlated they'd double-count one signal. Ours top out at 0.73, so all three stay."

**Q4. Why not use correlation on job or education — they're not numbers?**
"Right, Pearson needs numbers. For categorical columns we compare **group subscriber rates**: Professionals 44.3% versus Manual 23.7%. Same question — which groups line up with the answer — different tool."

**Q5. The score's mean is 28.6 but the median is 21. What does that tell you?**
"The distribution is right-skewed — a tail of high scorers pulls the mean up. Worth knowing: our tiers are terciles, which split by *count*, so skew doesn't break them."

## B. The scoring model

**Q6. Why weights 0.40 / 0.35 / 0.25 — why not equal thirds?**
"They follow the correlation ranking — the strongest signal gets the biggest weight — and they sum to 1.0. Equal weights would ignore the evidence we gathered in step two."

**Q7. Why not let an algorithm find the weights?**
"Trade-off: a fitted model might score slightly better, but we'd lose explainability. For this project we chose full transparency — and fitting with validation is explicitly our next step, not something we hid."

**Q8. Why min-max normalisation instead of z-scores?**
"Min-max keeps everything on a clean 0-to-1 scale, so the final score is an intuitive 0-to-100. Z-scores would work statistically but produce a harder-to-explain number. Also, our inputs are all positive and bounded, so min-max is stable here."

**Q9. Why ×100?**
"Presentation only. 57.8 reads better than 0.578. Mathematically identical."

**Q10. Why drop Total Number of Children when it correlates 0.23?**
"It measures nearly the same thing as children-at-home (r = 0.73 between the two). Including both double-counts family size. We kept the stronger, more specific one."

**Q11. What if a new customer has 6 children, or income above $196,511?**
"Honest answer: normalisation is fixed to this dataset's min and max, so a value beyond the range would push that component above 1 and the score could exceed 100. In production you'd cap it or refit the ranges. Good catch — it's a known limitation of min-max."

**Q12. Is this machine learning?**
"No. There's no training, no loss function, no gradient descent. It's a weighted index from correlation analysis. It sits in the same family as a credit-scorecard or a semester aggregate. We call it exactly that."

**Q13. How do you know the score isn't circular — flag predicting flag?**
"The score's inputs are only children, spend, and income. The flag is never an input. It's used after the fact — to test the tiers and to build segments. Slide 10 proves it: the app computes 57.8 from inputs alone."

## C. Validation & tiers

**Q14. Why terciles — 33rd and 67th percentiles — not fixed thresholds like 30 and 60?**
"Terciles are relative to this customer base and always produce three usable groups. Fixed thresholds would need an external benchmark we don't have. Boundaries came out at 16.7 and 29.2."

**Q15. Isn't in-sample validation weak?**
"Yes — it's the honest weakness. The correlations chose the weights and the same data tested them. A held-out set or cross-validation is the planned upgrade. What we can say: the pattern is monotonic and strong — 13.0, 25.8, 61.1 — not a fluke of one cut."

**Q16. Tier counts are on 16,519 rows but segments on 16,404 — why?**
"Scoring ran before de-duplication; the 115 duplicates were removed when segments were built. Both bases give the same 33.2% rate, so conclusions are unaffected — but it's a pipeline-order quirk we'd fix by deduping at cleaning."

## D. Segments & business

**Q17. Why six rule-based segments instead of k-means clustering?**
"Two reasons: explainability — every rule is a sentence anyone can check — and stability: k-means needs you to pick k and gives different answers each run. Clustering is on our extension list as a comparison, not a replacement."

**Q18. Core and High-potential differ only by the flag — is that a thin difference?**
"It's thin by construction, and we admit it: demographically they're twins — $108K versus $104K income. Behaviour data would separate them properly. The value of the group is precisely that similarity: it identifies non-subscribers who match your best customers."

**Q19. Why not just give High-potentials a discount?**
"Because their mean income is $104K — affordability isn't the barrier. Their spend sits $15/month below Core. The lever is trial and upgrade, not price. A discount would give away margin to people who could already pay."

**Q20. How much is one conversion worth in rupees/dollars?**
"We can't say — that needs customer lifetime value and actual conversion experiments, and neither exists in this data. We prioritise groups by profile and spend gap; we don't invent revenue numbers."

## E. Data & cleaning

**Q21. Why keep the *first* duplicate, not the last or an average?**
"Standard practice when there's no timestamp to say which record is newer. Keep-first is deterministic and documented in the code. Averaging would also smear categorical fields like occupation."

**Q22. The two-digit year fix — how do you know 66 means 1966?**
"We don't *know* — we inferred it. Tokens in the file run 10 to 80, which as 1910–1980 produces sensible adult customer ages. As 2010–2080 it would mean newborns with $100K incomes. The inference is documented, and it's a genuine caveat."

**Q23. Any errors in the cleaning?**
"One known edge case: a single customer born 1910 falls just outside our first age bin, so their AgeGroup is blank — one row in 16,404, which we disclose rather than patch silently."

**Q24. How do you extract State from 'Oakland-94601-California'?**
"Split on hyphens, take the last part. Verified: zero missing states in the final data, and California is correctly the largest state."

## F. The missing data story

**Q25. Be precise — what was promised and what arrived?**
"Promised in the brief: login frequency, session duration, books accessed, recency, genre, subscription tenure. Arrived: none of them. The only subscription field is the 0/1 flag. Avg Monthly Spend looks behavioural but is spend, not engagement."

**Q26. What would you do the day those columns arrive?**
"Four things: recency-based risk scoring — with inversion so long-inactive readers flag as churn risk; Active/Inactive/Churned classification from engagement thresholds; retention curves over tenure; and re-running correlation to see if behaviour beats profile — then fitting and hold-out-validating a proper model."

## G. The app, tools & project hygiene

**Q27. How does the dashboard update when I change a filter?**
"Streamlit reruns the script; the filter becomes a boolean mask over the data; every KPI and chart recomputes from the filtered rows. Data loads once via cache — that's why it's fast."

**Q28. Why put the methodology inside the app?**
"So nobody — including us — can quietly change the story. Formula, weights, reasons, segment rules: on screen, matching outputs/methodology.md in the repository."

**Q29. Where's the code and how is it organised?**
"Four Python scripts — EDA, scoring, segmentation, and the app — plus the three processed CSVs and outputs, on GitHub. The scoring script's approval gate means the weights can't be applied without a human typing 'y'."

**Q30. If you had one more week, what first?**
"Commit the missing cleaning script and a build log so everything rebuilds from raw, then the engagement-data roadmap and the fitted model with a held-out test. Reproducibility first — it's the foundation of the rest."

---

## Emergency notes for Krisha

- **Server down before demo?** Restart: `cd ~/Desktop/IR && /Users/krishasatishkadam/ebook-prototype/.venv/bin/python -m streamlit run src/app.py --server.headless true --server.port 8501` — then `open http://localhost:8501`. If it still fails, fall back to slides 10 and 15: *"These screenshots are from this exact app — the lookup result, and the KPIs changing under filters."*
- **Out of time?** Cut slides 14 and 16 (tour + methodology screenshots) — keep 7, 9, 10, 11, 13 and the demo. Never cut Part C (what's missing) — that's the academic honesty she's looking for.
- **If mam asks something no one knows:** "We'd rather not guess — from the data we have, X; anything beyond that we haven't verified." That sentence has never lost marks.

---

# Addendum — Krisha's simplified talk track (slides 6→end)

One flowing ~2-minute script, using only examples from our own data (no outside analogies).

**[Slide 6]** "Now the analysis. First we had to pick what goes into the score. We used **correlation** — it just measures, out of all the columns, which ones rise together with the flag. Look at children at home: among customers with **no children, only 19 in 100** subscribe. With **five children, 84 in 100** subscribe — that's why correlation is 0.46, our strongest signal. Spend (0.42) and income (0.29) also move with the flag. Home ownership? 0.001 — nothing — so we dropped it. Then we checked our three picks against each other, so we're not counting the same thing twice."

**[Slide 7]** "Here's that children pattern as a chart — **19% → 24% → 59% → 69% → 72% → 84%** — a clear staircase, which is why children got the biggest weight. But careful: this is **association, not causation** — customers who spend more also subscribe more, but maybe they're just richer in general; spending doesn't *make* them subscribe."

**[Slide 8]** "The **Subscriber Propensity Score** — propensity means likelihood. We can't add '3 children' to '$117' — different units — so we **normalise**: the biggest spender in our data ($176) gets 1.0, the smallest ($22) gets 0; our $117 customer sits at 0.6169. Then **weights** — children 40%, spend 35%, income 25%, from those correlation numbers — added, times 100. And this is **not AI**: the script stops and asks a human 'Approve these weights? y or n' first."

**[Slide 9]** "Customer **11001**: 3 children → 0.60, $117 → 0.62, $101,141 → 0.49. Weighted and added: **57.84** — High tier, flag is 1 — Core Subscriber. Just multiplication and addition."

**[Slide 10]** "Same customer in the live app: **57.8, High, Core**. Works for any of the 16,404 IDs."

**[Slide 11]** "Does it work? Line everyone up by score, cut into three **tiers**, then ask each group how many really subscribed: bottom third **13 in 100**, middle **26 in 100**, top **61 in 100** — always rising, top group converts **4.7×** the bottom. Fair test: the score never saw the flag while being built. Honest limit: checked on the same data it was built from."

**[Slide 12]** "Tier × flag = **six segments**. Interesting one: **High-potential Prospects** — same job, same income, same kids as a Core Subscriber, but they *didn't* click subscribe: 2,103 people. Biggest is Low-priority at 29%; no group crosses 60%."

**[Slide 13]** "Core: $108K, $106/mo, 3.1 kids — protect them. **Prospects** earn $104K — almost the same — but spend $91: money isn't the problem, so no discounts, offer **trials**. **Low-fit** subscribe despite low scores — 96% have no children — data can't explain why, so hold their pricing."

**[Slides 14–16]** "The rest lives in the app — five tabs, live filters — and the **full methodology is inside the app**; open tab five and the formula is right there. Nothing hidden."

**[Slide 17]** "Limitations, honestly: association is not cause; no behaviour data, so profile-based segments; weights set by judgement, tested in-sample; tiers relative to this dataset."

**[Slide 18 → demo]** *[Open dashboard → 16,404 · 33.2% → Tab ④: type any ID → 57.8, High, Core → filter Occupation = Professional → 4,922 · 44.3% → Tab ⑤: formula]*

**Closing:** "Last, honestly: the data we were *promised* — login frequency, sessions, books read, recency, genre, tenure — **none of those columns exist**, so churn and retention *cannot* be built from this file; we never pretended otherwise. The day those columns arrive, we rebuild with real behaviour data. Thank you!"

# Addendum — new Q&A answers (from doubt-clearing sessions)

**Q31. Why did you pick children, spend and income — not age, home ownership, cars, etc.?**
"Not random, ma'am — we ranked all six numeric columns by correlation with the flag. Children 0.46, spend 0.42, income 0.287 made the cut. **Total children was dropped as a duplicate** of children-at-home (they're 0.73 correlated — using both would count family size twice). **Cars was too weak** at 0.17. **Home ownership was 0.001** — owners and renters subscribe at the same rate in this data. Age, job and education *do* matter — we measured rates: 13% vs 52% across age groups, 44% vs 24% across jobs — but they're categories, not numbers, so they couldn't enter the correlation ranking; they're the first thing we'll add next version. We even disclosed the cost: half our High-potential Prospects are 55+ because the score can't see age. And we kept three inputs deliberately — with ten, the formula becomes a black box."

**Q32. Then why not put EVERYTHING in the score?**
"Three reasons: near-useless variables only add noise (home ownership: 0.001); duplicates double-count (total children vs children-at-home); and transparency — with three inputs I can compute any score on a slide in front of you. The trade-off is real and it's on our limitations slide. Always: the strongest *in this dataset*, never 'the most important factors'."

**Q33. How can a customer have a HIGH score and still NOT be subscribed? (High-potential Prospects, deep dive)**
"Score and flag come from different worlds: the score is computed from their *profile* — children, spend, income — and answers 'do they look like a subscriber?' The flag is the fact: did they actually click subscribe? Nothing forces agreement — High tier means top third of the ranking, not a guarantee. That's exactly why High tier converts at 61.1%, not 100% — the missing 39% *is* this segment: 2,103 of the 5,411 High-tier people. Why don't they subscribe? On money and family they're twins of Core ($104K vs $108K income, 71% Prof/Mgmt in both) — but **51% (1,078) are aged 55+**, from cohorts that subscribe at only 13–29%, and the score doesn't use age at all. Score says yes, cohort says no, flag says 0. The final 'why' — awareness, reading habit, print preference — is unknowable from this file, and we say that instead of inventing it. Mirror image exists too: 699 Low-fit Subscribers who subscribed despite low scores — both directions prove correlation shifts odds, never decides individuals. The score's imperfection *is* the business opportunity — and we test the hypothesis with campaigns, not assumptions."
