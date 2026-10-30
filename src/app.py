import os
import sys
import html as _html
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

# Phase 2 Final Report module (lives next to this file in src/)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_report

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
        background: #ffffff; border: 1px solid #dbe1ff; border-radius: 14px;
        padding: 14px 16px; box-shadow: 0 2px 6px rgba(15,23,42,.05);
    }
    div[data-testid="stMetricLabel"] { font-size: .85rem; color: #64748b; }
    div[data-testid="stMetricValue"] { font-size: 1.65rem; font-weight: 700; color: #1a1f5c; }

    /* ── shared: indigo / lavender palette ── */
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

    /* ── explanation layer: three-line box under every chart ── */
    .explain { background: #f7f8ff; border: 1px solid #dbe1ff;
               border-left: 4px solid #3f4de6; border-radius: 0 10px 10px 0;
               padding: 9px 14px; font-size: .86rem; color: #33385f;
               margin-top: 8px; line-height: 1.5; }
    .explain div { margin: 3px 0; }

    /* ── Start Here ── */
    .flow { display: flex; gap: 10px; margin-top: 6px; }
    .flow .step { flex: 1; background: #ffffff; border: 1px solid #dbe1ff;
                  border-top: 4px solid #3f4de6; border-radius: 10px;
                  padding: 10px 12px; font-size: .83rem; line-height: 1.45; }
    .flow .step strong { color: #1a1f5c; display: block; margin-bottom: 4px; }
    .tour { background: #eef0ff; border: 1px solid #a5b4fc; border-radius: 12px;
            padding: 16px 20px; font-size: .95rem; line-height: 1.55; color: #33385f; }
    .tour h4 { margin: 0 0 8px 0; color: #1a1f5c; }
    .honest { background: #fff7e6; border: 1px solid #f5d38a; color: #7a4f00;
              border-radius: 12px; padding: 14px 18px; font-size: .9rem;
              line-height: 1.55; }
    .honest li { margin-bottom: 6px; }

    /* ── Glossary ── */
    .gterm { background: #ffffff; border: 1px solid #dbe1ff; border-radius: 10px;
             padding: 10px 14px; margin-bottom: 8px; font-size: .9rem;
             line-height: 1.5; color: #33385f; }
    .gterm strong { color: #1a1f5c; }
    .gex { color: #5b6285; font-size: .85rem; margin-top: 4px; display: block; }
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
GLOSSARY_TIP = "Technical terms are defined with ⓘ tooltips here and on the Glossary page."


def takeaway(text):
    st.caption(text)


def explain(shows, reads, means):
    """Three-line explanation box shown under every chart."""
    st.markdown(
        f'<div class="explain">'
        f'<div><strong>What this shows</strong> — {shows}</div>'
        f'<div><strong>How to read it</strong> — {reads}</div>'
        f'<div><strong>What it means for the business</strong> — {means}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def hero_banner():
    """Draw the gradient hero banner (kept from the original design)."""
    fig, ax = plt.subplots(figsize=(12, 2.6), dpi=110)
    cmap = LinearSegmentedColormap.from_list("hero", ["#0f2027", "#203a43", "#2c5364", "#1e3a5f"])
    grad = np.linspace(0, 1, 512).reshape(1, -1)
    ax.imshow(grad, aspect="auto", cmap=cmap, extent=[0, 1, 0, 1])
    ax.text(0.04, 0.62, "eBook Subscriber Intelligence", color="white",
            fontsize=26, fontweight="bold", va="center")
    ax.text(0.04, 0.28, "Propensity scoring  •  Six customer segments  •  Retention & conversion playbook",
            color="#b9d4ff", fontsize=12.5, va="center")
    from matplotlib.patches import Polygon
    cx, cy = 0.87, 0.50
    ww, hh, drop = 0.085, 0.42, 0.05
    ax.add_patch(Polygon(
        [(cx - ww, cy + hh / 2 - drop), (cx, cy + hh / 2),
         (cx, cy - hh / 2), (cx - ww, cy - hh / 2 - drop)],
        closed=True, facecolor="#eef4ff", edgecolor="#93c5fd", linewidth=1.5, zorder=2))
    ax.add_patch(Polygon(
        [(cx, cy + hh / 2 + 0), (cx + ww, cy + hh / 2 - drop),
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


# ── Data (unchanged loaders) ──────────────────────────────────
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


@st.cache_data
def load_v2():
    """Load the v2 scored engagement file + significance-check table."""
    v2 = pd.read_csv("data/processed/v2/scored.csv")
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


@st.cache_data
def load_final_report():
    """Unfiltered Final Report payload — built only from outputs/v2 and
    data/processed/v2 files by src/v2_report.py (never from filtered views)."""
    return v2_report.load_report()


v2_all, sig_v2 = load_v2()


@st.cache_data
def load_sensitivity():
    """Recompute the engagement score under four weight sets on the classified
    subscribers, to show how far the Low/Medium/High tiers depend on the
    approved 0.40/0.35/0.25 split.

    Inputs are min-max normalised exactly as src/v2_score.py does it (recency
    inverted; logins and session minutes scaled over all 5,455 rows, recency
    skipping NaN) and are then held FIXED — only the weights change. Tiers are
    re-cut from each set's own terciles, using the same pd.cut recipe.

    Status is never recomputed here: it is defined on Days Since Last Activity
    alone (plus the >=1-login guard) and reads no score term, so reweighting
    cannot move anyone between Active / Inactive / Churned.
    """
    sets = [("Baseline (approved)", (0.40, 0.35, 0.25)),
            ("Equal thirds", (1 / 3, 1 / 3, 1 / 3)),
            ("Recency-light", (0.25, 0.45, 0.30)),
            ("Recency-heavy", (0.50, 0.30, 0.20))]
    tiers = ["Low", "Medium", "High"]
    order = {"Low": 0, "Medium": 1, "High": 2}

    pop = v2_all[v2_all["Status"].isin(STATUS_ORDER_P2)].copy()

    def minmax(series):
        return (series - series.min()) / (series.max() - series.min())

    # normalise on the FULL 5,455-row basis, then keep the classified rows —
    # this is what makes the baseline reproduce the shipped Tier column
    r_s = minmax(v2_all["Days Since Last Activity"]).loc[pop.index]
    l_s = minmax(v2_all["Avg Logins Per Month"]).loc[pop.index]
    m_s = minmax(v2_all["Avg Session Minutes"]).loc[pop.index]

    scored_sets = {}
    for name, (wr, wl, wm) in sets:
        score = (100 * (wr * (1 - r_s) + wl * l_s + wm * m_s)).round(2)
        lo, hi = score.quantile([1 / 3, 2 / 3])
        tier = pd.cut(score, bins=[-1, lo, hi, 101],
                      labels=tiers).astype(str)
        scored_sets[name] = {"weights": (wr, wl, wm), "score": score,
                             "tier": tier, "lo": lo, "hi": hi}

    base = scored_sets["Baseline (approved)"]
    base_score = base["score"]
    base_tier = base["tier"]
    base_active_low = int(((base_tier == "Low") &
                           (pop["Status"] == "Active")).sum())

    rows = []
    for name, d in scored_sets.items():
        same = int((d["tier"] == base_tier).sum())
        # Spearman = Pearson correlation of the ranks. Computed this way on
        # purpose: Series.corr(method="spearman") calls scipy, which Streamlit
        # Cloud does not ship, and this gives the identical value (verified
        # against scipy locally: max abs diff 1.1e-16).
        rho = base_score.rank().corr(d["score"].rank())
        moved = [order[b] - order[a]
                 for b, a in zip(d["tier"], base_tier)]
        over1 = sum(1 for mv in moved if abs(mv) > 1)
        act_low = int(((d["tier"] == "Low") &
                       (pop["Status"] == "Active")).sum())
        mig = pd.crosstab(pd.Series(base_tier, name="baseline"),
                          pd.Series(d["tier"], name=name)
                          ).reindex(index=tiers, columns=tiers, fill_value=0)
        rows.append({"name": name, "weights": d["weights"],
                     "same_pct": same / len(pop) * 100, "rho": rho,
                     "over1": over1, "active_low": act_low, "mig": mig,
                     "lo": d["lo"], "hi": d["hi"]})
    return rows, base_active_low, len(pop)


STATUS_ORDER_P2 = ["Active", "Inactive", "Churned"]
STATUS_COLORS = {"Active": "#2a9d8f", "Inactive": "#e9c46a",
                 "Churned": "#e76f51", "Unclassified": "#adb5bd"}
V2_CLS_ALL = v2_all[v2_all["Status"] != "Unclassified"]
V2_CUTS = V2_CLS_ALL["Engagement Score"].quantile([1 / 3, 2 / 3]).values
V2_BOUNDS = {
    "Days Since Last Activity": (V2_CLS_ALL["Days Since Last Activity"].min(),
                                 V2_CLS_ALL["Days Since Last Activity"].max()),
    "Avg Logins Per Month": (V2_CLS_ALL["Avg Logins Per Month"].min(),
                             V2_CLS_ALL["Avg Logins Per Month"].max()),
    "Avg Session Minutes": (V2_CLS_ALL["Avg Session Minutes"].min(),
                            V2_CLS_ALL["Avg Session Minutes"].max()),
}

PAGE_HELP = {
    "status": "Active/Inactive/Churned from approved thresholds: Active = 30 days or fewer since last activity AND at least 1 login a month; Inactive = 31–90 days, or 30 days or fewer with fewer than 1 login a month (in practice 0 logins); Churned = more than 90 days. See Glossary.",
    "tier": "Low/Medium/High = tercile (equal third) of the engagement score — see Glossary.",
    "score": "0–100 weighted blend: recency 0.40, logins 0.35, session minutes 0.25 — see Glossary.",
    "recency": "Days Since Last Activity — how long since the last login; the core 'recency' signal — see Glossary.",
    "genre": "Most-read genre recorded per subscriber (single genre only) — see Glossary.",
    "corr": "Correlation: how two metrics move together (−1 to +1) — see Glossary.",
}

# ══════════════════════════════════════════════════════════════
# PAGE 1 — Start Here
# ══════════════════════════════════════════════════════════════
def page_start():
    rep = load_final_report()
    st.title("Start Here")

    st.markdown(
        f"""
        <div class="fr-head"><h3>What this project is, in three sentences</h3>
        <p>
        Most subscribers are staying: <strong>{rep["kpis"][1]["value"]}</strong> of the
        classified subscribers are <strong>Active</strong> — they logged in within the last 30 days
        (all {rep["total"]:,} subscribers in the engagement file).<br>
        <strong>{rep["kpis"][3]["value"]}</strong> are <strong>Churned</strong> — no activity for
        more than 90 days — and <strong>{rep["kpis"][2]["value"]}</strong> are
        <strong>Inactive</strong>, quiet for 31–90 days — or 30 days or fewer with no
        monthly logins — and still win-backable.<br>
        For each group the app prescribes what to do: keep Active readers engaged, win Inactive
        readers back before day 90, and run targeted win-back campaigns for Churned readers.
        </p></div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### How the project works — 5 steps")
    m_clean, m_score, m_status = rep["method"]
    steps = [
        ("1 · Clean the data", m_clean),
        ("2 · Explore", "Charts and correlations first, so what the data shows decides "
                        "what goes into the score."),
        ("3 · Score engagement", m_score),
        ("4 · Classify", m_status),
        ("5 · Recommend actions", "Three strategy cards — Retain (Active), Win back before "
                                   "90 days (Inactive), Win-back (Churned) — each tied to a "
                                   "finding and a literature theme."),
    ]
    st.markdown(
        '<div class="flow">' + "".join(
            f'<div class="step"><strong>{t}</strong>{_html.escape(txt)}</div>'
            for t, txt in steps) + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("#### How to use this app")
    how = [
        "**Start Here** — this page: the idea, the flow, a 6-step guided tour, and honest limits.",
        "**Final Report** — the full unfiltered story (KPIs, findings, strategy cards) with a "
        "downloadable HTML copy.",
        "**Explore the Data** — filter and slice every engagement chart: overview, behaviour, "
        "tiers, genre, demographics, tenure, correlation.",
        "**Customer Lookup** — type a Customer ID to see one subscriber's raw numbers, their "
        "normalised values and exactly how their score adds up.",
        "**Method and Data** — data profile, cleaning decisions, score weights, status rules: "
        "everything needed to reproduce the analysis.",
        "**Glossary** — plain-language definitions with everyday examples for every technical "
        "term used in the app.",
        "**Phase 1 - Propensity** — the original review-1 analysis: demographic propensity "
        "scoring and six customer segments (filters kept separate from Phase 2).",
    ]
    for line in how:
        st.markdown(f"- {line}")

    st.markdown("#### Guided tour — headline numbers in 6 steps")
    tour = [
        ("The data",
         rep["summary"]),
        ("Who is staying, who is leaving",
         rep["pie_takeaway"]),
        ("How engagement is scored",
         f"One number per subscriber (0–100): {rep['method'][1]}"),
        ("What separates Active from Churned",
         rep["findings"][0][1]),
        ("The high-value reader",
         rep["findings"][3][1]),
        ("What to do about it",
         " · ".join(c["title"] for c in rep["cards"])
         + " — the Inactive card runs before day 90, because every Inactive subscriber is "
           "still inside the win-back window."),
    ]
    st.session_state.setdefault("tour_i", 0)
    i = st.session_state.tour_i
    head, body = tour[i]
    st.markdown(
        f'<div class="tour"><h4>Step {i + 1}/6 — {head}</h4>{_html.escape(body)}</div>',
        unsafe_allow_html=True,
    )
    b1, b2, b3 = st.columns([1, 1, 4])
    if b1.button("← Back", width="stretch", disabled=(i == 0)):
        st.session_state.tour_i = max(0, i - 1)
        st.rerun()
    if b2.button("Next →", width="stretch", disabled=(i == len(tour) - 1)):
        st.session_state.tour_i = min(len(tour) - 1, i + 1)
        st.rerun()

    st.markdown("#### What this app can and cannot tell you")
    st.markdown(
        """
        <div class="honest"><ul>
        <li><strong>It shows who is leaving and which signals travel with leaving</strong>
        (recency, logins, session minutes) — it does <strong>not</strong> show why anyone
        cancels: there are no cancellation reasons in the data.</li>
        <li>Every relationship here is an <strong>association, not a cause</strong> — a factor
        that moves with churn is not proven to <em>make</em> churn happen.</li>
        <li>There are <strong>no cancellation dates</strong>, so the app cannot show retention
        curves — only a cross-sectional snapshot of different people at one moment.</li>
        </ul></div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Every technical term used above is defined on the Glossary page.")


# ══════════════════════════════════════════════════════════════
# PAGE 2 — Final Report (unfiltered)
# ══════════════════════════════════════════════════════════════
def page_report():
    try:
        rep = load_final_report()
    except Exception as exc:
        st.error(f"Final Report unavailable — {exc}. Run `python3 src/v2_report.py` first.")
        return
    st.caption(GLOSSARY_TIP)

    # 1 — title + one-sentence project summary
    st.markdown(
        f'<div class="fr-head"><h3>{_html.escape(rep["title"])}</h3>'
        f'<p>{_html.escape(rep["summary"])}</p></div>',
        unsafe_allow_html=True)
    st.caption(
        f"Unfiltered view of all {rep['total']:,} subscribers — filters on other pages "
        "do not affect this report.")

    # 2 — KPI cards (single row) + Unclassified noted separately
    st.markdown("**2 · Key numbers**")
    cols = st.columns(4)
    helps = [
        "Every subscriber in the engagement file (5,455 unique IDs after de-duplication).",
        PAGE_HELP["status"] + " Share of the classified rows; the 33 Unclassified are excluded.",
        PAGE_HELP["status"] + " The win-back window: 31–90 days quiet, plus anyone at 30 days or fewer with no monthly logins.",
        PAGE_HELP["status"] + " Over 90 days quiet — the win-back target.",
    ]
    for c, kpi, h in zip(cols, rep["kpis"], helps):
        c.metric(kpi["label"], kpi["value"], help=h)
    st.caption(rep["un_note"])

    # 3 — status pie + takeaway + explanation
    st.markdown("**3 · Status mix**")
    st.pyplot(v2_report.make_pie(rep), width="stretch")
    takeaway(rep["pie_takeaway"])
    explain(
        "The status mix across the full subscriber population (classified rows).",
        "Each slice's size and label show the count and share; the 33 Unclassified "
        "rows are excluded and noted above.",
        "The size of the staying-versus-leaving problem: how big the keep, win-back "
        "and hard-win-back jobs are.",
    )

    # 4 — key findings
    st.markdown("**4 · Key findings**")
    items = "".join(
        f"<li><strong>{_html.escape(lab)}</strong> — {v2_report.md_html(text)}</li>"
        for lab, text in rep["findings"])
    st.markdown(f'<ol class="fr-find">{items}</ol>', unsafe_allow_html=True)

    # 5 — score tiers: table, rationale, chart, watchlist
    st.markdown("**5 · Score tiers (classified rows)**")
    st.dataframe(pd.DataFrame(rep["tier_rows"]), width="stretch", hide_index=True)
    st.markdown(f'<div class="fr-note">{v2_report.md_html(rep["tier_note"])}</div>',
                unsafe_allow_html=True)
    st.markdown(
        f'<div class="fr-note"><strong>Tier cutoffs — why terciles:</strong> '
        f'{v2_report.md_html(rep["tier_rationale"])}</div>',
        unsafe_allow_html=True)
    st.pyplot(v2_report.make_tier_chart(), width="stretch")
    takeaway(rep["chart_caption"])
    explain(
        "Mean recency, logins, session minutes and books for the Low, Medium and "
        "High tiers (classified rows).",
        "Bars rise from Low to High; books is the independent panel — it is not part "
        "of the score, while recency, logins and session minutes are score inputs.",
        "Tiers genuinely separate behaviour, but three of the four panels rise partly "
        "by construction — read the books panel as the honest external check.",
    )
    w = rep["watchlist"]
    st.markdown(
        f'<div class="fr-note"><strong>Watchlist — early-warning group:</strong> '
        f'{w["n"]} Active subscribers sit in the Low tier (mean recency {w["recency"]} days, '
        f'{w["logins"]} logins, {w["session"]} session minutes, {w["books"]} books).</div>',
        unsafe_allow_html=True)
    try:
        wl = pd.read_csv("outputs/v2/watchlist.csv")
        with st.expander("Technical details — watchlist rows (11 subscribers)"):
            st.dataframe(wl, width="stretch", hide_index=True)
            st.caption("Source: outputs/v2/watchlist.csv — Active today, score already Low: "
                       "the earliest possible warning list.")
    except FileNotFoundError:
        pass

    # 5b — sensitivity of the tiers to the weight split
    st.markdown("**5b · Sensitivity — do the tiers depend on our weights?**")
    try:
        sens_rows, base_al, n_cls = load_sensitivity()
    except Exception as exc:
        sens_rows = None
        st.info(f"Sensitivity check unavailable — {exc}.")
    if sens_rows:
        st.caption(
            f"We re-ran the score on the {n_cls:,} classified subscribers under "
            "four weight splits, holding the normalised inputs fixed and re-cutting "
            "tiers from each set's own terciles. Status is defined on recency alone, "
            "so it cannot move — only the tiers are being tested here.")
        overview = pd.DataFrame([{
            "Weight set": r["name"],
            "Recency / Logins / Sessions":
                " / ".join(f"{w:.2f}" for w in r["weights"]),
            "Same tier as approved": f"{r['same_pct']:.1f}%",
            "Rank correlation (Spearman)": round(r["rho"], 3),
            "Moved >1 tier": f"{r['over1']:,}",
            "Active in Low tier": f"{r['active_low']:,}",
        } for r in sens_rows])
        st.dataframe(overview, width="stretch", hide_index=True)

        for r in sens_rows:
            if r["name"] == "Baseline (approved)":
                continue
            with st.expander(
                    f"Migration table — {r['name']} "
                    f"({r['same_pct']:.1f}% keep their tier)"):
                st.dataframe(r["mig"], width="stretch")

        # honest caveat: the tiers are robust, the watchlist is not
        al = [r["active_low"] for r in sens_rows]
        st.markdown(
            f'<div class="fr-note"><strong>What this means:</strong> the three '
            f'tiers are robust — {min(r["same_pct"] for r in sens_rows[1:]):.0f}%'
            f'–{max(r["same_pct"] for r in sens_rows[1:]):.0f}% of subscribers keep '
            f'their tier and the rank correlation never drops below '
            f'{min(r["rho"] for r in sens_rows[1:]):.3f}, with no subscriber moving '
            f'more than one tier. The <strong>watchlist count above is not '
            f'robust</strong>: those {base_al} Active-in-Low subscribers fall to '
            f'{min(al)} or rise to {max(al)} under equally defensible weight splits, '
            f'so treat the list as a ranked early-warning group rather than a fixed '
            f'size.</div>',
            unsafe_allow_html=True)
        with st.expander("Technical details — method behind the sensitivity check"):
            st.markdown(
                "Inputs are min-max normalised exactly as in `src/v2_score.py` "
                "(recency inverted; logins and session minutes scaled over all "
                "5,455 rows) and held fixed — only the weights change. Tiers are "
                "re-cut from each set's own 1/3 and 2/3 quantiles. Status is read "
                "from `scored.csv` and never recomputed. Full per-subscriber output: "
                "`outputs/v2/sensitivity.csv` and `outputs/v2/sensitivity_summary.md`, "
                "generated by `src/v2_sensitivity_standalone.py`.")

    # 6 — high-value profile
    st.markdown("**6 · High-value subscriber profile (Active+High vs Churned)**")
    sig_cols = ["comparison", "high_value", "churned", "difference",
                "p_value", "effect_size", "effect_size_type", "plain_english"]
    st.dataframe(
        rep["sig_rows"][sig_cols].rename(columns=lambda c: c.replace("_", " ")),
        width="stretch", hide_index=True)
    st.markdown(f'<div class="fr-note">{v2_report.md_html(rep["sig_note"])}</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="fr-note">{v2_report.md_html(rep["sig_foot"])}</div>',
                unsafe_allow_html=True)
    st.caption("p-value, effect size (Cohen's d / Cramér's V) and the multiple-test "
               "correction are defined on the Glossary page.")

    # 7 — strategy cards
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

    # 8 — limitations
    st.markdown("**8 · Limitations**")
    lims = "".join(
        f'<li><strong>{_html.escape(l["lead"])}</strong> {_html.escape(l["body"])}</li>'
        for l in rep["limitations"])
    st.markdown(f'<div class="fr-lims"><ul>{lims}</ul></div>', unsafe_allow_html=True)

    # 9 — method in brief
    st.markdown("**9 · Method in brief**")
    meth_items = "".join(f"<li>{_html.escape(m)}</li>" for m in rep["method"])
    st.markdown(f'<div class="fr-note fr-method"><ul>{meth_items}</ul></div>',
                unsafe_allow_html=True)

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


# ══════════════════════════════════════════════════════════════
# PAGE 3 — Explore the Data (filters + 7 sub-tabs)
# ══════════════════════════════════════════════════════════════
def page_explore():
    st.title("Explore the Data")
    st.caption(GLOSSARY_TIP)

    # ── filters: collapsed expander at the top (moved out of the sidebar) ──
    with st.expander("🔎 Filters", expanded=False):
        r1 = st.columns(4)
        p2_status = r1[0].selectbox(
            "Status", ["All"] + ["Active", "Inactive", "Churned", "Unclassified"],
            key="p2_status", help=PAGE_HELP["status"])
        p2_tier = r1[1].selectbox("Tier", ["All", "Low", "Medium", "High"],
                                  key="p2_tier", help=PAGE_HELP["tier"])
        p2_genre = r1[2].selectbox(
            "Genre", ["All"] + sorted(v2_all["Genre Preference"].unique()),
            key="p2_genre", help=PAGE_HELP["genre"])
        p2_age = r1[3].selectbox("AgeGroup", ["All"] + sorted(v2_all["AgeGroup"].unique()),
                                 key="p2_age",
                                 help="Birth-year band of the subscriber — see Glossary.")
        r2 = st.columns(4)
        p2_occ = r2[0].selectbox("Occupation", ["All"] + sorted(v2_all["Occupation"].unique()),
                                 key="p2_occ",
                                 help="Job category recorded on the customer file.")
        p2_edu = r2[1].selectbox("Education Level",
                                 ["All"] + sorted(v2_all["Education Level"].unique()),
                                 key="p2_edu",
                                 help="Highest education recorded on the customer file.")
        p2_ten = r2[2].selectbox("Tenure band",
                                 ["All", "0-6", "7-12", "13-24", "25-48", "49+"],
                                 key="p2_ten",
                                 help="Months since subscription started — cross-sectional, "
                                      "not a retention curve (see Glossary).")
        p2_state = r2[3].selectbox("State", ["All"] + sorted(v2_all["State"].dropna().unique()),
                                   key="p2_state", help="US state of the subscriber.")

    st.info(
        "**Notes on this page**\n"
        "- The **tenure view is cross-sectional and not a retention curve** — the data has no cancellation dates.\n"
        "- The **33 Unclassified rows are shown separately** and excluded from tier charts and status shares.\n"
        "- **Tier-by-logins agreement is partly by construction**: recency defines status and carries 40% of "
        "the score, and logins and session minutes are score inputs."
    )

    # ── apply filters ──
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
    cls2 = f2[f2["Status"] != "Unclassified"]
    n_cls = len(cls2)
    n_un2 = int((f2["Status"] == "Unclassified").sum())
    st.caption(f"Showing **{n2:,}** of {len(v2_all):,} subscribers · filters apply to "
               "this page only")

    # ── KPI row (single row, st.metric cards) ──
    k = st.columns(6)
    k[0].metric("Subscribers in view", f"{n2:,}",
                help=f"Filtered count out of {len(v2_all):,} in the engagement file.")
    sc = cls2["Status"].value_counts()
    for i, s in enumerate(STATUS_ORDER_P2, start=1):
        share = (sc.get(s, 0) / n_cls) if n_cls else 0.0
        k[i].metric(f"Share {s}", f"{share:.1%}",
                    f"{int(sc.get(s, 0)):,} of {n_cls:,} classified",
                    help=PAGE_HELP["status"] + " Share of classified rows only.")
    st.caption(
        f"Unclassified rows in view: **{n_un2}** — shown separately, excluded from "
        "tier charts and the shares above (see Glossary)."
    )

    sub = st.tabs(["① Overview", "② Behaviour", "③ Tiers", "④ Genre",
                   "⑤ Demographics", "⑥ Tenure", "⑦ Correlation"])

    # ── ① Overview ────────────────────────────────────────────
    with sub[0]:
        st.subheader("Overview — status mix and score distribution")
        if n2 == 0:
            st.info("No subscribers match the current filters.")
        else:
            col_pie, col_hist = st.columns(2)
            with col_pie:
                counts = cls2["Status"].value_counts().reindex(STATUS_ORDER_P2).fillna(0)
                if counts.sum() > 0:
                    fig, ax = plt.subplots(figsize=(6, 4.4))
                    ax.pie(counts.values,
                           labels=[f"{s}\n{int(c):,}" for s, c in zip(counts.index, counts.values)],
                           colors=[STATUS_COLORS[s] for s in counts.index],
                           autopct="%1.1f%%", startangle=90, textprops=dict(fontsize=9.5))
                    ax.set_title("Status mix of the current view (classified rows)")
                    st.pyplot(fig)
                    takeaway("Active is the largest slice of this view; the Unclassified rows "
                             "are excluded here and reported in the KPI caption. Association, not causation.")
                    explain(
                        "The Active/Inactive/Churned split of whatever the filters select.",
                        "Bigger slice = more subscribers in that status; percentages are of "
                        "the classified rows in view.",
                        "How much of the selected audience is healthy, at risk, or already "
                        "gone — the workload for retention effort.",
                    )
                else:
                    st.info("Only Unclassified rows match — status mix needs classified rows.")
            with col_hist:
                fig, ax = plt.subplots(figsize=(6.4, 4.4))
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
                explain(
                    "How the filtered subscribers spread across the 0–100 engagement score, "
                    "with the Low/Medium/High cut points marked.",
                    "Right of the dashed lines = higher engagement; the lines are terciles "
                    "(equal thirds of the full population).",
                    "Whether the selection skews engaged or disengaged — and how many sit "
                    "near the Low tier boundary.",
                )

    # ── ② Behaviour ───────────────────────────────────────────
    with sub[1]:
        st.subheader("Behaviour by status")
        if n_cls == 0:
            st.info("No classified rows match the current filters.")
        else:
            BEHAV = [("Avg Logins Per Month", "Avg Logins Per Month"),
                     ("Avg Session Minutes", "Avg Session Minutes"),
                     ("Books Accessed", "Books Accessed (descriptive only)"),
                     ("Days Since Last Activity", "Days Since Last Activity")]
            fig, axes = plt.subplots(2, 2, figsize=(11, 7.4))
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
            explain(
                "The spread of logins, session minutes, books and days since activity for "
                "Active, Inactive and Churned subscribers.",
                "Each box shows the middle half of that group; boxes that don't overlap mean "
                "the groups genuinely differ. The recency panel follows the status rule by "
                "definition.",
                "Behaviour — not just demographics — separates the groups, so usage-based "
                "messaging (how much someone read) is the right lever.",
            )

    # ── ③ Tiers (full population — filters do not apply) ──────
    with sub[2]:
        rep = load_final_report()
        st.subheader("Score tiers — Low / Medium / High")
        st.caption("This tab shows the **full subscriber population** (tier definitions and "
                   "the watchlist are population-level facts; the filters above do not apply "
                   "here).")
        st.dataframe(pd.DataFrame(rep["tier_rows"]), width="stretch", hide_index=True)
        st.markdown(f'<div class="fr-note">{v2_report.md_html(rep["tier_note"])}</div>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<div class="fr-note"><strong>Tier cutoffs — why terciles:</strong> '
            f'{v2_report.md_html(rep["tier_rationale"])}</div>',
            unsafe_allow_html=True)
        st.pyplot(v2_report.make_tier_chart(), width="stretch")
        takeaway(rep["chart_caption"])
        explain(
            "Mean recency, logins, session minutes and books in each score tier "
            "(classified rows).",
            "All four panels rise Low → High; books is not a score input, so its rise is "
            "the independent confirmation — the other three rise partly by construction.",
            "Tier labels track real behaviour differences, with one honest outside check "
            "(books) behind them.",
        )
        w = rep["watchlist"]
        st.markdown(
            f'<div class="fr-note"><strong>Watchlist — early-warning group:</strong> '
            f'{w["n"]} Active subscribers sit in the Low tier (mean recency {w["recency"]} days, '
            f'{w["logins"]} logins, {w["session"]} session minutes, {w["books"]} books) — '
            f'still Active today, engagement already Low.</div>',
            unsafe_allow_html=True)
        with st.expander("Technical details — watchlist rows and status x tier table"):
            try:
                st.dataframe(pd.read_csv("outputs/v2/watchlist.csv"),
                             width="stretch", hide_index=True)
            except FileNotFoundError:
                st.caption("outputs/v2/watchlist.csv not found — run src/v2_tier_docs.py.")
            ct = pd.crosstab(v2_all["Status"], v2_all["Tier"]).reindex(
                index=["Active", "Inactive", "Churned", "Unclassified"],
                columns=["Low", "Medium", "High"]).fillna(0).astype(int)
            st.markdown("**Status x tier (full population):**")
            st.dataframe(ct, width="stretch")

    # ── ④ Genre ───────────────────────────────────────────────
    with sub[3]:
        st.subheader("Genre preference")
        if n_cls == 0:
            st.info("No classified rows match the current filters.")
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
                explain(
                    "What each status group reads: genre shares stacked per status.",
                    "Identical-looking stacks across the three groups mean genre mix is the "
                    "same regardless of status.",
                    "Don't build status or churn campaigns on genre — it carries no signal here.",
                )
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
                explain(
                    "Active rate (green) and Churned rate (red) within each genre; groups "
                    "under 100 subscribers are excluded from the chart.",
                    "Paired bars of similar height across genres = genre doesn't predict "
                    "status; red-flagged small groups are too few to judge.",
                    "No genre-targeted retention play is justified by this data; the "
                    "Fantasy-looking gap fails the multiple-test correction (see Glossary).",
                )
            with st.expander("Technical details — genre rate table"):
                st.dataframe(
                    gt[["n", "active_pct", "churned_pct", "small"]].round(1)
                    .rename(columns={"n": "classified n", "active_pct": "Active %",
                                     "churned_pct": "Churned %"}),
                    width="stretch")

    # ── ⑤ Demographics ────────────────────────────────────────
    with sub[4]:
        st.subheader("Demographic profile")
        if n_cls == 0:
            st.info("No classified rows match the current filters.")
        else:
            RATE_DIMS = ["IncomeBand", "Occupation", "AgeGroup", "Education Level"]
            fig, axes = plt.subplots(2, 2, figsize=(13, 7.6))
            for ax, dim in zip(axes.ravel(), RATE_DIMS):
                ct = pd.crosstab(cls2[dim], cls2["Status"])
                for s in STATUS_ORDER_P2:
                    if s not in ct:
                        ct[s] = 0
                ct = ct[STATUS_ORDER_P2]
                nn = ct.sum(axis=1)
                ok = nn >= 100
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
            explain(
                "Active and Churned rates for each demographic group with at least 100 "
                "subscribers (income band, occupation, age group, education).",
                "Green = share Active, red = share Churned inside each group; taller gaps "
                "between groups mean demographics move with status — but only modestly "
                "(small effect sizes, see Glossary).",
                "Use demographics for tailoring, not for judging churn risk: effects are "
                "real but small, and behaviour counts for more.",
            )

            hv2 = cls2[(cls2["Status"] == "Active") & (cls2["Tier"] == "High")]
            ch2 = cls2[cls2["Status"] == "Churned"]
            if len(hv2) and len(ch2):
                NUM4 = ["Annual Income", "Avg Monthly Spend",
                        "Number of Children At Home", "Age"]
                fig, axes = plt.subplots(2, 2, figsize=(11, 6.6))
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
                         "practical terms — see the effect-size table in the details. "
                         "Association, not causation.")
                explain(
                    "Average income, spend, children and age of the high-value group "
                    "(Active + High tier) next to Churned subscribers.",
                    "Compare the two bars inside each panel; visibly close bars = small "
                    "difference even if a p-value calls it significant.",
                    "The high-value profile is a tendency (wealthier, slightly younger "
                    "families), not a dividing line — target gently.",
                )
            else:
                st.info("The current filters leave no Active+High or Churned rows to compare.")

            st.warning(
                "**Differences are small in practical terms (Cohen's d about 0.2-0.3, "
                "Cramer's V under 0.1); associations only.** With n≈1,803 vs 901, small "
                "gaps can be significant while still being practically small — read the "
                "effect size, not just the p-value (both defined on the Glossary page). "
                "**Genre: Fantasy is not robust after the multiple-test correction.**")
            with st.expander("Technical details — effect-size table (Active+High vs Churned)"):
                st.dataframe(
                    sig_v2[["comparison", "high_value", "churned", "difference",
                            "p_value", "effect_size", "effect_size_type",
                            "plain_english", "Note"]],
                    width="stretch", height=340)
                st.caption("Table computed on the full dataset (not filtered).")

    # ── ⑥ Tenure ──────────────────────────────────────────────
    with sub[5]:
        st.subheader("Status mix by tenure band")
        st.info("**Cross-sectional comparison, not a retention curve** — the data has no "
                "cancellation dates, so it cannot show how any cohort's status changes over "
                "time (see Glossary).")
        if n_cls == 0:
            st.info("No classified rows match the current filters.")
        else:
            BANDS = ["0-6", "7-12", "13-24", "25-48", "49+"]
            ct = (pd.crosstab(cls2["Tenure Band"], cls2["Status"])
                  .reindex(index=BANDS, columns=STATUS_ORDER_P2)
                  .fillna(0))
            pct = ct.div(ct.sum(axis=1).replace(0, np.nan), axis=0).mul(100)
            fig, ax = plt.subplots(figsize=(10, 4.8))
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
            explain(
                "How Active/Inactive/Churned shares look inside each tenure band "
                "(months since subscribing).",
                "Compare the colour proportions across the five bands; similar mixes mean "
                "tenure doesn't separate statuses (churned rates are non-monotone).",
                "Tenure alone shouldn't drive win-back targeting — and no retention-over-time "
                "claim can be made from this snapshot.",
            )
            with st.expander("Technical details — counts by tenure band"):
                tbl = ct.copy()
                tbl.columns = [f"{c} n" for c in tbl.columns]
                tbl["classified n"] = ct.sum(axis=1)
                st.dataframe(tbl, width="stretch")

    # ── ⑦ Correlation ─────────────────────────────────────────
    with sub[6]:
        st.subheader("Correlation heatmap — engagement metrics")
        if n2 < 10:
            st.info("Need at least 10 rows to compute correlations with the current filters.")
        else:
            cols5 = ["Days Since Last Activity", "Avg Logins Per Month",
                     "Avg Session Minutes", "Books Accessed", "Subscription Tenure Months"]
            corr = f2[cols5].corr()
            fig, ax = plt.subplots(figsize=(8, 5.8))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                        vmin=-1, vmax=1, ax=ax)
            ax.set_title("Pearson correlations — engagement metrics + tenure")
            st.pyplot(fig)
            takeaway("Logins vs books is the only strong pair (r≈0.88): both measure usage "
                     "frequency, so both would double-count in one score — books stays "
                     "descriptive. Tenure barely correlates with anything. Association, not causation.")
            explain(
                "How strongly each pair of engagement metrics moves together (−1 to +1).",
                "Near +1 = the two rise together (0.88 logins vs books = basically the same "
                "information — double-counting, see Glossary); near 0 = unrelated.",
                "Justifies excluding books from the score: counting it would weight usage "
                "frequency twice.",
            )


# ══════════════════════════════════════════════════════════════
# PAGE 4 — Customer Lookup
# ══════════════════════════════════════════════════════════════
def page_lookup():
    st.title("Customer Lookup")
    st.caption("Enter a Customer ID (e.g. 11001) to see the raw inputs, their normalised "
               "values, the weighted contributions, score, tier and status. "
               + GLOSSARY_TIP)
    p2_id = st.text_input("Customer ID", key="p2_lookup_id",
                          help="Identifier from the customer file (numbers like 11001).")
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
                k1.metric("Engagement score", f"{r['Engagement Score']:.1f}",
                          help=PAGE_HELP["score"])
                k2.metric("Tier", r["Tier"], help=PAGE_HELP["tier"])
                k3.metric("Status", r["Status"], help=PAGE_HELP["status"])
                k4.metric("Genre", r["Genre Preference"], help=PAGE_HELP["genre"])

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
                    wl_, ws_ = round(0.35 / 0.60, 4), round(0.25 / 0.60, 4)
                    st.caption("Unclassified (no recency): score uses logins + session only, "
                               "weights renormalised to sum to 1 (see Glossary).")
                else:
                    wl_, ws_ = 0.35, 0.25
                contrib.append(["Avg Logins Per Month", r["Avg Logins Per Month"],
                                round(l_s, 3), wl_, round(100 * wl_ * l_s, 2)])
                contrib.append(["Avg Session Minutes", r["Avg Session Minutes"],
                                round(s_s, 3), ws_, round(100 * ws_ * s_s, 2)])
                contrib.append(["Books Accessed", r["Books Accessed"], "—", 0.00,
                                "excluded (r=0.88 with logins)"])
                st.markdown("**Raw inputs → normalised → weighted contributions**")
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
                st.caption("Normalised = min-max scaling to 0–1 against the full range of "
                           "that metric (see Glossary); weight = that input's share of the "
                           "score.")


# ══════════════════════════════════════════════════════════════
# PAGE 5 — Method and Data
# ══════════════════════════════════════════════════════════════
def page_method():
    st.title("Method and Data")
    st.caption("Everything needed to reproduce the analysis. " + GLOSSARY_TIP)

    st.markdown("**Data profile**")
    try:
        raw = pd.read_csv("data/raw/eBook_Engagement.csv")
        clean_v2 = pd.read_csv("data/processed/v2/engagement_clean.csv")
        p = st.columns(6)
        p[0].metric("Raw engagement rows", f"{len(raw):,}",
                    help="Rows in data/raw/eBook_Engagement.csv before cleaning (never modified).")
        p[1].metric("Cleaned subscribers", f"{len(clean_v2):,}",
                    help="Unique subscribers after dropping exact duplicates (see cleaning rules below).")
        p[2].metric("Rows with an imputed value", f"{int(clean_v2['Imputed'].sum()):,}",
                    help="Rows where a blank behaviour value was median-filled and flagged "
                         "'Imputed' — never recency (see Glossary).")
        p[3].metric("Distinct genres", f"{clean_v2['Genre Preference'].nunique()}",
                    help=PAGE_HELP["genre"] + " Canonical set after collapsing spelling variants.")
        p[4].metric("Missing/invalid recency",
                    f"{int(clean_v2['Days Since Last Activity'].isna().sum())}",
                    help="Rows left unclassified rather than guessed — the 33 Unclassified "
                         "(see Glossary).")
        p[5].metric("Scored rows", f"{len(v2_all):,}",
                    help="Rows in data/processed/v2/scored.csv with status, score and tier.")
    except FileNotFoundError as exc:
        st.error(f"Data file missing — {exc}. Run the v2 pipeline first.")

    st.markdown("**Approved methodology sections**")
    try:
        with open("outputs/v2/methodology.md") as f:
            meth = f.read()
        import re as _re
        parts = _re.split(r"(?=^## )", meth, flags=_re.M)
        main_head = ("1.", "2.", "5.", "7.")
        other = []
        for part in parts:
            if part.startswith("## "):
                head = part[3:].split("\n", 1)[0]
                if head.startswith(main_head):
                    st.markdown(part)
                else:
                    other.append(part)
            else:
                other.append(part)
        with st.expander("Technical details — remaining methodology sections "
                         "(outputs, merge, standing rules, significance checks)"):
            st.markdown("".join(other))
    except FileNotFoundError:
        st.error("outputs/v2/methodology.md not found — run the v2 pipeline first.")


# ══════════════════════════════════════════════════════════════
# PAGE 6 — Glossary
# ══════════════════════════════════════════════════════════════
def page_glossary():
    st.title("Glossary")
    st.caption("Plain-language definitions with an everyday example for every technical "
               "term used in this app.")
    terms = [
        ("Active",
         "A subscriber who logged in within the last 30 days, with at least one login per "
         "month — our definition of 'still using the service'.",
         "A gym member who visited this month — clearly still a member in practice."),
        ("Inactive",
         "A subscriber quiet for 31 to 90 days (or under 30 days with zero average logins) "
         "— the habit has lapsed but it isn't a sustained lapse yet.",
         "Someone who went to the gym last month but not this one — still worth a nudge."),
        ("Churned",
         "A subscriber with no activity for more than 90 days — three full monthly cycles.",
         "A member whose last visit was four months ago — effectively gone until "
         "proven otherwise."),
        ("Recency (Days Since Last Activity)",
         "How many days since the subscriber last logged in. Higher = colder = weaker "
         "engagement.",
         "Of two friends, one texted you yesterday and the other last month — the second "
         "one's habit is fading."),
        ("Engagement score (0–100)",
         "One number per subscriber blending recency (40%), monthly logins (35%) and "
         "session minutes (25%), each scaled to 0–1 and weighted, then multiplied by 100.",
         "Like a driving score that combines how recently you drove, how often, and for "
         "how long — a single grade from the three."),
        ("Min-max scaling",
         "Squeezing a metric so its values run from 0 (worst) to 1 (best) using that "
         "metric's actual minimum and maximum — raw logins and raw minutes can't be "
         "compared until they're on one scale.",
         "Converting two different tests' marks into 'percent of the top score' so they "
         "can be added together."),
        ("Weights",
         "How much each input counts in the score; ours sum to 1 (0.40 + 0.35 + 0.25).",
         "A school grade where the final exam is worth 40% and two other pieces 35% and "
         "25% — each part pulls the total by its share."),
        ("Tercile / tier",
         "Splitting scores into three equal-sized groups: Low (up to the lower cut), "
         "Medium, High. The cut points come from the data (the score's one-third and "
         "two-third marks), not from round numbers.",
         "Lining students up by grade and cutting the line into bottom, middle and top "
         "thirds — the cuts land where the data lands."),
        ("Correlation and double-counting",
         "Correlation (−1 to +1) measures how two metrics move together. If two are highly "
         "correlated, using both in one score double-counts the same behaviour.",
         "Height and weight correlate strongly; scoring health by both would credit tall "
         "people twice for essentially one fact. That is why books (r=0.88 with logins) is "
         "excluded from our score."),
        ("Effect size — Cohen's d and Cramér's V",
         "How big a difference actually is, once you stop caring about sample size: d for "
         "numbers (0.2 small, 0.5 medium, 0.8 large), V for categories (0 to 1).",
         "A one-minute difference in average commute between two cities can be real and "
         "statistically solid, yet nobody would move house for it — small effect."),
        ("p-value",
         "How surprising the observed difference would be if there were really no "
         "difference at all. Small p (< 0.05) = surprising; with many tests we tighten the "
         "bar (Bonferroni ≈ 0.0056 for our 9 tests) so random flukes don't get promoted to "
         "findings.",
         "Flipping a coin 10 times and getting 8 heads: unlikely enough that you'd doubt "
         "the coin — but if you tried 100 different coins, one will look odd by luck."),
        ("Cross-sectional vs retention curve",
         "A cross-section is a photo of different people at one moment; a retention curve "
         "follows the same people over time. Our data has no cancellation dates, so we only "
         "have the photo.",
         "A stadium crowd photo vs tracking one season-ticket holder's attendance for a "
         "year — only the second shows how behaviour changes over time."),
        ("Imputation",
         "Filling a missing value with a typical observed value (we use the column median) "
         "and flagging the row as Imputed. Recency is never imputed — we won't invent when "
         "someone last showed up.",
         "A student missing one homework mark gets the class median — recorded as a fill, "
         "so everyone knows it wasn't actually handed in."),
        ("Unclassified",
         "The 33 subscribers whose recency is missing or invalid: they cannot honestly be "
         "placed in Active/Inactive/Churned, so they're shown separately and scored from "
         "logins + session only.",
         "A library card with no date stamp — you can't claim when the person last "
         "visited, so you don't guess."),
        ("Watchlist (early-warning group)",
         "Active subscribers who already sit in the Low score tier — still within the 30-day "
         "window but with weak behaviour; the earliest signal that someone is sliding toward "
         "Inactive.",
         "A regular customer who came in this week but bought noticeably less than usual — "
         "worth checking on before they disappear."),
    ]
    for name, definition, example in terms:
        st.markdown(
            f'<div class="gterm"><strong>{_html.escape(name)}</strong> — '
            f'{_html.escape(example and definition)}'
            f'<span class="gex"><em>Everyday example:</em> {_html.escape(example)}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════
# PAGE 7 — Phase 1 (original review-1 analysis, intact)
# ══════════════════════════════════════════════════════════════
def page_phase1():
    st.title("Phase 1 - Propensity")
    st.caption(
        "Based on demographic and spend data only; no usage-based engagement metrics were "
        "available in the source dataset. " + GLOSSARY_TIP)

    # ── Phase 1 filters (its own set, out of the sidebar) ─────
    with st.expander("🔎 Phase 1 filters", expanded=False):
        fc = st.columns(5)
        state_sel = fc[0].selectbox(
            "State", ["All"] + sorted(segmented["State"].dropna().unique()),
            help="US state of the customer (Phase 1 file).")
        occ_sel = fc[1].selectbox(
            "Occupation", ["All"] + sorted(segmented["Occupation"].dropna().unique()),
            help="Job category on the customer file.")
        edu_sel = fc[2].selectbox(
            "Education Level", ["All"] + sorted(segmented["Education Level"].dropna().unique()),
            help="Highest education recorded on the customer file.")
        age_sel = fc[3].selectbox(
            "AgeGroup", ["All"] + sorted(segmented["AgeGroup"].dropna().unique()),
            help="Birth-year band (Phase 1 file).")
        seg_sel = fc[4].multiselect(
            "Segment", SEG_ORDER, default=SEG_ORDER,
            help="One of the six propensity segments (see the Segment Profiles tab).")

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

    st.caption(
        f"Showing **{len(filtered):,}** of {len(segmented):,} customers · "
        "these filters apply to the Phase 1 tabs below only"
    )

    # ── KPI row (single row, help on every card) ──────────────
    n = len(filtered)
    sub_rate = filtered["eBook Subscriber Flag"].mean() if n else 0.0
    avg_score = filtered["Subscriber_Propensity_Score"].mean() if n else 0.0
    avg_spend = filtered["Clean_Avg Monthly Spend"].mean() if n else 0.0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers in view", f"{n:,}", f"{n / len(segmented) * 100:.1f}% of base",
              help="Customers matching the Phase 1 filters.")
    c2.metric("Subscriber rate", f"{sub_rate:.1%}", f"vs {overall_rate:.1%} overall",
              help="Share of customers with the subscriber flag set to 1.")
    c3.metric("Avg propensity score", f"{avg_score:.1f}", "scale 0–100",
              help="Phase 1 score of how likely a customer is to subscribe "
                   "(0.40 children + 0.35 spend + 0.25 income) — review-1 model.")
    c4.metric("Avg monthly spend", f"${avg_spend:.1f}", "per customer",
              help="Mean monthly spend of the customers in view.")

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
            fig1, ax1 = plt.subplots(figsize=(6.4, 5.0))
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
            explain(
                "The six propensity segments sized by how many filtered customers are in each.",
                "Bigger slice = more people; the centre number is the filtered total.",
                "Shows where the customer base concentrates — protect the large slices and "
                "treat small ones as niche or untapped.",
            )
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
                explain(
                    "The share of customers who subscribed, split by occupation.",
                    "Bars past the red dashed line beat this view's average; shorter bars "
                    "lag.",
                    "Point acquisition and retention spend at the occupations above the line.",
                )
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
                explain(
                    "The share of customers who subscribed, split by birth-year band.",
                    "Taller bar = higher subscription share; the dashed line is the average "
                    "of the current view.",
                    "Age bands above the line respond best — useful for targeting campaigns.",
                )
        st.markdown("**Where do propensity scores sit?**")
        fig4, ax4 = plt.subplots(figsize=(10, 3.2))
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
        explain(
            "How propensity scores spread across the filtered customers, with the "
            "Low/Medium/High boundaries marked.",
            "Right of the lines = high propensity to subscribe; the lines are tercile cuts "
            "(equal thirds — see Glossary).",
            "The shape tells you how much of the audience is worth chasing hardest for "
            "conversion.",
        )

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
            fig5, ax5 = plt.subplots(figsize=(7.5, 5.4))
            sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f",
                        linewidths=0.6, ax=ax5, vmin=-1, vmax=1,
                        cbar_kws={"label": "Pearson r"})
            ax5.set_title("Pearson correlations among numeric fields", fontsize=12, fontweight="bold")
            st.pyplot(fig5)
            takeaway("Children at home (0.46) and monthly spend (0.42) relate to subscription more than "
                     "income (0.29); income and spend correlate with each other (≈0.61) but stay below the "
                     "0.8 collinearity threshold, so both were kept in the score.")
            explain(
                "How strongly each pair of Phase 1 numeric fields moves together, including "
                "the subscriber flag.",
                "Near ±1 = the two move together (see Glossary for correlation and "
                "double-counting); the Subscriber Flag row shows which fields travel with "
                "subscription.",
                "Confirms the three score inputs are distinct enough to count separately "
                "and shows what drives subscription.",
            )

    # ── Tab 3: Segment profiles ───────────────────────────────
    with tabs[2]:
        st.subheader("Segment profiles")
        age_map = {"1910-1949": 1930, "1950-1959": 1955, "1960-1969": 1965, "1970-1979": 1975}
        rows = []
        for seg in SEG_ORDER:
            sub_s = filtered[filtered["Segment"] == seg]
            if len(sub_s) == 0:
                continue
            rows.append({
                "Segment": seg,
                "Customers": len(sub_s),
                "Mean Age (yr)": round(sub_s["AgeGroup"].map(age_map).mean(), 0),
                "Mean Income ($)": round(sub_s["Clean_Annual Income"].mean(), 0),
                "Mean Spend ($/mo)": round(sub_s["Clean_Avg Monthly Spend"].mean(), 1),
                "Mean Children": round(sub_s["Clean_Children At Home"].mean(), 1),
                "Top Occupation": sub_s["Occupation"].mode().iloc[0],
                "Top State": sub_s["State"].mode().iloc[0],
            })
        if not rows:
            st.info("No customers match the current filters.")
        else:
            prof_df = pd.DataFrame(rows)
            st.dataframe(prof_df.set_index("Segment"), width="stretch", height=250)
            takeaway("Read across a row for that segment's average customer. "
                     "Core Subscribers top income and spend; High-potential Prospects run close behind.")

            st.markdown("**Side-by-side comparison**")
            metrics = [("Mean Income ($)", "#2563eb"), ("Mean Spend ($/mo)", "#16a34a"),
                       ("Mean Children", "#d97706")]
            fig6, axes = plt.subplots(1, 3, figsize=(13, 3.6))
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
            explain(
                "Average income, spend and children for each of the six segments "
                "(three panels, one metric each).",
                "Compare bar heights across segments inside each panel — same segments on "
                "the same three metrics.",
                "The segments carrying the most value today (Core) and the closest runners-up "
                "— the order for upsell and retention attention.",
            )

    # ── Tab 4: Customer lookup ────────────────────────────────
    with tabs[3]:
        st.subheader("Customer lookup")
        st.caption("Enter a Customer ID from the dataset (e.g. 11000) to see that person's "
                   "score, tier and segment.")
        cus_id = st.text_input("Customer ID", key="p1_lookup_id")
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
                    k1.metric("Propensity score", f"{r['Subscriber_Propensity_Score']:.1f}",
                              help="Phase 1 propensity score (0–100) — likelihood to subscribe.")
                    k2.metric("Tier", r["Tier"], help="Low/Medium/High by propensity tercile.")
                    k3.metric("Segment", segment, help="One of the six Phase 1 segments.")
                    k4.metric("Subscriber?", "Yes" if int(r["eBook Subscriber Flag"]) == 1 else "No",
                              help="Whether the customer file flags this person as a subscriber.")
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


# ══════════════════════════════════════════════════════════════
# Navigation (7 pages; Phase 1 kept as the last section)
# ══════════════════════════════════════════════════════════════
nav = st.navigation(
    [
        st.Page(page_start, title="Start Here", icon="🏠", default=True),
        st.Page(page_report, title="Final Report", icon="📄"),
        st.Page(page_explore, title="Explore the Data", icon="📊"),
        st.Page(page_lookup, title="Customer Lookup", icon="🔍"),
        st.Page(page_method, title="Method and Data", icon="📐"),
        st.Page(page_glossary, title="Glossary", icon="📖"),
        st.Page(page_phase1, title="Phase 1 - Propensity", icon="🎯"),
    ],
    position="sidebar",
)
nav.run()
