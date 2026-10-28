# -*- coding: utf-8 -*-
"""Section 2 narrative: project overview, procedure commentary, code notes."""

SECTION2 = [
    ("h2", "2.1 Project overview"),
    ("p", "The proposed application keeps a single list of tasks for the current "
          "session, letting the user add an item, see everything in one place, strike "
          "through what is finished and remove what is no longer needed. The intended "
          "user is a university student working on a laptop browser; the expected "
          "features are the six functional requirements listed in Table 1. The "
          "application is intentionally modest so that the experiment measures the "
          "quality of the AI assistance rather than the difficulty of the software."),

    ("h2", "2.2 Requirements"),
    ("p", "Requirements were written before any prompt was sent, so that the generated "
          "code could be judged against a fixed target rather than against whatever the "
          "tool happened to produce. Table 1 separates functional requirements (what the "
          "program must do) from basic quality requirements (how the program must behave "
          "and be written). Each requirement is written so that it can be checked by a "
          "single test case, which later supports the mapping between requirements and "
          "tests."),

    ("h2", "2.3 Tools and technologies"),
    ("p", "The experiment uses ChatGPT as the AI assistant, HTML and CSS for structure "
          "and presentation, JavaScript for behaviour, a plain text editor for saving "
          "the files and a modern browser as the combined execution and testing "
          "environment. Table 2 states the role of each tool and the evidence it "
          "produces. Keeping the toolchain this small also makes the experiment easy to "
          "reproduce."),

    ("h2", "2.4 Experimental procedure"),
    ("p", "The procedure below is written so that a second person could repeat the "
          "experiment and obtain comparable material. Each step states its purpose, the "
          "action to be taken, the learning outcome it should produce and the evidence "
          "to be collected. Steps 1 to 4 build the baseline; steps 5 to 8 establish what "
          "happens when the code is actually run; steps 9 to 11 cover targeted debugging "
          "and the comparison of versions; step 12 judges the final implementation "
          "against the requirements. The steps are iterative in practice: if testing "
          "reveals a defect, the developer returns to step 9 with a precise description "
          "of the observed behaviour rather than a guess."),
    ("table", "procedure"),

    ("h2", "2.5 Example prompts"),
    ("p", "The prompts below are written examples of the kind of instruction used in "
          "the experiment; they are not transcripts of an actual conversation and must "
          "be replaced by, or compared with, the real prompts and responses recorded "
          "during the run (Appendix A). Each prompt is self-contained: it states the "
          "role and audience, the features required, the constraints to respect and the "
          "shape of the expected answer."),
    ("prompts", None),

    ("h2", "2.6 Code example"),
    ("p", "The following JavaScript fragment is an illustrative example of the code the "
          "experiment is expected to produce for the first functional requirement. It is "
          "kept short so that it can be discussed line by line; it is not evidence of an "
          "experimental result."),
    ("code", None),
    ("p", "The function reads the value of the input field and trims surrounding "
          "whitespace. If nothing remains, it reports the problem and returns without "
          "changing the data, which covers the empty-input requirement. Otherwise it "
          "creates a task object, appends it to the tasks array, calls renderTasks() to "
          "redraw the list and clears the field for the next item. The example "
          "concentrates three requirements in one place \u2014 input validation, state "
          "change and interface refresh \u2014 so it can be checked by reading, by "
          "running the corresponding test cases and by asking the tool to explain its "
          "choices."),

    ("h2", "2.7 Challenges and limitations"),
    ("p", "Table 4 lists the challenges that are reasonable to anticipate when an AI "
          "tool is used this way. These are potential challenges to investigate: "
          "they are not problems that have been observed in this experiment. Anything "
          "actually encountered during the run is recorded verbatim in the experiment "
          "log (Table 5) with its verification status, so that the two categories are "
          "never confused."),
    ("table", "challenges"),

    ("h2", "2.8 Experiment log"),
    ("p", "Table 5 is the running record of the experiment. It is filled in during the "
          "run, not afterwards, so that observations are not reconstructed from memory. "
          "The \u201cChatGPT assistance\u201d column records what was asked and returned; "
          "the \u201cactual observation\u201d column records what really happened on "
          "screen or in the console; the verification status column shows whether the "
          "step has been checked, is still pending, or could not be reproduced."),
    ("table", "log"),

    ("h2", "2.9 Testing table"),
    ("p", "Table 6 defines the test cases used to evaluate the implementation. They "
          "cover each functional requirement, the boundaries around empty and "
          "whitespace-only input, repeated actions and the end state after everything "
          "has been deleted. Expected behaviour is stated in advance so that it cannot "
          "be adjusted to match the observed result. Actual results and verdicts remain "
          "pending until the tests have been executed in the browser and the evidence "
          "attached in Appendix D."),
    ("table", "tests"),
]
