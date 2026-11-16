# Before / after (fidelity-first)

Every "after" below uses only material in its "before" or in an evidence block shown with it. Where the
honest result is "leave it and flag it", the example says so. All passages are synthetic.

---

## 1. Hype and over-claiming around real statistics

**Before:**
> In recent years, adolescent sleep has attracted increasing attention as a pivotal public-health
> concern. Our findings demonstrate that evening screen time causes poor sleep (r = 0.21, 95% CI 0.13 to
> 0.29), paving the way for a new paradigm in digital-health policy.

**After:**
> Evening screen time was associated with worse sleep quality (r = 0.21, 95% CI 0.13 to 0.29).

**Report:**
- *Prose edits:* removed the formulaic opener and "paving the way for a new paradigm".
- *Claim-strength change (author must confirm):* "demonstrate that … causes" → "was associated with".
  The manuscript reports a correlation, which does not support a causal verb.
- *Substantive proposal:* the opener's point (why adolescent sleep matters) could be kept as a sentence
  with a citation if the author has one. None was supplied, so nothing was added.

The statistic, CI, and direction of the effect are unchanged.

---

## 2. A citation cluster

**Before:**
> Moreover, it is worth noting that many prior studies have linked evening device use to delayed sleep
> onset [3, 7, 9, 12, 15].

**After:**
> Prior studies have linked evening device use to delayed sleep onset [3, 7, 9, 12, 15].

**Report:**
- *Prose edits:* removed "Moreover" and "it is worth noting that"; dropped "many" as an empty
  intensifier. The five citations make the point.
- *Substantive proposal:* consider saying what the strongest of these studies found (design, size).
  Which ones those are is the author's call.

All five keys stay, attached to the same claim. **Wrong fix:** "The closest prior study is [7]" (drops
four citations and invents a ranking).

---

## 3. An uncertain mechanism

**Before:**
> It is worth noting that, importantly, the mechanisms underlying this relationship remain unclear, as
> light exposure, displaced sleep time, and arousal have each been proposed, but none has been isolated
> experimentally [4].

**After:**
> The mechanism remains unclear. Light exposure, displaced sleep time, and arousal have each been
> proposed, but none has been isolated experimentally [4].

**Wrong fix:** "Blue-light exposure suppresses melatonin, delaying sleep onset [4]." This picks one
mechanism and turns an open question into a finding.

---

## 4. A null result

**Before:**
> The intervention did not significantly reduce PSQI scores relative to control (mean difference −0.6,
> 95% CI −1.3 to 0.1; p = 0.08).

**After:** unchanged. The sentence is already precise.

**Wrong fixes:**
- "The intervention trended toward reducing PSQI scores." (reframes a null result as a partial success)
- "The intervention had no effect on sleep." (turns absence of evidence into evidence of absence; the CI
  includes a 1.3-point improvement)

---

## 5. An unsupported claim with no numbers anywhere in the manuscript

**Before:**
> Our adaptive reminder system performed much better than the standard schedule and was really robust.

**After:**
> Our adaptive reminder system performed better than the standard schedule.

**Report:**
- *Prose edits:* removed "much" (casual intensifier).
- *Claim-strength change (author must confirm):* dropped "and was really robust". No robustness
  analysis appears in the manuscript.
- *Unresolved issue:* nothing in the manuscript supports this claim. There is no outcome, estimate,
  CI, test, or table, and neither reminder condition appears in Methods. `[AUTHOR: evidence needed for
  this claim]`, or delete the sentence.

Cutting "really robust" removes an unsupported claim, which is allowed: it weakens toward the
evidence. **Wrong fix:** "improved adherence by 18% (95% CI 9–27%; Table 3)". Every number and the
table pointer there are invented, and "make it concrete" does not change that.

---

## 6. The same claim when an evidence block is supplied

**User-supplied evidence block:**
> Adaptive reminders: 7-day adherence 71% (n = 58). Standard schedule: 54% (n = 60). Difference 17
> points, 95% CI 0.4 to 33.6, chi-square p = 0.046.

**After:**
> Seven-day adherence was 71% with adaptive reminders (n = 58) and 54% with the standard schedule
> (n = 60), a difference of 17 percentage points (95% CI 0.4 to 33.6; p = 0.046).

**Report:**
- *Evidence-block additions (author must confirm):* every number comes from the supplied block, which
  the report quotes so the author can confirm it belongs in the manuscript. "Robust" was dropped
  because the block contains no robustness analysis.

---

## 7. A limitation and a sample-size inconsistency

**Before:**
> Of the 240 participants, 130 identified as female and 120 identified as male. Because the sample was
> drawn from four schools in one region, and because screen time was self-reported, these results may
> not generalize to other populations.

**After:** the first sentence is unchanged. The second becomes:
> Because the sample came from four schools in one region and screen time was self-reported, these
> results may not generalize to other populations.

**Report:**
- *Unresolved issue:* 130 + 120 = 250, but N = 240. Neither number was changed. Correct the counts or
  report the remaining category.

"May not generalize" stays. **Wrong fix:** quietly changing 130 to 120.

---

## 8. A legitimate em-dash and a legitimate "demonstrate"

**Before:**
> One participant said: "I'd put the phone down — then pick it right back up." We prove that the
> adherence estimator is unbiased under missingness completely at random (Theorem 1).

**After:** unchanged. The em-dash is inside a verbatim quotation, and "prove" describes a formal
theorem, where it is the correct verb.

---

## 9. Funding-proposal mode: an NIH Specific Aims opening

**Before:**
> Early detection of sepsis is a very important and timely problem with many applications. In this
> proposal we will explore whether machine learning might possibly help. Aim 1: apply our model to ICU
> data. Aim 2: extend Aim 1 to multi-site data. This work will be groundbreaking.

**User-supplied record:**
> Preliminary: single-site retrospective model (2 ICUs, 4,100 admissions) flagged sepsis a median 3.1 h
> before the qSOFA alert at a matched false-alarm rate (Fig. 1). Partner: one additional hospital has
> agreed to share data (letter attached).

**After (prose edits applied):**
> Sepsis is treatable when caught early. In our single-site preliminary study (2 ICUs, 4,100
> admissions), a retrospective model flagged sepsis a median 3.1 hours before the qSOFA alert at a
> matched false-alarm rate (Fig. 1). In this proposal we will explore whether machine learning might
> possibly help.
> Aim 1: apply our model to ICU data.
> Aim 2: extend Aim 1 to multi-site data.

**Report:**
- *Prose edits:* removed "very important and timely … many applications" and "groundbreaking".
- *Evidence-block additions (author must confirm):* the preliminary-result sentence. Every figure in it
  is quoted from the supplied record.
- *Substantive proposals (not applied):*
  - The objective is over-hedged for an Aims page. A suggested rewrite: "This proposal will test
    whether that lead time holds across hospitals." Removing "might possibly" changes the commitment,
    so the author decides.
  - Aims are method-shaped. A suggested rewrite: "Aim 1: Determine whether the lead time holds at
    matched false-alarm rates on retrospective data from the partner hospital."
  - Aim 2 depends on Aim 1. Consider making the aims independent, or state a fallback.
  - The partner letter could be cited on this page as feasibility evidence.
- *Unresolved issue:* there is no central hypothesis. The author needs to state one; this edit does not
  write it.

The aims and objective are left as written because rewording them changes what the proposal promises. Nothing
here beyond the supplied record is added: no extra partners, figures, prior awards, or letters.
