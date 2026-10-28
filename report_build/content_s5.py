# -*- coding: utf-8 -*-
"""Section 5 conclusion, references and the rubric-alignment matrix."""

CONCLUSION_STATUS = (
    "Provisional conclusion \u2014 update after the experiment has been executed and "
    "Sections 2.8, 2.9, 3 and 4 have been completed."
)

SECTION5 = [
    ("p", "This report set out to examine how a conversational AI tool can assist a "
          "student through the full path of a small software project: a browser-based "
          "task manager built with HTML, CSS and JavaScript. The approach was to fix "
          "the requirements first, define a twelve-step procedure covering prompting, "
          "code generation, human review, execution, testing, debugging, revision and "
          "comparison, and to pre-register ten evaluation criteria together with the "
          "evidence each one requires. The material produced so far \u2014 requirements, "
          "prompts, an illustrative code example, the experiment log, the test suite and "
          "the verification checklist \u2014 is enough for another student to repeat the "
          "work."),

    ("p", "The main limitation is equally clear: the observation fields are still "
          "empty. No conclusion about the tool's effectiveness can honestly be drawn "
          "until the program has been executed, the tests run and the transcripts and "
          "screenshots attached. This conclusion is therefore provisional. What can "
          "already be stated is the standard of proof the report applies: code is "
          "treated as a proposal until it has been reviewed line by line and observed "
          "working in the browser, expected behaviour is never reported as an actual "
          "result, and every claim must be traceable to a record in Table 5, Table 6 or "
          "Table 7."),

    ("p", "Three updates are required after testing. First, the observation columns of "
          "Tables 5, 6 and 7 must be completed and the status changed from pending to "
          "checked, with screenshots added in Appendix D. Second, the questions in "
          "Section 3.5 must be answered from that evidence, including the number of "
          "corrections needed before all test cases passed. Third, Sections 4 and 5 must "
          "be rewritten in the student's own words to reflect what happened, and the "
          "provisional label removed only if the experiment is complete. Only then may "
          "the report state whether the assistance was effective for this task, and on "
          "what evidence."),
]

REFERENCES = [
    "OpenAI, \u201cChatGPT,\u201d OpenAI, San Francisco, CA, 2023. [Online]. Available: "
    "https://openai.com/chatgpt/",

    "OpenAI et al., \u201cGPT-4 technical report,\u201d arXiv:2303.08774, 2023. [Online]. "
    "Available: https://arxiv.org/abs/2303.08774",

    "M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, "
    "H. Edwards, Y. Burda, N. Joseph, G. Brockman, and A. Ray et al., \u201cEvaluating "
    "large language models trained on code,\u201d arXiv:2107.03374, 2021. [Online]. "
    "Available: https://arxiv.org/abs/2107.03374",

    "WHATWG, \u201cHTML living standard,\u201d Web Hypertext Application Technology "
    "Working Group, 2025. [Online]. Available: https://html.spec.whatwg.org/",

    "MDN Web Docs, \u201cCSS: Cascading Style Sheets,\u201d Mozilla, [Online]. "
    "Available: https://developer.mozilla.org/en-US/docs/Web/CSS",

    "MDN Web Docs, \u201cJavaScript guide,\u201d Mozilla, [Online]. Available: "
    "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",

    "W3C, \u201cWeb Content Accessibility Guidelines (WCAG) 2.2,\u201d W3C "
    "Recommendation, Oct. 2023. [Online]. Available: https://www.w3.org/TR/WCAG22/",

    "OWASP, \u201cOWASP Top Ten,\u201d Open Worldwide Application Security Project, "
    "2021. [Online]. Available: https://owasp.org/www-project-top-ten/",

    "NIST, \u201cSecure Software Development Framework (SSDF) Version 1.1,\u201d NIST "
    "Special Publication 800-218, Gaithersburg, MD, Feb. 2022. [Online]. Available: "
    "https://csrc.nist.gov/pubs/sp/800/218/final",

    "ISO/IEC/IEEE, \u201cSystems and software engineering \u2014 Software testing "
    "\u2014 Part 1: General concepts,\u201d ISO/IEC/IEEE 29119-1:2022, Jan. 2022. "
    "[Online]. Available: https://www.iso.org/standard/81291.html",

    "IEEE, \u201cIEEE Standard for Software Quality Assurance Processes,\u201d IEEE "
    "Std 730-2014, Jun. 2014, doi: 10.1109/IEEESTD.2014.6835311.",

    "MDN Web Docs, \u201cHTML: HyperText Markup Language,\u201d Mozilla, [Online]. "
    "Available: https://developer.mozilla.org/en-US/docs/Web/HTML",
]

# criterion, marks, supporting sections, status
RUBRIC_ROWS = [
    ("Setup: Completeness and clarity", "5",
     "Section 1.1\u20131.5; Figure 1", "Report"),
    ("Setup: Quality of tool description", "5",
     "Sections 1.2\u20131.4, 1.8\u20131.9; references [1]\u2013[3]", "Report"),
    ("Experimentation: Thoroughness", "10",
     "Sections 2.1\u20132.4; Tables 2\u20133; Figure 2", "Report"),
    ("Experimentation: Documentation", "10",
     "Sections 2.5\u20132.6, 2.8\u20132.9; Tables 5\u20136; Appendices A\u2013C",
     "Report"),
    ("Experimentation: Creativity", "10",
     "Prompts P4\u2013P8; Sections 2.7, 3.5; edge-case tests TC-07\u2013TC-12",
     "Report"),
    ("Analysis: Quality of analysis", "15",
     "Section 3; Table 7; Figures 3\u20134", "Report"),
    ("Reflection: Insightfulness", "15",
     "Section 4 (personalise); Section 5; Appendix E", "Report"),
    ("Presentation: Clarity and organization", "10",
     "Whole document: cover, contents, headings, tables, captions, references",
     "Report"),
    ("Presentation: Video effectiveness", "10", "\u2014",
     "Separate video deliverable"),
    ("Peer review: Quality of feedback", "10", "\u2014",
     "Separate peer-review activity"),
]
