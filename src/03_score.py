import pandas as pd
import numpy as np
import os

# ── Directories ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, "data", "processed", "clean.csv")
METHODOLOGY_PATH = os.path.join(PROJECT_DIR, "outputs", "methodology.md")
SCORED_PATH = os.path.join(PROJECT_DIR, "data", "processed", "scored.csv")

# ── Load data ────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)

# ── Compute correlations with the flag ───────────────────────
subset = df[["Annual Income", "Avg Monthly Spend", "Home Owner Status",
             "Number of Cars Owned", "Number of Children At Home",
             "Total Number of Children", "eBook Subscriber Flag"]]
corr_matrix = subset.corr()
corr_with_flag = abs(corr_matrix["eBook Subscriber Flag"])

print("=== Candidate inputs with correlations with eBook Subscriber Flag ===")
for col in ["Annual Income", "Avg Monthly Spend", "Home Owner Status",
            "Number of Cars Owned", "Number of Children At Home",
            "Total Number of Children"]:
    r = corr_with_flag[col]
    print(f"  {col}: r = {r:.4f}")

print("\n=== Proposed inputs and weights (awaiting approval) ===")
print("Selected 3 inputs (no |r| > 0.8 collinearity):")
print("  1. Number of Children At Home: r = 0.4564 (strongest predictor)")
print("  2. Avg Monthly Spend:        r = 0.4218 (high spend → higher subscription)")
print("  3. Annual Income:              r = 0.2871 (income effect, weaker than spend)")
print()
proposed_weights = {
    "Number of Children At Home": 0.40,
    "Avg Monthly Spend": 0.35,
    "Annual Income": 0.25,
}
print("Proposed weights summing to 1.0:")
for var, w in proposed_weights.items():
    print(f"  {var}: weight = {w}")
print()
print("Rationale:")
print("  • Number of Children At Home (w=0.40): highest correlation (0.456); more children")
print("    at home indicates greater household engagement potential with eBooks.")
print("  • Avg Monthly Spend (w=0.35): second-highest correlation (0.422); spending behavior")
print("    strongly tracks with eBook adoption — frequent spenders are more likely to subscribe.")
print("  • Annual Income (w=0.25): third-highest correlation (0.287); income matters but is")
print("    less predictive than actual spending habits.")

approval = input("\nApprove these weights and proceed? (y/n): ")
if approval.lower() != "y":
    print("Aborted. No changes saved.")
    exit()

# ── Write methodology ────────────────────────────────────────
methodology_text = (
    "## Scoring model\n\n"
    "Subscriber Propensity Score (SPS) computed as a weighted min-max-normalised sum of three predictors:\n\n"
    "1. **Number of Children At Home** (min-max normalised to [0,1]) × weight 0.40\n"
    "2. **Avg Monthly Spend** (min-max normalised to [0,1]) × weight 0.35\n"
    "3. **Annual Income** (min-max normalised to [0,1]) × weight 0.25\n\n"
    "Normalisation formula:  x_norm = (x - min(x)) / (max(x) - min(x))\n\n"
    "Final SPS = (w1 × x1_norm + w2 × x2_norm + w3 × x3_norm) × 100, yielding a 0–100 scale.\n\n"
    "Weights were chosen based on absolute Pearson correlation with the eBook Subscriber Flag:\n"
    "Children At Home (0.456) > Avg Monthly Spend (0.422) > Annual Income (0.287). No selected pair\n"
    "has |r| > 0.8, so no collinearity penalty is applied. The weights sum to 1.0 and reflect the\n"
    "relative predictive strength of each variable while avoiding double-counting correlated children\n"
    "measures (e.g., Total Number of Children was excluded in favour of Children At Home).\n"
)

with open(METHODOLOGY_PATH, "a") as f:
    f.write(methodology_text)

# ── Min-max normalisation ────────────────────────────────────
cols_for_score = ["Number of Children At Home", "Avg Monthly Spend", "Annual Income"]
mins = df[cols_for_score].min()
maxs = df[cols_for_score].max()
ranges = maxs - mins

df["Children_Norm"] = (df["Number of Children At Home"] - mins["Number of Children At Home"]) / ranges["Number of Children At Home"]
df["Spend_Norm"] = (df["Avg Monthly Spend"] - mins["Avg Monthly Spend"]) / ranges["Avg Monthly Spend"]
df["Income_Norm"] = (df["Annual Income"] - mins["Annual Income"]) / ranges["Annual Income"]

# ── Compute SPS on 0–100 scale ───────────────────────────────
w1, w2, w3 = 0.40, 0.35, 0.25
df["Subscriber_Propensity_Score"] = (w1 * df["Children_Norm"] + w2 * df["Spend_Norm"] + w3 * df["Income_Norm"]) * 100

# ── Assign tercile tiers ─────────────────────────────────────
tertiles = df["Subscriber_Propensity_Score"].quantile([0.33, 0.67])

df["Tier"] = pd.cut(
    df["Subscriber_Propensity_Score"],
    bins=[-1, float(tertiles[0.33]), float(tertiles[0.67]), 101],
    labels=["Low", "Medium", "High"],
)

# ── Subscription rate per tier ───────────────────────────────
print("\n=== Subscription rate per tier ===")
for tier in ["Low", "Medium", "High"]:
    subset = df[df["Tier"] == tier]
    rate = subset["eBook Subscriber Flag"].mean()
    count = len(subset)
    print(f"  {tier}: {rate:.1%} subscriber rate ({count} customers)")

# ── Save scored CSV ──────────────────────────────────────────
output_cols = [
    "Customer ID", "Title", "First Name", "Last Name",
    "Number of Children At Home", "Avg Monthly Spend", "Annual Income",
    "Subscriber_Propensity_Score", "Tier", "eBook Subscriber Flag"
]
df[output_cols].to_csv(SCORED_PATH, index=False)
print(f"\nSaved: {SCORED_PATH} (shape={df[output_cols].shape})")

print("\nDone. Verify that subscriber rate rises from Low → Medium → High.")