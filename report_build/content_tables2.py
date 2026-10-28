# -*- coding: utf-8 -*-
"""Tables 4-7: challenges, experiment log, tests and evaluation criteria."

Every observation cell is deliberately left pending: no experimental run was
supplied when this report was generated, so no observed result is claimed.
"""

PENDING = "[Pending \u2014 record during the run]"

TABLE_CHALLENGES = {
    "caption": "Challenges to investigate (potential, not yet observed)",
    "headers": ["Challenge", "Why it may occur", "How it would be recognised",
                "Status"],
    "weights": [26, 30, 30, 14],
    "font": 7.6,
    "rows": [
        ["Requirement misunderstood",
         "The prompt is ambiguous or the tool infers a different scope.",
         "The code does something adjacent to what was asked; FR mapping shows a gap.",
         "Potential"],
        ["Syntax error, script does not load",
         "Generated code is never executed by the tool before it is returned [3].",
         "Blank page or console message naming a parse error.",
         "Potential"],
        ["Undefined function or wrong element id",
         "Fragments produced separately do not line up.",
         "Console reports \u201cis not defined\u201d, or a click produces no effect.",
         "Potential"],
        ["Edge case not handled",
         "Blank input, very long text or rapid clicks were not named in the prompt.",
         "TC-06, TC-07 or TC-08 fails during step 7.",
         "Potential"],
        ["Suggested correction does not work",
         "The diagnosis is based on an incomplete description of the symptom.",
         "The failed test still fails, or a new test fails after the change.",
         "Potential"],
        ["Inconsistent answers between runs",
         "Replies are generated probabilistically, not retrieved from a fixed source.",
         "The same prompt in a fresh chat returns a different structure.",
         "Potential"],
        ["Unsafe rendering of user text",
         "Generated code may insert typed text as HTML rather than as text [8].",
         "Markup typed as a task title is rendered by the browser.",
         "Potential"],
        ["Verbose or hard-to-follow explanation",
         "Conversational format favours completeness over focus.",
         "The actionable point is hard to locate in a long answer.",
         "Potential"],
    ],
}

_LOG_ROWS = [
    ["1", "Write the requirements (Table 1).",
     "Optional: ask the tool to critique the list for gaps.", PENDING, "Pending"],
    ["2", "Write the initial prompt P1.",
     "None yet; the prompt is authored by hand.", PENDING, "Pending"],
    ["3", "Send P2 and review the returned plan.",
     "Plan (files, data structure, functions) returned by ChatGPT.", PENDING, "Pending"],
    ["4", "Request code and save it unchanged as version 1.",
     "Three-file draft returned by ChatGPT.", PENDING, "Pending"],
    ["5", "Read version 1 line by line and annotate.",
     "P3 used to explain any unclear part of the code.", PENDING, "Pending"],
    ["6", "Open index.html in the browser and observe.",
     "None; execution is performed by the browser.", PENDING, "Pending"],
    ["7", "Run test cases TC-01 to TC-12 (Table 6).",
     "None; the observed behaviour is the ground truth.", PENDING, "Pending"],
    ["8", "Record every failure verbatim (symptom and console message).",
     "None; recording must stay independent of the tool.", PENDING, "Pending"],
    ["9", "Send P5 with the symptom, console message and relevant code.",
     "Diagnosis and proposed patch returned by ChatGPT.", PENDING, "Pending"],
    ["10", "Apply the accepted change as version 2 and re-test everything.",
     "P3-style follow-up: explain why the change fixes the symptom.",
     PENDING, "Pending"],
    ["11", "Compare version 1 with version 2.",
     "Optional: ask the tool to summarise the difference.", PENDING, "Pending"],
    ["12", "Complete the observation column of Table 7 and answer Section 3.5.",
     "None; the final judgement must be the student's own.", PENDING, "Pending"],
]

TABLE_LOG = {
    "caption": "Experiment log \u2014 assistance column states what is planned at each step; "
               "observations and status are completed during the run",
    "headers": ["Step", "Action performed", "ChatGPT assistance", "Actual observation",
                "Verification status"],
    "weights": [5, 27, 27, 26, 15],
    "font": 7.4,
    "rows": _LOG_ROWS,
}

TABLE_TESTS = {
    "caption": "Test cases: expected behaviour is fixed in advance; actual results and "
               "verdicts are filled after execution",
    "headers": ["ID", "Test and steps", "Expected behaviour", "Actual result",
                "Verdict"],
    "weights": [7, 30, 36, 17, 10],
    "font": 7.5,
    "rows": [
        ["TC-01", "Type \u201cSubmit lab report\u201d and press Add (FR-1).",
         "The task appears once in the list and the input field is cleared.",
         "[Pending]", "Pending"],
        ["TC-02", "Add three different tasks one after another (FR-2).",
         "All three tasks are visible, in the order they were added.",
         "[Pending]", "Pending"],
        ["TC-03", "Activate the complete control on the first task (FR-3).",
         "The task is shown as completed and remains in the list.",
         "[Pending]", "Pending"],
        ["TC-04", "Activate the complete control on the same task again (FR-3).",
         "The task returns to the not-completed state.",
         "[Pending]", "Pending"],
        ["TC-05", "Delete the middle task of three (FR-4).",
         "Only that task disappears; the other two are unchanged.",
         "[Pending]", "Pending"],
        ["TC-06", "Press Add with the input field empty (FR-5).",
         "Nothing is added and a visible message explains the problem.",
         "[Pending]", "Pending"],
        ["TC-07", "Type only spaces and press Add (FR-5).",
         "Nothing is added; the same message is shown.",
         "[Pending]", "Pending"],
        ["TC-08", "Add a task containing about 300 characters.",
         "The task is displayed and the layout is not broken.",
         "[Pending]", "Pending"],
        ["TC-09", "Add five tasks in quick succession (FR-6).",
         "Exactly five items are listed; no duplicates or missing items.",
         "[Pending]", "Pending"],
        ["TC-10", "Toggle and delete several times in a row (FR-6, QR-4).",
         "The list always matches the last action; no console errors appear.",
         "[Pending]", "Pending"],
        ["TC-11", "Delete every task until the list is empty.",
         "An empty list or an empty-state message is shown; no errors occur.",
         "[Pending]", "Pending"],
        ["TC-12", "Refresh the page after adding tasks.",
         "Behaviour matches the declared scope (in-memory: list is cleared).",
         "[Pending]", "Pending"],
    ],
}

_CRITERIA = [
    ("Relevance of generated code to requirements",
     "Map each requirement FR-1 to FR-6 to the code lines that implement it.",
     "Annotated requirement-to-code mapping.",
     "If every FR maps to working code, relevance is high; gaps or dead features "
     "indicate a prompt or comprehension problem."),
    ("Speed of creating an initial draft",
     "Record the timestamp of the first prompt and of the first complete three-file "
     "response.",
     "Conversation timestamps; note of any retries.",
     "Compare elapsed times across attempts; no speed claim is made without "
     "timestamps."),
    ("Readability and maintainability",
     "Independent read-through: unclear names, duplicated logic, length of functions.",
     "Annotated version 1 listing; review notes.",
     "Few unclear or duplicated elements suggest readable output; extensive rewriting "
     "suggests the opposite."),
    ("Helpfulness of explanations",
     "Check whether each answer addresses the question asked and matches the code when "
     "read line by line.",
     "Question-and-answer pairs checked against the listing.",
     "Explanations that match the code support learning; contradictions must be "
     "corrected by the reader."),
    ("Assistance with debugging",
     "Apply the suggested correction to a failing test case, then re-run that case and "
     "the full suite.",
     "Before-and-after results from Table 6.",
     "A fix that makes the failed case pass without breaking others is effective "
     "assistance."),
    ("Quality of test-case suggestions",
     "Compare the tool's test list with Table 6: cases found, cases missed, cases "
     "irrelevant here.",
     "Two lists side by side.",
     "Useful additions raise confidence; missing edge cases show where human test "
     "design is still needed."),
    ("Handling of edge cases",
     "Execute TC-06, TC-07, TC-08 and TC-11 on the unmodified first draft.",
     "Verdicts for those test cases.",
     "Passing before correction shows edge cases were anticipated; failing shows they "
     "must be demanded in the prompt."),
    ("Consistency of responses",
     "Repeat the same prompt in a fresh conversation and compare the two answers.",
     "Two saved transcripts of the same prompt.",
     "Similar structures indicate consistency; different designs must be reconciled by "
     "the developer."),
    ("Amount of human correction required",
     "List every edit made between version 1 and version 2 and classify it (defect, "
     "requirement, style).",
     "Version comparison; count and classification of edits.",
     "Many defect-class edits mean heavy dependence on review; mostly style edits mean "
     "the draft was close."),
    ("Security and reliability risks",
     "Review how user-typed text is inserted into the page and how input is validated; "
     "compare with [8] and [9].",
     "Security review notes; console error log.",
     "Unsafe patterns found must be corrected before the result is called usable."),
]

TABLE_EVALUATION = {
    "caption": "Evaluation criteria: method, required evidence, observation placeholder "
               "and interpretation rule",
    "headers": ["Criterion", "Evaluation method", "Evidence required",
                "Actual observation", "Interpretation if/when observed"],
    "weights": [18, 24, 19, 15, 24],
    "font": 7.2,
    "rows": [[c, m, e, "[Pending]", i] for (c, m, e, i) in _CRITERIA],
}
