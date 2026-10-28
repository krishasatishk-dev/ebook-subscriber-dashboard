# -*- coding: utf-8 -*-
"""Shared styles, page geometry, canvas and flowable helpers."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (KeepTogether, Paragraph, Preformatted, Spacer,
                                Table, TableStyle)
from reportlab.platypus.flowables import HRFlowable


def _register_serif():
    """Use Georgia when the system font is available, else Times."""
    font_dir = "/System/Library/Fonts/Supplemental/"
    names = [("Georgia", "Georgia.ttf"), ("Georgia-Bold", "Georgia Bold.ttf"),
             ("Georgia-Italic", "Georgia Italic.ttf"),
             ("Georgia-BoldItalic", "Georgia Bold Italic.ttf")]
    try:
        for name, filename in names:
            pdfmetrics.registerFont(TTFont(name, font_dir + filename))
        pdfmetrics.registerFontFamily(
            "Georgia", normal="Georgia", bold="Georgia-Bold",
            italic="Georgia-Italic", boldItalic="Georgia-BoldItalic")
        return "Georgia"
    except Exception:
        return "Times-Roman"


SERIF = _register_serif()

NAVY = colors.HexColor("#1F3864")
BLUE = colors.HexColor("#2E74B5")
LIGHT = colors.HexColor("#DEEAF6")
BAND = colors.HexColor("#F4F7FC")
RULE = colors.HexColor("#C9D4E4")
BODY = colors.HexColor("#262626")
MUTED = colors.HexColor("#5A6675")
WHITE = colors.white

PAGE_W, PAGE_H = A4
LM = RM = 59.0            # side margins (~2.08 cm)
TM = 64.0
BM = 62.0
CONTENT_W = PAGE_W - LM - RM

SANS = "Helvetica"
SANS_B = "Helvetica-Bold"
SANS_I = "Helvetica-Oblique"
MONO = "Courier"

# ----------------------------------------------------------------- styles ---
def _st(name, **kw):
    return ParagraphStyle(name, **kw)

ST = {
    "cover_label": _st("cover_label", fontName=SANS_B, fontSize=9, leading=12,
                       textColor=BLUE, alignment=TA_CENTER, spaceAfter=10),
    "cover_course": _st("cover_course", fontName=SANS_B, fontSize=21, leading=27,
                        textColor=NAVY, alignment=TA_CENTER, spaceAfter=6),
    "cover_assign": _st("cover_assign", fontName=SANS, fontSize=12.5, leading=17,
                        textColor=BLUE, alignment=TA_CENTER, spaceAfter=4),
    "cover_kind": _st("cover_kind", fontName=SANS_I, fontSize=10, leading=14,
                      textColor=MUTED, alignment=TA_CENTER),
    "cover_plabel": _st("cover_plabel", fontName=SANS_B, fontSize=8.5, leading=11,
                        textColor=BLUE, alignment=TA_LEFT),
    "cover_ptitle": _st("cover_ptitle", fontName=SANS_B, fontSize=14.5, leading=19,
                        textColor=NAVY, alignment=TA_LEFT),
    "cover_note": _st("cover_note", fontName=SERIF, fontSize=8.5, leading=12,
                      textColor=MUTED, alignment=TA_LEFT),
    "h1": _st("h1", fontName=SANS_B, fontSize=14, leading=18, textColor=NAVY,
              spaceBefore=2, spaceAfter=7),
    "h2": _st("h2", fontName=SANS_B, fontSize=10.8, leading=14.5, textColor=NAVY,
              spaceBefore=12, spaceAfter=5),
    "h3": _st("h3", fontName=SANS_B, fontSize=9.8, leading=13, textColor=BLUE,
              spaceBefore=9, spaceAfter=4),
    "body": _st("body", fontName=SERIF, fontSize=9.7, leading=14.4, textColor=BODY,
                alignment=TA_JUSTIFY, spaceAfter=7),
    "bullet": _st("bullet", fontName=SERIF, fontSize=9.7, leading=14.4,
                  textColor=BODY, alignment=TA_JUSTIFY, spaceAfter=4,
                  leftIndent=14, bulletIndent=4),
    "note": _st("note", fontName=SERIF, fontSize=9.3, leading=13.6, textColor=NAVY,
                alignment=TA_JUSTIFY, spaceAfter=7, leftIndent=8, rightIndent=8,
                borderColor=BLUE, borderWidth=0, backColor=colors.HexColor("#EEF4FB"),
                borderPadding=(6, 8, 6, 8)),
    "cap": _st("cap", fontName=SANS_I, fontSize=8.2, leading=11, textColor=MUTED,
               alignment=TA_LEFT, spaceBefore=3, spaceAfter=9),
    "capt": _st("capt", fontName=SANS_B, fontSize=8.4, leading=11.5, textColor=NAVY,
                alignment=TA_LEFT, spaceBefore=8, spaceAfter=4),
    "tc": _st("tc", fontName=SANS, fontSize=7.8, leading=9.9, textColor=BODY,
              alignment=TA_LEFT),
    "th": _st("th", fontName=SANS_B, fontSize=7.8, leading=9.9, textColor=WHITE,
              alignment=TA_LEFT),
    "code": _st("code", fontName=MONO, fontSize=8.0, leading=10.6, textColor=BODY),
    "plabel": _st("plabel", fontName=SANS_B, fontSize=8.6, leading=11.5,
                  textColor=NAVY, spaceBefore=6, spaceAfter=2),
    "prompt": _st("prompt", fontName=SERIF, fontSize=9.2, leading=13.4,
                  textColor=colors.HexColor("#1B2430"), alignment=TA_LEFT,
                  leftIndent=2),
    "ref": _st("ref", fontName=SERIF, fontSize=9.0, leading=13.0, textColor=BODY,
               alignment=TA_LEFT, leftIndent=22, firstLineIndent=-22,
               spaceAfter=6),
    "toc_title": _st("toc_title", fontName=SANS_B, fontSize=14, leading=18,
                     textColor=NAVY, spaceAfter=10),
}


class NumberedCanvas(pdfcanvas.Canvas):
    """Adds 'Page X of Y' footers (cover excluded) on final save."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_states = []

    def showPage(self):
        self._saved_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_states)
        for index, state in enumerate(self._saved_states, start=1):
            self.__dict__.update(state)
            if index > 1:
                self._draw_footer(index, total)
            super().showPage()
        super().save()

    def _draw_footer(self, index, total):
        self.saveState()
        self.setStrokeColor(RULE)
        self.setLineWidth(0.6)
        self.line(LM, 46, PAGE_W - RM, 46)
        self.setFont(SANS, 7.4)
        self.setFillColor(MUTED)
        self.drawString(LM, 34,
                        "Playing with AI Project \u2014 written report \u00b7 "
                        "Exploring AI Tools in Software Development")
        self.drawRightString(PAGE_W - RM, 34, "Page %d of %d" % (index, total))
        self.restoreState()


def _wrap(canvas, text, font, size, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if canvas.stringWidth(trial, font, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover_page(canvas, doc):
    """Cover page: colour bands, headings, project panel and student details."""
    from content_meta import COURSE, ASSIGNMENT, PROJECT, STUDENT

    cw = PAGE_W - LM - RM
    canvas.saveState()

    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 16, PAGE_W, 16, stroke=0, fill=1)
    canvas.setFillColor(BLUE)
    canvas.rect(0, PAGE_H - 21, PAGE_W, 5, stroke=0, fill=1)

    # course label and title
    canvas.setFillColor(BLUE)
    canvas.setFont(SANS_B, 9)
    canvas.drawCentredString(PAGE_W / 2.0, PAGE_H - 78,
                             "COURSERA  \u00b7  PEER-GRADED ASSIGNMENT  \u00b7  "
                             "WRITTEN REPORT")
    canvas.setFillColor(NAVY)
    canvas.setFont(SANS_B, 20)
    y = PAGE_H - 114
    for line in _wrap(canvas, COURSE, SANS_B, 20, cw):
        canvas.drawCentredString(PAGE_W / 2.0, y, line)
        y -= 26

    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.3)
    canvas.line(LM, y - 12, PAGE_W - RM, y - 12)

    canvas.setFillColor(BLUE)
    canvas.setFont(SANS, 12.5)
    ay = y - 38
    for line in _wrap(canvas, ASSIGNMENT, SANS, 12.5, cw):
        canvas.drawCentredString(PAGE_W / 2.0, ay, line)
        ay -= 17
    canvas.setFillColor(MUTED)
    canvas.setFont(SANS_I, 10)
    canvas.drawCentredString(PAGE_W / 2.0, ay - 4, "AI-assisted software development")

    # project panel
    panel_top = ay - 34
    panel_h = 84
    canvas.setFillColor(colors.HexColor("#EEF4FB"))
    canvas.setStrokeColor(NAVY)
    canvas.setLineWidth(1.0)
    canvas.rect(LM, panel_top - panel_h, cw, panel_h, stroke=1, fill=1)
    canvas.setFillColor(BLUE)
    canvas.setFont(SANS_B, 8.5)
    canvas.drawString(LM + 14, panel_top - 22, "PROJECT TITLE")
    canvas.setFillColor(NAVY)
    canvas.setFont(SANS_B, 14)
    ty = panel_top - 46
    for line in _wrap(canvas, PROJECT, SANS_B, 14, cw - 28):
        canvas.drawString(LM + 14, ty, line)
        ty -= 19

    # student information
    rows = [
        ("Student name", STUDENT["name"]),
        ("Roll number", STUDENT["roll"]),
        ("SAP ID", STUDENT["sap"]),
        ("Institution", STUDENT["institution"]),
        ("Course", COURSE),
        ("Assignment", ASSIGNMENT + " (written report)"),
        ("Platform", "Coursera"),
        ("Submission deadline", STUDENT["deadline"]),
        ("Date prepared", STUDENT["prepared"]),
    ]
    ry = panel_top - panel_h - 44
    canvas.setFillColor(BLUE)
    canvas.setFont(SANS_B, 8.5)
    canvas.drawString(LM, ry + 16, "STUDENT AND SUBMISSION DETAILS")
    for label, value in rows:
        ry -= 24
        canvas.setFont(SANS_B, 9)
        canvas.setFillColor(NAVY)
        canvas.drawString(LM, ry, label)
        canvas.setFont(SERIF, 10.5)
        canvas.setFillColor(BODY)
        canvas.drawString(LM + 150, ry, value)
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(LM, ry - 7, PAGE_W - RM, ry - 7)

    # evidence note
    note_top = ry - 34
    note_lines = _wrap(
        canvas,
        "Evidence note: observation, screenshot and pass/fail fields in this report are "
        "marked \u201cpending verification\u201d until the experiment has been executed.",
        SERIF, 9, cw - 28)
    note_h = 20 + 13 * len(note_lines)
    canvas.setFillColor(BAND)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.7)
    canvas.rect(LM, note_top - note_h, cw, note_h, stroke=1, fill=1)
    canvas.setFillColor(BLUE)
    canvas.setFont(SANS_B, 8)
    canvas.drawString(LM + 14, note_top - 16, "STATUS OF EVIDENCE")
    canvas.setFillColor(MUTED)
    canvas.setFont(SERIF, 9)
    ny = note_top - 30
    for line in note_lines:
        canvas.drawString(LM + 14, ny, line)
        ny -= 13

    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.7)
    canvas.line(LM, 92, PAGE_W - RM, 92)
    canvas.setFont(SANS, 7.6)
    canvas.setFillColor(MUTED)
    canvas.drawString(LM, 78, PROJECT)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, 12, stroke=0, fill=1)
    canvas.restoreState()


def body_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.7)
    canvas.line(LM, PAGE_H - 46, PAGE_W - RM, PAGE_H - 46)
    canvas.setFont(SANS, 7.4)
    canvas.setFillColor(MUTED)
    canvas.drawString(LM, PAGE_H - 42,
                      "Using ChatGPT to Assist in Developing a Student Task Manager "
                      "Application")
    canvas.drawRightString(PAGE_W - RM, PAGE_H - 42, "KRISHA KADAM \u00b7 A414")
    canvas.restoreState()


# ------------------------------------------------------------- flowables ----
def para(text, style="body"):
    return Paragraph(text, ST[style])


def h1(text, toc=True):
    p = Paragraph(text, ST["h1"])
    if toc:
        p.toc_level = 0
    return p


def h2(text, toc=True):
    p = Paragraph(text, ST["h2"])
    if toc:
        p.toc_level = 1
    return p


def h3(text, toc=True):
    p = Paragraph(text, ST["h3"])
    if toc:
        p.toc_level = 2
    return p


def rule(color=RULE, thickness=0.8, before=1, after=7):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceBefore=before, spaceAfter=after, lineCap="butt")


def bullets(items, style="bullet"):
    return [Paragraph(t, ST[style], bulletText="\u2022") for t in items]


def make_table(spec, number, keep=True):
    """Build a report table from a specification dictionary."""
    weights = spec["weights"]
    widths = [CONTENT_W * w / float(sum(weights)) for w in weights]
    fs = spec.get("font", 7.8)
    cell = _st("tcx", fontName=SANS, fontSize=fs, leading=fs + 2.1, textColor=BODY)
    head = _st("thx", fontName=SANS_B, fontSize=fs, leading=fs + 2.1, textColor=WHITE)
    data = [[Paragraph(str(c), head) for c in spec["headers"]]]
    for row in spec["rows"]:
        data.append([Paragraph(str(c), cell) for c in row])
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), BAND))
    table.setStyle(TableStyle(style))
    caption = Paragraph("<b>Table %d.</b> %s" % (number, spec["caption"]), ST["capt"])
    parts = [caption, table, Spacer(1, 8)]
    return KeepTogether(parts) if keep else parts


def code_block(text, number=None):
    pre = Preformatted(text, ST["code"])
    box = Table([[pre]], colWidths=[CONTENT_W], hAlign="LEFT")
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BAND),
        ("BOX", (0, 0), (-1, -1), 0.7, RULE),
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    out = [box, Spacer(1, 4)]
    if number is not None:
        out.append(Paragraph("<b>Listing 1.</b> %s" % number, ST["cap"]))
    return KeepTogether(out)


def prompt_block(label, text):
    lab = Paragraph(label, ST["plabel"])
    body_p = Paragraph(text, ST["prompt"])
    box = Table([[body_p]], colWidths=[CONTENT_W], hAlign="LEFT")
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7FAFD")),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, BLUE),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([lab, box, Spacer(1, 5)])


def figure_block(drawing, number, caption):
    cap = Paragraph("<b>Figure %d.</b> %s" % (number, caption), ST["cap"])
    return KeepTogether([Spacer(1, 3), drawing, cap])


def kv_rows(pairs):
    """Two-column label/value rows used on the cover page."""
    label = _st("kvl", fontName=SANS_B, fontSize=9, leading=13, textColor=NAVY)
    value = _st("kvv", fontName=SERIF, fontSize=10, leading=14, textColor=BODY)
    data = [[Paragraph(k, label), Paragraph(v, value)] for k, v in pairs]
    t = Table(data, colWidths=[130, CONTENT_W - 130], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
    ]))
    return t
