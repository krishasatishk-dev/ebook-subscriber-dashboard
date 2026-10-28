"""Final Report builder for Phase 2 (engagement).

Reads ONLY outputs/v2/ and data/processed/v2/ files and produces:
  - outputs/v2/final_report.html  (self-contained, opens offline)
  - the same content as a dict/figure that src/app.py renders as the
    first Phase 2 tab, so app and HTML can never disagree.

No number or recommendation text is hardcoded here: every figure comes
from scored.csv / status_summary.csv / significance_checks.csv, and every
sentence comes from insights.md or methodology.md (parsed at runtime).
Analysis code and data are untouched — this script only reads them.
"""

import base64
import html as html_mod
import io
import os
import re

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# tier chart + Stage-1 methodology text share the same producer module
sys_path_src = os.path.join(os.path.dirname(os.path.abspath(__file__)))
if sys_path_src not in os.sys.path:
    os.sys.path.insert(0, sys_path_src)
from v2_tier_docs import make_tier_chart  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "outputs", "v2")
DATA_DIR = os.path.join(ROOT, "data", "processed", "v2")
HTML_PATH = os.path.join(OUT_DIR, "final_report.html")

# Report palette (approved for this page)
INDIGO_DARK = "#1a1f5c"
INDIGO = "#3f4de6"
LAVENDER = "#a5b4fc"
LAVENDER_PALE = "#dbe1ff"
STATUS_HEX = {"Active": "#16a34a", "Inactive": "#d97706", "Churned": "#dc2626"}


# ── small markdown parsing helpers ─────────────────────────────
def _norm(text):
    """Collapse whitespace so sentences survive markdown line-wrapping."""
    return re.sub(r"\s+", " ", text).strip()


def _section(md, heading):
    """Return the raw text of the `## heading` section (up to next `## `)."""
    pat = re.compile(r"^## " + re.escape(heading) + r".*?$(.*?)(?=^## |^# |\Z)",
                     re.M | re.S)
    m = pat.search(md)
    return m.group(1) if m else ""


def _paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def _para_containing(text, key):
    """First paragraph containing `key`, whitespace-normalised."""
    for p in _paragraphs(text):
        if key in p:
            return _norm(p)
    raise KeyError(f"no paragraph containing {key!r}")


def _sentences(text):
    # second branch splits after a sentence period that closes a bold span
    # (e.g. "...statuses.** Next sentence") which the first branch misses
    return re.split(r"(?<=[.!?]) +|(?<=\.\*\*) +", _norm(text))


def _sentences_with(text, *keys):
    return [s for s in _sentences(text) if any(k in s for k in keys)]


def _strip_md(text):
    """Markdown bold/italics/backticks -> plain text (for the HTML file)."""
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    t = t.replace("`", "")
    return t


def _md_bold_to_html(text):
    """Markdown bold -> <strong>, rest escaped (for safe HTML embedding)."""
    parts = re.split(r"(\*\*.+?\*\*)", text)
    out = []
    for p in parts:
        if p.startswith("**") and p.endswith("**") and len(p) > 4:
            out.append("<strong>" + html_mod.escape(p[2:-2]) + "</strong>")
        else:
            out.append(html_mod.escape(p))
    return "".join(out).replace("`", "")


# public alias used by src/app.py so the app tab renders the exact same text
md_html = _md_bold_to_html


# ── load everything from the v2 files ──────────────────────────
def load_report():
    """Build the full report payload from outputs/v2 + data/processed/v2."""
    scored = pd.read_csv(os.path.join(DATA_DIR, "scored.csv"))
    status = pd.read_csv(os.path.join(OUT_DIR, "status_summary.csv"))
    sig = pd.read_csv(os.path.join(OUT_DIR, "significance_checks.csv"))
    with open(os.path.join(OUT_DIR, "insights.md")) as f:
        insights = f.read()
    with open(os.path.join(OUT_DIR, "methodology.md")) as f:
        meth = f.read()

    # ── 1. title + one-sentence summary (numbers from the files) ──
    st_map = {r["Status"]: r for _, r in status.iterrows()}
    total = len(scored)
    pct = lambda s: float(st_map[s]["% of classified"])
    n_un = int(st_map["Unclassified"]["Customers"])
    w_rows = re.findall(r"^\| (Days Since Last Activity \(inverted\)|Avg Logins"
                        r" Per Month|Avg Session Minutes) \| ([\d.]+) \|",
                        meth, re.M)
    weights = dict(w_rows)
    title = "Final Report — eBook Subscriber Insights (Phase 2)"
    summary = (
        f"Phase 2 of the eBook Subscriber Insights project scores all {total:,} "
        f"subscribers on recency, logins and session minutes using approved thresholds "
        f"and weights, splitting them into Active ({pct('Active'):.1f}%), Inactive "
        f"({pct('Inactive'):.1f}%) and Churned ({pct('Churned'):.1f}%) and setting a "
        f"recommended strategy for each segment."
    )

    # ── 2. KPI rows (status_summary.csv) ──────────────────────────
    kpis = [
        {"label": "Total subscribers", "value": f"{total:,}", "color": INDIGO_DARK},
        {"label": "% Active (of classified)", "value": f"{pct('Active'):.1f}%",
         "color": STATUS_HEX["Active"]},
        {"label": "% Inactive (of classified)", "value": f"{pct('Inactive'):.1f}%",
         "color": STATUS_HEX["Inactive"]},
        {"label": "% Churned (of classified)", "value": f"{pct('Churned'):.1f}%",
         "color": STATUS_HEX["Churned"]},
    ]
    un_note = (
        f"Unclassified: {n_un} rows — missing or invalid recency, never imputed; "
        f"reported separately and excluded from the three shares above."
    )

    # ── 3. status pie + takeaway ──────────────────────────────────
    pie_counts = {s: int(st_map[s]["Customers"]) for s in STATUS_HEX}
    pie_total = sum(pie_counts.values())
    pie_takeaway = (
        f"Active is the largest slice: {pie_counts['Active']:,} of the {pie_total:,} "
        f"classified subscribers ({pct('Active'):.1f}%) are Active versus "
        f"{pct('Churned'):.1f}% Churned — the {n_un} Unclassified rows are excluded "
        f"and shown separately. Association, not causation."
    )

    # ── 4. key findings: sentences lifted from insights.md ───────
    sec_b = _section(insights, "(b) What separates Active from Churned")
    sec_a = _section(insights, "(a) The high-value subscriber profile")
    sec_c = _section(insights, "(c) Null findings: genre and tenure")
    caution = _section(insights, "Multiple-comparison caution")
    para_behav = _para_containing(sec_b, "11.69")
    para_indep = _para_containing(sec_b, "books rise **4.1")
    para_effect = _para_containing(caution, "demographic effects are small")
    para_profile = _para_containing(sec_a, "$99,810")
    para_assoc = _para_containing(sec_a, "association, not a cause")
    para_genre = _para_containing(sec_c, "52.0%")
    para_tenure = _para_containing(sec_c, "16.5%")

    findings = [
        ("Behaviour gap — Active vs Churned",
         " ".join(_sentences_with(para_behav, "11.69", "median:"))),
        ("Independent check — books and tenure (not score inputs)",
         " ".join(_sentences_with(para_indep, "4.1", "real validation"))),
        ("How big are the demographic effects? — honest reading",
         " ".join(_sentences_with(para_effect, "demographic effects are small"))),
        ("High-value subscriber profile",
         " ".join(_sentences_with(para_profile, "$99,810"))),
        ("Null finding — genre does not separate statuses",
         " ".join(_sentences_with(para_genre, "52.0%", "no genre finding survives"))),
        ("Null finding — tenure does not separate churn",
         " ".join(_sentences_with(para_tenure, "Tenure does not reliably",
                                  "16.5%"))),
    ]

    # ── 5. tier table from scored.csv + by-construction note ──────
    cls = scored[scored["Status"] != "Unclassified"].copy()
    cuts_m = re.search(r"Low <= ([\d.]+) < Medium <= ([\d.]+) < High", meth)
    cut_low, cut_med = cuts_m.group(1), cuts_m.group(2)
    cut_map = {"Low": f"score ≤ {cut_low}", "Medium": f"≤ {cut_med}",
               "High": f"> {cut_med}"}
    tier_rows = []
    for tier in ["Low", "Medium", "High"]:
        sub = cls[cls["Tier"] == tier]
        tier_rows.append({
            "Tier": tier,
            "Cut": cut_map[tier],
            "Subscribers": f"{len(sub):,}",
            "Mean days since activity": f"{sub['Days Since Last Activity'].mean():.1f}",
            "Mean logins / month": f"{sub['Avg Logins Per Month'].mean():.2f}",
            "Mean session minutes": f"{sub['Avg Session Minutes'].mean():.1f}",
            "Mean books accessed": f"{sub['Books Accessed'].mean():.1f}",
        })
    validity = _section(meth, "7. Engagement score")
    tier_note = " ".join(
        _sentences_with(_para_containing(validity, "partly by construction"),
                        "partly by construction")
    ) + " " + " ".join(
        _sentences_with(validity, "NOT score inputs")
    )
    # Stage 1 additions: cutoff rationale (text from methodology, cuts inside it
    # were written there from the data), chart caption, Active-Low watchlist
    tier_rationale = _para_containing(meth,
                                      "Tiers use terciles of the engagement score")
    chart_caption = _para_containing(meth, "bar_behaviour_by_tier").split(
        "Caption: ", 1)[1]
    wl = scored[(scored["Status"] == "Active") & (scored["Tier"] == "Low")]
    watchlist = {
        "n": f"{len(wl):,}",
        "recency": f"{wl['Days Since Last Activity'].mean():.1f}",
        "logins": f"{wl['Avg Logins Per Month'].mean():.2f}",
        "session": f"{wl['Avg Session Minutes'].mean():.1f}",
        "books": f"{wl['Books Accessed'].mean():.1f}",
    }

    # ── 6. high-value comparison (significance_checks.csv) ───────
    sig_note_row = sig[sig["comparison"] == "(note)"]["plain_english"].iloc[0]
    sig_rows = sig[sig["comparison"] != "(note)"].copy()
    bonferroni = " ".join(_sentences_with(caution, "Bonferroni correction"))
    fantasy_foot = " ".join(_sentences_with(caution, "not presented as a finding"))
    assoc = " ".join(_sentences_with(para_assoc, "association, not a cause"))
    sig_note = f"{bonferroni} {sig_note_row} {assoc}"

    # ── 7. strategy cards ─────────────────────────────────────────
    sec_d = _section(insights, "(d) Recommendations")
    rec_pat = re.compile(
        r"(\d+)\. \*\*(.+?)\*\* \*\(themes?: (.+?)\)\.\* Finding: "
        r"(.+?)(?= \d+\. \*\*|\Z)")

    def parse_recs(text):
        recs = []
        for m in rec_pat.finditer(_norm(text)):
            recs.append({"lead": _strip_md(m.group(2)),
                         "theme": _strip_md(m.group(3)),
                         "finding": _strip_md(m.group(4))})
        return recs

    heads = re.split(r"^### ", sec_d, flags=re.M)[1:]
    head_inactive = _norm(heads[0].split("\n")[0])
    head_churned = _norm(heads[1].split("\n")[0])
    recs_inactive = parse_recs(heads[0])
    recs_churned = parse_recs(heads[1])
    if not recs_inactive or not recs_churned:
        raise RuntimeError("recommendation parsing failed — check insights.md (d)")

    themes = sorted(set(t.strip() for m in
                        re.finditer(r"themes?: (.+?)\)\.", sec_d)
                        for t in m.group(1).split(",")))
    active_theme = next((t for t in themes if "personalised" in t), themes[0])
    active_finding = _strip_md(
        " ".join(_sentences_with(_para_containing(sec_a, "1,803"), "1,803")))
    cards = [
        {"key": "retain", "title": "Active — Retain",
         "sub": (f"{st_map['Active']['Customers']:,} Active subscribers "
                 f"({pct('Active'):.1f}% of classified)"),
         "finding": active_finding, "theme": active_theme, "recs": []},
        {"key": "win", "title": "Inactive — Win back before 90 days",
         "sub": head_inactive, "finding": "", "theme": "", "recs": recs_inactive},
        {"key": "churn", "title": "Churned — Win-back",
         "sub": head_churned, "finding": "", "theme": "", "recs": recs_churned},
    ]

    # ── 8. limitations (insights.md section e) ────────────────────
    sec_e = _section(insights, "(e) Limitations")
    limitations = []
    # separator after the bold lead is "," (e.g. "**synthetic**, so ...") or " "
    for m in re.finditer(r"(\d+)\. \*\*(.+?)\*\*[, ]+(.+?)(?= \d+\. \*\*|\Z)",
                         _norm(sec_e)):
        limitations.append({"lead": _strip_md(m.group(2)),
                            "body": _strip_md(m.group(3))})
    if len(limitations) != 7:
        raise RuntimeError("limitations parsing failed — check insights.md (e)")

    # ── 9. method in brief (methodology.md) ───────────────────────
    c_rows = dict(re.findall(r"^\| (C\d) \| (.+?) \|", meth, re.M))
    d1 = _norm(meth[meth.index("D1"):meth.index("D1") + 700])
    dups = re.search(r"Drop (\d+) exact", c_rows["C1"]).group(1)
    uniq = re.search(r"→ ([\d,]+) unique", c_rows["C1"]).group(1)
    spell = re.search(r"\((\d+) raw spellings", c_rows["C2"]).group(1)
    ngen = re.search(r"exactly (\d+) genres", c_rows["C2"]).group(1)
    med = re.search(r"medians used: \*\*logins ([\d.]+), session ([\d.]+), "
                    r"books ([\d.]+)\*\*", meth)
    line_clean = (
        f"Cleaning — approved rules C1–C10: drop {dups} exact duplicate rows → "
        f"{uniq} unique IDs; map {spell} raw genre spellings to {ngen} canonical "
        f"genres; invalid or missing recency never filled (→ {n_un} Unclassified); "
        f"remaining behaviour blanks median-filled with an Imputed flag (D1: logins "
        f"{med.group(1)}, session {med.group(2)}, books {med.group(3)})."
    )
    line_weights = (
        f"Score weights — 100 × ({weights['Days Since Last Activity (inverted)']} × "
        f"inverted recency + {weights['Avg Logins Per Month']} × logins + "
        f"{weights['Avg Session Minutes']} × session minutes), inputs min-max "
        f"normalised; books excluded; tiers by terciles "
        f"(Low <= {cut_low} < Medium <= {cut_med} < High)."
    )
    st_tbl = re.findall(r"^\| \*\*(Active|Inactive|Churned|Unclassified)\*\* \| "
                        r"(.+?) \|", meth, re.M)
    rule_parts = [f"{name} = {_strip_md(rule)}"
                  for name, rule in st_tbl]
    for name in ("Active", "Inactive", "Churned"):
        for i, (n_, _) in enumerate(st_tbl):
            if n_ == name:
                rule_parts[i] += f" — {int(st_map[name]['Customers']):,} subscribers"
    line_status = "Status rules — " + "; ".join(rule_parts) + "."

    return {
        "title": title, "summary": summary, "total": total, "kpis": kpis,
        "un_note": un_note, "pie_counts": pie_counts,
        "pie_takeaway": pie_takeaway, "findings": findings,
        "tier_rows": tier_rows, "tier_note": tier_note,
        "tier_rationale": tier_rationale, "chart_caption": chart_caption,
        "watchlist": watchlist,
        "sig_rows": sig_rows, "sig_note": sig_note,
        "sig_foot": fantasy_foot, "cards": cards,
        "limitations": limitations,
        "method": [line_clean, line_weights, line_status],
        "n_un": n_un,
    }


# ── pie figure (shared by app + HTML) ───────────────────────────
def make_pie(report):
    counts = report["pie_counts"]
    fig, ax = plt.subplots(figsize=(6.2, 4.8))
    labels = [f"{s}\n{c:,} ({c / sum(counts.values()) * 100:.1f}%)"
              for s, c in counts.items()]
    ax.pie(list(counts.values()), labels=labels,
           colors=[STATUS_HEX[s] for s in counts], autopct="%1.1f%%",
           startangle=90, textprops=dict(fontsize=10))
    ax.set_title("Status mix — all subscribers (classified rows)", fontsize=12,
                 fontweight="bold")
    fig.patch.set_facecolor("white")
    fig.tight_layout()
    return fig


def fig_png_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


# ── self-contained HTML ─────────────────────────────────────────
def build_html(report, pie_b64, tier_b64=None):
    B = _md_bold_to_html
    if tier_b64 is None:
        tier_b64 = fig_png_b64(make_tier_chart())
    k = []
    for c in report["kpis"]:
        k.append(f'<div class="kpi"><div class="v" style="color:{c["color"]}">'
                 f'{html_mod.escape(c["value"])}</div>'
                 f'<div class="l">{html_mod.escape(c["label"])}</div></div>')
    findings = "".join(
        f'<li><strong>{html_mod.escape(label)}</strong> — {B(text)}</li>'
        for label, text in report["findings"])
    tiers = "".join(
        "<tr>" + "".join(f"<td>{html_mod.escape(str(v))}</td>"
                         for v in row.values()) + "</tr>"
        for row in report["tier_rows"])
    tier_head = "".join(f"<th>{html_mod.escape(str(c))}</th>"
                        for c in report["tier_rows"][0].keys())
    sig = report["sig_rows"]
    sig_cols = ["comparison", "high_value", "churned", "difference",
                "p_value", "effect_size", "effect_size_type", "plain_english"]
    sig_head = "".join(f"<th>{html_mod.escape(c.replace('_', ' '))}</th>"
                       for c in sig_cols)
    sig_body = "".join(
        "<tr>" + "".join(f"<td>{html_mod.escape(str(r[c]))}</td>"
                         for c in sig_cols) + "</tr>"
        for _, r in sig.iterrows())
    cards = []
    for c in report["cards"]:
        if c["recs"]:
            body = "".join(
                f'<div class="rec"><strong>{B(r["lead"])}</strong><br>'
                f'<span class="theme">{html_mod.escape(r["theme"])}</span><br>'
                f'{B(r["finding"])}</div>' for r in c["recs"])
        else:
            body = (f'<div class="rec"><span class="theme">'
                    f'{html_mod.escape(c["theme"])}</span><br>'
                    f'{B(c["finding"])}</div>')
        cards.append(
            f'<div class="card {c["key"]}"><h3>{html_mod.escape(c["title"])}</h3>'
            f'<div class="sub">{B(c["sub"])}</div>{body}</div>')
    lims = "".join(f'<li><strong>{html_mod.escape(l["lead"])}</strong> '
                   f'{html_mod.escape(l["body"])}</li>'
                   for l in report["limitations"])
    method = "".join(f"<li>{html_mod.escape(m)}</li>" for m in report["method"])
    cut_line = report["tier_rows"][0]["Cut"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_mod.escape(report["title"])}</title>
<style>
:root {{ --ink:{INDIGO_DARK}; --acc:{INDIGO}; --lav:{LAVENDER}; --lav2:{LAVENDER_PALE};
  --green:{STATUS_HEX["Active"]}; --amber:{STATUS_HEX["Inactive"]}; --red:{STATUS_HEX["Churned"]}; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#f4f5fd; color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
header {{ background:var(--ink); color:#fff; padding:34px 40px;
  border-bottom:6px solid var(--acc); }}
header h1 {{ margin:0 0 10px; font-size:1.9rem; }}
header p {{ margin:0; max-width:1050px; color:var(--lav); line-height:1.5; }}
main {{ max-width:1080px; margin:0 auto; padding:26px 18px 50px; }}
section {{ background:#fff; border:1px solid var(--lav2); border-radius:14px;
  padding:20px 24px; margin:20px 0; }}
h2 {{ font-size:1.12rem; margin:0 0 14px; color:var(--ink);
  border-left:5px solid var(--acc); padding-left:10px; }}
.kpis {{ display:flex; gap:14px; flex-wrap:wrap; }}
.kpi {{ flex:1 1 190px; background:#fff; border:1px solid var(--lav2);
  border-top:4px solid var(--acc); border-radius:12px; padding:14px 16px; }}
.kpi .v {{ font-size:1.9rem; font-weight:700; }}
.kpi .l {{ font-size:.84rem; color:#5b6285; margin-top:4px; }}
.note {{ background:var(--lav2); border:1px solid var(--lav); color:#33385f;
  padding:10px 14px; border-radius:10px; font-size:.9rem; line-height:1.5;
  margin-top:14px; }}
.takeaway {{ background:#eef0ff; border-left:4px solid var(--acc); color:#3a4175;
  padding:9px 13px; border-radius:0 8px 8px 0; font-size:.9rem; margin-top:12px; }}
img.pie {{ display:block; max-width:470px; margin:6px auto; }}
img.tierchart {{ display:block; max-width:100%; margin:10px auto; }}
ol.findings li, ul.lims li {{ margin:0 0 10px; line-height:1.5; font-size:.95rem; }}
ul.lims {{ margin:0; padding-left:20px; }}
table {{ border-collapse:collapse; width:100%; font-size:.9rem; }}
th {{ background:var(--ink); color:#fff; padding:8px 10px; text-align:left; }}
td {{ border-bottom:1px solid var(--lav2); padding:7px 10px; }}
tr:nth-child(even) td {{ background:#f7f8ff; }}
.cards {{ display:flex; gap:16px; align-items:stretch; }}
.card {{ flex:1; background:#fff; border:1px solid var(--lav2);
  border-radius:14px; padding:16px 18px; font-size:.9rem; }}
.card h3 {{ margin:0 0 4px; font-size:1.02rem; }}
.card .sub {{ font-size:.8rem; color:#5b6285; margin-bottom:8px; }}
.card.retain {{ border-top:6px solid var(--green); }}
.card.win {{ border-top:6px solid var(--amber); }}
.card.churn {{ border-top:6px solid var(--red); }}
.theme {{ display:inline-block; background:var(--lav2); color:#2f3568;
  border-radius:99px; padding:2px 10px; font-size:.76rem; font-weight:600;
  margin:4px 0; }}
.rec {{ border-top:1px dashed var(--lav); padding-top:8px; margin-top:8px;
  line-height:1.45; color:#3a4175; }}
.method li {{ margin-bottom:8px; font-size:.92rem; line-height:1.5; }}
footer {{ max-width:1080px; margin:0 auto; padding:0 18px 40px; color:#6a70a0;
  font-size:.8rem; }}
</style>
</head>
<body>
<header>
  <h1>{html_mod.escape(report["title"])}</h1>
  <p>{html_mod.escape(report["summary"])}</p>
</header>
<main>
  <section>
    <h2>2 · Key numbers</h2>
    <div class="kpis">{''.join(k)}</div>
    <div class="note">{html_mod.escape(report["un_note"])}</div>
  </section>
  <section>
    <h2>3 · Status mix</h2>
    <img class="pie" alt="Status mix pie chart"
         src="data:image/png;base64,{pie_b64}">
    <div class="takeaway">{html_mod.escape(report["pie_takeaway"])}</div>
  </section>
  <section>
    <h2>4 · Key findings</h2>
    <ol class="findings">{findings}</ol>
  </section>
  <section>
    <h2>5 · Score tiers (classified rows)</h2>
    <table><thead><tr>{tier_head}</tr></thead><tbody>{tiers}</tbody></table>
    <div class="note">{B(report["tier_note"])}</div>
    <div class="note"><strong>Tier cutoffs — why terciles:</strong> {B(report["tier_rationale"])}</div>
    <img class="tierchart" alt="Mean engagement metrics by tier"
         src="data:image/png;base64,{tier_b64}">
    <div class="takeaway">{html_mod.escape(report["chart_caption"])}</div>
    <div class="note"><strong>Watchlist — early-warning group:</strong> {report["watchlist"]["n"]} Active
    subscribers sit in the Low tier (mean recency {report["watchlist"]["recency"]} days,
    {report["watchlist"]["logins"]} logins, {report["watchlist"]["session"]} session minutes,
    {report["watchlist"]["books"]} books). Individual rows: outputs/v2/watchlist.csv.</div>
  </section>
  <section>
    <h2>6 · High-value subscriber profile (Active+High vs Churned)</h2>
    <table><thead><tr>{sig_head}</tr></thead><tbody>{sig_body}</tbody></table>
    <div class="note">{B(report["sig_note"])}</div>
    <div class="note">{B(report["sig_foot"])}</div>
  </section>
  <section>
    <h2>7 · Recommended strategy per segment</h2>
    <div class="cards">{''.join(cards)}</div>
  </section>
  <section>
    <h2>8 · Limitations</h2>
    <ul class="lims">{lims}</ul>
  </section>
  <section>
    <h2>9 · Method in brief</h2>
    <ul class="method">{method}</ul>
  </section>
</main>
<footer>Every number comes from outputs/v2/ and data/processed/v2/ — see
methodology.md and insights.md for the approved rules behind each figure.
Associations only: nothing here demonstrates causation. Tier cut shown in the
table: {html_mod.escape(cut_line)}.</footer>
</body>
</html>
"""


def write_html():
    report = load_report()
    fig = make_pie(report)
    page = build_html(report, fig_png_b64(fig), fig_png_b64(make_tier_chart()))
    with open(HTML_PATH, "w") as f:
        f.write(page)
    return report, page


if __name__ == "__main__":
    rep, page = write_html()
    print(f"wrote {HTML_PATH} ({len(page):,} bytes, "
          f"{os.path.getsize(HTML_PATH):,} bytes on disk)")
    print("sections:", len(rep["findings"]), "findings,",
          len(rep["limitations"]), "limitations,",
          [len(c["recs"]) for c in rep["cards"]], "recs/card")
