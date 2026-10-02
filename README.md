# 📚 eBook Subscriber Propensity & Segmentation Dashboard

An end-to-end customer-intelligence project: clean a raw eBook-subscription customer
dataset, explore it, score every customer's likelihood to subscribe, segment the base
into six actionable groups, and present it all in an interactive Streamlit dashboard.

## Quick start

```bash
# 1. Clone the repo
git clone <repo-url>
cd <repo-folder>

# 2. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run src/app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`) — open it in your browser.
Run everything from the **repo root** (the folder containing `src/`), because the app reads
data via relative paths (`data/processed/...`).

## What the dashboard contains

- **Introduction page** — project overview, pipeline explanation, and the six segments at a glance
- **① Overview** — segment donut, subscriber rate by occupation and age group (with average
  reference lines), and score distribution with tier boundaries
- **② Correlation Heatmap** — Pearson correlations among income, spend, children, and the flag
- **③ Segment Profiles** — profile table and side-by-side bar comparison per segment
- **④ Customer Lookup** — look up any Customer ID: score, tier, segment, and score inputs
- **⑤ Methodology** — the scoring model and segment definitions
- **Filters** — State, Occupation, Education Level, AgeGroup, Segment (sidebar); every KPI and
  chart recomputes live, and the filtered rows can be downloaded as CSV

## How the scoring works

1. **Inputs** chosen by correlation with the subscriber flag (no pair |r| > 0.8):

   | Input | r with flag |
   |---|---|
   | Children at home | 0.456 |
   | Avg monthly spend | 0.422 |
   | Annual income | 0.287 |

2. **Min-max normalise** each input to 0–1:
   `(x − min) / (max − min)`

3. **Weighted sum × 100** → Subscriber Propensity Score (0–100):

   ```
   Score = (0.40 × children + 0.35 × spend + 0.25 × income) × 100
   ```

4. **Tiers by terciles** (33rd / 67th percentile → boundaries 16.7 and 29.2):

   | Tier | Score range | Subscriber rate |
   |---|---|---|
   | Low | 0.1 – 16.7 | 12.9% |
   | Medium | 16.7 – 29.2 | 25.9% |
   | High | 29.2 – 98.4 | 61.1% |

   The 4.7× lift from Low to High validates the score.

5. **Six segments** = tier × actual subscription flag:

   | Segment | Rule | Size |
   |---|---|---|
   | Core Subscribers | Flag=1, Tier=High | 3,308 (20.2%) |
   | Low-fit Subscribers | Flag=1, Tier=Low | 699 (4.3%) |
   | High-potential Prospects | Flag=0, Tier=High | 2,103 (12.8%) |
   | Low-priority | Flag=0, Tier=Low | 4,712 (28.7%) |
   | Mid-tier Subscribers | Flag=1, Tier=Medium | 1,444 (8.8%) |
   | Mid-tier Non-subscribers | Flag=0, Tier=Medium | 4,138 (25.2%) |

## Project structure

```
├── src/
│   ├── 02_eda.py          # Exploratory analysis → charts, pivots, takeaways
│   ├── 03_score.py        # Propensity score + tiers (prints weights for approval)
│   ├── 04_segment.py      # Six-segment assignment + profiles
│   └── app.py             # Streamlit dashboard
├── data/
│   ├── processed/
│   │   ├── clean.csv      # Cleaned dataset (16,404 unique customers)
│   │   ├── scored.csv     # + propensity score and tier
│   │   └── segmented.csv  # + segment label (dashboard input)
├── outputs/
│   ├── charts/            # PNG charts from EDA and segmentation
│   ├── pivots/            # Pivot tables (Excel)
│   ├── methodology.md     # Scoring model + segment rules (rendered in Tab ⑤)
│   ├── eda_takeaways.md   # One-line takeaway under every chart
│   └── insights.md        # High-value profile, recommendations, limitations
└── requirements.txt
```

## Regenerating the outputs (optional)

The processed data and outputs are committed, so the dashboard works out of the box.
To rebuild from the raw CSV:

```bash
python3 src/02_eda.py      # charts + pivots
python3 src/03_score.py    # prints proposed weights, type y to approve
python3 src/04_segment.py  # segments + profiles
streamlit run src/app.py   # dashboard
```

## Data note

Based on demographic and spend data only — **no usage-based engagement metrics** were
available in the source dataset. The score reflects **association, not causation**, and
segments are profile-based rather than behaviour-based.

## Data hygiene applied

- 115 duplicate Customer IDs removed (16,519 → 16,404 rows)
- Two-digit birth years corrected (e.g. `66` → 1966, not 2066)
- Derived fields: AgeGroup, IncomeBand, State
- Title (99.5% missing) and Street Address2 (98.3% missing) excluded from analysis
