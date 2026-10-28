import os
import sys
import html as _html
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Phase 2 Final Report module (lives next to this file in src/)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_report

st.set_page_config(
    page_title="eBook Subscriber Intelligence",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Style ─────────────────────────────────────────────────────
st.markdown(
    """
<style>
    .block-container { padding-top: 2rem; }
    .hero-title { font-size: 2.4rem; font-weight: 700; color: #ffffff; margin: 0; }
    .hero-sub   { font-size: 1.05rem; color: #cfe3ff; margin-top: .3rem; }
    .card {
        background: #ffffff; border: 1px solid #e8ecf2; border-radius: 14px;
        padding: 18px 20px; box-shadow: 0 2px 6px rgba(15,23,42,.06); height: 100%;
    }
    .card h4 { margin: 0 0 6px 0; color: #0f172a; font-size: 1.02rem; }
    .card p  { margin: 0; color: #475569; font-size: .9rem; line-height: 1.45; }
    .seg-tag { display:inline-block; padding: 3px 10px; border-radius: 99px;
               font-size: .8rem; font-weight: 600; margin: 2px 4px 2px 0; }
    .note-bar {
        background: #fff7e6; border: 1px solid #f5d38a; color: #7a4f00;
        padding: 10px 14px; border-radius: 10px; font-size: .9rem;
    }
    div[data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e8ecf2; border-radius: 14px;
        padding: 14px 16px; box-shadow: 0 2px 6px rgba(15,23,42,.05);
    }
    div[data-testid="stMetricLabel"] { font-size: .85rem; color: #64748b; }
    div[data-testid="stMetricValue"] { font-size: 1.65rem; font-weight: 700; color: #0f172a; }

    /* ── Final Report (Phase 2) — indigo / lavender palette ── */
    .fr-head { background: #1a1f5c; color: #ffffff; border-bottom: 5px solid #3f4de6;
               border-radius: 12px; padding: 18px 22px; margin-bottom: 6px; }
    .fr-head h3 { margin: 0 0 8px 0; color: #ffffff; font-size: 1.3rem; }
    .fr-head p  { margin: 0; color: #a5b4fc; font-size: .95rem; line-height: 1.5; }
    .fr-kpis { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px; }
    .fr-kpi  { flex: 1 1 150px; background: #ffffff; border: 1px solid #dbe1ff;
               border-top: 4px solid #3f4de6; border-radius: 12px; padding: 12px 14px; }
    .fr-v { font-size: 1.6rem; font-weight: 700; }
    .fr-l { font-size: .8rem; color: #5b6285; margin-top: 3px; }
    .fr-note { background: #dbe1ff; border: 1px solid #a5b4fc; color: #33385f;
               padding: 9px 13px; border-radius: 10px; font-size: .88rem;
               margin-top: 12px; line-height: 1.5; }
    .fr-take { background: #eef0ff; border-left: 4px solid #3f4de6; color: #3a4175;
               padding: 9px 13px; border-radius: 0 8px 8px 0; font-size: .88rem;
               margin-top: 12px; line-height: 1.5; }
    .fr-find li { margin-bottom: 8px; font-size: .93rem; line-height: 1.5; }
    .fr-card { background: #ffffff; border: 1px solid #dbe1ff; border-radius: 12px;
               padding: 14px 16px; font-size: .86rem; height: 100%; }
    .fr-card.retain { border-top: 5px solid #16a34a; }
    .fr-card.win    { border-top: 5px solid #d97706; }
    .fr-card.churn  { border-top: 5px solid #dc2626; }
    .fr-ct { font-weight: 700; color: #1a1f5c; font-size: .98rem; }
    .fr-sub { color: #5b6285; font-size: .78rem; margin: 4px 0 8px 0; }
    .fr-theme { display: inline-block; background: #dbe1ff; color: #2f3568;
                border-radius: 99px; padding: 2px 9px; font-size: .72rem;
                font-weight: 600; margin: 3px 0; }
    .fr-rec { border-top: 1px dashed #a5b4fc; margin-top: 8px; padding-top: 7px;
              color: #3a4175; line-height: 1.45; }
    .fr-lims { background: #eef0ff; border: 1px solid #dbe1ff; border-radius: 10px;
               padding: 12px 16px 6px 16px; font-size: .9rem; color: #33385f; }
    .fr-lims li { margin-bottom: 7px; line-height: 1.45; }
    .fr-method li { margin-bottom: 7px; line-height: 1.45; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Palette & helpers ─────────────────────────────────────────
SEG_COLORS = {
    "Core Subscribers": "#1b9e77",
    "Low-fit Subscribers": "#d95f02",
    "High-potential Prospects": "#7570b3",
    "Low-priority": "#e7298a",
    "Mid-tier Subscribers": "#66a61e",
    "Mid-tier Non-subscribers": "#e6ab02",
}
SEG_ORDER = list(SEG_COLORS.keys())


def hero_banner():
    """Draw the gradient hero banner for the introduction page."""
    fig, ax = plt.subplots(figsize=(12, 2.6), dpi=110)
    cmap = LinearSegmentedColormap.from_list("hero", ["#0f2027", "#203a43", "#2c5364", "#1e3a5f"])
    grad = np.linspace(0, 1, 512).reshape(1, -1)
    ax.imshow(grad, aspect="auto", cmap=cmap, extent=[0, 1, 0, 1])
    ax.text(0.04, 0.62, "eBook Subscriber Intelligence", color="white",
            fontsize=26, fontweight="bold", va="center")
    ax.text(0.04, 0.28, "Propensity scoring  •  Six customer segments  •  Retention & conversion playbook",
            color="#b9d4ff", fontsize=12.5, va="center")

    # Open-book picture on the right side of the banner
    from matplotlib.patches import Polygon

    cx, cy = 0.87, 0.50
    ww, hh, drop = 0.085, 0.42, 0.05
    ax.add_patch(Polygon(
        [(cx - ww, cy + hh / 2 - drop), (cx, cy + hh / 2),
         (cx, cy - hh / 2), (cx - ww, cy - hh / 2 - drop)],
        closed=True, facecolor="#eef4ff", edgecolor="#93c5fd", linewidth=1.5, zorder=2))
    ax.add_patch(Polygon(
        [(cx, cy + hh / 2), (cx + ww, cy + hh / 2 - drop),
         (cx + ww, cy - hh / 2 - drop), (cx, cy - hh / 2)],
        closed=True, facecolor="#cfe0ff", edgecolor="#93c5fd", linewidth=1.5, zorder=2))
    for frac in (0.30, 0.55, 0.80):
        y = cy + hh / 2 - frac * hh
        ax.plot([cx - 0.02, cx - ww + 0.016], [y, y - drop],
                color="#7ea6e8", lw=1.1, solid_capstyle="round", zorder=3)
        ax.plot([cx + 0.02, cx + ww - 0.016], [y, y - drop],
                color="#7ea6e8", lw=1.1, solid_capstyle="round", zorder=3)
    ax.plot([cx, cx], [cy - hh / 2, cy + hh / 2],
            color="#60a5fa", lw=2.4, solid_capstyle="round", zorder=4)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.patch.set_facecolor("#0f2027")
    plt.tight_layout(pad=0)
    return fig


def takeaway(text):
    st.caption(text)


def rate_bar(ax, labels, values, color, avg=None, fmt="{:.1%}", horizontal=False):
    """Bar chart with value labels and an optional dataset-average line."""
    if horizontal:
        bars = ax.barh(labels, values, color=color)
        ax.bar_label(bars, fmt=fmt, padding=4, fontsize=9, fontweight="bold")
        ax.invert_yaxis()
        if avg is not None:
            ax.axvline(avg, color="#d62728", ls="--", lw=1.4)
            ax.text(avg, -0.6, f"average {avg:.1%}", color="#d62728", fontsize=8.5)
        ax.set_xlim(0, max(values) * 1.18)
    else:
        bars = ax.bar(labels, values, color=color)
        ax.bar_label(bars, fmt=fmt, padding=3, fontsize=9, fontweight="bold")
        if avg is not None:
            ax.axhline(avg, color="#d62728", ls="--", lw=1.4)
            ax.text(len(labels) - 0.4, avg, f" average {avg:.1%}", color="#d62728",
                    fontsize=8.5, ha="right", va="bottom")
        ax.set_ylim(0, max(values) * 1.15)


# ── Data ──────────────────────────────────────────────────────
@st.cache_data
def load_data():
    scored = pd.read_csv("data/processed/scored.csv")
    segmented = pd.read_csv("data/processed/segmented.csv")
    clean = pd.read_csv("data/processed/clean.csv").drop_duplicates("Customer ID", keep="first")
    segmented = segmented.merge(
        clean[["Customer ID", "Education Level"]].drop_duplicates("Customer ID"),
        on="Customer ID", how="left",
    )
    return scored, segmented, clean


scored, segmented, clean = load_data()
overall_rate = segmented["eBook Subscriber Flag"].mean()
score_bounds = segmented["Subscriber_Propensity_Score"].quantile([0.33, 0.67]).values


# ── Phase 2 data (engagement) ─────────────────────────────────
@st.cache_data
def load_v2():
    """Load the v2 scored engagement file + significance-check table."""
    v2 = pd.read_csv("data/processed/v2/scored.csv")
    # Age from Birth Date at the report's reference date (same rule as v2_segments.py)
    v2["Age"] = (pd.Timestamp("2026-10-02") - pd.to_datetime(v2["Birth Date"])).dt.days / 365.25
    v2["Tenure Band"] = pd.cut(
        v2["Subscription Tenure Months"],
        bins=[-1, 6, 12, 24, 48, 1000],
        labels=["0-6", "7-12", "13-24", "25-48", "49+"],
    ).astype(str)
    sig = pd.read_csv("outputs/v2/significance_checks.csv")
    sig["Note"] = ""
    sig.loc[sig["comparison"] == "Genre Preference: Fantasy", "Note"] = \
        "not robust after multiple-test correction"
    return v2, sig


v2_all, sig_v2 = load_v2()


@st.cache_data
def load_final_report():
    """Unfiltered Final Report payload — built only from outputs/v2 and
    data/processed/v2 files by src/v2_report.py (never from filtered views)."""
    return v2_report.load_report()
STATUS_ORDER_P2 = ["Active", "Inactive", "Churned"]
STATUS_COLORS = {"Active": "#2a9d8f", "Inactive": "#e9c46a",
                 "Churned": "#e76f51", "Unclassified": "#adb5bd"}
V2_CLS_ALL = v2_all[v2_all["Status"] != "Unclassified"]
V2_CUTS = V2_CLS_ALL["Engagement Score"].quantile([1 / 3, 2 / 3]).values
# Min-max bounds used by the approved score (fit on classified rows)
V2_BOUNDS = {
    "Days Since Last Activity": (V2_CLS_ALL["Days Since Last Activity"].min(),
                                 V2_CLS_ALL["Days Since Last Activity"].max()),
    "Avg Logins Per Month": (V2_CLS_ALL["Avg Logins Per Month"].min(),
                             V2_CLS_ALL["Avg Logins Per Month"].max()),
    "Avg Session Minutes": (V2_CLS_ALL["Avg Session Minutes"].min(),
                            V2_CLS_ALL["Avg Session Minutes"].max()),
}
V2_WEIGHTS = {"Days Since Last Activity": 0.40, "Avg Logins Per Month": 0.35,
              "Avg Session Minutes": 0.25}

# ── Navigation ────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "intro"

with st.sidebar:
    st.markdown("### 🧭 Navigation")
    nav1, nav2 = st.columns(2)
    if nav1.button(
        "🏠 Intro",
        type="primary" if st.session_state.page == "intro" else "secondary",
        width="stretch",
    ):
        st.session_state.page = "intro"
        st.rerun()
    if nav2.button(
        "📈 Dashboard",
        type="primary" if st.session_state.page == "dashboard" else "secondary",
        width="stretch",
    ):
        st.session_state.page = "dashboard"
        st.rerun()

# ═══════════════════════ INTRO PAGE ═══════════════════════════
if st.session_state.page == "intro":
    st.pyplot(hero_banner(), width="stretch")
    st.write("")

    st.markdown(
        """
        <div style="text-align:center; padding:1.4rem 0 0.3rem 0;">
            <div style="font-size:3.4rem; line-height:1;">📚</div>
            <h1 style="margin:0.7rem 0 0.35rem; font-size:2.3rem;">
                Welcome to the eBook Subscriber Intelligence Dashboard
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("➡️  Open the Dashboard", type="primary", width="content"):
        st.session_state.page = "dashboard"
        st.rerun()

# ═══════════════════════ DASHBOARD ════════════════════════════
else:
    # ── Sidebar filters ───────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🔎 Filters")
        state_sel = st.selectbox("State", ["All"] + sorted(segmented["State"].dropna().unique()))
        occ_sel = st.selectbox("Occupation", ["All"] + sorted(segmented["Occupation"].dropna().unique()))
        edu_sel = st.selectbox("Education Level", ["All"] + sorted(segmented["Education Level"].dropna().unique()))
        age_sel = st.selectbox("AgeGroup", ["All"] + sorted(segmented["AgeGroup"].dropna().unique()))
        seg_sel = st.multiselect("Segment", SEG_ORDER, default=SEG_ORDER)
        st.markdown("---")
        st.markdown(
            """<div class="note-bar">ℹ️ Based on demographic and spend data only;
            no usage-based engagement metrics were available in the source dataset.</div>""",
            unsafe_allow_html=True,
        )

        # ── Phase 2 filters (update the Phase 2 tabs only) ────────
        st.markdown("---")
        st.markdown("### 🎯 Phase 2 filters")
        st.caption("These update the Phase 2 tabs only.")
        p2_status = st.selectbox(
            "Status", ["All"] + ["Active", "Inactive", "Churned", "Unclassified"],
            key="p2_status")
        p2_tier = st.selectbox("Tier", ["All", "Low", "Medium", "High"], key="p2_tier")
        p2_genre = st.selectbox(
            "Genre", ["All"] + sorted(v2_all["Genre Preference"].unique()), key="p2_genre")
        p2_age = st.selectbox(
            "AgeGroup", ["All"] + sorted(v2_all["AgeGroup"].unique()), key="p2_age")
        p2_occ = st.selectbox(
            "Occupation", ["All"] + sorted(v2_all["Occupation"].unique()), key="p2_occ")
        p2_edu = st.selectbox(
            "Education Level", ["All"] + sorted(v2_all["Education Level"].unique()),
            key="p2_edu")
        p2_ten = st.selectbox(
            "Tenure band", ["All", "0-6", "7-12", "13-24", "25-48", "49+"], key="p2_ten")
        p2_state = st.selectbox(
            "State", ["All"] + sorted(v2_all["State"].dropna().unique()), key="p2_state")

    mask = np.ones(len(segmented), dtype=bool)
    if state_sel != "All":
        mask &= segmented["State"] == state_sel
    if occ_sel != "All":
        mask &= segmented["Occupation"] == occ_sel
    if edu_sel != "All":
        mask &= segmented["Education Level"] == edu_sel
    if age_sel != "All":
        mask &= segmented["AgeGroup"] == age_sel
    if seg_sel:
        mask &= segmented["Segment"].isin(seg_sel)
    filtered = segmented[mask]

    # ── Header ────────────────────────────────────────────────
    st.title("📈 eBook Subscriber Dashboard")
    st.caption(
        f"Showing **{len(filtered):,}** of {len(segmented):,} customers · "
        "filters in the sidebar update the tabs in their own section"
    )
    st.subheader("Phase 1 - Propensity")

    # ── KPI row ───────────────────────────────────────────────
    n = len(filtered)
    sub_rate = filtered["eBook Subscriber Flag"].mean() if n else 0.0
    avg_score = filtered["Subscriber_Propensity_Score"].mean() if n else 0.0
    avg_spend = filtered["Clean_Avg Monthly Spend"].mean() if n else 0.0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers in view", f"{n:,}", f"{n / len(segmented) * 100:.1f}% of base")
    c2.metric("Subscriber rate", f"{sub_rate:.1%}", f"vs {overall_rate:.1%} overall")
    c3.metric("Avg propensity score", f"{avg_score:.1f}", "scale 0–100")
    c4.metric("Avg monthly spend", f"${avg_spend:.1f}", "per customer")

    tabs = st.tabs(
        ["① Overview", "② Correlation Heatmap", "③ Segment Profiles",
         "④ Customer Lookup", "⑤ Methodology"]
    )

    # ── Tab 1: Overview ───────────────────────────────────────
    with tabs[0]:
        st.subheader("Overview — who is in view and how they behave")

        col_pie, col_blank = st.columns([1, 1])
        with col_pie:
            st.markdown("**Segment mix of the current selection**")
            counts = filtered["Segment"].value_counts().reindex(SEG_ORDER).fillna(0)
            fig1, ax1 = plt.subplots(figsize=(6.4, 5.2))
            if counts.sum() > 0:
                labels = [f"{s}\n{int(c):,} ({c / counts.sum() * 100:.1f}%)"
                          for s, c in zip(counts.index, counts.values)]
                ax1.pie(
                    counts.values, labels=labels, colors=[SEG_COLORS[s] for s in counts.index],
                    autopct=None, startangle=90, wedgeprops=dict(width=0.42),
                    textprops=dict(fontsize=8.6),
                )
                ax1.text(0, 0.08, f"{int(counts.sum()):,}", ha="center", va="center",
                         fontsize=17, fontweight="bold", color="#0f172a")
                ax1.text(0, -0.14, "customers", ha="center", va="center",
                         fontsize=9, color="#64748b")
            ax1.set_title("Segment distribution (donut)", fontsize=12, fontweight="bold")
            st.pyplot(fig1)
            takeaway("Each slice is one segment; size = share of the filtered customers. "
                     "No single segment should dominate above 60% of the full base.")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Subscriber rate by occupation**")
            rates = filtered.groupby("Occupation")["eBook Subscriber Flag"].mean().sort_values(ascending=True)
            if len(rates) == 0:
                st.info("No customers match the current filters.")
            else:
                fig2, ax2 = plt.subplots(figsize=(6, 3.6))
                rate_bar(ax2, rates.index, rates.values, "#4c9f70",
                         avg=sub_rate if n else None, horizontal=True)
                ax2.set_xlabel("Subscriber rate")
                ax2.set_title("")
                st.pyplot(fig2)
                takeaway("Bars above the red dashed line convert better than this selection's average — "
                         "Professional and Management workers typically lead.")
        with col_b:
            st.markdown("**Subscriber rate by age group**")
            age_order = ["1910-1949", "1950-1959", "1960-1969", "1970-1979"]
            rates_a = filtered.groupby("AgeGroup")["eBook Subscriber Flag"].mean().reindex(age_order).dropna()
            if len(rates_a) == 0:
                st.info("No customers match the current filters.")
            else:
                fig3, ax3 = plt.subplots(figsize=(6, 3.6))
                rate_bar(ax3, rates_a.index, rates_a.values, "#3b82f6",
                         avg=sub_rate if n else None)
                ax3.set_ylabel("Subscriber rate")
                ax3.tick_params(axis="x", labelsize=8.5)
                st.pyplot(fig3)
                takeaway("The 1960–1969 cohort (born 1960s) subscribes far more than any other age band "
                         "in the full dataset — 51.6% vs 33.2% average.")

        st.markdown("**Where do propensity scores sit?**")
        fig4, ax4 = plt.subplots(figsize=(10, 3.4))
        ax4.hist(filtered["Subscriber_Propensity_Score"], bins=25, color="#8b5cf6",
                 edgecolor="white", alpha=0.9)
        for x, lab, col in [(score_bounds[0], "Low | Medium", "#d97706"),
                            (score_bounds[1], "Medium | High", "#059669")]:
            ax4.axvline(x, color=col, ls="--", lw=1.6)
            ax4.text(x, ax4.get_ylim()[1] * 0.97, f" {lab} boundary\n (score {x:.1f})",
                     color=col, fontsize=8.5, va="top", fontweight="bold")
        ax4.set_xlabel("Subscriber Propensity Score (0–100)")
        ax4.set_ylabel("Customers")
        st.pyplot(fig4)
        takeaway("Vertical dashed lines are the tercile cuts: scores left of them are the Low tier, "
                 "between them Medium, right of them High. Tier validation: 13.0% / 25.8% / 61.1% subscriber rate.")

    # ── Tab 2: Correlation heatmap ────────────────────────────
    with tabs[1]:
        st.subheader("Correlation heatmap")
        st.markdown(
            "How strongly do the numeric fields move together? The **eBook Subscriber Flag** row "
            "shows which variables are associated with subscription."
        )
        plot_df = filtered[["Clean_Annual Income", "Clean_Avg Monthly Spend",
                            "Clean_Children At Home", "eBook Subscriber Flag"]].rename(columns={
            "Clean_Annual Income": "Annual Income",
            "Clean_Avg Monthly Spend": "Avg Monthly Spend",
            "Clean_Children At Home": "Children At Home",
            "eBook Subscriber Flag": "Subscriber Flag",
        })
        if n == 0:
            st.info("No customers match the current filters.")
        else:
            corr = plot_df.corr()
            fig5, ax5 = plt.subplots(figsize=(7.5, 5.6))
            sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f",
                        linewidths=0.6, ax=ax5, vmin=-1, vmax=1,
                        cbar_kws={"label": "Pearson r"})
            ax5.set_title("Pearson correlations among numeric fields", fontsize=12, fontweight="bold")
            st.pyplot(fig5)
            takeaway("Children at home (0.46) and monthly spend (0.42) relate to subscription more than "
                     "income (0.29); income and spend correlate with each other (≈0.61) but stay below the "
                     "0.8 collinearity threshold, so both were kept in the score.")

    # ── Tab 3: Segment profiles ───────────────────────────────
    with tabs[2]:
        st.subheader("Segment profiles")
        age_map = {"1910-1949": 1930, "1950-1959": 1955, "1960-1969": 1965, "1970-1979": 1975}
        rows = []
        for seg in SEG_ORDER:
            sub = filtered[filtered["Segment"] == seg]
            if len(sub) == 0:
                continue
            rows.append({
                "Segment": seg,
                "Customers": len(sub),
                "Mean Age (yr)": round(sub["AgeGroup"].map(age_map).mean(), 0),
                "Mean Income ($)": round(sub["Clean_Annual Income"].mean(), 0),
                "Mean Spend ($/mo)": round(sub["Clean_Avg Monthly Spend"].mean(), 1),
                "Mean Children": round(sub["Clean_Children At Home"].mean(), 1),
                "Top Occupation": sub["Occupation"].mode().iloc[0],
                "Top State": sub["State"].mode().iloc[0],
            })
        if not rows:
            st.info("No customers match the current filters.")
        else:
            prof_df = pd.DataFrame(rows)
            st.dataframe(prof_df.set_index("Segment"), width="stretch", height=260)
            takeaway("Read across a row for that segment's average customer. "
                     "Core Subscribers top income and spend; High-potential Prospects run close behind.")

            st.markdown("**Side-by-side comparison**")
            metrics = [("Mean Income ($)", "#2563eb"), ("Mean Spend ($/mo)", "#16a34a"),
                       ("Mean Children", "#d97706")]
            fig6, axes = plt.subplots(1, 3, figsize=(13, 3.8))
            x = np.arange(len(prof_df))
            for ax, (col, color) in zip(axes, metrics):
                vals = pd.to_numeric(prof_df[col], errors="coerce").fillna(0)
                bars = ax.bar(x, vals, color=color, width=0.62)
                ax.bar_label(bars, fmt="{:,.0f}" if col != "Mean Children" else "{:.1f}",
                             padding=3, fontsize=8.5, fontweight="bold")
                ax.set_title(col, fontsize=11, fontweight="bold")
                ax.set_xticks(x)
                ax.set_xticklabels(prof_df["Segment"], rotation=40, ha="right", fontsize=8)
                ax.set_ylim(0, vals.max() * 1.16 if vals.max() > 0 else 1)
            plt.tight_layout()
            st.pyplot(fig6)
            takeaway("Three views of the same six segments: Core leads every metric, Low-priority trails, "
                     "and High-potential Prospects sit near Core — the conversion upside.")

    # ── Tab 4: Customer lookup ────────────────────────────────
    with tabs[3]:
        st.subheader("Customer lookup")
        st.caption("Enter a Customer ID from the dataset (e.g. 11000) to see that person's score, tier and segment.")
        cus_id = st.text_input("Customer ID")
        if cus_id.strip():
            try:
                cid = int(cus_id)
            except ValueError:
                st.error("Please enter a numeric Customer ID.")
                cid = None
            if cid is not None:
                row = scored[scored["Customer ID"] == cid]
                if row.empty:
                    st.warning(f"No customer with ID {cid} found.")
                else:
                    r = row.iloc[0]
                    seg_row = filtered[filtered["Customer ID"] == cid]
                    segment = seg_row["Segment"].iloc[0] if len(seg_row) else "N/A"
                    c_clean = clean[clean["Customer ID"] == cid]
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("Propensity score", f"{r['Subscriber_Propensity_Score']:.1f}")
                    k2.metric("Tier", r["Tier"])
                    k3.metric("Segment", segment)
                    k4.metric("Subscriber?", "Yes" if int(r["eBook Subscriber Flag"]) == 1 else "No")
                    if len(c_clean):
                        cc = c_clean.iloc[0]
                        st.markdown("**Inputs used in the score**")
                        i1, i2, i3 = st.columns(3)
                        i1.metric("Children at home", int(cc["Number of Children At Home"]))
                        i2.metric("Avg monthly spend", f"${cc['Avg Monthly Spend']:,}")
                        i3.metric("Annual income", f"${cc['Annual Income']:,}")
                        st.caption(
                            f"Profile: {cc['Education Level']} · {cc['Occupation']} · "
                            f"{cc['Gender']} · {cc['AgeGroup']} · {cc['State'] if 'State' in cc else ''}"
                        )

    # ── Tab 5: Methodology ────────────────────────────────────
    with tabs[4]:
        st.subheader("Methodology")
        st.caption("The scoring model and segment definitions exactly as documented in outputs/methodology.md")
        try:
            with open("outputs/methodology.md", "r") as f:
                st.markdown(f.read())
        except FileNotFoundError:
            st.error("outputs/methodology.md not found — run src/03_score.py first.")

    # ── Download (Phase 1) ────────────────────────────────────
    st.markdown("---")
    st.download_button(
        "⬇️  Download the filtered Phase 1 data as CSV",
        filtered.to_csv(index=False).encode("utf-8"),
        file_name="segmented_filtered.csv",
        mime="text/csv",
        width="stretch",
    )

    # ═══════════════ PHASE 2 — ENGAGEMENT ═════════════════════
    st.markdown("---")
    st.subheader("Phase 2 - Engagement")

    st.info(
        "**Notes on this page**\n"
        "- The **tenure view is cross-sectional and not a retention curve** — the data has no cancellation dates.\n"
        "- The **33 Unclassified rows are shown separately** and excluded from tier charts and status shares.\n"
        "- **Tier-by-logins agreement is partly by construction**: recency defines status and carries 40% of "
        "the score, and logins and session minutes are score inputs."
    )

    # ── Apply the Phase 2 sidebar filters ─────────────────────
    mask2 = np.ones(len(v2_all), dtype=bool)
    if p2_status != "All":
        mask2 &= v2_all["Status"] == p2_status
    if p2_tier != "All":
        mask2 &= v2_all["Tier"] == p2_tier
    if p2_genre != "All":
        mask2 &= v2_all["Genre Preference"] == p2_genre
    if p2_age != "All":
        mask2 &= v2_all["AgeGroup"] == p2_age
    if p2_occ != "All":
        mask2 &= v2_all["Occupation"] == p2_occ
    if p2_edu != "All":
        mask2 &= v2_all["Education Level"] == p2_edu
    if p2_ten != "All":
        mask2 &= v2_all["Tenure Band"] == p2_ten
    if p2_state != "All":
        mask2 &= v2_all["State"] == p2_state
    f2 = v2_all[mask2]
    n2 = len(f2)
    cls2 = f2[f2["Status"] != "Unclassified"]       # tier/status charts use this
    n_cls = len(cls2)
    n_un2 = int((f2["Status"] == "Unclassified").sum())

    # ── Phase 2 KPI row ───────────────────────────────────────
    k = st.columns(6)
    k[0].metric("Subscribers in view", f"{n2:,}",
                f"{n2 / len(v2_all) * 100:.1f}% of {len(v2_all):,}")
    sc = cls2["Status"].value_counts()
    for i, s in enumerate(STATUS_ORDER_P2, start=1):
        share = (sc.get(s, 0) / n_cls) if n_cls else 0.0
        k[i].metric(f"Share {s}", f"{share:.1%}",
                    f"{int(sc.get(s, 0)):,} of {n_cls:,} classified")
    k[4].metric("Average score", f"{f2['Engagement Score'].mean():.1f}" if n2 else "—",
                "scale 0–100")
    recency_view = f2["Days Since Last Activity"]
    k[5].metric("Avg days since activity",
                f"{recency_view.mean():.0f}" if recency_view.notna().any() else "—",
                "days")
    st.caption(
        f"Unclassified rows in view: **{n_un2}** — shown separately, excluded from "
        "tier charts and the Active/Inactive/Churned shares above."
    )

    p2_tabs = st.tabs([
        "⓪ Final Report", "① Overview", "② Behaviour by Status", "③ Correlation Heatmap",
        "④ Genre", "⑤ Demographic Profile", "⑥ Tenure View", "⑦ Customer Lookup",
        "⑧ Methodology",
    ])

    # ── P2 Tab 0: Final Report (unfiltered — ignores sidebar filters) ──
    with p2_tabs[0]:
        try:
            rep = load_final_report()
        except Exception as exc:
            st.error(f"Final Report unavailable — {exc}. "
                     "Run `python3 src/v2_report.py` first.")
            rep = None
        if rep is not None:
            # 1 — title + one-sentence project summary
            st.markdown(
                f'<div class="fr-head"><h3>{_html.escape(rep["title"])}</h3>'
                f'<p>{_html.escape(rep["summary"])}</p></div>',
                unsafe_allow_html=True)
            st.caption(
                f"Unfiltered view of all {rep['total']:,} subscribers — "
                "the sidebar filters do not affect this page.")

            # 2 — KPI cards + Unclassified noted separately
            st.markdown("**2 · Key numbers**")
            k_html = "".join(
                f'<div class="fr-kpi"><div class="fr-v" style="color:{c["color"]}">'
                f'{_html.escape(c["value"])}</div>'
                f'<div class="fr-l">{_html.escape(c["label"])}</div></div>'
                for c in rep["kpis"])
            st.markdown(
                f'<div class="fr-kpis">{k_html}</div>'
                f'<div class="fr-note">{_html.escape(rep["un_note"])}</div>',
                unsafe_allow_html=True)

            # 3 — status pie + one-line takeaway
            st.markdown("**3 · Status mix**")
            st.pyplot(v2_report.make_pie(rep), width="stretch")
            st.markdown(
                f'<div class="fr-take">{_html.escape(rep["pie_takeaway"])}</div>',
                unsafe_allow_html=True)

            # 4 — key findings (sentences lifted from insights.md)
            st.markdown("**4 · Key findings**")
            items = "".join(
                f"<li><strong>{_html.escape(lab)}</strong> — {v2_report.md_html(text)}</li>"
                for lab, text in rep["findings"])
            st.markdown(f'<ol class="fr-find">{items}</ol>', unsafe_allow_html=True)

            # 5 — score tiers + by-construction note
            st.markdown("**5 · Score tiers (classified rows)**")
            st.dataframe(pd.DataFrame(rep["tier_rows"]), width="stretch",
                         hide_index=True)
            st.markdown(
                f'<div class="fr-note">{v2_report.md_html(rep["tier_note"])}</div>',
                unsafe_allow_html=True)

            # 6 — high-value profile + small-effect note
            st.markdown("**6 · High-value subscriber profile (Active+High vs Churned)**")
            sig_cols = ["comparison", "high_value", "churned", "difference",
                        "p_value", "effect_size", "effect_size_type", "plain_english"]
            st.dataframe(
                rep["sig_rows"][sig_cols].rename(columns=lambda c: c.replace("_", " ")),
                width="stretch", hide_index=True)
            st.markdown(
                f'<div class="fr-note">{v2_report.md_html(rep["sig_note"])}</div>',
                unsafe_allow_html=True)
            st.markdown(
                f'<div class="fr-note">{v2_report.md_html(rep["sig_foot"])}</div>',
                unsafe_allow_html=True)

            # 7 — one strategy card per segment
            st.markdown("**7 · Recommended strategy per segment**")
            for col, c in zip(st.columns(3), rep["cards"]):
                if c["recs"]:
                    body = "".join(
                        f'<div class="fr-rec"><strong>{v2_report.md_html(r["lead"])}</strong> '
                        f'<span class="fr-theme">{_html.escape(r["theme"])}</span><br>'
                        f'{v2_report.md_html(r["finding"])}</div>'
                        for r in c["recs"])
                else:
                    body = (f'<div class="fr-rec"><span class="fr-theme">'
                            f'{_html.escape(c["theme"])}</span><br>'
                            f'{v2_report.md_html(c["finding"])}</div>')
                col.markdown(
                    f'<div class="fr-card {c["key"]}">'
                    f'<div class="fr-ct">{_html.escape(c["title"])}</div>'
                    f'<div class="fr-sub">{v2_report.md_html(c["sub"])}</div>{body}</div>',
                    unsafe_allow_html=True)

            # 8 — limitations (insights.md section e)
            st.markdown("**8 · Limitations**")
            lims = "".join(
                f'<li><strong>{_html.escape(l["lead"])}</strong> '
                f'{_html.escape(l["body"])}</li>' for l in rep["limitations"])
            st.markdown(f'<div class="fr-lims"><ul>{lims}</ul></div>',
                        unsafe_allow_html=True)

            # 9 — method in brief
            st.markdown("**9 · Method in brief**")
            meth_items = "".join(f"<li>{_html.escape(m)}</li>" for m in rep["method"])
            st.markdown(f'<div class="fr-note fr-method"><ul>{meth_items}</ul></div>',
                        unsafe_allow_html=True)

            # Download: byte-identical to outputs/v2/final_report.html when present
            try:
                with open(v2_report.HTML_PATH, "rb") as fh:
                    report_bytes = fh.read()
            except FileNotFoundError:
                report_bytes = v2_report.build_html(
                    rep, v2_report.fig_png_b64(v2_report.make_pie(rep))).encode("utf-8")
            st.download_button(
                "⬇️  Download final_report.html (self-contained, opens offline)",
                report_bytes, file_name="final_report.html", mime="text/html",
                width="stretch")

    # ── P2 Tab 1: Overview ────────────────────────────────────
    with p2_tabs[1]:
        st.subheader("Overview — status mix and score distribution")
        if n2 == 0:
            st.info("No subscribers match the current Phase 2 filters.")
        else:
            col_pie, col_hist = st.columns(2)
            with col_pie:
                counts = cls2["Status"].value_counts().reindex(STATUS_ORDER_P2).fillna(0)
                if counts.sum() > 0:
                    fig, ax = plt.subplots(figsize=(6, 4.6))
                    ax.pie(counts.values,
                           labels=[f"{s}\n{int(c):,}" for s, c in zip(counts.index, counts.values)],
                           colors=[STATUS_COLORS[s] for s in counts.index],
                           autopct="%1.1f%%", startangle=90, textprops=dict(fontsize=9.5))
                    ax.set_title("Status mix of the current view (classified rows)")
                    st.pyplot(fig)
                    takeaway("Active is the largest slice of this view; the 33 Unclassified rows "
                             "are excluded here and reported separately above. Association, not causation.")
                else:
                    st.info("Only Unclassified rows match — status mix needs classified rows.")
            with col_hist:
                fig, ax = plt.subplots(figsize=(6.4, 4.6))
                ax.hist(f2["Engagement Score"].dropna(), bins=25, color="#8b5cf6",
                        edgecolor="white")
                for x, lab, c in [(V2_CUTS[0], "Low|Medium", "#d97706"),
                                  (V2_CUTS[1], "Medium|High", "#059669")]:
                    ax.axvline(x, color=c, ls="--", lw=1.5)
                    ax.text(x, ax.get_ylim()[1] * 0.97, f" {lab}\n ({x:.1f})",
                            color=c, fontsize=8.5, va="top", fontweight="bold")
                ax.set_title("Engagement score distribution (0–100)")
                ax.set_xlabel("Engagement Score")
                st.pyplot(fig)
                takeaway("Dashed lines are the full-data tercile cuts; scores are driven by "
                         "inverted recency (40%), logins (35%) and session minutes (25%). "
                         "Association, not causation.")

    # ── P2 Tab 2: Behaviour by status ─────────────────────────
    with p2_tabs[2]:
        st.subheader("Behaviour by status")
        if n_cls == 0:
            st.info("No classified rows match the current Phase 2 filters.")
        else:
            BEHAV = [("Avg Logins Per Month", "Avg Logins Per Month"),
                     ("Avg Session Minutes", "Avg Session Minutes"),
                     ("Books Accessed", "Books Accessed (descriptive only)"),
                     ("Days Since Last Activity", "Days Since Last Activity")]
            fig, axes = plt.subplots(2, 2, figsize=(11, 8))
            for ax, (m, title) in zip(axes.ravel(), BEHAV):
                sns.boxplot(data=cls2, x="Status", y=m, order=STATUS_ORDER_P2,
                            hue="Status", hue_order=STATUS_ORDER_P2,
                            palette=STATUS_COLORS, legend=False, ax=ax)
                ax.set_title(title)
                ax.set_xlabel("")
            fig.suptitle("Behaviour metrics by status (Unclassified excluded)", fontsize=13)
            fig.tight_layout()
            st.pyplot(fig)
            takeaway("Active subscribers sit highest on logins, session minutes and books and "
                     "lowest on recency; recency spreads follow the status definition itself, "
                     "while logins/session are score inputs — comparisons by status are "
                     "near-independent, by tier they would be circular. Association, not causation.")

    # ── P2 Tab 3: Correlation heatmap ─────────────────────────
    with p2_tabs[3]:
        st.subheader("Correlation heatmap — engagement metrics")
        if n2 < 10:
            st.info("Need at least 10 rows to compute correlations with the current filters.")
        else:
            cols5 = ["Days Since Last Activity", "Avg Logins Per Month",
                     "Avg Session Minutes", "Books Accessed", "Subscription Tenure Months"]
            corr = f2[cols5].corr()
            fig, ax = plt.subplots(figsize=(8.5, 6.4))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                        vmin=-1, vmax=1, ax=ax)
            ax.set_title("Pearson correlations — engagement metrics + tenure")
            st.pyplot(fig)
            takeaway("Logins vs books is the only strong pair (r≈0.88): both measure usage "
                     "frequency, so both would double-count in one score — books stays "
                     "descriptive. Tenure barely correlates with anything. Association, not causation.")

    # ── P2 Tab 4: Genre ───────────────────────────────────────
    with p2_tabs[4]:
        st.subheader("Genre preference")
        if n_cls == 0:
            st.info("No classified rows match the current Phase 2 filters.")
        else:
            left, right = st.columns(2)
            genre_order = cls2["Genre Preference"].value_counts().index.tolist()
            with left:
                mix = (pd.crosstab(cls2["Status"], cls2["Genre Preference"])
                       .reindex(index=STATUS_ORDER_P2, columns=genre_order)
                       .fillna(0))
                mix_pct = mix.div(mix.sum(axis=1).replace(0, np.nan), axis=0).mul(100).fillna(0)
                fig, ax = plt.subplots(figsize=(7, 4.6))
                palette = plt.cm.tab20(np.linspace(0, 0.9, len(genre_order)))
                bottom = np.zeros(len(STATUS_ORDER_P2))
                for i, g in enumerate(genre_order):
                    ax.bar(range(len(STATUS_ORDER_P2)), mix_pct[g], bottom=bottom,
                           label=g, color=palette[i])
                    bottom += mix_pct[g].values
                ax.set_xticks(range(len(STATUS_ORDER_P2)))
                ax.set_xticklabels(STATUS_ORDER_P2)
                ax.set_ylabel("Share of status (%)")
                ax.set_title("Genre mix by status")
                ax.legend(fontsize=7, bbox_to_anchor=(1.02, 1), loc="upper left")
                st.pyplot(fig)
                takeaway("Genre taste barely moves with status — Fiction is ~20% of every "
                         "status group, so preference does not separate Active from Churned. "
                         "Association, not causation.")
            with right:
                gt = pd.crosstab(cls2["Genre Preference"], cls2["Status"])
                for s in STATUS_ORDER_P2:
                    if s not in gt:
                        gt[s] = 0
                gt = gt[STATUS_ORDER_P2]
                gt.columns = ["active", "inactive", "churned"]
                gt["n"] = gt.sum(axis=1)
                gt["active_pct"] = gt["active"] / gt["n"] * 100
                gt["churned_pct"] = gt["churned"] / gt["n"] * 100
                gt["small"] = gt["n"] < 100
                plot_g = gt[~gt["small"]].sort_values("active_pct", ascending=False)
                fig, ax = plt.subplots(figsize=(7, 4.6))
                x = np.arange(len(plot_g))
                ax.bar(x - 0.2, plot_g["active_pct"], width=0.4, label="Active %", color="#2a9d8f")
                ax.bar(x + 0.2, plot_g["churned_pct"], width=0.4, label="Churned %", color="#e76f51")
                ax.set_xticks(x)
                ax.set_xticklabels(plot_g.index, rotation=45, ha="right", fontsize=8)
                ax.set_ylabel("% of genre")
                ax.set_title("Active and Churned rate per genre")
                ax.legend()
                st.pyplot(fig)
                small_note = (", ".join(gt[gt["small"]].index) + " (n<100, table only)"
                              if gt["small"].any() else "no group under n=100")
                takeaway(f"Rates vary moderately across genres (small groups excluded: {small_note}). "
                         "Genre: Fantasy differences are NOT robust after multiple-test correction. "
                         "Association, not causation.")
            st.dataframe(
                gt[["n", "active_pct", "churned_pct", "small"]].round(1)
                .rename(columns={"n": "classified n", "active_pct": "Active %",
                                 "churned_pct": "Churned %"}),
                width="stretch")

    # ── P2 Tab 5: Demographic profile ────────────────────────
    with p2_tabs[5]:
        st.subheader("Demographic profile")
        if n_cls == 0:
            st.info("No classified rows match the current Phase 2 filters.")
        else:
            col_charts, col_sig = st.columns([3, 2])
            with col_charts:
                RATE_DIMS = ["IncomeBand", "Occupation", "AgeGroup", "Education Level"]
                fig, axes = plt.subplots(2, 2, figsize=(13, 8))
                for ax, dim in zip(axes.ravel(), RATE_DIMS):
                    ct = pd.crosstab(cls2[dim], cls2["Status"])
                    for s in STATUS_ORDER_P2:
                        if s not in ct:
                            ct[s] = 0
                    ct = ct[STATUS_ORDER_P2]
                    nn = ct.sum(axis=1)
                    ok = nn >= 100                       # small groups are not charted
                    act = ct["Active"] / nn * 100
                    chu = ct["Churned"] / nn * 100
                    xs = np.arange(ok.sum())
                    ax.bar(xs - 0.2, act[ok], width=0.4, label="Active %", color="#2a9d8f")
                    ax.bar(xs + 0.2, chu[ok], width=0.4, label="Churned %", color="#e76f51")
                    ax.set_xticks(xs)
                    ax.set_xticklabels(act[ok].index.astype(str), rotation=45, ha="right",
                                       fontsize=8)
                    ax.set_title(f"{dim} ({ok.sum()} groups n≥100)")
                    ax.set_ylabel("% of group")
                    if (~ok).any():
                        ax.text(0.99, 0.95, f"small excluded: {', '.join(act[~ok].index)}",
                                transform=ax.transAxes, ha="right", va="top", fontsize=7.5,
                                color="#b91c1c")
                axes[0, 0].legend(fontsize=8)
                fig.suptitle("Active and Churned rates by demographic (n≥100 groups only)",
                             fontsize=13)
                fig.tight_layout()
                st.pyplot(fig)
                takeaway("Higher income bands and Professional/Management/1960s cohorts run "
                         "higher Active and lower Churned rates; groups under 100 are excluded "
                         "from the charts and marked in red. Association, not causation.")

                hv2 = cls2[(cls2["Status"] == "Active") & (cls2["Tier"] == "High")]
                ch2 = cls2[cls2["Status"] == "Churned"]
                if len(hv2) and len(ch2):
                    NUM4 = ["Annual Income", "Avg Monthly Spend",
                            "Number of Children At Home", "Age"]
                    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
                    for ax, m in zip(axes.ravel(), NUM4):
                        bars = ax.bar(["Active+High", "Churned"],
                                      [hv2[m].mean(), ch2[m].mean()],
                                      color=["#2a9d8f", "#e76f51"])
                        ax.bar_label(bars, fmt=",.1f", padding=3, fontsize=9,
                                     fontweight="bold")
                        ax.set_title(f"Mean {m}")
                    fig.suptitle(f"High-value (Active+High, n={len(hv2)}) vs Churned "
                                 f"(n={len(ch2)})", fontsize=13)
                    fig.tight_layout()
                    st.pyplot(fig)
                    takeaway("High-value subscribers earn and spend more with slightly more "
                             "children; gaps are statistically significant but small in "
                             "practical terms — see the effect-size table beside. "
                             "Association, not causation.")
                else:
                    st.info("The current filters leave no Active+High or Churned rows to compare.")

            with col_sig:
                st.markdown("**Effect sizes: Active+High vs Churned**")
                st.dataframe(
                    sig_v2[["comparison", "high_value", "churned", "difference",
                            "p_value", "effect_size", "effect_size_type",
                            "plain_english", "Note"]],
                    width="stretch", height=420)
                st.warning(
                    "**Differences are small in practical terms (Cohen's d about 0.2-0.3, "
                    "Cramer's V under 0.1); associations only.** With n≈1,803 vs 901, small "
                    "gaps can be significant while still being practically small — read the "
                    "effect size, not just the p-value. **Genre: Fantasy is not robust after "
                    "multiple-test correction.**")
                takeaway("Table computed on the full dataset (not filtered); rows with "
                         "p<0.05 but small d/V confirm the pattern is real yet modest.")

    # ── P2 Tab 6: Tenure view ─────────────────────────────────
    with p2_tabs[6]:
        st.subheader("Status mix by tenure band")
        st.info("**Cross-sectional comparison, not a retention curve** — the data has no "
                "cancellation dates, so it cannot show how any cohort's status changes over time.")
        if n_cls == 0:
            st.info("No classified rows match the current Phase 2 filters.")
        else:
            BANDS = ["0-6", "7-12", "13-24", "25-48", "49+"]
            ct = (pd.crosstab(cls2["Tenure Band"], cls2["Status"])
                  .reindex(index=BANDS, columns=STATUS_ORDER_P2)
                  .fillna(0))
            pct = ct.div(ct.sum(axis=1).replace(0, np.nan), axis=0).mul(100)
            fig, ax = plt.subplots(figsize=(10, 5))
            w = 0.27
            for i, s in enumerate(STATUS_ORDER_P2):
                ax.bar(np.arange(len(BANDS)) + (i - 1) * w, pct[s].fillna(0), width=w,
                       label=s, color=STATUS_COLORS[s])
            ax.set_xticks(np.arange(len(BANDS)))
            ax.set_xticklabels([f"{b} mo" for b in BANDS])
            ax.set_ylabel("Share of band (%)")
            ax.set_title("Status mix by tenure band (classified rows)")
            ax.legend()
            st.pyplot(fig)
            takeaway("Status mix is broadly similar across tenure bands — long-tenure "
                     "subscribers are not automatically more Active; cross-sectional, NOT a "
                     "retention curve. Association, not causation.")
            tbl = ct.copy()
            tbl.columns = [f"{c} n" for c in tbl.columns]
            tbl["classified n"] = ct.sum(axis=1)
            st.dataframe(tbl, width="stretch")

    # ── P2 Tab 7: Customer lookup ─────────────────────────────
    with p2_tabs[7]:
        st.subheader("Customer lookup by Customer ID")
        st.caption("Enter a Customer ID (e.g. 11001) to see the raw inputs, their normalised "
                   "values, the weighted contributions, score, tier and status.")
        p2_id = st.text_input("Customer ID (Phase 2)", key="p2_lookup_id")
        if p2_id.strip():
            try:
                cid2 = int(p2_id)
            except ValueError:
                st.error("Please enter a numeric Customer ID.")
                cid2 = None
            if cid2 is not None:
                row2 = v2_all[v2_all["Customer ID"] == cid2]
                if row2.empty:
                    st.warning(f"No subscriber with ID {cid2} in the engagement file "
                               "(it covers subscribers only).")
                else:
                    r = row2.iloc[0]
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("Engagement score", f"{r['Engagement Score']:.1f}")
                    k2.metric("Tier", r["Tier"])
                    k3.metric("Status", r["Status"])
                    k4.metric("Genre", r["Genre Preference"])

                    def nz(v, b):
                        return (v - b[0]) / (b[1] - b[0])

                    contrib = []
                    is_un = r["Status"] == "Unclassified"
                    rec_raw = r["Days Since Last Activity"]
                    if pd.isna(rec_raw):
                        contrib.append(["Days Since Last Activity (inverted)",
                                        "missing — never imputed", "—", "—", "—"])
                    else:
                        sc_r = nz(rec_raw, V2_BOUNDS["Days Since Last Activity"])
                        contrib.append(["Days Since Last Activity (inverted)", rec_raw,
                                        round(1 - sc_r, 3), 0.40,
                                        round(100 * 0.40 * (1 - sc_r), 2)])
                    l_s = nz(r["Avg Logins Per Month"], V2_BOUNDS["Avg Logins Per Month"])
                    s_s = nz(r["Avg Session Minutes"], V2_BOUNDS["Avg Session Minutes"])
                    if is_un:
                        wl, ws = round(0.35 / 0.60, 4), round(0.25 / 0.60, 4)
                        st.caption("Unclassified (no recency): score uses logins + session only, "
                                   "weights renormalised to sum to 1.")
                    else:
                        wl, ws = 0.35, 0.25
                    contrib.append(["Avg Logins Per Month", r["Avg Logins Per Month"],
                                    round(l_s, 3), wl, round(100 * wl * l_s, 2)])
                    contrib.append(["Avg Session Minutes", r["Avg Session Minutes"],
                                    round(s_s, 3), ws, round(100 * ws * s_s, 2)])
                    contrib.append(["Books Accessed", r["Books Accessed"], "—", 0.00,
                                    "excluded (r=0.88 with logins)"])
                    st.markdown("**Raw inputs → normalised → weighted contributions**")
                    # astype(str): the column mixes numbers with "—"/notes, and pyarrow
                    # refuses mixed str/float columns
                    st.dataframe(pd.DataFrame(
                        contrib,
                        columns=["Input", "Raw value", "Normalised 0-1 (used)",
                                 "Weight", "Contribution (of 100)"]).astype(str),
                        width="stretch")
                    st.caption(
                        f"Tenure {int(r['Subscription Tenure Months'])} months · "
                        f"{r['Age']:.0f} years · {r['Occupation']} · {r['Education Level']} · "
                        f"${r['Annual Income']:,}/yr · ${r['Avg Monthly Spend']}/mo · "
                        f"income band {r['IncomeBand']} · {r['State']}"
                    )

    # ── P2 Tab 8: Methodology ─────────────────────────────────
    with p2_tabs[8]:
        st.subheader("Methodology — Phase 2")
        st.caption("Cleaning rules, approved thresholds, the engagement score and significance "
                   "checks exactly as documented in outputs/v2/methodology.md")
        try:
            with open("outputs/v2/methodology.md", "r") as f:
                st.markdown(f.read())
        except FileNotFoundError:
            st.error("outputs/v2/methodology.md not found — run the v2 pipeline first.")

    # ── Phase 2 download + navigation ─────────────────────────
    st.markdown("---")
    d1, d2 = st.columns([2, 1])
    with d1:
        st.download_button(
            "⬇️  Download the filtered Phase 2 data as CSV",
            f2.to_csv(index=False).encode("utf-8"),
            file_name="engagement_filtered.csv",
            mime="text/csv",
            width="stretch",
        )
    with d2:
        if st.button("🏠 Back to Introduction"):
            st.session_state.page = "intro"
            st.rerun()
