"""
v2 stage 6 — status/tier views on demographics, genre, tenure, high-value profile
and an independent-validation section.

Reads data/processed/v2/scored.csv. Charts -> outputs/v2/charts/, companion tables
-> outputs/v2/tables/. Every chart carries a title, a one-line takeaway and an
"associations, not causes" line. The 33 Unclassified rows are excluded from all
tier- and status-based charts/tables and reported separately. Any group with fewer
than 100 classified subscribers is flagged "small" in its table, left out of the
chart, and no conclusion is drawn from it.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

sns.set_theme(style="whitegrid")

SCORED = "data/processed/v2/scored.csv"
CHARTS = "outputs/v2/charts"
TABLES = "outputs/v2/tables"
SMALL_N = 100            # groups below this are "small" — table only, no conclusions
ASSOC = "Associations, not causes."

os.makedirs(CHARTS, exist_ok=True)
os.makedirs(TABLES, exist_ok=True)

df = pd.read_csv(SCORED)
CLASS = df[df["Status"] != "Unclassified"].copy()   # 5,422 rows for all charts/tables
UNCLASS = df[df["Status"] == "Unclassified"].copy()  # 33 rows, reported separately
STATUS_ORDER = ["Active", "Inactive", "Churned"]


def save_chart(fig, filename, title, takeaway):
    """Suptitle on top, one-line takeaway (with the association line) under the plot."""
    fig.suptitle(title, fontsize=14, y=1.0)
    fig.text(0.5, -0.03, f"Takeaway: {takeaway} {ASSOC}", ha="center",
             fontsize=9, style="italic")
    fig.savefig(os.path.join(CHARTS, filename), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"chart  {filename}")


def save_table(t, filename):
    t.to_csv(os.path.join(TABLES, filename), index=False)
    print(f"table  {filename}")


def rate_table(data, col, top10=False):
    """Group sizes + Active/Inactive/Churned counts and rates + small flag."""
    counts = pd.crosstab(data[col], data["Status"])
    for s in STATUS_ORDER:
        if s not in counts:
            counts[s] = 0
    counts = counts[STATUS_ORDER]
    counts.columns = ["active_n", "inactive_n", "churned_n"]
    counts["classified_n"] = counts.sum(axis=1)
    counts["active_pct"] = (counts["active_n"] / counts["classified_n"] * 100).round(1)
    counts["inactive_pct"] = (counts["inactive_n"] / counts["classified_n"] * 100).round(1)
    counts["churned_pct"] = (counts["churned_n"] / counts["classified_n"] * 100).round(1)
    counts["small"] = counts["classified_n"] < SMALL_N
    counts = counts.reset_index()
    if top10:
        counts = counts.sort_values("classified_n", ascending=False).head(10)
    if col in ("Occupation", "Education Level", "IncomeBand"):
        counts = counts.sort_values("active_pct", ascending=False)
    elif col == "State":
        pass  # keep top-10-by-size order
    else:
        counts = counts.sort_values("active_pct", ascending=False)
    return counts.reset_index(drop=True)


def plot_rates(tbl, col, filename, title):
    """Grouped bars of Active% and Churned% — small groups excluded from the chart."""
    plot_df = tbl[~tbl["small"]]
    long = plot_df.melt(id_vars=[col], value_vars=["active_pct", "churned_pct"],
                        var_name="Rate", value_name="Percent")
    long["Rate"] = long["Rate"].map({"active_pct": "Active %", "churned_pct": "Churned %"})
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(data=long, x=col, y="Percent", hue="Rate", ax=ax)
    ax.set_ylabel("Rate (% of group)")
    ax.set_xlabel(col)
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="", frameon=False)
    nt = plot_df
    takeaway = (f"Active rate spans {nt['active_pct'].min():.0f}-{nt['active_pct'].max():.0f}% "
                f"(best: {nt.loc[nt['active_pct'].idxmax(), col]}), Churned rate spans "
                f"{nt['churned_pct'].min():.0f}-{nt['churned_pct'].max():.0f}% "
                f"(worst: {nt.loc[nt['churned_pct'].idxmax(), col]}); "
                + ("groups under 100 are table-only and marked small."
                   if tbl["small"].any() else "all groups have n>=100."))
    save_chart(fig, filename, title, takeaway)


# ── (1) Rates by demographics ────────────────────────────────
DIMS = [
    ("IncomeBand", "income_band", "Churned and Active Rate by Income Band"),
    ("Occupation", "occupation", "Churned and Active Rate by Occupation"),
    ("AgeGroup", "age_group", "Churned and Active Rate by Age Group"),
    ("Education Level", "education", "Churned and Active Rate by Education Level"),
    ("Number of Children At Home", "children_home", "Churned and Active Rate by Children At Home"),
    ("State", "state_top10", "Churned and Active Rate by State (Top 10 by Subscribers)"),
]
for col, slug, title in DIMS:
    tbl = rate_table(CLASS, col, top10=(col == "State"))
    save_table(tbl, f"table_rates_{slug}.csv")
    plot_rates(tbl, col, f"rate_by_{slug}.png", title)

# ── (2) Genre mix by status + rates per genre ────────────────
genre_order = CLASS["Genre Preference"].value_counts().index.tolist()
mix_ct = pd.crosstab(CLASS["Status"], CLASS["Genre Preference"]).reindex(STATUS_ORDER)
save_table(mix_ct.reset_index(), "table_genre_mix_by_status.csv")
mix_pct = mix_ct.div(mix_ct.sum(axis=1), axis=0).mul(100)[genre_order]
fig, ax = plt.subplots(figsize=(12, 6))
mix_pct.plot(kind="bar", stacked=True, ax=ax, width=0.7)
ax.set_ylabel("Share of status group (%)")
ax.set_xlabel("")
ax.set_xticklabels(STATUS_ORDER, rotation=0)
ax.legend(title="Genre", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
save_chart(fig, "genre_mix_by_status.png", "Genre Mix by Status",
           "Genre taste is nearly flat across statuses — Fiction is about 20% of every "
           "status group, so preference does not separate Active from Churned.")

genre_tbl = rate_table(CLASS, "Genre Preference")
save_table(genre_tbl, "table_genre_rates.csv")
plot_rates(genre_tbl, "Genre Preference", "genre_rates.png",
           "Active Rate and Churned Rate per Genre")

# ── (3) Status mix by tenure band (cross-sectional) ──────────
BAND_LABELS = ["0-6", "7-12", "13-24", "25-48", "49+"]
CLASS["Tenure Band"] = pd.cut(CLASS["Subscription Tenure Months"],
                              bins=[-1, 6, 12, 24, 48, 1000], labels=BAND_LABELS)
band_counts = pd.crosstab(CLASS["Tenure Band"], CLASS["Status"]).reindex(BAND_LABELS)
band_counts.columns = [c.lower() + "_n" for c in band_counts.columns]
band_tbl = band_counts.copy()
band_tbl["classified_n"] = band_tbl.sum(axis=1)
for s in STATUS_ORDER:
    band_tbl[s.lower() + "_pct"] = (band_tbl[s.lower() + "_n"] / band_tbl["classified_n"] * 100).round(1)
band_tbl["small"] = band_tbl["classified_n"] < SMALL_N
band_tbl = band_tbl.reset_index()
save_table(band_tbl, "table_status_by_tenure_band.csv")

fig, ax = plt.subplots(figsize=(11, 6))
x = range(len(BAND_LABELS))
w = 0.27
for i, s in enumerate(STATUS_ORDER):
    ax.bar([xi + (i - 1) * w for xi in x],
           band_tbl[s.lower() + "_pct"], width=w, label=s)
ax.set_xticks(list(x))
ax.set_xticklabels(BAND_LABELS)
ax.set_xlabel("Subscription tenure (months)")
ax.set_ylabel("Share of band (%)")
ax.legend(title="", frameon=False)
save_chart(fig, "status_mix_by_tenure_band.png", "Status Mix by Tenure Band",
           "Status mix is similar across tenure bands (no monotone pattern), and this is a "
           "CROSS-SECTIONAL comparison, NOT a retention curve — the data has no cancellation "
           "dates, so it cannot show how any cohort's status changes over time.")

# ── (4) High-value profile: Active + High tier vs Churned ────
hv = CLASS[(CLASS["Status"] == "Active") & (CLASS["Tier"] == "High")].copy()
ch = CLASS[CLASS["Status"] == "Churned"].copy()
# Age comes from data/processed/clean.csv's Birth Date at reference date 2026-10-02
# (clean.csv carries no literal Age column — derived here so all outputs agree)
REF = pd.Timestamp("2026-10-02")
for g in (hv, ch):
    g["Age"] = (REF - pd.to_datetime(g["Birth Date"])).dt.days / 365.25

NUMERIC = ["Age", "Annual Income", "Avg Monthly Spend", "Number of Children At Home"]
num_tbl = pd.DataFrame({
    f"High-value (n={len(hv)})": hv[NUMERIC].mean().round(1),
    f"Churned (n={len(ch)})": ch[NUMERIC].mean().round(1),
})
num_tbl.columns.name = "Variable"
num_tbl["Difference"] = (num_tbl.iloc[:, 0] - num_tbl.iloc[:, 1]).round(1)
save_table(num_tbl.reset_index().rename(columns={"index": "Variable"}),
           "table_high_value_numeric.csv")

fig, axes = plt.subplots(2, 2, figsize=(11, 8))
for ax, m in zip(axes.ravel(), NUMERIC):
    vals = [hv[m].mean(), ch[m].mean()]
    sns.barplot(x=["High-value", "Churned"], y=vals, ax=ax, hue=["High-value", "Churned"],
                legend=False, palette=["#2a9d8f", "#e76f51"])
    ax.set_title(f"Mean {m}")
    ax.set_ylabel("Mean")
    ax.set_xlabel("")
fig.tight_layout()
save_chart(fig, "high_value_numeric.png", "High-Value vs Churned — Numeric Profile",
           f"High-value subscribers average ${hv['Annual Income'].mean():,.0f} income and "
           f"${hv['Avg Monthly Spend'].mean():.0f}/month spend vs ${ch['Annual Income'].mean():,.0f} "
           f"and ${ch['Avg Monthly Spend'].mean():.0f} for Churned, on {hv['Age'].mean():.0f} vs "
           f"{ch['Age'].mean():.0f} years and {hv['Number of Children At Home'].mean():.1f} vs "
           f"{ch['Number of Children At Home'].mean():.1f} children at home.")

CATEG = ["AgeGroup", "Occupation", "Education Level", "Genre Preference"]
rows = []
for col in CATEG:
    p_hv = hv[col].value_counts(normalize=True).mul(100).round(1)
    p_ch = ch[col].value_counts(normalize=True).mul(100).round(1)
    comp = pd.DataFrame({"High-value %": p_hv, "Churned %": p_ch}).fillna(0)
    comp["Difference"] = (comp["High-value %"] - comp["Churned %"]).round(1)
    part = comp.reset_index().rename(columns={"index": col})
    part.insert(0, "Variable", col)
    part = part.rename(columns={col: "Group"})
    rows.append(part)
categ_tbl = pd.concat(rows, ignore_index=True)
save_table(categ_tbl, "table_high_value_categorical.csv")

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
for ax, col in zip(axes.ravel(), CATEG):
    p_hv = hv[col].value_counts(normalize=True).mul(100)
    p_ch = ch[col].value_counts(normalize=True).mul(100)
    comp = pd.DataFrame({"High-value": p_hv, "Churned": p_ch}).fillna(0)
    comp = comp.sort_values("High-value", ascending=False)
    comp.plot(kind="bar", ax=ax, color=["#2a9d8f", "#e76f51"], width=0.8)
    ax.set_title(col)
    ax.set_ylabel("% of group")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(fontsize=8)
fig.tight_layout()
save_chart(fig, "high_value_categorical.png", "High-Value vs Churned — Age, Occupation, Education, Genre",
           "High-value subscribers skew Professional and aged 1960-1969 more than Churned, "
           "while top genres (Fiction/Romance) are similar in both groups.")

# ── (5) Validation: independent checks ───────────────────────
tier_means = (CLASS.groupby("Tier", observed=True)[["Books Accessed", "Subscription Tenure Months"]]
              .mean().reindex(["Low", "Medium", "High"]).round(2))
save_table(tier_means.reset_index(), "table_validation_tier_independent.csv")

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, m in zip(axes, ["Books Accessed", "Subscription Tenure Months"]):
    sns.barplot(x=tier_means.index, y=tier_means[m], ax=ax,
                hue=tier_means.index, legend=False, palette="viridis")
    ax.set_title(f"Mean {m} by Tier")
    ax.set_ylabel("Mean")
    ax.set_xlabel("")
fig.tight_layout()
save_chart(fig, "validation_tier_books_tenure.png",
           "Validation — Books Accessed and Tenure by Tier (independent of the score)",
           "Books and tenure are NOT score inputs, so their rise across Low->High tiers is a "
           "valid independent check of the score; tier-by-logins would be circular because "
           "logins and session minutes ARE score inputs.")

status_means = (CLASS.groupby("Status")[["Avg Logins Per Month", "Avg Session Minutes"]]
                .mean().reindex(STATUS_ORDER).round(2))
save_table(status_means.reset_index(), "table_validation_status_behaviour.csv")

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, m in zip(axes, ["Avg Logins Per Month", "Avg Session Minutes"]):
    sns.barplot(x=status_means.index, y=status_means[m], ax=ax,
                hue=status_means.index, legend=False, palette="mako")
    ax.set_title(f"Mean {m} by Status")
    ax.set_ylabel("Mean")
    ax.set_xlabel("")
fig.tight_layout()
save_chart(fig, "validation_status_logins_session.png",
           "Validation — Logins and Session Minutes by Status",
           "Status bands are defined on recency (logins only enter as a >=1 guard), so these "
           "behaviour means by status are a near-independent check; the same comparison BY TIER "
           "is circular because logins and session minutes are score inputs — and note "
           "tier-vs-status agreement is partly by construction.")

# ── Unclassified reported separately ─────────────────────────
un_tbl = pd.DataFrame([{
    "Rows": len(UNCLASS),
    "Tier split (Low/Med/High)": "/".join(
        str(int((UNCLASS["Tier"] == t).sum())) for t in ["Low", "Medium", "High"]),
    "Mean logins": round(UNCLASS["Avg Logins Per Month"].mean(), 2),
    "Mean session min": round(UNCLASS["Avg Session Minutes"].mean(), 2),
    "Mean books": round(UNCLASS["Books Accessed"].mean(), 2),
    "Mean income": round(UNCLASS["Annual Income"].mean(), 0),
    "Mean spend": round(UNCLASS["Avg Monthly Spend"].mean(), 1),
}])
save_table(un_tbl, "table_unclassified_reported_separately.csv")

# ── Biggest differences, plain English ───────────────────────
print("\nBiggest differences — high-value (Active+High, n=%d) vs Churned (n=%d):"
      % (len(hv), len(ch)))
inc_hv, inc_ch = hv["Annual Income"].mean(), ch["Annual Income"].mean()
sp_hv, sp_ch = hv["Avg Monthly Spend"].mean(), ch["Avg Monthly Spend"].mean()
ch_hv, ch_ch = hv["Number of Children At Home"].mean(), ch["Number of Children At Home"].mean()
ag_hv, ag_ch = hv["Age"].mean(), ch["Age"].mean()
print(f"- Money: high-value average ${inc_hv:,.0f} a year vs ${inc_ch:,.0f} for churned "
      f"({(inc_hv / inc_ch - 1) * 100:.0f}% higher) and spend ${sp_hv:.0f}/month vs "
      f"${sp_ch:.0f} ({(sp_hv / sp_ch - 1) * 100:.0f}% more).")
print(f"- Life stage: age {ag_hv:.0f} vs {ag_ch:.0f} on average "
      f"(high-value are {ag_hv - ag_ch:+.1f} years) with {ch_hv:.1f} vs {ch_ch:.1f} "
      f"children at home.")
for col in CATEG:
    p_hv = hv[col].value_counts(normalize=True).mul(100)
    p_ch = ch[col].value_counts(normalize=True).mul(100)
    comp = pd.DataFrame({"hv": p_hv, "ch": p_ch}).fillna(0)
    d = (comp["hv"] - comp["ch"]).abs()
    top = d.idxmax()
    print(f"- {col}: '{top}' differs most — {comp.loc[top, 'hv']:.0f}% of high-value "
          f"vs {comp.loc[top, 'ch']:.0f}% of churned ({d[top]:+.0f} points).")

# ── Significance checks: Active+High vs Churned ──────────────
def cohens_d(a, b):
    """Pooled-SD Cohen's d for two independent samples."""
    d = (((len(a) - 1) * a.std(ddof=1) ** 2 + (len(b) - 1) * b.std(ddof=1) ** 2)
         / (len(a) + len(b) - 2)) ** 0.5
    return (a.mean() - b.mean()) / d


def effect_words(size, label):
    """Plain-English effect line using 0.2 / 0.5 / 0.8 thresholds (on the
    rounded value, so the word always matches the number shown)."""
    size = round(float(size), 2)
    a = abs(size)
    word = ("negligible" if a < 0.2 else "small" if a < 0.5
            else "medium" if a < 0.8 else "large")
    return f"{word} effect ({label}={size:.2f})"


sig_rows = []
for var in ["Annual Income", "Avg Monthly Spend", "Age", "Number of Children At Home"]:
    a, b = hv[var], ch[var]
    _, p = stats.ttest_ind(a, b, equal_var=False)          # Welch t-test
    d = cohens_d(a, b)
    sig_rows.append({
        "comparison": var,
        "high_value": round(a.mean(), 2),
        "churned": round(b.mean(), 2),
        "difference": round(a.mean() - b.mean(), 2),
        "difference_unit": "mean difference",
        "test": "Welch t-test",
        "p_value": float(f"{p:.3g}"),
        "effect_size": round(d, 3),
        "effect_size_type": "Cohen's d",
        "plain_english": effect_words(d, "d"),
    })

for col, cat in [("Occupation", "Management"), ("Education Level", "Graduate Degree"),
                 ("AgeGroup", "1960-1969"), ("Genre Preference", "Fantasy")]:
    hp = (hv[col] == cat).mean() * 100
    cp = (ch[col] == cat).mean() * 100
    table = [[int((hv[col] == cat).sum()), int((hv[col] != cat).sum())],
             [int((ch[col] == cat).sum()), int((ch[col] != cat).sum())]]
    chi2, p, _, _ = stats.chi2_contingency(table)
    v = (chi2 / (len(hv) + len(ch))) ** 0.5                  # Cramer's V for a 2x2 table
    sig_rows.append({
        "comparison": f"{col}: {cat}",
        "high_value": round(hp, 1),
        "churned": round(cp, 1),
        "difference": round(hp - cp, 1),
        "difference_unit": "percentage points",
        "test": "chi-square",
        "p_value": float(f"{p:.3g}"),
        "effect_size": round(v, 3),
        "effect_size_type": "Cramér's V",
        "plain_english": effect_words(v, "V"),
    })

sig_rows.append({
    "comparison": "(note)",
    "high_value": len(hv), "churned": len(ch), "difference": "",
    "difference_unit": "", "test": "", "p_value": "", "effect_size": "",
    "effect_size_type": "",
    "plain_english": ("With these sample sizes (n=1803 vs 901) small gaps can be "
                      "significant while still being practically small — read the "
                      "effect size, not just the p-value."),
})
sig_tbl = pd.DataFrame(sig_rows)
sig_tbl.to_csv("outputs/v2/significance_checks.csv", index=False)
print("\noutputs/v2/significance_checks.csv:")
print(sig_tbl.to_string(index=False))

# ── BUILD_LOG note (idempotent — skipped if this stage is already logged) ──
with open("outputs/v2/BUILD_LOG.md") as f:
    existing = f.read()
if "## Stage 6 — segment views" not in existing:
    with open("outputs/v2/BUILD_LOG.md", "a") as f:
        f.write("\n## Stage 6 — segment views\n"
                "- Wrote `src/v2_segments.py`: rate-by-demographic charts + tables, genre mix and "
                "rates, tenure-band status mix (labelled cross-sectional, not a retention curve), "
                "the Active+High vs Churned profile, and the validation section (books/tenure by "
                "tier, logins/session by status).\n"
                "- The 33 Unclassified rows are out of every tier/status chart and have their own "
                "small table; the only group under 100 subscribers is Genre 'Unknown' (54), which "
                "is table-only and marked small.\n"
                "- Every caption carries the associations-not-causes line; methodology.md section 7 "
                "now states which comparisons are circular and which are the independent checks.\n"
                "- Biggest gaps printed: high-value vs churned differ most on money (income/spend), "
                "age and occupation share.\n")
    print("\nBUILD_LOG stage 6 appended.")
print("13 charts in outputs/v2/charts/, tables in outputs/v2/tables/.")
