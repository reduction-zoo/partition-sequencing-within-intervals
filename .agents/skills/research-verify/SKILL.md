---
name: research-verify
description: Test a candidate reduction by solving injected target instances independently and validating recovered source outputs.
---

# Research Verify

Test the complete reduction rule with separately implemented oracles and
seek counterexamples beyond the prepared cases. This work stays in the main
conversation; independent agent assessment belongs to research-review.

Read the shared [reduction contract](../../../research/reduction.md): problems
are (I, S), and the rule is (F, G) with recovery from every valid target output.

## Inputs and boundary

Read the fixed question, contract, prepared checker, candidate and proof. Check
the oracle against the problem definitions. Execute algorithm.py
as a subprocess; do not import it into any oracle or duplicate its reduction and
test only that duplicate. While verifying, preserve the candidate being tested.
For a defect, save evidence and switch to the responsible skill in this same
conversation to repair it; do not weaken the checker to make the candidate pass.

## Deliverables

Keep `verify.py` and `verification.md` in `work/`. Follow
[artifact ownership](../research-session/SKILL.md#artifact-ownership): raw runs
and reproducers belong in the current round or a named `work/evidence/` directory.
`verification.md` identifies the tested candidate, current coverage, limitations
and supporting run paths. It does not duplicate round diagnoses or prior logs.
The script accepts `--candidate PATH`.
Implement independent small-instance solvers and output checks without importing
check.py or algorithm.py. Test gadget composition, degenerate inputs and target
restrictions. Independently obtain valid outputs of the actual target instances,
run `algorithm.py --extract` with `source` and `target_solution`, and validate
membership of the recovered output in S_A(x). Exercise both Boolean outputs for
decisions, alternate witnesses and no-solution answers for search, and alternate
global optima for optimization. Verify optimality independently; do not compare
raw source/target outputs or objective values unless the theorem requires it.
Record output coverage separately from instance coverage.
Run the new checks. Reuse prepared test evidence when the candidate and prepared
tests are unchanged; otherwise run the affected prepared checks as well.

Save reproducing source instances, actual target outputs and expected/recovered source answers for
mismatches. For recovery failures, also save the target witness and recovered
source witness or extraction error. Distinguish invalid target encodings, candidate execution errors,
oracle defects and mathematical counterexamples. Record exact commands, outcomes,
seeds, finite coverage and untested domains. Inspect correspondence between the
implementation and stated construction; flag size-growth concerns for review.

## Completion and repair

Request independent review when the relevant prepared and additional checks have
passed and no known mismatch or checker defect remains. For a failure, save the
artifact, reproducer, expected and actual behavior, then repair the candidate or
test machinery in this conversation. Rerun affected checks and retain confirmed
counterexamples as regressions. A test failure does not create a new campaign.
General proof, novelty and significance judgments belong to review.
