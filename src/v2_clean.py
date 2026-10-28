"""
v2 stage 1 — clean the raw engagement file.

Applies cleaning rules C1-C10 from outputs/v2/methodology.md (approved 23 Oct 2026).
Raw file data/raw/eBook_Engagement.csv is only read, never written.
Writes data/processed/v2/engagement_clean.csv.
"""
import numpy as np
import pandas as pd

RAW = "data/raw/eBook_Engagement.csv"
CLEAN_CUSTOMERS = "data/processed/clean.csv"   # v1 cleaned customer file (subscribers flagged)
OUT = "data/processed/v2/engagement_clean.csv"

# Canonical 8 genres; every raw spelling maps to one of these (rule C2)
GENRE_MAP = {
    "business": "Business", "fantasy": "Fantasy", "fiction": "Fiction",
    "mystery": "Mystery", "non fiction": "Non Fiction", "nonfiction": "Non Fiction",
    "non-fiction": "Non Fiction", "romance": "Romance",
    "sci fi": "Sci-Fi", "sci-fi": "Sci-Fi", "science fiction": "Sci-Fi",
    "self help": "Self Help", "self-help": "Self Help",
}

df = pd.read_csv(RAW)
n_raw = len(df)
print(f"Raw rows: {n_raw}")

# C1 — drop the 45 exact duplicate rows, keep first (same rule as v1 dedupe)
df = df.drop_duplicates()
print(f"C1 after dedupe: {len(df)} unique rows ({n_raw - len(df)} duplicates dropped)")

# Normalise text fields before missing checks
df["Genre Preference"] = df["Genre Preference"].astype("string").str.strip()

# C4 — negative 'days since last activity' is a date error; set to missing, never invent a value
recency = pd.to_numeric(df["Days Since Last Activity"], errors="coerce")
neg_mask = recency < 0
print(f"C4 negative recency set to missing: {int(neg_mask.sum())}")
recency[neg_mask] = np.nan
df["Days Since Last Activity"] = recency

# C6 — implausible behaviour values (decimal-shift errors) set to missing, counts logged
logins = pd.to_numeric(df["Avg Logins Per Month"], errors="coerce")
session = pd.to_numeric(df["Avg Session Minutes"], errors="coerce")
books = pd.to_numeric(df["Books Accessed"], errors="coerce")
print(f"C6 logins>60 set to missing: {int((logins > 60).sum())}")
print(f"C6 session>180 set to missing: {int((session > 180).sum())}")
print(f"C6 books>60 set to missing: {int((books > 60).sum())}")
logins[logins > 60] = np.nan
session[session > 180] = np.nan
books[books > 60] = np.nan
df["Avg Logins Per Month"] = logins
df["Avg Session Minutes"] = session
df["Books Accessed"] = books

# Decision D1 (approved 23 Oct 2026, methodology.md section 5): median-fill the
# three behaviour columns (original blanks + the ones C6 blanked). Recency is
# NEVER imputed — blank recency stays Unclassified because status is decided on recency.
fill_cols = ["Avg Logins Per Month", "Avg Session Minutes", "Books Accessed"]
medians = df[fill_cols].median()
print("D1 medians used for imputation:")
for c in fill_cols:
    print(f"  {c}: {medians[c]:.2f}")
was_missing = df[fill_cols].isna()
df["Imputed"] = was_missing.any(axis=1).astype(int)
for c in fill_cols:
    df[c] = df[c].fillna(medians[c])
print(f"D1 fills — logins {int(was_missing['Avg Logins Per Month'].sum())}, "
      f"session {int(was_missing['Avg Session Minutes'].sum())}, "
      f"books {int(was_missing['Books Accessed'].sum())}")
print(f"D1 rows with at least one imputed value: {int(df['Imputed'].sum())}")

# C7 — genuine zero logins are kept as real zeros (checked here, not modified)
print(f"C7 genuine zero-login rows kept: {int((df['Avg Logins Per Month'] == 0).sum())}")

# C8 — recency above 365 kept as-is (likely a capture cap at 400)
print(f"C8 recency>365 kept: {int((df['Days Since Last Activity'] > 365).sum())}")

# C2 + C3 — collapse 23 genre spellings to 8; missing genre labelled 'Unknown'
df["Genre Preference"] = (
    df["Genre Preference"].fillna("").str.lower().map(GENRE_MAP).fillna("Unknown")
)
print(f"C2/C3 genre counts:\n{df['Genre Preference'].value_counts().to_string()}")

# Remaining missing values (C9, as amended by D1): only recency blanks stay
# empty — the three behaviour columns were median-filled above.
print("Missing after cleaning:")
print(df.isna().sum().to_string())

# C10 — validate the join key against v1 subscribers (merge itself happens in a later stage)
customers = pd.read_csv(CLEAN_CUSTOMERS)
subs = set(customers.loc[customers["eBook Subscriber Flag"] == 1, "Customer ID"])
ids = set(df["Customer ID"])
print(f"C10 unique engagement IDs: {len(ids)}; all match v1 subscribers: {ids <= subs}")

df.to_csv(OUT, index=False)
print(f"Wrote {OUT}")
