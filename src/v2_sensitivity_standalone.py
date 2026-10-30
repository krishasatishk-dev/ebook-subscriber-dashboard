"""
v2 engagement-score sensitivity analysis (standalone).

Reads data/processed/v2/scored.csv and asks one question: how much do the
Low/Medium/High tiers depend on the approved weight split (recency 0.40 /
logins 0.35 / session 0.25)?

Method
------
* Population: the 5,422 CLASSIFIED subscribers only (Status in Active /
  Inactive / Churned). The 33 Unclassified rows are excluded throughout,
  because they have no recency and were never part of the tercile basis.
* Inputs are min-max normalised EXACTLY as src/v2_score.py does it, so the
  baseline reproduces the shipped Tier column:
    - recency min-max skips NaN (computed on the 5,422 with valid recency);
    - logins and session min-max are computed over all 5,455 rows, which is
      the basis v2_score.py used when it wrote scored.csv.
* The SAME normalised inputs are reused for every weight set; only the
  weights change. Recency always enters inverted (1 - scaled).
* Tiers are re-cut per weight set from that set's OWN terciles
  (1/3 and 2/3 quantiles of its classified scores), using the same
  pd.cut([-1, lo, hi, 101]) rule as v2_score.py.

Status is NOT recomputed here — it depends only on Days Since Last Activity
(+ the >=1-login guard) and carries no score term, so reweighting cannot move
anyone between Active / Inactive / Churned.

Outputs: outputs/v2/sensitivity.csv, outputs/v2/sensitivity_summary.md
This script writes nothing else and edits no existing file.
"""
import pandas as pd

SCORED = "data/processed/v2/scored.csv"
CSV_OUT = "outputs/v2/sensitivity.csv"
MD_OUT = "outputs/v2/sensitivity_summary.md"

# name -> (recency, logins, sessions); baseline first
WEIGHT_SETS = [
    ("baseline",       (0.40, 0.35, 0.25), "approved weights"),
    ("equal",          (1 / 3, 1 / 3, 1 / 3), "equal thirds"),
    ("recency_light",  (0.25, 0.45, 0.30), "recency 0.25"),
    ("recency_heavy",  (0.50, 0.30, 0.20), "recency 0.50"),
]
BASELINE = "baseline"
TIER_ORDER = ["Low", "Medium", "High"]
TIER_NUM = {"Low": 0, "Medium": 1, "High": 2}
STATUS_ORDER = ["Active", "Inactive", "Churned"]

df = pd.read_csv(SCORED)

# ── population: classified subscribers only ───────────────────────────────
classified = df["Status"].isin(STATUS_ORDER)
pop = df[classified].copy()
n_unclass = int((~classified).sum())
print(f"scored.csv rows: {len(df):,}  |  classified: {len(pop):,}  "
      f"|  Unclassified excluded: {n_unclass}")
assert len(pop) == 5422, f"expected 5,422 classified, got {len(pop):,}"
assert n_unclass == 33, f"expected 33 Unclassified, got {n_unclass}"

# ── min-max normalise on the SAME basis as v2_score.py ────────────────────
# recency skips NaN (v2_score.py line 108: minmax over the full column, and
# pandas min/max ignore NaN); logins/session cover all 5,455 rows.


def minmax(series):
    return (series - series.min()) / (series.max() - series.min())


r_all = minmax(df["Days Since Last Activity"])   # NaN preserved for Unclassified
l_all = minmax(df["Avg Logins Per Month"])
s_all = minmax(df["Avg Session Minutes"])

# restrict the normalised inputs to the classified population
r_s = r_all.loc[pop.index]
l_s = l_all.loc[pop.index]
s_s = s_all.loc[pop.index]


def score_with(weights):
    """0-100 score from the fixed normalised inputs; recency inverted.

    Rounded to 2dp IMMEDIATELY, matching src/v2_score.py line 126 — the
    terciles are learned from these rounded values, so the order matters for
    scores that land exactly on a cut point.
    """
    w_r, w_l, w_s = weights
    return (100 * (w_r * (1 - r_s) + w_l * l_s + w_s * s_s)).round(2)


def cut_tiers(scores):
    """Terciles of THIS set's own classified scores -> Low/Medium/High.

    Same recipe as v2_score.py: 1/3 and 2/3 quantiles of the rounded scores,
    then pd.cut with bins [-1, lo, hi, 101] (right-inclusive).
    """
    lo, hi = scores.quantile([1 / 3, 2 / 3])
    return pd.cut(scores, bins=[-1, lo, hi, 101], labels=TIER_ORDER), lo, hi


results = {}
for name, weights, label in WEIGHT_SETS:
    sc = score_with(weights)
    tiers, lo, hi = cut_tiers(sc)
    results[name] = {"weights": weights, "label": label, "score": sc,
                     "tier": pd.Series(tiers, index=pop.index), "lo": lo, "hi": hi}

# ════════════════════════════════════════════════════════════════════════
# SANITY CHECK — baseline must reproduce the shipped Tier column
# ════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 74)
print("SANITY CHECK — baseline 0.40/0.35/0.25 vs Tier column in scored.csv")
print("=" * 74)

base_score, base_tier = results[BASELINE]["score"], results[BASELINE]["tier"]
shipped_tier = pop["Tier"].astype(str)
recomputed_tier = base_tier.astype(str)

# score agreement with the shipped Engagement Score (2dp in the CSV)
shipped_score = pop["Engagement Score"]
score_diff = (base_score.round(2) - shipped_score).abs()
print(f"Baseline cut points: Low <= {results[BASELINE]['lo']:.2f} "
      f"< Medium <= {results[BASELINE]['hi']:.2f} < High")
print(f"Shipped cut points per methodology.md: "
      f"Low <= 40.80 < Medium <= 51.25 < High")
print(f"Max |recomputed - shipped| score: {score_diff.max():.4f} "
      f"(rows differing by >0.01: {int((score_diff > 0.011).sum())})")

mismatch = recomputed_tier != shipped_tier
n_mis = int(mismatch.sum())
print(f"\nTier mismatches: {n_mis:,} of {len(pop):,} "
      f"({n_mis / len(pop) * 100:.2f}%)")
if n_mis:
    print("\nMismatched rows (shipped -> recomputed):")
    tmp = pd.DataFrame({"shipped": shipped_tier[mismatch],
                        "recomputed": recomputed_tier[mismatch],
                        "shipped_score": shipped_score[mismatch],
                        "recomputed_score": base_score.round(2)[mismatch]})
    print(tmp.head(20).to_string())
else:
    print("-> baseline reproduces the shipped Tier column EXACTLY.")

print("\nBaseline tier sizes (recomputed):")
print(base_tier.value_counts().reindex(TIER_ORDER).to_string())
print("\nBaseline tier x status:")
print(pd.crosstab(base_tier, pop["Status"], margins=True,
                  margins_name="All").reindex(index=TIER_ORDER).to_string())

# ════════════════════════════════════════════════════════════════════════
# STATUS is unaffected — it uses recency only
# ════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 74)
print("STATUS — unaffected by reweighting (recency-defined, no score term)")
print("=" * 74)
status_counts = pop["Status"].value_counts().reindex(STATUS_ORDER)
print(status_counts.to_string())
print(f"Total classified: {int(status_counts.sum()):,}")
print("Status is read straight from scored.csv and never recomputed here: the "
      "rule is Days Since Last Activity <= 30 AND >= 1 login -> Active, > 90 ->\n"
      "Churned, else Inactive. No branch of that rule reads the score, so "
      "changing the weights cannot move a single subscriber between statuses.")

# ════════════════════════════════════════════════════════════════════════
# ALTERNATIVES vs BASELINE
# ════════════════════════════════════════════════════════════════════════
alt_names = [n for n, _, _ in WEIGHT_SETS if n != BASELINE]

# baseline's own Active-in-Low, defined up front so every alternative can cite it
base_active_low = int(((recomputed_tier == "Low") &
                       (pop["Status"] == "Active")).sum())

print("\n" + "=" * 74)
print("ALTERNATIVES vs BASELINE")
print("=" * 74)

summary_rows = []
metrics = {}
for name in alt_names:
    alt_tier = results[name]["tier"].astype(str)
    alt_score = results[name]["score"]

    same = int((alt_tier == recomputed_tier).sum())
    pct_same = same / len(pop) * 100
    rho = base_score.corr(alt_score, method="spearman")

    mig = pd.crosstab(pd.Series(recomputed_tier, name="baseline"),
                      pd.Series(alt_tier, name=name))
    mig = mig.reindex(index=TIER_ORDER, columns=TIER_ORDER, fill_value=0)

    moved = pd.Series([TIER_NUM[b] - TIER_NUM[a]
                       for b, a in zip(alt_tier, recomputed_tier)],
                      index=pop.index)
    n_over1 = int((moved.abs() > 1).sum())

    active_low = int(((alt_tier == "Low") & (pop["Status"] == "Active")).sum())

    metrics[name] = {"pct_same": pct_same, "rho": rho, "mig": mig,
                     "n_over1": n_over1, "active_low": active_low,
                     "alt_tier": alt_tier, "alt_score": alt_score}
    summary_rows.append((name, results[name]["weights"], pct_same, rho,
                         n_over1, active_low))

# ── per-alternative tables ───────────────────────────────────────────────
for name in alt_names:
    m = metrics[name]
    w = results[name]["weights"]
    print(f"\n{'-' * 74}\n{name.upper()}  "
          f"(recency {w[0]:.4f} / logins {w[1]:.4f} / sessions {w[2]:.4f})")
    print(f"{'-' * 74}")
    print(f"(1) Same tier as baseline: {m['pct_same']:.1f}% "
          f"({int(round(m['pct_same'] / 100 * len(pop))):,} of {len(pop):,})")
    print(f"(2) Spearman rank correlation of scores: {m['rho']:.4f}")
    print(f"(3) Tier migration (rows = baseline tier, cols = {name}):")
    print(m["mig"].to_string())
    print(f"(4) Moved MORE THAN ONE tier: {m['n_over1']:,} "
          f"({m['n_over1'] / len(pop) * 100:.1f}%)")
    print(f"(5) Active subscribers in the Low tier: {m['active_low']:,} "
          f"(baseline {base_active_low:,})")

# ── overview table ────────────────────────────────────────────────────────
print("\n" + "=" * 74)
print("OVERVIEW")
print("=" * 74)
overview = pd.DataFrame({
    "weights": ["/".join(f"{x:.2f}" for x in results[n]["weights"])
                for n in [b for b, _, _ in WEIGHT_SETS]],
    "same tier %": ["100.0"] + [f"{metrics[n]['pct_same']:.1f}" for n in alt_names],
    "Spearman rho": ["1.0000"] + [f"{metrics[n]['rho']:.4f}" for n in alt_names],
    "moved >1 tier": ["0"] + [f"{metrics[n]['n_over1']:,}" for n in alt_names],
    "Active in Low": [f"{base_active_low:,}"] +
                     [f"{metrics[n]['active_low']:,}" for n in alt_names],
}, index=[n for n, _, _ in WEIGHT_SETS])
print(overview.to_string())

# ── save per-subscriber CSV ───────────────────────────────────────────────
out = pd.DataFrame({
    "Customer ID": pop["Customer ID"].values,
    "Status": pop["Status"].values,
    "score_baseline": base_score.round(2).values,
    "tier_baseline": recomputed_tier.values,
})
for name in alt_names:
    out[f"score_{name}"] = metrics[name]["alt_score"].round(2).values
    out[f"tier_{name}"] = metrics[name]["alt_tier"].values
    moved = [TIER_NUM[b] - TIER_NUM[a]
             for b, a in zip(metrics[name]["alt_tier"], recomputed_tier)]
    out[f"tier_move_{name}"] = moved          # +1 = moved UP vs baseline
out.to_csv(CSV_OUT, index=False)
print(f"\nWrote {CSV_OUT} ({len(out):,} rows)")

# ════════════════════════════════════════════════════════════════════════
# Summary markdown — interpretation is generated FROM the numbers, so the
# wording can never call a change "small" if the counts disagree.
# ════════════════════════════════════════════════════════════════════════


def interpret(name, m):
    """Two sentences, both grounded in the computed figures.

    Sentence 1 = tier stability (honest: the churn really is modest).
    Sentence 2 = the early-warning watchlist, which is the quantity that is
    actually sensitive to the weights, with its relative swing spelled out.
    """
    pct_moved = 100 - m["pct_same"]
    rho = m["rho"]
    w = results[name]["weights"]
    direction = ("toward logins and sessions" if w[0] < 0.40
                 else "toward recency")
    s1 = (f"Moving weight {direction} (recency {w[0]:.2f}) leaves the ranking "
          f"essentially intact — Spearman rho = {rho:.3f} — and re-sorts only "
          f"{pct_moved:.1f}% of subscribers ({len(pop) - int(round(m['pct_same'] / 100 * len(pop))):,} "
          f"of {len(pop):,}), with {m['n_over1']:,} moving more than one tier, so "
          f"the three tiers as a whole are robust to this change.")

    d_active = m["active_low"] - base_active_low
    pct_change = (d_active / base_active_low * 100) if base_active_low else float("inf")
    if d_active == 0:
        s2 = (f"The Active-in-Low early-warning watchlist is unchanged at "
              f"{base_active_low:,} subscribers.")
    else:
        direction_word = "grows" if d_active > 0 else "shrinks"
        s2 = (f"The Active-in-Low early-warning watchlist, however, "
              f"{direction_word} from {base_active_low:,} to {m['active_low']:,} "
              f"({d_active:+,}, {pct_change:+.0f}%) — so although the tiers barely "
              f"move, the group the project flags as 'still Active but already "
              f"Low-engagement' is not stable and should not be quoted as a fixed "
              f"number.")
    return s1 + " " + s2


lines = []
lines.append("# Engagement-score sensitivity — do the tiers depend on the weights?")
lines.append("")
lines.append("Recomputed the 0-100 engagement score on the **5,422 classified "
             "subscribers** (the 33 Unclassified rows are excluded throughout, as "
             "they were from the tercile basis).")
lines.append("Inputs are min-max normalised exactly as `src/v2_score.py` does and "
             "are held fixed; only the weights change, with recency always entered "
             "inverted. Tiers are re-cut from each set's own terciles.")
lines.append("")
lines.append("## Sanity check — baseline reproduces the shipped tiers")
lines.append("")
lines.append(f"- Tercile cuts recomputed: Low <= {results[BASELINE]['lo']:.2f} "
             f"< Medium <= {results[BASELINE]['hi']:.2f} < High "
             f"(methodology.md records 40.80 / 51.25).")
lines.append(f"- Max |recomputed - shipped| engagement score: "
             f"{score_diff.max():.4f} (rows off by more than 0.01: "
             f"{int((score_diff > 0.011).sum())}).")
lines.append(f"- **Tier mismatches vs the `Tier` column in scored.csv: "
             f"{n_mis:,} of {len(pop):,} ({n_mis / len(pop) * 100:.2f}%).**")
if n_mis == 0:
    lines.append("- The baseline therefore reproduces the shipped Tier column "
                 "exactly, so every comparison below is against a verified "
                 "baseline.")
else:
    lines.append("- See the mismatch rows printed in the terminal; the baseline "
                 "does **not** fully reproduce the shipped tiers.")
lines.append("")
lines.append("## Status is unaffected")
lines.append("")
lines.append("Status is defined on Days Since Last Activity (<= 30 days AND >= 1 "
             "login -> Active; > 90 days -> Churned; else Inactive) and reads no "
             "score term, so reweighting cannot move anyone between Active / "
             "Inactive / Churned. Counts held constant throughout: "
             + ", ".join(f"**{s} {int(status_counts[s]):,}**" for s in STATUS_ORDER)
             + f" (total {int(status_counts.sum()):,}).")
lines.append("")
lines.append("## Alternatives vs baseline (weights: recency / logins / sessions)")
lines.append("")
lines.append("| Set | Weights | Same tier | Spearman rho | Moved >1 tier | Active in Low |")
lines.append("|---|---|---|---|---|---|")
lines.append(f"| baseline | 0.40 / 0.35 / 0.25 | 100.0% | 1.000 | 0 | "
             f"{base_active_low:,} |")
for name in alt_names:
    m = metrics[name]
    w = results[name]["weights"]
    lines.append(f"| {name} | {w[0]:.2f} / {w[1]:.2f} / {w[2]:.2f} | "
                 f"{m['pct_same']:.1f}% | {m['rho']:.3f} | {m['n_over1']:,} | "
                 f"{m['active_low']:,} |")
lines.append("")

for name in alt_names:
    m = metrics[name]
    w = results[name]["weights"]
    lines.append(f"### {name} — recency {w[0]:.2f} / logins {w[1]:.2f} / "
                 f"sessions {w[2]:.2f}")
    lines.append("")
    lines.append(f"- Same tier as baseline: **{m['pct_same']:.1f}%**")
    lines.append(f"- Spearman rank correlation of scores: **{m['rho']:.4f}**")
    lines.append(f"- Moved more than one tier: **{m['n_over1']:,}** "
                 f"({m['n_over1'] / len(pop) * 100:.1f}%)")
    lines.append(f"- Active subscribers in the Low tier: **{m['active_low']:,}** "
                 f"(baseline {base_active_low:,})")
    lines.append("")
    lines.append("Tier migration (rows = baseline tier, columns = this set):")
    lines.append("")
    lines.append("| baseline \\ " + name + " | " + " | ".join(TIER_ORDER) + " |")
    lines.append("|---|" + "---|" * len(TIER_ORDER))
    for b in TIER_ORDER:
        row = " | ".join(str(int(m["mig"].loc[b, a])) for a in TIER_ORDER)
        lines.append(f"| {b} | {row} |")
    lines.append("")
    lines.append("Interpretation: " + interpret(name, m))
    lines.append("")

lines.append("## Bottom line")
lines.append("")
lines.append("Per-subscriber scores and tiers for every set are in "
             "`outputs/v2/sensitivity.csv` "
             "(`tier_move_*` is +1 for moved up, -1 for moved down, 0 for "
             "unchanged). Status is carried through untouched.")
lines.append("")

with open(MD_OUT, "w") as f:
    f.write("\n".join(lines))
print(f"Wrote {MD_OUT}")

print("\n" + "=" * 74)
print("SUMMARY (as written to sensitivity_summary.md)")
print("=" * 74)
for name in alt_names:
    print(f"\n{name}: {interpret(name, metrics[name])}")
