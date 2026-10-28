"""
v2 stage 2 — classify cleaned engagement rows as Active / Inactive / Churned.

Applies ONLY the thresholds approved in outputs/v2/methodology.md section 2 (23 Oct 2026):
  Active       : Days Since Last Activity <= 30 AND Avg Logins Per Month >= 1
  Inactive     : everything between (31-90 days, or <=30 days with 0 logins)
  Churned      : Days Since Last Activity > 90
  Unclassified : recency missing/invalid (never guessed)
Reads data/processed/v2/engagement_clean.csv, writes engagement_status.csv + status_summary.csv.
"""
import pandas as pd

CLEAN = "data/processed/v2/engagement_clean.csv"
OUT = "data/processed/v2/engagement_status.csv"
SUMMARY = "outputs/v2/status_summary.csv"

df = pd.read_csv(CLEAN)

recency = df["Days Since Last Activity"]
logins = df["Avg Logins Per Month"]

# Start everyone as Inactive-candidate; assign the unambiguous bands first
status = pd.Series("Inactive", index=df.index)

# Unclassified — recency decides the segment, so missing/invalid recency is never guessed
unclass = recency.isna()
status[unclass] = "Unclassified"

# Churned — more than three full cycles (90 days) of silence
status[recency > 90] = "Churned"

# Active — within one cycle AND at least one login (data-consistency guard)
active = (recency <= 30) & (logins >= 1)
status[active] = "Active"

df["Status"] = status

counts = (
    df["Status"].value_counts()
    .reindex(["Active", "Inactive", "Churned", "Unclassified"])
    .rename_axis("Status")
    .reset_index(name="Customers")
)
classified = counts.loc[counts["Status"] != "Unclassified", "Customers"].sum()
counts["% of classified"] = (counts["Customers"] / classified * 100).round(1)
counts.loc[counts["Status"] == "Unclassified", "% of classified"] = None

print(counts.to_string(index=False))
print(f"Total rows: {len(df)}; classified: {classified}")
print(f"Median days since activity by status:")
print(df.groupby("Status")["Days Since Last Activity"].median().to_string())

df.to_csv(OUT, index=False)
counts.to_csv(SUMMARY, index=False)
print(f"Wrote {OUT} and {SUMMARY}")
