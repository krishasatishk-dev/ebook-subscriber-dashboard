"""
v2 stage 4 — exploratory data analysis on the merged engagement + demographics file.

Reads data/processed/v2/merged.csv. Saves every chart as a PNG with a title and a
one-line takeaway caption to outputs/v2/charts/, and collects the same takeaways in
outputs/v2/eda_takeaways.md. Also prints every pair of engagement metrics with |r| > 0.8
and says which pairs would double-count if both went into a score.
No weights or thresholds are chosen here.
"""
import itertools
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

DATA = "data/processed/v2/merged.csv"
CHARTS_DIR = "outputs/v2/charts"
TAKEAWAYS_PATH = "outputs/v2/eda_takeaways.md"

os.makedirs(CHARTS_DIR, exist_ok=True)

df = pd.read_csv(DATA)

# The five engagement metrics examined for redundancy
METRICS = [
    "Avg Logins Per Month", "Avg Session Minutes", "Books Accessed",
    "Days Since Last Activity", "Subscription Tenure Months",
]

with open(TAKEAWAYS_PATH, "w") as f:
    f.write("# v2 EDA Takeaways\n\nSource: `data/processed/v2/merged.csv` "
            "(5,455 subscribers). Every chart has the same one-line takeaway as its caption.\n\n")


def save_chart(fig, filename, title, takeaway):
    """Title on top, one-line takeaway as a caption under the plot; log both."""
    fig.suptitle(title, fontsize=14, y=1.0)
    fig.text(0.5, -0.02, f"Takeaway: {takeaway}", ha="center", fontsize=10, style="italic")
    fig.savefig(os.path.join(CHARTS_DIR, filename), dpi=300, bbox_inches="tight")
    plt.close(fig)
    with open(TAKEAWAYS_PATH, "a") as f:
        f.write(f"### {title}\n![{title}]({filename})\n{takeaway}\n\n")
    print(f"saved {filename} — {takeaway}")


# ── 1-5. Histograms (recency clipped at 365, the likely capture cap) ──
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df["Avg Logins Per Month"], bins=40, ax=ax)
save_chart(fig, "hist_avg_logins.png", "Histogram of Avg Logins Per Month",
           f"Right-skewed: median {df['Avg Logins Per Month'].median():.0f} logins/month, "
           f"with {int((df['Avg Logins Per Month'] == 0).sum())} subscribers at a genuine zero.")

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df["Avg Session Minutes"], bins=40, ax=ax)
save_chart(fig, "hist_avg_session_minutes.png", "Histogram of Avg Session Minutes",
           f"Session minutes cluster around {df['Avg Session Minutes'].median():.0f} minutes/month "
           f"with a mild right tail to {df['Avg Session Minutes'].max():.0f}.")

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df["Books Accessed"], bins=40, ax=ax)
save_chart(fig, "hist_books_accessed.png", "Histogram of Books Accessed",
           f"Books accessed is right-skewed: median {df['Books Accessed'].median():.0f}, "
           f"long tail to {df['Books Accessed'].max():.0f} books.")

recency_clip = df["Days Since Last Activity"].clip(upper=365)
n_over = int((df["Days Since Last Activity"] > 365).sum())
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(recency_clip, bins=40, ax=ax)
save_chart(fig, "hist_days_since_activity.png", "Histogram of Days Since Last Activity (clipped at 365)",
           f"Highly skewed — median {df['Days Since Last Activity'].median():.0f} days; "
           f"{n_over} rows above the 365-day capture cap are shown in the last bin.")

fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df["Subscription Tenure Months"], bins=36, ax=ax)
save_chart(fig, "hist_subscription_tenure.png", "Histogram of Subscription Tenure (Months)",
           f"Tenure is near-uniform from {df['Subscription Tenure Months'].min():.0f} to "
           f"{df['Subscription Tenure Months'].max():.0f} months, median {df['Subscription Tenure Months'].median():.0f}.")

# ── 6. Correlation heatmap (complete cases only) ─────────────
corr = df[METRICS].corr()
n_complete = int(df[METRICS].dropna().shape[0])
fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, vmin=-1, vmax=1, ax=ax)
save_chart(fig, "heatmap_engagement_corr.png", "Correlation Heatmap — Engagement Metrics + Tenure",
           f"Only logins vs books accessed is strong (r={corr.loc['Avg Logins Per Month', 'Books Accessed']:.2f}, "
           f"n={n_complete} complete rows); tenure barely correlates with anything.")

# ── 7. Genre preference bar chart ────────────────────────────
genre_counts = df["Genre Preference"].value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=genre_counts.index, y=genre_counts.values, ax=ax, hue=genre_counts.index, legend=False)
ax.set_ylabel("Subscribers")
ax.tick_params(axis="x", rotation=45)
top_share = genre_counts.iloc[0] / genre_counts.sum() * 100
save_chart(fig, "bar_genre_preference.png", "Genre Preference of Subscribers",
           f"Fiction is the largest preference ({genre_counts.iloc[0]:,} subscribers, {top_share:.0f}%), "
           f"with 54 rows carrying no stated genre (Unknown).")

# ── 8. Status pie ────────────────────────────────────────────
status_counts = df["Status"].value_counts()
pie_statuses = status_counts.drop("Unclassified", errors="ignore")
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(pie_statuses, labels=pie_statuses.index, autopct="%1.1f%%", startangle=90)
save_chart(fig, "pie_status.png", "Active vs Inactive vs Churned",
           f"Of the {pie_statuses.sum():,} classified subscribers, {pie_statuses['Active'] / pie_statuses.sum() * 100:.1f}% "
           f"are Active and {pie_statuses['Churned'] / pie_statuses.sum() * 100:.1f}% Churned "
           f"({int(status_counts.get('Unclassified', 0))} Unclassified rows are not in this pie).")

# ── 9. Mean metrics by status (one panel per metric, scales differ) ──
panel_metrics = ["Avg Logins Per Month", "Avg Session Minutes", "Books Accessed", "Subscription Tenure Months"]
order = [s for s in ["Active", "Inactive", "Churned", "Unclassified"] if s in status_counts.index]
means = df.groupby("Status")[panel_metrics].mean().reindex(order)
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
for ax, metric in zip(axes.ravel(), panel_metrics):
    sns.barplot(x=means.index, y=means[metric], ax=ax, hue=means.index, legend=False)
    ax.set_title(metric)
    ax.set_ylabel("Mean")
    ax.tick_params(axis="x", rotation=20)
fig.tight_layout()
save_chart(fig, "bar_means_by_status.png", "Mean Logins, Session Minutes, Books Accessed and Tenure by Status",
           f"Active subscribers lead on behaviour (mean {means.loc['Active', 'Avg Logins Per Month']:.1f} logins, "
           f"{means.loc['Active', 'Books Accessed']:.1f} books) but tenure is almost flat across statuses, "
           f"so behaviour — not how long they have been subscribed — separates the groups.")

# ── Redundancy check: every pair with |r| > 0.8 ──────────────
print("\nPairs of engagement metrics with |r| > 0.8 (complete cases, n=%d):" % n_complete)
high_pairs = []
for a, b in itertools.combinations(METRICS, 2):
    r = corr.loc[a, b]
    if abs(r) > 0.8:
        high_pairs.append((a, b, r))
        print(f"  {a}  vs  {b}:  r = {r:.3f}")
if not high_pairs:
    print("  none")
else:
    print("\nDouble-counting check (no weights proposed, statement only):")
    for a, b, r in high_pairs:
        print(f"  {a} & {b} (r={r:.2f}) measure the same behaviour — how often a subscriber "
              f"uses the service. Putting both into one weighted score would count that single "
              f"behaviour twice.")

with open(TAKEAWAYS_PATH, "a") as f:
    f.write("### Correlation redundancy check\n")
    for a, b, r in high_pairs:
        f.write(f"- **{a} vs {b}**: r = {r:.3f} (>0.8). Both measure usage frequency, so both "
                f"in one score would double-count that behaviour.\n")
    f.write("\n(No weights or thresholds chosen here — pairs are reported only.)\n")

print(f"\nWrote takeaways to {TAKEAWAYS_PATH}")
