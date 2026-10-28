"""Original vector diagrams for the Coursera AI report (reportlab graphics)."""

import math

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors

NAVY = colors.HexColor("#1F3864")
BLUE = colors.HexColor("#2E74B5")
LIGHT = colors.HexColor("#DEEAF6")
LIGHT2 = colors.HexColor("#F4F7FC")
GREY = colors.HexColor("#8A94A6")
TEXT = colors.HexColor("#1F2933")
WHITE = colors.white

BOLD = "Helvetica-Bold"
REG = "Helvetica"


def _head(x, y, ang, size=6.0, color=NAVY):
    a1, a2 = ang - 0.42, ang + 0.42
    p2 = (x - size * math.cos(a1), y - size * math.sin(a1))
    p3 = (x - size * math.cos(a2), y - size * math.sin(a2))
    return Polygon(
        [x, y, p2[0], p2[1], p3[0], p3[1]],
        fillColor=color,
        strokeColor=None,
    )


def arrow(d, x1, y1, x2, y2, color=NAVY, width=1.1, dashed=False, head=True):
    dash = [3.0, 2.2] if dashed else None
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width, strokeDashArray=dash))
    if head:
        d.add(_head(x2, y2, math.atan2(y2 - y1, x2 - x1), color=color))


def double_arrow(d, x1, y, x2, color=NAVY, width=1.1):
    arrow(d, x1, y, x2, y, color=color, width=width)
    arrow(d, x2, y, x1, y, color=color, width=width)


def box(d, x, y, w, h, text, fill=WHITE, stroke=NAVY, tc=NAVY, size=8.0,
        font=BOLD, radius=3, lw=1.0):
    d.add(Rect(x, y, w, h, rx=radius, ry=radius, fillColor=fill,
               strokeColor=stroke, strokeWidth=lw))
    lines = text.split("\n")
    lh = size + 2.0
    total = lh * len(lines)
    top = y + h / 2 + total / 2 - size
    for i, ln in enumerate(lines):
        d.add(String(x + w / 2, top - i * lh, ln, fontName=font, fontSize=size,
                     fillColor=tc, textAnchor="middle"))


def label(d, x, y, text, size=6.8, color=TEXT, anchor="middle", font=REG):
    d.add(String(x, y, text, fontName=font, fontSize=size, fillColor=color,
                 textAnchor=anchor))


def figure1():
    """Developer / ChatGPT / editor / browser / testing interaction."""
    W, H = 470, 214
    d = Drawing(W, H)
    bw, bh = 112, 46
    dev = (8, 150)
    ai = (179, 150)
    ed = (350, 150)
    br = (350, 52)
    ts = (8, 52)

    box(d, *dev, bw, bh, "Student\ndeveloper", fill=LIGHT2)
    box(d, *ai, bw, bh, "ChatGPT\n(AI assistant)", fill=NAVY, tc=WHITE)
    box(d, *ed, bw, bh, "Code editor\n(save the files)", fill=LIGHT2)
    box(d, *br, bw, bh, "Web browser\n(runs the code)", fill=LIGHT2)
    box(d, *ts, bw, bh, "Testing &\nverification", fill=LIGHT2)

    # developer <-> ChatGPT
    double_arrow(d, dev[0] + bw, 173, ai[0], color=BLUE)
    label(d, 149.5, 162, "prompts  \u2192", size=6.6, color=BLUE)
    label(d, 149.5, 182, "\u2190  responses", size=6.6, color=BLUE)

    # editor -> browser
    arrow(d, 406, 150, 406, 98)
    label(d, 400, 121, "open the files", size=6.6, anchor="end")

    # browser -> testing
    arrow(d, 350, 75, 120, 75)
    label(d, 235, 80, "run the test cases and observe the behaviour", size=6.6)

    # testing -> developer
    arrow(d, 64, 98, 64, 150)
    label(d, 70, 121, "pass / fail evidence", size=6.6, anchor="start")

    return d


def figure2():
    """Prompt -> code -> review -> execute -> test -> revise loop."""
    W, H = 470, 132
    d = Drawing(W, H)
    steps = [
        "1. State the\nproblem",
        "2. Generate\ncode",
        "3. Human\nreview",
        "4. Execute in\nthe browser",
        "5. Test and\nrecord",
    ]
    w, h, y = 76, 44, 66
    xs = [6 + i * 94 for i in range(5)]
    for i, (x, txt) in enumerate(zip(xs, steps)):
        fill = NAVY if i in (0, 4) else LIGHT2
        tc = WHITE if i in (0, 4) else NAVY
        box(d, x, y, w, h, txt, fill=fill, tc=tc, size=7.6)
        if i < 4:
            arrow(d, x + w, y + h / 2, xs[i + 1], y + h / 2)

    x1, x5 = xs[0] + w / 2, xs[4] + w / 2
    arrow(d, x5, y, x5, 34, head=False)
    arrow(d, x5, 34, x1, 34, head=False)
    arrow(d, x1, 34, x1, y - 1)
    label(d, W / 2, 20, "6. Revise: refine the prompt or correct the code, then repeat",
          size=7.4, color=NAVY, font=BOLD)
    return d


def figure3():
    """Division of labour between the AI tool and the developer."""
    W, H = 470, 182
    d = Drawing(W, H)

    d.add(Rect(4, 4, 228, 174, rx=4, ry=4, fillColor=LIGHT, strokeColor=BLUE, strokeWidth=1))
    d.add(Rect(238, 4, 228, 174, rx=4, ry=4, fillColor=LIGHT2, strokeColor=NAVY, strokeWidth=1))
    d.add(Rect(4, 148, 228, 30, rx=4, ry=4, fillColor=NAVY, strokeColor=None))
    d.add(Rect(238, 148, 228, 30, rx=4, ry=4, fillColor=BLUE, strokeColor=None))
    d.add(String(118, 159, "ChatGPT can assist with", fontName=BOLD, fontSize=9,
                 fillColor=WHITE, textAnchor="middle"))
    d.add(String(352, 159, "The human developer must", fontName=BOLD, fontSize=9,
                 fillColor=WHITE, textAnchor="middle"))

    left = [
        "Draft code from a written specification",
        "Explain unfamiliar code in plain language",
        "Suggest possible causes of a defect",
        "Propose alternative design approaches",
        "Draft test-case ideas and checklists",
        "Draft documentation and code comments",
    ]
    right = [
        "Define and confirm the requirements",
        "Judge whether the logic is actually correct",
        "Run the code in a real browser",
        "Test edge cases and record the evidence",
        "Decide which suggestions to accept",
        "Take responsibility for the final artefact",
    ]
    for i, t in enumerate(left):
        yy = 130 - i * 19
        d.add(String(14, yy, "\u2022", fontName=BOLD, fontSize=8, fillColor=NAVY))
        d.add(String(24, yy, t, fontName=REG, fontSize=7.8, fillColor=TEXT))
    for i, t in enumerate(right):
        yy = 130 - i * 19
        d.add(String(248, yy, "\u2022", fontName=BOLD, fontSize=8, fillColor=BLUE))
        d.add(String(258, yy, t, fontName=REG, fontSize=7.8, fillColor=TEXT))
    return d


def figure4():
    """Evaluation criteria used in the analysis (Section 3)."""
    W, H = 470, 158
    d = Drawing(W, H)
    cols = [
        ("Output quality", [
            "Relevance to requirements", "Readability and up-keep",
            "Edge-case handling", "Consistency of answers",
        ]),
        ("Process and interaction", [
            "Speed of first draft", "Quality of explanations",
            "Debugging help", "Test-case suggestions",
        ]),
        ("Risk and oversight", [
            "Human correction needed", "Security considerations",
            "Reliability of claims", "Accountability",
        ]),
    ]
    xs = [4, 164, 324]
    w = 142
    for x, (title, chips) in zip(xs, cols):
        d.add(Rect(x, 132, w, 22, rx=3, ry=3, fillColor=NAVY, strokeColor=None))
        d.add(String(x + w / 2, 139, title, fontName=BOLD, fontSize=8,
                     fillColor=WHITE, textAnchor="middle"))
        for i, c in enumerate(chips):
            yy = 102 - i * 26
            d.add(Rect(x + 3, yy, w - 6, 22, rx=3, ry=3, fillColor=LIGHT,
                       strokeColor=BLUE, strokeWidth=0.7))
            d.add(String(x + w / 2, yy + 7.5, c, fontName=REG, fontSize=7.6,
                         fillColor=NAVY, textAnchor="middle"))
    return d
