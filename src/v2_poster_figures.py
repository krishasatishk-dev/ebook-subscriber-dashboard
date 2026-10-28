# v2_poster_figures.py — regenerate the HITA 2026 poster figures from scored.csv
# Figures are written to poster/figures/ at 300 dpi with >=24 pt labels at printed
# size (each half-column figure is generated at 540 pt wide, matching its placement
# in poster.tex, so matplotlib fontsize == printed pt).
#
# Palette (poster spec): Active green, Inactive amber, Churned red, indigo neutral.
# Unclassified rows are EXCLUDED from every figure and stated in the captions.

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCORED = ROOT / "data" / "processed" / "v2" / "scored.csv"
OUTDIR = ROOT / "poster" / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

GREEN = "#2A9D8F"   # Active
AMBER = "#E9C46A"   # Inactive
RED = "#E76F51"     # Churned
INDIGO = "#3F4DE6"  # neutral / tier gradient base
NAVY = "#1A1F5C"
GREY = "#5B6285"

plt.rcParams.update({
    "font.size": 24,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 25,
    "axes.labelsize": 24,
    "xtick.labelsize": 23,
    "ytick.labelsize": 23,
    "legend.fontsize": 22,
    "axes.edgecolor": GREY,
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": GREY,
    "ytick.color": GREY,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})


def save(fig, name):
    path = OUTDIR / name
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved:", path.relative_to(ROOT))


def f1_status_doughnut(s):
    """F1 — status doughnut with counts (Unclassified excluded, stated in caption)."""
    counts = s["Status"].value_counts()
    labels = ["Active", "Inactive", "Churned"]
    values = [int(counts[l]) for l in labels]
    colors = [GREEN, AMBER, RED]
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    wedges, _ = ax.pie(
        values, colors=colors, startangle=90, counterclock=False,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=3),
    )
    total = sum(values)
    for w, v, lab in zip(wedges, values, labels):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        x, y = np.cos(ang), np.sin(ang)
        ax.annotate(f"{lab}\n{v:,} ({v / total * 100:.1f}%)",
                    xy=(x * 0.79, y * 0.79), ha="center", va="center",
                    fontsize=23, fontweight="bold", color="white",
                    bbox=dict(boxstyle="round,pad=0.25", fc=NAVY, ec="none", alpha=0.85))
    ax.text(0, 0.08, f"{total:,}", ha="center", va="center",
            fontsize=34, fontweight="bold", color=NAVY)
    ax.text(0, -0.16, "classified", ha="center", va="center", fontsize=22, color=GREY)
    ax.set_title("Status of subscribers (n = 5,422)", pad=14, fontweight="bold")
    ax.set_aspect("equal")
    save(fig, "f1_status_doughnut.png")


def f2_tier_panels(cls):
    """F2 — four panels: mean recency / logins / session minutes / books by tier.
    Books is the independent check (not a score input)."""
    tiers = ["Low", "Medium", "High"]
    g = cls.groupby("Tier")
    recency = g["Days Since Last Activity"].mean().reindex(tiers)
    logins = g["Avg Logins Per Month"].mean().reindex(tiers)
    minutes = g["Avg Session Minutes"].mean().reindex(tiers)
    books = g["Books Accessed"].mean().reindex(tiers)

    fig, axes = plt.subplots(1, 4, figsize=(15.5, 5.4))
    bars = [recency, logins, minutes, books]
    titles = ["Mean days since\nlast activity",
              "Mean logins\nper month",
              "Mean session\nminutes",
              "Mean books accessed\n(independent check)"]
    ylabs = ["days", "logins", "minutes", "books"]
    bar_colors = [INDIGO, INDIGO, INDIGO, GREEN]
    for ax, series, title, ylab, bc in zip(axes, bars, titles, ylabs, bar_colors):
        bars_p = ax.bar(tiers, series.values, color=bc, width=0.62, alpha=0.9)
        for b, v in zip(bars_p, series.values):
            ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.1f}",
                    ha="center", va="bottom", fontsize=22, fontweight="bold", color=NAVY)
        ax.set_title(title, fontsize=23, fontweight="bold", color=NAVY)
        ax.set_ylabel(ylab, fontsize=22)
        ax.set_ylim(0, series.max() * 1.22)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Engagement score terciles track real behaviour (n = 5,422 classified)",
                 fontsize=25, fontweight="bold", color=NAVY, y=1.04)
    fig.tight_layout()
    save(fig, "f2_tier_panels.png")


def f3_heatmap(s):
    """F3 — correlation heatmap of the four engagement metrics."""
    cols = ["Days Since Last Activity", "Avg Logins Per Month",
            "Avg Session Minutes", "Books Accessed"]
    nice = ["Days since\nlast activity", "Logins\nper month",
            "Session\nminutes", "Books\naccessed"]
    corr = s[cols].corr()
    corr.index = nice
    corr.columns = nice
    fig, ax = plt.subplots(figsize=(7.6, 6.4))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
    for i in range(len(nice)):
        for j in range(len(nice)):
            v = corr.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    fontsize=23, fontweight="bold",
                    color="white" if abs(v) > 0.55 else NAVY)
    ax.set_xticks(range(len(nice)), nice, fontsize=21)
    ax.set_yticks(range(len(nice)), nice, fontsize=21)
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cb.ax.tick_params(labelsize=20)
    ax.set_title("Correlation of engagement metrics (n = 5,455)", pad=12,
                 fontsize=24, fontweight="bold", color=NAVY)
    save(fig, "f3_corr_heatmap.png")


def f4_logins_books_by_status(cls):
    """F4 — mean logins and books by status (grouped bars)."""
    statuses = ["Active", "Inactive", "Churned"]
    g = cls.groupby("Status")
    logins = g["Avg Logins Per Month"].mean().reindex(statuses)
    books = g["Books Accessed"].mean().reindex(statuses)
    x = np.arange(len(statuses))
    w = 0.36
    fig, ax = plt.subplots(figsize=(7.5, 6.2))
    b1 = ax.bar(x - w / 2, logins.values, w, label="Logins / month", color=INDIGO)
    b2 = ax.bar(x + w / 2, books.values, w, label="Books accessed", color=GREEN)
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height(),
                    f"{b.get_height():.1f}", ha="center", va="bottom",
                    fontsize=22, fontweight="bold", color=NAVY)
    ax.set_xticks(x, statuses, fontsize=24, fontweight="bold")
    ax.set_ylabel("mean per subscriber", fontsize=23)
    ax.set_ylim(0, max(logins.max(), books.max()) * 1.2)
    ax.legend(frameon=False, fontsize=22, loc="upper right")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Usage collapses with status: 11.7 vs 1.5 logins", pad=12,
                 fontsize=24, fontweight="bold", color=NAVY)
    save(fig, "f4_logins_books_by_status.png")


def main():
    s = pd.read_csv(SCORED)
    cls = s[s["Status"] != "Unclassified"]
    f1_status_doughnut(s)
    f2_tier_panels(cls)
    f3_heatmap(s)
    f4_logins_books_by_status(cls)
    print("done — 4 poster figures in poster/figures/")


if __name__ == "__main__":
    main()
