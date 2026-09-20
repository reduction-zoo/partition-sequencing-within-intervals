---
name: research-review
description: Independently review a complete reduction rule as a registered harness subagent and return evidence to the main researcher.
---

# Research Review

Assess the actual candidate theorem for correctness, novelty and significance
after executable verification. Form your own judgment from the evidence in an
independent reviewer context; do not repeat preparation or candidate development.

Read the shared [reduction contract](../../../research/reduction.md): problems
are (I, S), and the rule is (F, G) with recovery from every valid target output.

## Inputs and boundary

Read the fixed question, algorithm.py, proof.md, preparation.md and verification.md.
Write only in the assigned review directory. Do not modify the candidate,
testing machinery or their reports. Do not spawn agents. Agent confidence
and agreement are not evidence of correctness. Do not change acceptance criteria.

This review runs from a harness registration
([harness contract](../../../harness/README.md#reviewer-registration)) that fixes
what it may touch. Record in `review.md` the mechanisms actually in force — tool
denial, depth cap, sandbox, or only these instructions — together with the model
route used. A different model than the proposer's is not by itself independence,
and an enforced boundary is not evidence for any judgment below.

## Deliverable

Write `review.md` with an explicit advance, revise or stop decision and separate judgments:

- Correctness: audit legal target construction for every legal source input,
  nonempty valid-output semantics, gadget composition, and recovery membership
  in S_A(x) for every y in S_B(F(x)). For optimization check global optimality,
  for decisions check both answers, and for search include no-solution behavior.
  Audit deterministic
  execution, runtime and encoding bit size of both forward and backward maps.
  Check the implemented recovery as well as its proof; a candidate that only
  maps instances is incomplete. Review construction and recovery as one rule,
  including the full injected-instance test loop.
  Identify the exact current file location, inference and missing premise for each
  proof gap. Confirm quotations against the current file. Write targeted independent
  checks when needed; do not rerun all suites merely to repeat passing evidence.
- Novelty: check primary literature against the theorem actually proved, including
  equivalent formulations and consequences of existing results. Record URLs,
  theorem locations, search date and unresolved coverage. Initial topic screening
  does not settle novelty of the final construction.
- Significance: explain the concrete contribution relative to the closest known
  results and the fixed acceptance criteria. Separate openness from importance.

For a follow-up review, read the previous findings and repair record, assess the
changed argument and its consequences, and reuse unaffected evidence. Return
concrete findings to the main conversation without directing a full restart.

When the candidate relies on a shared experience entry, inspect its supporting
argument and check that its premises hold here. Report unsupported generalizations
or contradictions in review.md; do not edit the shared entry. A prior success,
retrieval match or helpfulness report is not a proof of this application.

## Decision

Advance only when all three judgments are supported. Finite tests cannot substitute
for a general proof; incomplete literature coverage must remain explicit and cannot
be treated as confirmation. Revise for repairable gaps, stating the affected
artifact, required correction and evidence needed. Stop for a known result or one
that fails the fixed significance criteria. Approval means eligible for expert
review, never publication acceptance.
