# -*- coding: utf-8 -*-
"""Tables 1-3: requirements, tools and the experimental procedure."""

TABLE_REQUIREMENTS = {
    "caption": "Functional and quality requirements for the task manager (written before prompting)",
    "headers": ["ID", "Requirement", "Type", "How it will be checked"],
    "weights": [7, 46, 13, 34],
    "font": 7.8,
    "rows": [
        ["FR-1", "Add a task when the user types text and presses the Add button or Enter.",
         "Functional", "Test TC-01"],
        ["FR-2", "Display every task in a list, in the order it was added, with its text "
                 "and its status.", "Functional", "Test TC-02"],
        ["FR-3", "Mark a task as completed and change its appearance; allow the status to "
                 "be reversed.", "Functional", "Tests TC-03, TC-04"],
        ["FR-4", "Delete a single task without affecting the others.", "Functional",
         "Test TC-05"],
        ["FR-5", "Reject empty or whitespace-only input with a visible message and add "
                 "nothing.", "Functional", "Tests TC-06, TC-07"],
        ["FR-6", "Update the interface immediately after every action, without reloading "
                 "the page.", "Functional", "Tests TC-09, TC-10"],
        ["QR-1", "Readable code: meaningful names, consistent indentation, short "
                 "functions.", "Quality", "Read-through in Section 3"],
        ["QR-2", "Usable on a laptop screen: clear labels, visible feedback for invalid "
                 "input.", "Quality", "Manual check, TC-06"],
        ["QR-3", "Maintainable: task data kept separate from the rendering logic; no "
                 "duplicated blocks.", "Quality", "Code review notes"],
        ["QR-4", "Reliable: no uncaught errors in the browser console during normal use.",
         "Quality", "Console observation, TC-10"],
    ],
}

TABLE_TOOLS = {
    "caption": "Tools and technologies, with the role of each and the evidence it produces",
    "headers": ["Tool", "Role in the experiment", "Evidence it produces"],
    "weights": [20, 48, 32],
    "font": 8.0,
    "rows": [
        ["ChatGPT (OpenAI)",
         "Conversational AI assistant: plans, drafts code, explains it, proposes fixes, "
         "suggests test cases and drafts documentation.",
         "Saved transcripts of every prompt and response, with dates."],
        ["HTML", "Defines the page structure: input field, button and task list [4], [12].",
         "The index.html file of each version."],
        ["CSS", "Defines the presentation, including the visual state of completed tasks "
                "[5].", "The style.css file of each version."],
        ["JavaScript", "Implements the behaviour: validation, state change and "
                       "re-rendering [6].", "The script.js file of each version."],
        ["Browser and developer console",
         "Combined execution and test environment; reports runtime and syntax errors.",
         "Screenshots of the running app and of console messages."],
        ["Text editor and version copies",
         "Where files are saved, edited and compared between version 1 and version 2.",
         "Two saved versions and an annotated comparison (or a Git diff)."],
    ],
}

_PROCEDURE = [
    ("1", "Define the problem and the requirements",
     "Write the functional and quality requirements in Table 1 and decide the scope "
     "boundary before opening the chat.",
     "Requirements must be testable; a specification is what makes later judgement "
     "possible.",
     "Dated requirements document (Table 1)."),
    ("2", "Prepare an initial prompt",
     "Draft prompt P1: role, goal, six features, constraints (no frameworks, three files, "
     "beginner-readable code) and required output format.",
     "Prompt structure controls output quality; ambiguity in, ambiguity out.",
     "Exact prompt text, date and time."),
    ("3", "Request an implementation plan",
     "Send P2 and ask for the file structure, the in-memory data structure and the main "
     "functions before any code is accepted.",
     "Reviewing a design is cheaper than reviewing a full listing.",
     "Plan response, saved to the transcript file."),
    ("4", "Generate an initial code draft",
     "Send P3 (or ask for the code directly after the plan) and save the three files as "
     "version 1 without editing them yet.",
     "Establishes the unmodified baseline against which all later changes are compared.",
     "Version 1 files and the raw response."),
    ("5", "Review the suggested code",
     "Read version 1 line by line: missing functions, wrong element identifiers, logic "
     "that contradicts a requirement, unsafe rendering of user text.",
     "Static review finds defects before execution and trains close reading.",
     "Annotated review notes with line references."),
    ("6", "Run the code in a suitable environment",
     "Open index.html in a modern browser; observe the first screen and any console "
     "messages.",
     "Confirms whether generated code executes at all in the real environment.",
     "Screenshot of the running page; console output."),
    ("7", "Test each required feature",
     "Execute test cases TC-01 to TC-12 (Table 6) in order and fill the actual-result "
     "column immediately.",
     "Expected behaviour fixed in advance cannot be adjusted to match the outcome.",
     "Completed Table 6 with verdicts."),
    ("8", "Record errors and unexpected behaviour",
     "For each failure, write down the exact steps, the observed behaviour and the exact "
     "console message \u2014 the symptom, not a theory.",
     "Precise symptoms are what makes a useful follow-up prompt possible.",
     "Rows added to the experiment log (Table 5)."),
    ("9", "Ask ChatGPT for targeted debugging assistance",
     "Send P5 containing the observed symptom, the console message and only the relevant "
     "code fragment.",
     "Learning to describe a defect precisely; testing whether the tool diagnoses from "
     "evidence.",
     "Prompt P5 and the returned suggestion."),
    ("10", "Review and test any suggested correction",
     "Apply the smallest accepted change as version 2, re-run the failed test case, then "
     "re-run the whole suite to check for regressions.",
     "A fix is itself unverified until re-tested; regression testing prevents partial "
     "repairs.",
     "Version 2 files; re-run of Table 6."),
    ("11", "Compare the initial and revised versions",
     "Place version 1 and version 2 side by side (diff or annotated notes) and list what "
     "changed and why.",
     "Makes the contribution of each round explicit rather than assumed.",
     "Comparison notes or a diff."),
    ("12", "Evaluate against the requirements",
     "Complete the observation column of Table 7 criterion by criterion and answer the "
     "questions in Section 3.5 from the records.",
     "Converts raw material into an evidence-based judgement of effectiveness.",
     "Filled Table 7 and written interpretation."),
]

TABLE_PROCEDURE = {
    "caption": "Twelve-step experimental procedure: purpose, action, expected learning "
               "outcome and evidence to collect",
    "headers": ["No.", "Purpose", "Action to be taken",
                "Expected learning outcome", "Evidence to collect"],
    "weights": [6, 19, 30, 23, 22],
    "font": 7.4,
    "rows": [list(r) for r in _PROCEDURE],
}
