---
status: proof-route-hold
openness: unverified
difficulty: uncertain
importance: uncertain
tags: []
last-literature-check: null
---

# Research question — replace before running

This is a template, not a vetted open problem. Create one stable problem record
in the independent research repository. The website keeps only its question brief
and solution metadata, using `website/templates/question-record.json`.
Replace the metadata with evidence-based values, adjust relative links for the
new location, and keep the board row synchronized. Reuse the record on later
searches; append dated findings below rather than creating a combined dossier.
Write in English and follow [screening-method.md](screening-method.md). Include decisive evidence in the
campaign question rather than relying only on mutable working notes.

## Exact question and acceptance target

- Primary origin: explicit published question or precisely inferred gap:
- Mathematical objects, definitions, complete domain, and hypotheses:
- Fully quantified statement to prove or settle:
- Does a disproof qualify? What exact negative result would count?
- Required deterministic construction or algorithm, if applicable:
- Worst-case time, representation, and encoding bounds:
- Source and target problems (I, S), encodings and no-solution semantics:
- Forward map F and target legality to prove:
- Output sets S_A/S_B and recovery G: prove G(x,y) ∈ S_A(x) for every y ∈ S_B(F(x)):
- Valid output restrictions, totality, and composition obligations:
- New complexity-theoretic contribution beyond applicable known reductions:

## Known results and remaining gap

| Primary result | Exact hypotheses | Conclusion/bounds | Why it does not settle the target |
|---|---|---|---|
| | | | |

- Strongest applicable positive and negative results:
- General theorem or composition consequences checked:
- Exact gap and mathematical significance of resolving it:
- Weakest result meeting acceptance; partial results that would not suffice:

## Openness evidence

| Search date and query | Primary URL and version | Theorem/page | Effect on target |
|---|---|---|---|
| | | | |

- Equivalent formulations and synonymous statements checked:
- Historical progress, latest versions, and follow-ups checked:
- Failed approaches and applicable lower bounds:
- Evidence of present openness; unavailable sources and coverage limits:

## Proof route and initial investigation

- Existing lemmas or constructions to build on:
- Focused missing argument and proposed mechanism:
- Failure modes; observations that would refute the approach:
- Bounded experiment or proof exercise, tools, and time/compute budget:
- Executed commands, actual results, and counterexamples:
- What those results establish and what they do not:
- Remaining route to a general proof and independent checking plan:

## Difficulty, importance, and reporting summary

Use the [reporting criteria](screening-method.md#reporting-difficulty-and-importance).
Use not assessed if an earlier screening gate blocked assessment.

| Dimension | Assessment | Evidence and uncertainty |
|---|---|---|
| Difficulty | low / moderate / high / uncertain | Hardest missing step; executed probe; failed routes; limits of the estimate |
| Importance | limited / moderate / high / uncertain | Exact new theorem consequence; breadth; difference from known results |

- Why the difficulty and importance judgments support the proposed priority:
- Overlap with other candidates and the distinct contribution of this target:
- Next bounded proof exercise and what its result would change:

## Screening decision

Enter `pass`, `hold`, or `reject` with evidence. Stop at the first blocking
gate and mark later gates `not assessed`.

| Gate | Result | Evidence and reason |
|---|---|---|
| 1. Precise mathematical question | | |
| 2. Applicable known results | | |
| 3. Supported openness | | |
| 4. Mathematical significance | | |
| 5. Plausible proof route | | |
| 6. Bounded initial investigation | | |

Overall decision and first blocking gate:

## Research history

- Date, actual queries and coverage limits, findings, failed routes and status changes:
- Related problems, proof artifacts and reproducible checks:

## Campaign contract

- Fixed statement and qualifying positive/negative outcomes:
- Allowed approaches, tools, resource budget, and stopping conditions:
- Required general proof and applicable construction/extraction bounds:
- Independent verification obligations and literature recheck:
- Record partial progress honestly; a different theorem needs a new campaign.

The target must be a deterministic polynomial-time reduction under [the shared contract](reduction.md).
Each rule includes forward instance construction and a deterministic polynomial-time
backward map from any valid target output to a valid source output. For exact
optimization, validity includes global optimality; for decisions, decode both answers. Specify both
algorithms, their premises and resource bounds, and the injected-instance test loop.
New endpoints are allowed. Library compatibility and immediate integration value
are not mathematical screening gates.
Actual production integration requires a mature result and separate authorization.
