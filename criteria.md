# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

Overall accuracy is at least 0.65 on the held-out test set.


**Why this target:** Four labels make random guessing about 0.25, so 0.65 would indicate that the model learned the question-type vocabulary rather than only the most common label. The corpus has deliberately different kinds of film questions, so I do not expect near-perfect accuracy.



---

## 2.

Macro F1 is at least 0.60 on the held-out test set.


**Why this target:** Macro F1 gives the 34 scene-identification examples the same weight as the 75 plot-interpretation examples. The smaller identification class should be noisier, so 0.60 is a useful but realistic overall balance target.



---

## 3.

Every label has an F1 of at least 0.45 on the held-out test set.


**Why this target:** The hardest boundary is plot interpretation versus fact/context, while scene identification has fewer examples. A 0.45 floor allows for those difficult cases but still requires every label to perform better than a weak one-label strategy.



---

## 4.

The largest and smallest label shares differ by no more than 20 percentage points.


**Why this target:** The source naturally contains many plot questions and fewer identification questions. The current 75-versus-34 spread is 20.5 points, so this target checks whether later additions or corrections make the training set materially more lopsided.



---

## 5.

On the 30-post staff agreement set, my labels agree with staff on at least 24 posts (80%).


**Why this target:** Agreement is a separate check on labeling consistency rather than model performance. An 80% target leaves room for genuinely ambiguous examples while requiring me to apply written decision rules consistently.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
