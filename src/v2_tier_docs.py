"""Stage 1 gap-closer: tier-cutoff rationale, status-vs-score justification,
status x tier table, Active-Low watchlist, and the behaviour-by-tier chart.

Reads data/processed/v2/scored.csv; writes:
  - outputs/v2/watchlist.csv            (row-level early-warning subscribers)
  - outputs/v2/charts/bar_behaviour_by_tier.png
  - inserts (idempotently) the approved text + tables into outputs/v2/methodology.md

No threshold, weight, scoring/status logic, cleaning code or scored.csv number
is touched — this script only reads them.
"""

import os

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCORED = os.path.join(ROOT, "data", "processed", "v2", "scored.csv")
METH = os.path.join(ROOT, "outputs", "v2", "methodology.md")
WATCH = os.path.join(ROOT, "outputs", "v2", "watchlist.csv")
CHART = os.path.join(ROOT, "outputs", "v2", "charts",
                     "bar_behaviour_by_tier.png")

# approved wording (owner's text — reproduced verbatim)
JUSTIFICATION = (
    "Status is defined on recency (plus a minimum-1-login guard), not on the score, "
    "because (1) the rules had to be written and approved before the score existed, "
    "(2) the score already contains recency at 40%, so using both would count recency "
    "twice, and (3) recency is the most direct and easily explained signal of leaving. "
    "The score is used afterwards to rank engagement and in the status-by-tier table."
)
TIER_RATIONALE = (
    "Tiers use terciles of the engagement score (Low up to the lower cut {lo}, "
    "Medium up to the upper cut {hi}, High above). Reasons: fixed numbers such as "
    "33/66 would be arbitrary; equal-sized thirds guarantee no lopsided tier; cutoffs "
    "come from the data rather than numbers we chose. Limitation: tiers are relative "
    "to this subscriber population, not absolute standards."
)
CHART_CAPTION = (
    "books and tenure are independent of the score while recency, logins and session "
    "minutes are score inputs, so the gradient in those three is partly by construction"
)

TIER_ORDER = ["Low", "Medium", "High"]
STATUS_ORDER = ["Active", "Inactive", "Churned", "Unclassified"]
METRICS = [("Days Since Last Activity", "Mean days since activity"),
           ("Avg Logins Per Month", "Mean logins / month"),
           ("Avg Session Minutes", "Mean session minutes"),
           ("Books Accessed", "Mean books accessed")]


def load():
    s = pd.read_csv(SCORED)
    cls = s[s["Status"] != "Unclassified"]
    cuts = cls["Engagement Score"].quantile([1 / 3, 2 / 3])
    return s, cls, float(cuts.iloc[0]), float(cuts.iloc[1])


def watchlist_rows(s):
    """Active subscribers sitting in the Low tier — the early-warning group."""
    cols = ["Customer ID", "Status", "Tier", "Engagement Score",
            "Days Since Last Activity", "Avg Logins Per Month",
            "Avg Session Minutes", "Books Accessed"]
    wl = s[(s["Status"] == "Active") & (s["Tier"] == "Low")][cols]
    return wl.sort_values("Engagement Score")


def status_tier_table(s):
    ct = pd.crosstab(s["Status"], s["Tier"]).reindex(index=STATUS_ORDER,
                                                      columns=TIER_ORDER)
    ct["Total"] = ct.sum(axis=1)
    return ct


def watchlist_summary(wl):
    return {
        "n": len(wl),
        "recency": wl["Days Since Last Activity"].mean(),
        "logins": wl["Avg Logins Per Month"].mean(),
        "session": wl["Avg Session Minutes"].mean(),
        "books": wl["Books Accessed"].mean(),
    }


def make_tier_chart():
    """Four small panels: mean recency/logins/session/books by tier (classified)."""
    s = pd.read_csv(SCORED)
    cls = s[s["Status"] != "Unclassified"]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.4))
    for ax, (col, title) in zip(axes, METRICS):
        means = cls.groupby("Tier")[col].mean().reindex(TIER_ORDER)
        bars = ax.bar(TIER_ORDER, means.values, color="#3f4de6", width=0.62)
        fmt = "{:.1f}" if col == "Days Since Last Activity" else "{:.2f}" \
            if col == "Avg Logins Per Month" else "{:.1f}"
        ax.bar_label(bars, fmt=fmt, padding=3, fontsize=9, fontweight="bold")
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.set_ylim(0, means.max() * 1.18)
        ax.tick_params(labelsize=9)
    fig.suptitle("Mean engagement metrics by tier (classified rows — the 33 "
                 "Unclassified are excluded)", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    return fig


# ── methodology.md updates (idempotent) ────────────────────────
def _md_table(df, index_name):
    head = "| " + index_name + " | " + " | ".join(df.columns) + " |"
    sep = "|" + "---|" * (len(df.columns) + 1)
    rows = ["| " + str(i) + " | " + " | ".join(str(v) for v in r) + " |"
            for i, r in zip(df.index, df.values)]
    return "\n".join([head, sep] + rows)


def update_methodology(s, lo, hi, wl, ct):
    with open(METH) as f:
        meth = f.read()
    if "Tiers use terciles of the engagement score" in meth:
        print("methodology.md already updated — skipping")
        return meth

    # ── section 2: justification + watchlist table ──
    anchor2 = ("- Tenure is deliberately **not** used in the status rule — a "
               "72-month subscriber can churn this month, and a 1-month "
               "subscriber can be active.")
    assert meth.count(anchor2) == 1, "section 2 anchor not found"
    wsum = watchlist_summary(wl)
    watch_md = "\n".join([
        "| Group | Count | Mean recency (days) | Mean logins | Mean session minutes | Mean books |",
        "|---|---|---|---|---|---|",
        f"| Active subscribers in the Low tier (early-warning group) | "
        f"{wsum['n']} | {wsum['recency']:.1f} | {wsum['logins']:.2f} | "
        f"{wsum['session']:.1f} | {wsum['books']:.1f} |",
    ])
    block2 = (
        anchor2
        + "\n\n### Why status is not defined on the score\n\n"
        + JUSTIFICATION
        + "\n\n**Watchlist — Active subscribers in the Low tier** "
        + "(early-warning group: they are still Active today but their score says "
        + "their engagement is already Low; the individual rows are saved in "
        + "`outputs/v2/watchlist.csv`):\n\n"
        + watch_md + "\n"
    )
    meth = meth.replace(anchor2, block2, 1)

    # ── section 7: justification + status x tier + tier cutoffs + chart ──
    anchor7 = ("Unclassified rows are excluded from tier-based charts and tables "
               "and shown separately.")
    assert meth.count(anchor7) == 1, "section 7 anchor not found"
    chart_path = "outputs/v2/charts/bar_behaviour_by_tier.png"
    block7 = (
        anchor7
        + "\n\n### Why status is not defined on the score\n\n"
        + JUSTIFICATION
        + "\n\n**Status x tier (subscribers; computed from "
        + "`data/processed/v2/scored.csv`):**\n\n"
        + _md_table(ct, "Status")
        + "\n\n### Tier cutoffs — why terciles\n\n"
        + TIER_RATIONALE.format(lo=f"({lo:.2f})", hi=f"({hi:.2f})")
        + "\n\n**Behaviour by tier chart** — `" + chart_path + "` (four panels: "
        + "mean recency, logins, session minutes, books by tier, Unclassified "
        + "excluded). Caption: " + CHART_CAPTION + ".\n"
    )
    meth = meth.replace(anchor7, block7, 1)

    with open(METH, "w") as f:
        f.write(meth)
    print("methodology.md updated (2 justifications, 2 tables, tier rationale, "
          "chart reference)")
    return meth


def main():
    s, cls, lo, hi = load()
    wl = watchlist_rows(s)
    wl.to_csv(WATCH, index=False)
    print(f"watchlist.csv: {len(wl)} rows -> {WATCH}")
    ct = status_tier_table(s)
    update_methodology(s, lo, hi, wl, ct)
    fig = make_tier_chart()
    fig.savefig(CHART, dpi=120, bbox_inches="tight")
    print(f"chart -> {CHART}")
    print("cuts:", f"Low <= {lo:.2f} < Medium <= {hi:.2f} < High")
    print("status x tier:\n", ct)


if __name__ == "__main__":
    main()
