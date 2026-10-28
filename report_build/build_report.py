# -*- coding: utf-8 -*-
"""Assemble the Coursera written report and export it as a PDF."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table)
from reportlab.platypus.tableofcontents import TableOfContents

import content_meta as M
import content_prompts as CP
import content_s2 as S2
import content_s3 as S3
import content_s4 as S4
import content_s5 as S5
import content_tables1 as T1
import content_tables2 as T2
import diagrams as DG
import layout as L
from layout import (BAND, BLUE, BODY, CONTENT_W, MUTED, NAVY, SANS, SANS_B,
                    SANS_I, SERIF, ST, bullets, code_block, figure_block, h1,
                    h2, h3, kv_rows, make_table, para, prompt_block, rule)

BIG_TABLES = {"procedure", "log", "tests", "evaluation"}

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.join(OUT_DIR, "AI_Project_Report_KRISHA_KADAM.pdf")

TABLE_SPECS = {
    "requirements": T1.TABLE_REQUIREMENTS,
    "tools": T1.TABLE_TOOLS,
    "procedure": T1.TABLE_PROCEDURE,
    "challenges": T2.TABLE_CHALLENGES,
    "log": T2.TABLE_LOG,
    "tests": T2.TABLE_TESTS,
    "evaluation": T2.TABLE_EVALUATION,
}
TABLE_NO = {key: i + 1 for i, key in enumerate(
    ["requirements", "tools", "procedure", "challenges", "log", "tests",
     "evaluation", "rubric"])}

def _norm(seq):
    """Yield (kind, text) pairs from strings or (kind, text, ...) tuples."""
    for item in seq:
        if isinstance(item, str):
            yield "p", item
        else:
            yield item[0], item[1]


PROMPT_BY_ID = {pid: (label, text) for pid, label, text in CP.PROMPTS}
BODY_PROMPTS = ["P1", "P3", "P4", "P6", "P7", "P8"]
APP_A_PROMPTS = ["P2", "P5"]

FIG1_CAPTION = ("Interaction between the developer, ChatGPT, the code editor, the "
                "browser and the testing step. Responses may contain code, explanations "
                "and suggested fixes, which the developer copies into the editor; only the "
                "browser executes code.")
FIG2_CAPTION = ("Iteration loop used in the experiment: prompt, generated code, human "
                "review, execution in the browser, testing and revision.")
FIG3_CAPTION = ("Division of labour: the tool proposes, the developer reviews, runs, "
                "tests and remains accountable for the result.")
FIG4_CAPTION = ("The ten evaluation criteria grouped into output quality, process and "
                "interaction, and risk and oversight.")


# --------------------------------------------------------------- document ----
class ReportDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, pagesize=L.A4,
                                 leftMargin=L.LM, rightMargin=L.RM,
                                 topMargin=L.TM, bottomMargin=L.BM,
                                 title="Using ChatGPT to Assist in Developing a "
                                       "Student Task Manager Application",
                                 author=M.STUDENT["name"],
                                 subject="Coursera written report: Playing with AI "
                                         "Project",
                                 creator="Report generator", **kw)
        cover_frame = Frame(0, 0, L.PAGE_W, L.PAGE_H, id="cover",
                            leftPadding=0, rightPadding=0,
                            topPadding=0, bottomPadding=0)
        body_frame = Frame(L.LM, L.BM, CONTENT_W, L.PAGE_H - L.TM - L.BM,
                           id="body", leftPadding=0, rightPadding=0,
                           topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[cover_frame], onPage=L.cover_page),
            PageTemplate(id="body", frames=[body_frame], onPage=L.body_page),
        ])
        self._hcount = 0

    def beforeDocument(self):
        self._hcount = 0

    def afterFlowable(self, flowable):
        level = getattr(flowable, "toc_level", None)
        if level is None:
            return
        text = flowable.getPlainText()
        self._hcount += 1
        key = "sec%d" % self._hcount
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level, 0)
        self.notify("TOCEntry", (level, text, self.page, key))


def _toc_styles():
    s0 = ParagraphStyle("toc0", fontName=SANS_B, fontSize=9.6, leading=15,
                        textColor=NAVY, spaceBefore=5)
    s1 = ParagraphStyle("toc1", fontName=SANS, fontSize=9.2, leading=13.6,
                        textColor=BODY, leftIndent=16)
    return [s0, s1]


# ------------------------------------------------------------------ story ----
def _rubric_spec():
    return {
        "caption": "Rubric-alignment matrix for the written report (the assignment "
                   "totals 100 marks across written report, video and peer review)",
        "headers": ["Criterion", "Marks", "Where it is addressed in this report",
                    "Deliverable"],
        "weights": [27, 8, 45, 20],
        "font": 7.8,
        "rows": [list(r) for r in S5.RUBRIC_ROWS],
    }


def _record_sheet_spec():
    return {
        "caption": "Prompt record sheet \u2014 paste the prompts actually used, with the "
                   "date, time and where the response was saved",
        "headers": ["Prompt ID", "Date and time", "Actual prompt text used",
                    "Response saved at (file / link)"],
        "weights": [10, 16, 48, 26],
        "font": 7.8,
        "rows": [[pid, "", "", ""] for pid in
                 ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]],
    }


def _extended_log_spec():
    return {
        "caption": "Extended experiment log for further entries (continuation of "
                   "Table 5)",
        "headers": ["Date and time", "Step", "Observation (verbatim)",
                    "Evidence reference"],
        "weights": [16, 8, 50, 26],
        "font": 7.8,
        "rows": [["", "", "", ""] for _ in range(8)],
    }


def build_story():
    story = []
    add = story.append

    def emit(parts):
        if isinstance(parts, list):
            story.extend(parts)
        else:
            story.append(parts)

    def add_table(key):
        emit(make_table(TABLE_SPECS[key], TABLE_NO[key],
                        keep=key not in BIG_TABLES))

    add(NextPageTemplate("body"))
    add(PageBreak())

    # ----------------------------------------------------------- contents ----
    add(Paragraph("Table of Contents", ST["toc_title"]))
    toc = TableOfContents()
    toc.levelStyles = _toc_styles()
    toc.dotsMinLevel = 0
    add(toc)
    add(PageBreak())

    # ---------------------------------------------------- executive summary ---
    add(h1("Executive Summary"))
    add(rule())
    for _kind, text in _norm(M.EXEC_SUMMARY):
        add(para(text))
    add(para("<b>How to read this report:</b> procedures, prompts and test suites are "
             "complete as supplied; only records produced by the experiment may be "
             "reported as findings, and every field reserved for an observed result "
             "is marked pending verification until the run is complete.", "note"))

    # ------------------------------------------------------------ section 1 ---
    add(h1("Section 1: Setup and Introduction"))
    add(rule())
    for kind, text in _norm(M.SECTION1):
        if kind == "h2" and text.startswith("1.8"):
            add(figure_block(DG.figure1(), 1, FIG1_CAPTION))
        if kind == "h2":
            add(h2(text))
        else:
            add(para(text))

    # ------------------------------------------------------------ section 2 ---
    add(h1("Section 2: Experimentation and Documentation"))
    add(rule())
    add(para("<b>Project title:</b> " + M.PROJECT + ".", "note"))
    for kind, text in _norm(S2.SECTION2):
        if kind == "h2":
            add(h2(text))
        elif kind == "p":
            add(para(text))
        elif kind == "table":
            if text == "procedure":
                add(figure_block(DG.figure2(), 2, FIG2_CAPTION))
            add_table(text)
        elif kind == "prompts":
            for pid in BODY_PROMPTS:
                label, body_text = PROMPT_BY_ID[pid]
                add(prompt_block("%s \u00b7 %s" % (pid, label), body_text))
        elif kind == "code":
            add(code_block(
                CP.CODE_JS,
                "Illustrative addTask() function for the task manager. The snippet is "
                "shown for review and discussion; it is not an experimental result."))

    # ------------------------------------------------------------ section 3 ---
    add(h1("Section 3: Effectiveness Analysis"))
    add(rule())
    for kind, text in _norm(S3.SECTION3):
        if kind == "h2" and text.startswith("3.5"):
            add(figure_block(DG.figure3(), 3, FIG3_CAPTION))
        if kind == "h2":
            add(h2(text))
        elif kind == "p":
            add(para(text))
        elif kind == "table":
            add(figure_block(DG.figure4(), 4, FIG4_CAPTION))
            add_table(text)

    # ------------------------------------------------------------ section 4 ---
    add(h1("Section 4: Reflection and Future Implications"))
    add(rule())
    add(para(S4.NOTE_S4, "note"))
    for question, answer in S4.SECTION4:
        add(h3(question, toc=False))
        add(para(answer))

    # ------------------------------------------------------------ section 5 ---
    add(h1("Section 5: Conclusion"))
    add(rule())
    add(para("<b>" + S5.CONCLUSION_STATUS + "</b>", "note"))
    for _kind, text in _norm(S5.SECTION5):
        add(para(text))

    add(PageBreak())

    # ----------------------------------------------------------- references ---
    add(h1("References"))
    add(rule())
    for i, ref in enumerate(S5.REFERENCES, start=1):
        add(para("[%d]&nbsp;&nbsp;%s" % (i, ref), "ref"))

    add(Spacer(1, 10))
    add(h1("Rubric Alignment", toc=False))
    add(rule())
    add(para("The matrix below shows which sections of this written report address "
             "each marked criterion of the assignment. The video and the peer-review "
             "activity are separate deliverables and are not part of this document; "
             "the report does not claim to satisfy them."))
    emit(make_table(_rubric_spec(), TABLE_NO["rubric"]))

    # ----------------------------------------------------------- appendices ---
    add(PageBreak())
    add(h1("Appendix A: Example Prompts and Prompt Record Sheet"))
    add(rule())
    add(para("Prompts P1, P3, P4, P6, P7 and P8 are printed in Section 2.5. The two "
             "further prompts used for planning and for targeted debugging are given "
             "below, followed by a blank record sheet in which the prompts actually "
             "used during the experiment, their date and time and the location of the "
             "saved response must be entered. Replace these examples with the genuine "
             "transcript material before submission."))
    for pid in APP_A_PROMPTS:
        label, body_text = PROMPT_BY_ID[pid]
        add(prompt_block("%s \u00b7 %s" % (pid, label), body_text))
    add(h2("Prompt record sheet"))
    emit(make_table(_record_sheet_spec(), 9))

    add(PageBreak())
    add(h1("Appendix B: Experiment Log"))
    add(rule())
    add(para("Table 5 in Section 2.8 is the structured log keyed to the twelve steps. "
             "This appendix provides space for additional entries made during the run, "
             "including the time of each observation and a reference to the evidence "
             "(screenshot name, transcript file or console note) that supports it."))
    emit(make_table(_extended_log_spec(), 10))

    add(PageBreak())
    add(h1("Appendix C: Test Cases and Verification Checklist"))
    add(rule())
    add(para("The test cases themselves are defined in Table 6 (TC-01 to TC-12). The "
             "checklist below is used to confirm that the evidence for each part of "
             "the experiment exists before the report is submitted. Each item must be "
             "ticked only when the corresponding material is present."))
    add(h2("Verification checklist", toc=False))
    for item in CP.EVIDENCE_CHECKLIST:
        add(Paragraph("[&nbsp;&nbsp;&nbsp;]&nbsp;&nbsp;" + item, ST["bullet"]))

    add(PageBreak())
    add(h1("Appendix D: Screenshots and Evidence"))
    add(rule())
    add(para(CP.APPENDIX_D_NOTE))
    slots = Table(
        [[Paragraph("<b>%s</b><br/><font color='#5A6675' size=7>%s</font>"
                    % (code, desc), ST["tc"]),
          Paragraph("<i>Paste screenshot here</i>",
                    ParagraphStyle("slot", fontName=SANS_I, fontSize=8,
                                   textColor=MUTED, alignment=TA_LEFT))]
         for code, desc in CP.SCREENSHOT_SLOTS],
        colWidths=[CONTENT_W * 0.42, CONTENT_W * 0.58],
        rowHeights=[86] * len(CP.SCREENSHOT_SLOTS), hAlign="LEFT")
    slots.setStyle(L.TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.6, L.RULE),
        ("BACKGROUND", (0, 0), (0, -1), L.BAND),
        ("BOX", (0, 0), (-1, -1), 0.9, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    add(Spacer(1, 4))
    add(slots)

    add(PageBreak())
    add(h1("Appendix E: Final Reflection Notes"))
    add(rule())
    add(para(CP.APPENDIX_E_NOTE))
    add(h2("Guiding questions for your own notes", toc=False))
    for item in bullets([
        "What surprised you about the first draft returned by the tool?",
        "Which requirement needed the most human correction, and why?",
        "Which test case failed for a reason you did not expect?",
        "What would you prompt differently if you repeated the experiment?",
        "What did you understand better after the experiment than before it?",
    ]):
        add(item)
    add(Spacer(1, 8))
    lines = Table([[""] * 1 for _ in range(9)],
                  colWidths=[CONTENT_W], rowHeights=[26] * 9, hAlign="LEFT")
    lines.setStyle(L.TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.6, L.RULE),
        ("BOX", (0, 0), (-1, -1), 0, L.RULE),
    ]))
    add(lines)
    add(Spacer(1, 6))
    add(para("<i>End of report.</i>", "cap"))

    return _pair_headings(story)


def _pair_headings(story):
    """Keep a heading on the same page as the paragraph that follows it."""
    out, i, n = [], 0, len(story)
    while i < n:
        item = story[i]
        style_name = getattr(getattr(item, "style", None), "name", None)
        if (style_name in ("h1", "h2", "h3") and i + 1 < n
                and isinstance(story[i + 1], Paragraph)
                and getattr(story[i + 1], "style", None) is not None
                and story[i + 1].style.name == "body"):
            out.append(KeepTogether([item, story[i + 1]]))
            i += 2
        else:
            out.append(item)
            i += 1
    return out


# ------------------------------------------------------------ word counts ----
def count_words():
    counts = {}
    counts["Executive Summary"] = sum(len(t.split()) for _k, t in _norm(M.EXEC_SUMMARY))
    s1 = sum(len(t.split()) for k, t in _norm(M.SECTION1) if k == "p")
    counts["Section 1"] = s1
    s2 = sum(len(t.split()) for k, t in _norm(S2.SECTION2) if k == "p")
    counts["Section 2"] = s2
    s3 = sum(len(t.split()) for k, t in _norm(S3.SECTION3) if k == "p")
    counts["Section 3"] = s3
    s4 = sum(len(a.split()) for _, a in S4.SECTION4)
    counts["Section 4"] = s4
    s5 = sum(len(t.split()) for _k, t in _norm(S5.SECTION5))
    counts["Section 5"] = s5
    counts["TOTAL (main prose)"] = sum(counts.values())
    return counts


def main():
    doc = ReportDoc(OUT_PDF)
    story = build_story()
    doc.multiBuild(story, canvasmaker=L.NumberedCanvas)
    counts = count_words()
    for key, value in counts.items():
        print("%-24s %5d words" % (key, value))
    print("Saved:", OUT_PDF, os.path.getsize(OUT_PDF), "bytes")
    return OUT_PDF


if __name__ == "__main__":
    main()
