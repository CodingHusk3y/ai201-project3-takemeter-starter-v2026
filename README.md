# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

I collected 200 public questions from the Movies & TV Stack Exchange
community, which covers films and television across many decades, countries,
genres, and production roles rather than one show or release. The source is
public without an invited account: I used the Stack Exchange API's `movies`
site endpoint with the `withbody` filter and kept each question title and full
body. The classifier sorts each question into `scene_identification`,
`production_detail`, `plot_interpretation`, or `fact_context`. I read 30
questions closely before settling the distinctions and retained the source URL
in each row's `note` field.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `scene_identification`

**Definition:** Asks to identify a film or television work from a remembered
scene, image, line, or sequence.

**Example 1:**
> Film where the scalp of the co-pilot of a plane is removed during flight

**Example 2:**
> Identify a 2016 TV show episode from a single scene: Female close-up hand
enters a keypad door code with an audio bridge

### `production_detail`

**Definition:** Primarily asks how a film or television work was made,
performed, edited, credited, translated, or technically achieved; the requested
answer is about real-world production, not an in-story cause.

**Example 1:**
> How do they film the mirror scenes in movies?

**Example 2:**
> How do actors stop breathing when playing "dead"?

### `plot_interpretation`

**Definition:** Primarily asks why an in-story event happens or what a
character, ending, title, or theme means; the requested answer must be an
interpretation of the fictional work.

**Example 1:**
> What caused and ended the time loop in Groundhog Day?

**Example 2:**
> Is there any definitive evidence that Teddy was or was not crazy?

### `fact_context`

**Definition:** Primarily asks for a checkable fact or external context about a
work, release, language, technology, or relationship that is not a production
technique or an in-story interpretation.

**Example 1:**
> Is the Unix operating system featured in Jurassic Park real?

**Example 2:**
> What's the difference between "and" and "&" in movie credits?

### The hardest boundary

**Which two labels:** `plot_interpretation` and `fact_context`

**The decision rule I used every time:** Label the primary answer being
requested, in this order: (1) identify the work from remembered scene details
as `scene_identification`; (2) explain a real-world filmmaking method as
`production_detail`; (3) explain an event, character choice, ending, title, or
theme inside the fictional work as `plot_interpretation`; (4) use
`fact_context` for a checkable external fact or relationship. A question's
wording ("why" or "how") does not override the subject of the answer.

### Boundary stress test

I gave the four definitions and the precedence rule to an AI tool and asked it
for eight deliberately borderline questions. I classified each before looking
for overlap:

| Generated boundary post | Classification | Why |
|---|---|---|
| “I remember a black-and-white thriller where a woman hears a phone ring in an empty station. What film is it?” | `scene_identification` | The requested answer is the work's name. |
| “Which movie has the scene where a child repeats ‘don't open the red door’ while the camera stays outside?” | `scene_identification` | The concrete remembered sequence is evidence for identification. |
| “Why does the hero leave the money behind after finding it in the final scene?” | `plot_interpretation` | It asks for an in-story character motivation. |
| “The ending shows the clock stopped at 3:17; what does that detail mean?” | `plot_interpretation` | It asks for meaning within the film, even though the answer may be uncertain. |
| “How did the crew hide the camera in the apartment mirror shot?” | `production_detail` | It asks for a real-world filming technique. |
| “Why did the director cut from the actor’s face to a close-up of the key?” | `production_detail` | The question is about an editing choice made by filmmakers, not a character’s reason. |
| “Was the computer interface shown in the film based on a real operating system?” | `fact_context` | It asks for an externally checkable technology fact. |
| “Which release of the film is the official continuity for the sequel?” | `fact_context` | It asks for a release/continuity relationship, not what an in-story event means. |

The test exposed one important tightening: “why” alone is not enough to assign
`plot_interpretation`. I now ask whether the answer concerns fictional events,
production decisions, or an external fact, and use the precedence order above.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**

The posts came from the public Movies & TV Stack Exchange API:
https://api.stackexchange.com/2.3/questions?site=movies&pagesize=100&filter=withbody.
The API returned public question text and source links; no login, invitation, or
private community was used.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

I read 30 posts before fixing the taxonomy. I then applied the written
question-type rule to the 200-row corpus, using source tags and wording as a
pre-labeling aid, and spot-checked the resulting rows against the full text.
This is disclosed pre-labeling, not a claim that every label was assigned
unaided.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `scene_identification` | 34 | 17.0% |
| `production_detail` | 40 | 20.0% |
| `plot_interpretation` | 75 | 37.5% |
| `fact_context` | 51 | 25.5% |
| **Total** | **200** | **100%** |

**What I noticed while reading 30–40 posts:** The most substantial questions
usually named a concrete scene, quote, date, device, or character and supplied
enough surrounding context to make the question testable. Several plot
questions compared multiple events or competing explanations rather than just
asserting that a scene was confusing. Production questions often named a
specific technique or artifact (mirrors, credits, subtitles, Unix interfaces).
The weakest-looking examples were short questions with one unsupported premise
and little context; that observation informed the hard boundary, but I did not
use "good" versus "bad" as a label.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* Why does the talk show host always sit on the right?
>
> *Could have been:* `fact_context` or `production_detail`
>
> *I chose, because:* `fact_context`; it asks for a convention's external
context, not how a particular programme was filmed.

**2.**
> *The post:* Is the title "The Last Jedi" singular or plural?
>
> *Could have been:* `plot_interpretation` or `fact_context`
>
> *I chose, because:* `plot_interpretation`; the question asks what the title
refers to within the story, not merely how the title was translated.

**3.**
> *The post: Which version of Blade Runner is Blade Runner 2049 a sequel of?
>
> *Could have been:*
`fact_context` or `plot_interpretation`
>
> *I chose, because:* `fact_context`; it asks for an externally checkable
production/release relationship and explicitly rejects opinion.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

Pending the notebook training run.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Help me turn observations from a broad film-question
community into mutually exclusive labels.
- *What came back:* Candidate distinctions based on question purpose rather than
a subjective good/bad score.
- *What I changed:* I kept four operational labels and wrote a precedence rule
for the plot/fact boundary.

**Moment 2**

- *What I asked for:* Help collect and organize 200 public questions without
using a login.
- *What came back:* A public Stack Exchange API collection with title, full
body, tags, and source link.
- *What I changed:* I read a 30-question sample, retained the complete text,
and disclosed the rule-based pre-labeling.

**Pre-labelling disclosure:**

The first-pass labels were generated from the question title, public tags, and
the written taxonomy rule, then spot-checked. No private, invited, or
login-gated material was used.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
