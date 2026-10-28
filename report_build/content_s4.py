# -*- coding: utf-8 -*-
"""Section 4: reflection and future implications."""

NOTE_S4 = (
    "This section is a draft for you to personalise. Bracketed prompts such as "
    "\u201c[add your observation]\u201d are placeholders: replace them with your own experience "
    "once the experiment has been run, and delete any statement that does not match what "
    "actually happened."
)

SECTION4 = [
    ("1. What can a student learn by using ChatGPT during software development?",
     'Used carefully, the tool behaves like a patient tutor that never tires of follow-up questions. A student can learn how a problem is decomposed into files and functions, why one data structure is chosen over another, and what an unfamiliar line does — learning that normally requires reading several documentation pages. The condition is active reading: the explanation must be checked against the code instead of accepted. [Add the specific concept you understood better after this experiment.]'),
    ("2. How can AI tools be incorporated into a normal programming workflow?",
     "The most defensible place for AI is at the boundaries of the work: clarifying requirements, drafting a plan, producing a first skeleton, explaining unfamiliar code, proposing hypotheses when something breaks, generating a test checklist and drafting documentation. A workable routine is plan → draft → review → run → test → revise, with the tool consulted at the plan, draft, explanation and debugging stages while the human keeps review and verification. Keeping AI-assisted changes in version control makes the tool's contribution visible and reversible. [Note where the assistance was most and least useful in your own workflow.]"),
    ("3. Which development tasks are well suited to AI assistance?",
     "Tasks with quick, unambiguous feedback and low stakes suit it best: boilerplate "
     "structure, routine CRUD-style functions, rewriting a snippet for clarity, drafting "
     "comments and README text, enumerating test scenarios and explaining error "
     "messages. In this project that includes the HTML skeleton, the list rendering, the "
     "documentation and the initial test list."),
    ("4. Which tasks require particularly careful human judgment?",
     "Decisions that are hard to reverse or hard to detect: whether the requirements "
     "themselves are correct, whether the logic really implements them, how input is "
     "handled safely, what happens at the boundaries, whether a fix has broken something "
     "else, and whether the software is ready to be used or submitted. Errors here can "
     "pass unnoticed, because the tool gives no warning that it is uncertain."),
    ("5. Why must AI-generated code be reviewed and tested?",
     "Because the generator never executes the program: it produces text that resembles "
     "working code, and resemblance is not evidence [3]. Review catches misunderstandings "
     "of the requirements; testing catches everything that only appears at runtime \u2014 "
     "wrong identifiers, unhandled input, events bound to elements that do not exist. "
     "Testing also turns an opinion about quality into a record that a reviewer or a "
     "future maintainer can check."),
    ("6. What are the risks of relying too heavily on AI?",
     'Skill erosion is the quiet risk: if reading, writing and debugging are always outsourced, the ability to judge the output declines precisely when it is most needed. Other risks are silent requirement drift, duplicated or insecure patterns spreading across a project, over-trust in an authoritative tone, and unclear accountability when generated code fails. Practical risks also remain: material pasted into a chat may be retained by the service [1], and the provenance of generated fragments may be unclear.'),
    ("7. How could AI influence software development in the future?",
     'The likely direction is deeper integration into the development environment: tools that propose changes across several files, run tests themselves, explain failures and keep documentation in step with code. That would raise the baseline speed of routine work and shift attention towards specification, review and verification. It would also raise the cost of being unable to read code, since the volume of code one person oversees would grow.'),
    ("8. What are the possible effects on learning, productivity, collaboration and "
     "developer responsibilities?",
     'For learning, the effect depends on use: as a Socratic assistant it can accelerate understanding, as an answer machine it can short-circuit it. Drafts and documentation are clearly faster; written prompts and transcripts can make design reasoning easier to share and review. Accountability increases rather than decreases — submitting generated code means asserting that it works, a claim only the developer can support with tests. [Add how your own practice changed during this experiment.]'),
    ("9. How can developers use AI responsibly?",
     "By declaring its use where disclosure is required, by never entering confidential data into a chat, by reviewing output as one would review a colleague's pull request, by testing before claiming correctness, by respecting the terms of service and licences of the tool [1], and by staying accountable for what is delivered. Responsible use also means correcting the tool when it is wrong rather than keeping a flawed suggestion."),
    ("10. What would be improved in a future version of this experiment?",
     'Three improvements are already identifiable before the run: repeat each prompt in a fresh conversation to measure consistency, record timestamps for every prompt so that speed claims rest on data, and add a small automated check so that verification is not purely manual. Extending the application with browser storage would allow persistence and refresh behaviour to be tested rather than assumed. [Add the improvements you identify after completing the run.]'),
]
