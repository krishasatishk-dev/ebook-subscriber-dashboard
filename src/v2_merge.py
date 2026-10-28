"""
v2 stage 3 — merge engagement statuses with v1 customer demographics.

Inner-joins data/processed/v2/engagement_status.csv (cleaned engagement + Status,
the stage-1 file plus the stage-2 status column) to data/processed/clean.csv on
Customer ID. clean.csv is de-duplicated keep-first first, the same rule v1 used
in src/04_segment.py:27-28 — 115 Customer IDs appear twice in clean.csv and
keeping both would break the one-row-per-customer rule.
Writes data/processed/v2/merged.csv.
"""
import pandas as pd

ENG = "data/processed/v2/engagement_status.csv"
CLEAN = "data/processed/clean.csv"
OUT = "data/processed/v2/merged.csv"

eng = pd.read_csv(ENG)
clean = pd.read_csv(CLEAN)

eng_ids = set(eng["Customer ID"])
clean_ids = set(clean["Customer ID"])
matched = eng_ids & clean_ids
print(f"Unique IDs in engagement file: {len(eng_ids)}")
print(f"Unique IDs in clean.csv (raw rows {len(clean)}): {len(clean_ids)}")
print(f"Matched IDs: {len(matched)}")
print(f"Unmatched in engagement (no customer row): {len(eng_ids - clean_ids)}")
print(f"Unmatched in clean.csv (no engagement row): {len(clean_ids - matched)}")

# How many doubled IDs differ specifically on the subscriber flag (all 115 dups,
# and the subset that also appears in the engagement file)
dup_all = clean.loc[clean["Customer ID"].duplicated(keep=False), "Customer ID"].unique()
flag_nunq = (
    clean[clean["Customer ID"].isin(dup_all)]
    .groupby("Customer ID")["eBook Subscriber Flag"].nunique()
)
n_flag_diff = int((flag_nunq > 1).sum())
overlap = [cid for cid in dup_all if cid in eng_ids]
n_flag_diff_overlap = int((flag_nunq.reindex(overlap) > 1).sum())
print(f"clean.csv duplicated Customer IDs: {len(dup_all)}; "
      f"differing on subscriber flag: {n_flag_diff}")
print(f"  of those also in the engagement file: {len(overlap)}; "
      f"differing on flag among those: {n_flag_diff_overlap}")

# Decision D2 (approved 23 Oct 2026, methodology.md section 5): when one Customer
# ID has two records, prefer the flag=1 (subscriber) record; if flags are equal,
# keep the first (v1's rule, src/04_segment.py:27-28).
clean = (
    clean.sort_values("eBook Subscriber Flag", ascending=False, kind="stable")
    .drop_duplicates(subset="Customer ID", keep="first")
)
print(f"clean.csv after prefer-flag=1 dedupe: {len(clean)} rows")

# State is embedded in 'City-ZipCode-State' (e.g. 'Boston-2101-Massachusetts')
clean["State"] = clean["City-ZipCode-State"].astype("string").str.rsplit("-", n=1).str[-1]

# Demographics kept for v2 (clean.csv has no 'Age' column; Birth Date + AgeGroup
# are the age information that exists)
demo_cols = [
    "Customer ID", "eBook Subscriber Flag", "Birth Date", "AgeGroup",
    "Education Level", "Occupation",
    "Gender", "Marital Status", "Home Owner Status", "Number of Cars Owned",
    "Number of Children At Home", "Annual Income", "IncomeBand",
    "Avg Monthly Spend", "State",
]
eng_cols = [
    "Subscription Tenure Months", "Avg Logins Per Month", "Avg Session Minutes",
    "Books Accessed", "Days Since Last Activity", "Genre Preference", "Status",
]

merged = clean[demo_cols].merge(eng[eng_cols + ["Customer ID"]], on="Customer ID", how="inner")

# Assert the join produced exactly one row per customer and no ID was lost or multiplied
assert merged["Customer ID"].is_unique, "duplicate Customer ID after join"
assert len(merged) == len(matched), f"row count {len(merged)} != matched IDs {len(matched)}"
print(f"Join OK: {len(merged)} rows, one per Customer ID")

# Confirm every engagement ID resolved to a flag=1 (subscriber) record under D2
n_sub = int((merged["eBook Subscriber Flag"] == 1).sum())
print(f"Engagement IDs matched to a flag=1 subscriber record: {n_sub} of {len(merged)}")
assert n_sub == len(merged), "an engagement ID matched a non-subscriber record"

merged.to_csv(OUT, index=False)
print(f"Wrote {OUT}")
print(merged["Status"].value_counts().to_string())
