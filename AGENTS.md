# AGENTS.md

PROJECT: "eBook Subscriber Insights using EDA", an industrial research prototype. Two phases. Phase 1 (review 1, already done) used only the customer file. Phase 2 (now) adds engagement data. Never overwrite or delete Phase 1 code or outputs; write Phase 2 to outputs/v2/ and data/processed/v2/ with scripts named src/v2_*.py.

DATA:
- data/raw/customer_data.csv (16,519 rows; cleaned copy data/processed/clean.csv, 16,404 unique customers, 33.2% subscribers).
- data/raw/eBook_Engagement.csv (5,500 rows: Customer ID, Subscription Tenure Months, Avg Logins Per Month, Avg Session Minutes, Books Accessed, Days Since Last Activity, Genre Preference). Subscribers only (flag=1). Joins to clean.csv on Customer ID; all 5,455 unique IDs match.
- Never modify raw files. Never add synthetic, simulated or random data. Every number comes from these files.

KNOWN ISSUES in the engagement file: 45 exact duplicate rows; missing values (session minutes 81, books 43, recency 28, genre 54); 26 spellings of 8 genres; 6 negative recency values; logins above 60 (7 rows); session minutes above 180 (8 rows, likely decimal-shift errors); books above 60 (7 rows); recency above 365 (11 rows, several exactly 400); 416-417 genuine zero-login rows (keep).

WORKING RULES:
- Active, Inactive and Churned come only from thresholds I approve, written in outputs/v2/methodology.md BEFORE they are applied.
- Every cleaning decision, weight and threshold needs a one-line rationale in methodology.md.
- Never choose weights or thresholds yourself: propose them and wait for my approval.
- Append 3-4 plain-English lines to outputs/v2/BUILD_LOG.md after every stage.
- Stack: Python, pandas, numpy, matplotlib, seaborn, plotly, streamlit. Code in src/, commented.
- Every chart has a title and a one-line takeaway caption.
- Work in stages and stop after each stage to show output.
