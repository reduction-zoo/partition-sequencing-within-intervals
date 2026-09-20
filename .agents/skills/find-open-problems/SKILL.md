---
name: find-open-problems
description: Find or reassess open research targets for original reduction algorithms, and maintain their problem catalog records.
---

# Find open problems

Deliver evidence-backed questions whose positive results would be original
deterministic polynomial-time reduction algorithms. Keep
openness, proof feasibility, mathematical importance, and proved results distinct.
Implementing known reductions and optimizing current library overhead are outside
this selection task.

Read the shared [reduction contract](../../../research/reduction.md): problems
are (I, S), and the rule is (F, G) with recovery from every valid target output.

## Use the repository records

Read the repository [README](../../../README.md) for the research contract.
Use these resources where the task needs them:

- **Finding or revisiting questions:** search the [problem catalog](../../../README.md)
  by endpoints, restrictions, and aliases; read matching cards before creating one.
  In the website repository, published question records live in `website/questions/`.
- **Making a screening decision:** apply the six gates in the
  [screening method](../../../research/screening-method.md), their canonical definition.
- **Recording a literature-screened question:** use the board's
  `website/templates/question-record.json` and `edit-question-website`.
- **Starting a proof attempt or experiment:** follow the
  [repository boundary](../../../research/repository.md#selection-and-research-boundary),
  then use the [campaign question template](../../../research/question.md).

For a proposed proof route, search [research experience](../../../research/experience/README.md)
by structure and assumptions. Check the evidence and applicability of relevant
entries, and record how they support or exclude that route in the problem card.
Experiential heuristics do not establish openness or impossibility. Do not repeat
an excluded construction without identifying a premise that changes.

Take scope and candidate count from the user's current request and established
preferences. Proceed with a stated provisional focus when missing details do not
block useful work. A broad inventory may contain holds; an admitted shortlist
contains only all-pass candidates under ordinary selection. For an authorized
exploratory campaign, use the screening method's
[admission criteria](../../../research/screening-method.md#exploratory-admission):
route readiness may remain unresolved while a campaign investigates it.
Report those counts separately, and return
fewer admitted candidates when the evidence does not support the requested count.

## Establish the mathematical target

Fix Π_A = (I_A, S_A) and Π_B = (I_B, S_B), their input/output encodings,
restrictions and no-solution behavior. Seek explicit deterministic polynomial-time
F and G satisfying the shared contract, with worst-case bit bounds. Decision,
search and exact optimization targets are eligible without converting everything
to a threshold decision problem. Specify a plausible construction and recovery
route for handoff. The research contribution must lie in the reduction, not just
in wrapping a solver or implementing a known generic encoding.
New endpoint problems are allowed; current library APIs do not determine eligibility.
A known generic encoding can satisfy the reduction definition while failing novelty.
Structural lemmas qualify as support for a fixed reduction target.

## Investigate the unresolved claim

Use Web and arXiv by default, with Hugging Face paper search where relevant.
Start from primary-literature open questions or precise theorem gaps. Check
synonymous and equivalent formulations, historical progress, later versions,
follow-ups, and failed approaches. Inspect proofs and compositions when existing
theorems may imply the target.

Record actual queries, search dates, primary URLs and versions, theorem/page
locations, and matching or mismatching hypotheses. Explain what supports present
openness and what remains outside the search coverage, including inaccessible
sources and unavailable tools. An empty search or an
unimplemented library rule does not establish openness. Recheck dated claims;
withdrawn lists are search leads, not accepted evidence.

Apply the screening gates in order. At a rejection, retain the decisive evidence
and move on. At a hold, name the missing evidence and leave later gates unassessed.
Direct further investigation toward candidates with a viable remaining route.

For a candidate reaching the proof-route gates, identify usable lemmas, the
hardest missing step, and a mechanism to test. A literature-only selection request
can end here with an explicitly untested route; Gate 6 is not a prerequisite for
a question to appear on the board. When initial investigation is in scope, first
establish the independent repository, fixed question and initial Git commit under
the repository standard. Use Research Session for Prepare and counted attempts,
with finite family or candidate limits and no execution timeouts. Use the supplied
round budget or disclose the session default. Record the mechanism, results, counterexamples, and remaining
obligations. Finite success does not prove the theorem; bounded synthesis failure
excludes only the tested construction family. Follow Gate 6 before admission.

## Maintain the board

Keep literature-based question briefs in `website/questions/<slug>.json`, using
`edit-question-website` and the existing template. A separate repository is
needed only when actual research begins. Keep one record per fixed question and
update its references, dated coverage and assessments as evidence changes.

Once research begins, store proof attempts, experiments, counterexamples and
round records in the independent repository. Preserve rejected approaches there.
Update the board with supported assessments and solution metadata; keep its
schema and presentation unchanged. Screening holds and rejected leads may be
reported to the user without creating website entries or new archival folders.

## Report the decision

Lead with the admitted count, holds, and decisive findings. For multiple candidates,
use a comparison table in the user-facing response:

| Reduction target A → B | Openness evidence / date | Difficulty and reason | Importance and consequence | Status / priority |
|---|---|---|---|---|

Apply the method's [reporting criteria](../../../research/screening-method.md#reporting-difficulty-and-importance).
Difficulty is low/moderate/high/uncertain; importance is limited/moderate/high/uncertain.
Use not assessed when screening stopped before that judgment. Give a concrete
reason and uncertainty for each rating. Moderate difficulty needs evidence from
an investigated route. Importance needs an exact new theorem consequence beyond
known results. Keep both dimensions visible even in a single-candidate summary.

Each retained card must explain the hardest missing step, the available evidence
and its limits, and the consequence of success. Identify unexecuted investigations
as such. State the decision first, then
its evidence. Keep each paragraph on one question or judgment; define terms where
needed and cite sources beside the claims they support. Cut repeated explanations
and split overloaded sentences without changing mathematical qualifiers,
definitions, or certainty. Use prose to explain the comparison, not repeat its cells.

End with a priority rationale and the next bounded proof task. Account for overlap
between related questions; do not imply independent papers or hide the tradeoff
between difficulty and importance behind a total score. If none qualify, say so.

Selection is complete when records and index agree, assessments expose their
evidence and limits, and the handoff names a concrete next step. If solving was
also requested, continue through the repository's campaign workflow with a fixed
statement and acceptance criteria. A changed theorem needs a new campaign.
This skill does not authorize production integration, external issue creation,
or additional agents.
