# -*- coding: utf-8 -*-
"""Illustrative prompts, the code example and appendix material."""

PROMPTS = [
    ("P1", "Generate the initial application",
     "You are helping a university student build a beginner-level web app. Write a "
     "single-page student task manager using only HTML, CSS and JavaScript (no frameworks "
     "and no external libraries). Features: add a task from a text input, show all tasks, "
     "mark a task as completed, delete a task, show a message and add nothing when the "
     "input is empty, and update the list immediately after every action. Keep the code "
     "readable for a beginner, use meaningful names, and give me three files: index.html, "
     "style.css and script.js."),
    ("P2", "Request an implementation plan first",
     "Before writing any code, describe the file structure, the data structure you would "
     "use to store the tasks in memory, and the main functions you plan to create. Keep it "
     "short and explain each choice in one sentence."),
    ("P3", "Explain the generated code",
     "Explain the script.js code you just produced. For each function, describe what it "
     "does, which event triggers it, and how the list on the screen is updated. Assume I "
     "am new to JavaScript and point out anything you think a beginner is likely to "
     "misunderstand."),
    ("P4", "Identify potential bugs",
     "Review this task manager for bugs before I run it. Focus on: empty or "
     "whitespace-only input, deleting the wrong item, items disappearing after an update, "
     "duplicate identifiers, and any place where user-typed text could be treated as HTML. "
     "List each issue, the line it occurs on, and why it would fail."),
    ("P5", "Targeted debugging with an observed symptom",
     "When I press Add with an empty input, here is what actually happens: [describe the "
     "observed behaviour]. The exact browser console message is: [paste error]. The "
     "relevant function is: [paste code]. Explain the most likely cause and give the "
     "smallest change that fixes it, without rewriting the rest of the file."),
    ("P6", "Design test cases",
     "List test cases for this task manager covering adding tasks, displaying them, "
     "completing them, deleting them, empty input, whitespace-only input, long text and "
     "repeating each action several times. For every test case give the steps, the "
     "expected result, and what would count as a failure."),
    ("P7", "Improve readability without changing behaviour",
     "Improve the readability of this function without changing its behaviour: rename "
     "unclear variables, split the function into smaller ones, and add a brief comment only "
     "where the logic is not obvious. Then tell me exactly what you changed and why."),
    ("P8", "Produce documentation",
     "Write a short README for this project: what the application does, which files it "
     "contains, how to run it locally, how to test it manually, and the known limitations "
     "of the current version. Use plain language and do not claim features that are not in "
     "the code."),
]

CODE_JS = """// Adds one task after checking the input. (Illustrative example.)
function addTask() {
  const input = document.getElementById("taskInput");
  const text = input.value.trim();

  if (text === "") {
    showError("Please type a task before adding.");  // empty-input rule
    input.focus();
    return;                                           // change nothing
  }

  const task = { id: Date.now(), text: text, done: false };
  tasks.push(task);        // update the data first ...
  renderTasks();           // ... then refresh the whole list
  input.value = "";        // clear the field for the next task
  input.focus();
}"""

APPENDIX_D_NOTE = (
    "Insert genuine screenshots only. Useful captures are: the ChatGPT conversation "
    "showing each prompt and response; the browser window with the application running; "
    "the developer console before and after a fix; and the filled test table. Crop the "
    "images so that they fit the page width, and add the date and the step number to each "
    "caption."
)

APPENDIX_E_NOTE = (
    "Use this space for your own reflection after the experiment has been run. The "
    "paragraphs in Section 4 are drafts: replace bracketed placeholders with your own "
    "observations, delete anything you disagree with, and keep the balanced conclusion "
    "that AI assistance does not remove the need for programming knowledge, testing or "
    "accountability."
)

EVIDENCE_CHECKLIST = [
    "Requirements table (Table 1) agreed before prompting.",
    "Prompt P1 (or its real replacement) copied into Appendix A with date and time.",
    "Initial code draft saved as version 1 in a separate folder.",
    "Browser execution of version 1 recorded (screenshot or console note).",
    "All test cases in Table 6 executed, with actual results filled in.",
    "Any defect found described verbatim in Table 5 (symptom, not theory).",
    "Debugging prompt and response pasted into Appendix A.",
    "Version 2 saved after applying the accepted correction.",
    "Version 1 and version 2 compared (diff or annotated notes).",
    "Observation column of Table 7 completed for every criterion.",
    "Screenshots attached in Appendix D and referenced in the text.",
    "Section 4 and Section 5 updated from \u201cpending\u201d to the final conclusion.",
]

SCREENSHOT_SLOTS = [
    ("D.1", "ChatGPT conversation: initial prompt and first response"),
    ("D.2", "The task manager running in the browser (version 1)"),
    ("D.3", "Browser console showing any errors observed while testing"),
    ("D.4", "The corrected version 2 after the debugging round"),
    ("D.5", "Completed test table or a pass/fail summary"),
]
