# -*- coding: utf-8 -*-
"""Cover page details, executive summary and Section 1."""

COURSE = "Exploring AI Tools in Software Development"
ASSIGNMENT = "Playing with AI Project & Peer Review"
REPORT_KIND = "Written Report"
PROJECT = ("Using ChatGPT to Assist in Developing a "
           "Student Task Manager Application")

STUDENT = {
    "name": "KRISHA KADAM",
    "roll": "A414",
    "sap": "70022500747",
    "institution": "[Institution name]",
    "deadline": "26 October 2026, 12:29 PM IST",
    "prepared": "[DD Month 2026]",
}

EXEC_SUMMARY = [
    "Software development is increasingly supported by artificial intelligence (AI) "
    "tools that can draft code, explain unfamiliar constructs and suggest fixes. This "
    "report documents an experiment for the Coursera course \u201cExploring AI Tools in "
    "Software Development\u201d in which ChatGPT, a conversational AI system published by "
    "OpenAI, is used as an assistant across the activities of a small software project: "
    "building a browser-based student task manager with HTML, CSS and JavaScript.",

    "The project was chosen because its scope is small enough for a student to read, run "
    "and test completely, yet it exercises a realistic range of development activities: "
    "writing requirements, generating an implementation, explaining generated code, "
    "debugging, designing test cases and producing documentation. The experiment follows "
    "a twelve-step procedure (Section 2.4) that runs from requirements through prompting, "
    "code generation, human review, execution, testing, targeted debugging, revision and "
    "comparison to a final evaluation against the requirements.",

    "Effectiveness is assessed against ten criteria, including relevance of generated code "
    "to the requirements, speed of the first draft, readability, explanations, debugging "
    "support, test-case suggestions, edge-case handling, consistency, the human correction "
    "required and security risks. For each criterion, Table 7 states how it will be "
    "evaluated and "
    "what evidence is required, so that any judgement rests on recorded observations "
    "rather than on impressions.",

    "Evidence status: the procedure, prompts, log and test suite supplied here are "
    "complete and reproducible, but every field reserved for an observed result is marked "
    "pending verification until the experiment has been executed and the material "
    "attached (Sections 2.8 and 2.9, Appendix D). Expectations about what the tool will "
    "return are therefore written as questions to investigate rather than as findings. The "
    "significance of the work lies in its method: it shows how a student can work with an "
    "AI assistant while human review, testing and accountability remain at the centre of "
    "the process.",
]

SECTION1 = [
    ("h2", "1.1 Introduction to AI-assisted software development"),
    ("p", "A software project normally passes through a familiar sequence of activities: "
          "understanding what the user needs, designing a solution, writing code, running "
          "it, fixing defects, testing against the requirements and documenting it. "
          "AI-assisted software development means using a machine-learning system to take "
          "a share of those activities. Current tools hold a conversation, accept "
          "plain-language instructions and return code fragments, explanations, test "
          "ideas and documentation drafts within seconds. The defining characteristic of "
          "this workflow is that the AI produces a proposal rather than a finished "
          "product: its output must still be executed, checked and then accepted or "
          "rejected by a human developer."),

    ("h2", "1.2 What ChatGPT is and its intended purpose"),
    ("p", "ChatGPT is a conversational AI application published by OpenAI [1]. It is "
          "built on a large language model (LLM), a neural network trained on very large "
          "amounts of text so that it can predict plausible continuations of a given "
          "input [2]. A user types a message (a prompt), the model returns a reply, and "
          "earlier turns stay part of the context. ChatGPT is intended as a "
          "general-purpose assistant for answering questions, drafting and summarising "
          "text, analysis, brainstorming and programming help. Two limitations follow "
          "from that design: the model does not run or compile code, so it cannot observe "
          "whether its own suggestion works, and replies are generated probabilistically, "
          "so the same prompt can yield different answers."),

    ("h2", "1.3 Capabilities relevant to this experiment"),
    ("p", "The capabilities that matter here are: (i) code generation from a "
          "natural-language description of features; (ii) code explanation, where the "
          "tool describes what a function does and why; (iii) debugging assistance, "
          "where it proposes likely causes and candidate corrections for a reported "
          "symptom; (iv) brainstorming of alternative designs; (v) documentation "
          "drafting, such as comments or a README file; and (vi) test-case suggestions. "
          "Each is a capability to be tested in this experiment, not a guarantee of "
          "correctness."),

    ("h2", "1.4 Why ChatGPT was selected for this experiment"),
    ("p", "ChatGPT was selected because it is widely accessible to students, it covers "
          "every activity the experiment needs in a single interface, and its chat format "
          "keeps the whole interaction \u2014 prompt, response, follow-up, correction "
          "\u2014 visible and easy to record as evidence. Editor-based completion tools "
          "also assist, but their suggestions arrive silently and are harder to document "
          "step by step. The conversational form also allows deliberate prompt "
          "refinement, a skill this course aims to develop."),

    ("h2", "1.5 Objective and scope of the task manager project"),
    ("p", "The objective is to investigate how far ChatGPT can assist a student in "
          "producing a small but complete web application, and how much human review and "
          "testing is needed before it can be considered correct. The application is a "
          "single-page student task manager that adds tasks, displays them, marks them "
          "complete, deletes them, rejects empty input and refreshes the interface after "
          "each action. It is deliberately small so that every line can be read and the "
          "quality of the assistance can be judged rather than trusted. Servers, "
          "databases, accounts, deployment and frameworks are out of scope; task data is "
          "held in memory."),

    ("h2", "1.6 Technologies and development environment"),
    ("p", "Three technologies are enough. HTML (HyperText Markup Language) defines the "
          "page structure \u2014 the input field, the button and the list [4], [12]. CSS "
          "(Cascading Style Sheets) defines the presentation \u2014 spacing, colours and "
          "the visual treatment of completed tasks [5]. JavaScript defines the behaviour "
          "\u2014 validating input, changing the data and re-rendering the list [6]. The "
          "browser is both the execution and the test environment: opening the file runs "
          "the code and the developer console reports errors. Any modern browser and any "
          "text editor are sufficient; there is no build step."),

    ("h2", "1.7 How conversational prompts guide software development"),
    ("p", "A prompt is the instruction given to the tool. Here it acts as a lightweight "
          "specification: it names the goal, lists the features, states the constraints "
          "(no frameworks, beginner-readable code, three separate files) and describes "
          "the expected format of the answer. Vague prompts produce vague output, so "
          "prompts are refined across turns \u2014 first for a plan, then for code, then "
          "for an explanation, then for a targeted fix. The quality of the dialogue is "
          "therefore part of what is studied: a clearer prompt should require less "
          "correction."),

    ("h2", "1.8 Limitations of AI-generated code"),
    ("p", "Code that reads plausibly is not the same as code that has been verified [3]. "
          "Typical failure modes include syntax errors that prevent the script from "
          "loading, logic that quietly violates a requirement, missing handling of edge "
          "cases such as blank input, references to identifiers that do not exist in the "
          "project, and security weaknesses \u2014 for example inserting user-typed text "
          "with innerHTML, which can allow unintended markup to be interpreted as HTML "
          "[8]. The model cannot execute the code it writes, so none of these problems "
          "are detected by the tool itself; they surface only when a person runs the "
          "program."),

    ("h2", "1.9 Human review, testing, privacy and responsible use"),
    ("p", "Three responsibilities remain with the developer. First, review: AI output is "
          "read line by line against the requirements before it is used, and anything not "
          "understood is questioned. Second, testing: the program is "
          "executed in the browser and exercised against the test cases in Table 6, edge "
          "cases included, before any claim of correctness. Third, responsible use: no "
          "personal or confidential material is pasted into the chat, the tool's terms of "
          "service are respected [1], and AI assistance is declared as the course "
          "requires. Accountability for the code and the report stays with the student, "
          "not with the tool."),
]
