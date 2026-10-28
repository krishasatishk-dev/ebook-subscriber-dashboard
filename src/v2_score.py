"""
v2 stage 5 — engagement score.

STEP A (runs now): prints the candidate inputs with their correlations, PROPOSES
weights summing to 1 (recency inverted, logins, session minutes; books excluded as
a descriptive metric only), warns that status is defined on recency, and shows how
the tier-by-status table changes under recency weight 0.45 and 0.25.
Then it STOPS — no scored.csv, no methodology "Engagement score" section.

STEP B (after approval): flip WEIGHTS_APPROVED to True (and set the approved
weights + the Unclassified handling), rerun. It min-max normalises, inverts
recency, scores 0-100, assigns Low/Medium/High by terciles, writes everything to
methodology.md and data/processed/v2/scored.csv, and appends to BUILD_LOG.md.
"""
import pandas as pd

MERGED = "data/processed/v2/merged.csv"
SCORED_OUT = "data/processed/v2/scored.csv"
METHODOLOGY = "outputs/v2/methodology.md"
BUILD_LOG = "outputs/v2/BUILD_LOG.md"

# ── Set after your approval (APPROVED 23 Oct 2026) ───────────
WEIGHTS_APPROVED = True             # approved 0.40 / 0.35 / 0.25 on 23 Oct 2026
WEIGHTS = {"Days Since Last Activity": 0.40,   # approved set
           "Avg Logins Per Month": 0.35,
           "Avg Session Minutes": 0.25}
BOOKS_WEIGHT = 0.0                  # descriptive only, stays out of the score
UNCLASSIFIED_PARTIAL_SCORE = True   # approved: Unclassified rows get a logins+session
                                    # score with those two weights renormalised
# ─────────────────────────────────────────────────────────────

CANDIDATES = ["Days Since Last Activity", "Avg Logins Per Month",
              "Avg Session Minutes", "Books Accessed"]

df = pd.read_csv(MERGED)

# ═══════════════════════ STEP A ═══════════════════════
print("Candidate inputs and their pairwise correlations:")
print(df[CANDIDATES].corr().round(3).to_string())

print("\nPROPOSED score (weights sum to 1.0):")
proposals = [
    ("Days Since Last Activity (inverted)", 0.40,
     "How recently someone last showed up is the clearest sign a subscription is still in use, so it carries the largest share."),
    ("Avg Logins Per Month", 0.35,
     "Login frequency is the direct measure of habit — just under recency because it averages across months rather than showing right now."),
    ("Avg Session Minutes", 0.25,
     "Time spent adds depth beyond visit counts but is the noisiest input (r=0.38 with logins), so it gets the smallest share."),
]
for name, w, why in proposals:
    print(f"  {w:.2f}  {name} — {why}")
print("  0.00  Books Accessed — EXCLUDED from the score: r=0.88 with Avg Logins "
      "Per Month means including both would count usage frequency twice; kept as a "
      "descriptive metric only.")

print("\nWARNING — construction overlap: status (Active/Inactive/Churned) is itself "
      "defined on Days Since Last Activity (and logins). A score that also uses "
      "recency will agree with status partly BY CONSTRUCTION, not as independent "
      "evidence. Treat any tier-vs-status agreement accordingly, especially at "
      "recency weight 0.40-0.45.")


def preview_tiers(weights, label):
    """Min-max scale, invert recency, score 0-100, tercile tiers, tier x status."""
    pop = df[df["Days Since Last Activity"].notna()].copy()
    r = pop["Days Since Last Activity"]
    r_s = (r - r.min()) / (r.max() - r.min())
    l = pop["Avg Logins Per Month"]
    l_s = (l - l.min()) / (l.max() - l.min())
    s = pop["Avg Session Minutes"]
    s_s = (s - s.min()) / (s.max() - s.min())
    score = 100 * (weights[0] * (1 - r_s) + weights[1] * l_s + weights[2] * s_s)
    tiers = pd.qcut(score, 3, labels=["Low", "Medium", "High"])
    tiers.name = "Tier"
    print(f"\n--- {label}: recency {weights[0]:.2f} / logins {weights[1]:.2f} / "
          f"session {weights[2]:.2f} "
          f"(n={len(pop)} classified rows; Unclassified excluded) ---")
    print("Tier sizes:")
    print(tiers.value_counts().reindex(["Low", "Medium", "High"]).to_string())
    print("Tier x Status:")
    print(pd.crosstab(tiers, pop["Status"], margins=True).to_string())


print("\n\nHow the tier-by-status table changes with the recency weight")
print("(alternatives keep logins:session at the proposed balance):")
preview_tiers((0.40, 0.35, 0.25), "PROPOSED")
preview_tiers((0.45, 0.30, 0.25), "ALTERNATIVE — recency 0.45")
preview_tiers((0.25, 0.40, 0.35), "ALTERNATIVE — recency 0.25")

n_unclass = int(df["Days Since Last Activity"].isna().sum())
print(f"\nUnclassified rows (no recency): {n_unclass} — no score under the proposed "
      "formula unless you approve a partial score from logins+session only "
      "(UNCLASSIFIED_PARTIAL_SCORE option in this script).")
print("\nSTOP — awaiting your approval of the weights. Nothing written to "
      "scored.csv or methodology.md.")

if not WEIGHTS_APPROVED:
    raise SystemExit(0)

# ═══════════════════════ STEP B (only after approval) ═══════════════════════
pop_mask = df["Days Since Last Activity"].notna()


def minmax(series):
    return (series - series.min()) / (series.max() - series.min())


r_s = minmax(df["Days Since Last Activity"])
l_s = minmax(df["Avg Logins Per Month"])
s_s = minmax(df["Avg Session Minutes"])

w_r = WEIGHTS["Days Since Last Activity"]
w_l = WEIGHTS["Avg Logins Per Month"]
w_s = WEIGHTS["Avg Session Minutes"]

# Score = weighted sum of 0-1 inputs; recency enters INVERTED (1 - scaled):
# fresh activity scores high, long absence scores low. Scale to 0-100.
score = 100 * (w_r * (1 - r_s) + w_l * l_s + w_s * s_s)

if UNCLASSIFIED_PARTIAL_SCORE:
    # Unclassified rows have no recency; give them logins+session only with the
    # remaining weights renormalised to sum to 1 (flagged, reported separately)
    partial = (w_l * l_s + w_s * s_s) / (w_l + w_s)
    score[~pop_mask] = 100 * partial[~pop_mask]

df["Engagement Score"] = score.round(2)

# Tercile cuts learned on the classified population, applied to everyone
classified_score = df.loc[pop_mask, "Engagement Score"]
lo, hi = classified_score.quantile([1 / 3, 2 / 3])
df["Tier"] = pd.cut(df["Engagement Score"], bins=[-1, lo, hi, 101],
                    labels=["Low", "Medium", "High"])

df.to_csv(SCORED_OUT, index=False)

print("\nSTEP B — score written")
print(f"Tercile cut points: Low <= {lo:.2f} < Medium <= {hi:.2f} < High")
print("\nTier sizes (classified rows; Unclassified shown if partial score approved):")
print(df["Tier"].value_counts().reindex(["Low", "Medium", "High"]).to_string())

print("\nMean of every metric per tier (including Books Accessed):")
metrics = ["Days Since Last Activity", "Avg Logins Per Month", "Avg Session Minutes",
           "Books Accessed", "Subscription Tenure Months", "Engagement Score"]
print(df.groupby("Tier", observed=False)[metrics].mean().round(2).to_string())

print("\nTier x Status:")
print(pd.crosstab(df["Tier"], df["Status"], margins=True).to_string())
print(f"\nUnclassified rows reported separately: {n_unclass} "
      f"(score present: {int(df.loc[~pop_mask, 'Engagement Score'].notna().sum())})")

# Document the score in methodology.md
with open(METHODOLOGY, "a") as f:
    f.write("\n## 7. Engagement score — APPROVED WEIGHTS\n\n")
    f.write("Inputs min-max normalised to 0-1 on the classified population "
            "(rows with valid recency); recency inverted as `1 - scaled` so fresh "
            "activity scores high; weighted sum x 100; tiers by terciles "
            f"(Low <= {lo:.2f} < Medium <= {hi:.2f} < High).\n\n")
    f.write("| Input | Weight | Why |\n|---|---|---|\n")
    for name, w, why in proposals:
        f.write(f"| {name} | {w:.2f} | {why} |\n")
    f.write("| Books Accessed | 0.00 (excluded) | r=0.88 with logins (0.90 before imputation) — would double-count usage frequency; descriptive only |\n")
    f.write(f"\nUnclassified rows ({n_unclass}): "
            + ("scored from logins+session only with those weights renormalised, reported separately."
               if UNCLASSIFIED_PARTIAL_SCORE else "no score — no recency, recency never imputed.") + "\n")
    f.write("\nConstruction-overlap warning: status is defined on recency, so "
            "tier-vs-status agreement is partly by construction, not independent validation.\n")

# Append to BUILD_LOG.md
with open(BUILD_LOG, "a") as f:
    f.write(f"\n## Stage 5c — engagement score (Step B, weights approved 0.40/0.35/0.25)\n"
            f"- Weighted 0-100 score from inverted recency {w_r:.2f}, logins {w_l:.2f}, "
            f"session minutes {w_s:.2f} (books excluded, r=0.90 with logins).\n"
            f"- Tiers by terciles: Low <= {lo:.2f} < Medium <= {hi:.2f} < High; "
            f"scored.csv has all rows, Unclassified handled separately.\n"
            f"- Documented in methodology.md under 'Engagement score'.\n")
print("Wrote scored.csv, methodology.md section 7, BUILD_LOG stage 5.")
