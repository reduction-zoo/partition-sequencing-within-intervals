# Round 001 — mechanism A, corrected enforcer window

Status: plan recorded before the first discriminating check ran.

## Plan

- **Gap.** No correct executable rule exists. The previous upstream
  implementation was removed as unsound: with the enforcer released at
  `floor(B/2)`, odd totals leave the enforcer schedulable, so NO instances of
  Partition become feasible in the target (issue #1006 audit comment: 28 of
  about 40 NO instances, seed 42).
- **Mechanism (A).** Keep one task per element with window `[0, B+1]` and length
  `s_i`, and release the unit-length enforcer at `r = ceil(B/2)` with deadline
  `d = ceil((B+1)/2)`. For even `B` this pins the enforcer to `[B/2, B/2+1)`; for
  odd `B` it gives `r = d`, so the enforcer is unschedulable and the target is
  infeasible. Recovery returns the element tasks scheduled before the enforcer.
- **Relevant prior evidence.** The removed implementation and its root cause
  (issue #1006, PR #1052) are recorded in `question.md`. Experience search: the
  campaign's `research/experience/` holds only its README, and the board's local
  collection
  (`/Users/xiweipan/Codes/autoresearch-gadgets/research/experience/entries/`)
  holds no entries yet, so no prior finding applies; there is no match to record
  rather than a match that was ignored.
- **First discriminating check.**
  `uv run --locked python campaigns/partition-sequencing-within-intervals/work/check.py --candidate campaigns/partition-sequencing-within-intervals/work/algorithm.py`
  over the 16 injected cases: each case runs the forward map, solves the
  constructed target independently (subset DP and CP-SAT), feeds up to eight
  distinct valid target outputs per case to recovery, and validates the recovered
  source output against independent ground truth. The odd-total cases are the
  discriminating ones: a feasible schedule for an odd-total constructed instance
  refutes mechanism A outright.
- **What each outcome would establish.** Passing every case means the rule
  survives the prepared finite suite; it does not establish the general theorem.
  A counterexample refutes mechanism A and moves the campaign to mechanism B
  (`question.md`) or to a different horizon gadget, with the counterexample kept
  as a regression case.

## Evidence

Command, run from the repository root with the candidate at its committed
revision:

```sh
uv run --locked python campaigns/partition-sequencing-within-intervals/work/check.py \
  --candidate campaigns/partition-sequencing-within-intervals/work/algorithm.py
```

Retained output: `candidate-suite.txt` in this directory. Result:
**CANDIDATE SUITE PASSED** — 16 source instances, 59 distinct valid target
outputs fed through recovery, every recovered source output valid against
independent ground truth. CP-SAT and the subset dynamic program agreed on every
constructed target.

The discriminating cases behaved as Lemma 2 predicts. The three odd-total
instances (`odd-total-no` with `B = 3`, `all-equal-odd-no` with `B = 9`,
`odd-total-no-small` with `B = 7`) produced infeasible targets, and the four
even-total instances without a witness (`single-element-no` with `B = 4`,
`even-total-no` with `B = 6`, `even-total-no-gap` with `B = 8`,
`even-total-no-duplicates` with `B = 18`) also produced infeasible targets, so
no NO instance leaked a feasible schedule — the failure the removed
implementation exhibited. `textbook-even-yes`
(`[3,1,2,4]`, `B = 10`) tested eight distinct schedules, including schedules
whose task order differs from the one the construction suggests, and recovery
returned `{3,2}` or `{1,4}` as appropriate. `eight-ones-yes` exercised the
nine-task target above the permutation limit and still produced eight distinct
valid schedules.

## Diagnosis

Mechanism A survived the prepared finite suite; no counterexample, oracle defect
or execution failure appeared. The failure mode of the removed upstream
implementation is not reproducible here: releasing the enforcer at
`ceil(B/2)` rather than `floor(B/2)` makes `r = d` exactly on odd totals, so the
target is infeasible there. This is finite evidence about one implementation, not
the general theorem; the general argument is `work/proof.md` and still needs
independent verification and review.

Experience extraction: the campaign's `research/experience/` holds only its
README, and the board's local collection has no entries, so no prior finding
applied and none was bypassed. **None** created or updated: the odd-total
enforcer condition is specific to this gadget and is already recorded in
`question.md` as the failure mechanism, and the cross-question admission rules
are still undecided.

## Next action

Verify: implement an independent second checker (`work/verify.py`) that does not
import `check.py` or `algorithm.py`, covering alternate valid target outputs,
degenerate inputs and the NO correspondence, then record `work/verification.md`.
Request independent review once verification passes and no proof obligation is
left unstated.
