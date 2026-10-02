import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

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
#### What is this?
A decision-support dashboard for the **eBook subscription dataset** (16,404 unique customers
after de-duplication). It answers two questions:

> **1.** Which customers are most likely to subscribe?  **2.** How should we treat each group differently?

**How the analysis was built (the pipeline behind every tab):**
1. **Data prep** — cleaned the raw CSV: fixed two-digit birth years, derived AgeGroup /
   IncomeBand / State, removed 115 duplicate Customer IDs.
2. **EDA** — measured how each variable relates to the subscription flag. Strongest signals:
   children at home (r = 0.46), monthly spend (r = 0.42), income (r = 0.29).
3. **Propensity Score** — a 0–100 score = weighted blend of those three signals
   (40% children + 35% spend + 25% income). Validated: subscriber rate rises
   **13.0% → 25.8% → 61.1%** from Low to High tier.
4. **Segmentation** — combined score tier × actual flag into **6 mutually exclusive segments**.
        """
    )

    st.markdown("#### The six segments at a glance")
    seg_counts = segmented["Segment"].value_counts()
    rows = [SEG_ORDER[0:3], SEG_ORDER[3:6]]
    for row in rows:
        cols = st.columns(3)
        for col, seg in zip(cols, row):
            n = int(seg_counts.get(seg, 0))
            pct = n / len(segmented) * 100
            color = SEG_COLORS[seg]
            blurb = {
                "Core Subscribers": "Subscribe + top-third score. Your high-value base: income $107.8K, spend $106/mo.",
                "Low-fit Subscribers": "Subscribe but bottom-third score. Explained by low profile (96% childless) — retention risk.",
                "High-potential Prospects": "Do NOT subscribe but top-third score. Look like Core Subscribers — prime conversion targets.",
                "Low-priority": "Neither subscribe nor score well. Lowest-value group; keep outreach minimal.",
                "Mid-tier Subscribers": "Subscribe, middle score. Solid base for upsell to Core status.",
                "Mid-tier Non-subscribers": "No subscription, middle score. Secondary conversion pool.",
            }[seg]
            col.markdown(
                f"""<div class="card">
                <h4><span style="color:{color}">●</span> {seg}</h4>
                <p><b>{n:,} customers · {pct:.1f}%</b><br>{blurb}</p>
                </div>""",
                unsafe_allow_html=True,
            )
        st.write("")

    st.markdown(
        """<div class="note-bar">ℹ️ <b>Data note:</b> Based on demographic and spend data only;
        no usage-based engagement metrics were available in the source dataset.
        Scores and segments describe <i>association</i>, not causation.</div>""",
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
        "filters in the sidebar update every tab"
    )

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

    # ── Download ──────────────────────────────────────────────
    st.markdown("---")
    d1, d2 = st.columns([2, 1])
    with d1:
        st.download_button(
            "⬇️  Download the filtered data as CSV",
            filtered.to_csv(index=False).encode("utf-8"),
            file_name="segmented_filtered.csv",
            mime="text/csv",
            width="stretch",
        )
    with d2:
        if st.button("🏠 Back to Introduction"):
            st.session_state.page = "intro"
            st.rerun()
