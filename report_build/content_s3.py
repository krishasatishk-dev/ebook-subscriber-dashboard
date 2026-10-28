# -*- coding: utf-8 -*-
"""Section 3: effectiveness analysis."""

SECTION3 = [
    ("h2", "3.1 Approach to the analysis"),
    ("p", "The analysis evaluates how effectively ChatGPT supported the development of "
          "the task manager. Ten criteria were fixed before the experiment so that the "
          "assessment could not be shaped after the fact (Figure 4). For every "
          "criterion, Table 7 states the evaluation method, the evidence required, a "
          "placeholder for the actual observation and the interpretation rule \u2014 "
          "what different outcomes would mean. Until the experiment has been run the "
          "observation column reads \u201cpending\u201d. Writing the interpretation rules in "
          "advance is what allows a later reader to distinguish a genuine result from a "
          "story constructed to fit the outcome."),
    ("table", "evaluation"),

    ("h2", "3.2 Potential strengths to look for"),
    ("p", "If the tool performs as its design suggests, four strengths should appear in "
          "the record. The first is speed: a complete first draft of three files can "
          "arrive in one response, so the developer reaches a runnable program sooner, "
          "and the time from prompt to draft can be measured from the conversation "
          "timestamps. The second is accessible explanation: asked to describe an "
          "unfamiliar construct such as a DOM event, the tool can usually explain it at "
          "the reader's level, which supports learning while working. The third is "
          "alternatives: a follow-up prompt can produce a different data structure or "
          "rendering approach, giving a choice that would otherwise require reading "
          "several tutorials. The fourth is the unglamorous work \u2014 test-case lists, "
          "comments and README text \u2014 produced quickly, which raises the chance that "
          "a beginner will test and document at all. Follow-up prompts also allow "
          "interactive refinement, narrowing the gap between what was asked for and "
          "what was returned."),

    ("h2", "3.3 Potential weaknesses to look for"),
    ("p", "The corresponding risks are equally concrete. Generated code may be "
          "incorrect or incomplete: it may parse cleanly and still violate a "
          "requirement, or call a function that was never defined. Requirements can be "
          "misread when the prompt is ambiguous \u2014 asking for a \u201clist of "
          "tasks\u201d leaves open whether items persist after a refresh. Edge cases are "
          "the first casualty: whitespace-only input, very long text, rapid repeated "
          "clicks and deleting the final item are often absent from a first draft unless "
          "named in the prompt. Responses are not fully consistent, so the same question "
          "in a fresh conversation may yield a different structure. Security weaknesses "
          "can enter quietly, for example rendering user-typed text with innerHTML "
          "instead of textContent [8]. Above all, none of these problems are visible "
          "until a person runs and tests the program, so the output is only as good as "
          "the verification that follows."),

    ("h2", "3.4 Plausible code versus verified code"),
    ("p", "The distinction at the centre of this analysis is between code that looks "
          "correct and code that has been shown to be correct in the environment where "
          "it runs. A generated function can be well formatted, sensibly named and "
          "logically convincing and still fail for a reason that only appears at "
          "runtime: a wrong element id, an event bound before the element exists, or an "
          "assumption about input that the browser does not enforce [3]. Verification "
          "means executing the program, observing each required behaviour, exercising "
          "the edge cases and recording the result \u2014 exactly the activity in steps "
          "6 to 8 of the procedure. In this report, only statements supported by such a "
          "record may be called findings; everything else is a hypothesis, and is "
          "labelled as such."),

    ("h2", "3.5 Questions specific to this experiment"),
    ("p", "The following questions are what the completed experiment is expected to "
          "answer, phrased as questions because the evidence is not yet in place: Does "
          "the first draft satisfy all six functional requirements without edits? How "
          "many separate corrections are needed before every test case in Table 6 "
          "passes? Does the tool suggest test cases the student had not thought of, and "
          "are they relevant here? Does its explanation of its own code match what the "
          "code does line by line? How does the response change if the same prompt is "
          "repeated in a new conversation? Which of the ten criteria in Table 7 needs "
          "little human correction, and which requires substantial rework?"),
]
