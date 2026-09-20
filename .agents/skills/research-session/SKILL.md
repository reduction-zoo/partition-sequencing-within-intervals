---
name: research-session
description: Start or resume a reduction research campaign with a round budget, executable tests, and independent review.
---

# Research Session

Develop an original deterministic reduction for one fixed question. Own the work
in one persistent harness session, from testing foundations to a reviewed proof
and paper, or an evidence-backed stopping decision. Use the harness's native
session and subagent tools; stage changes do not create new sessions or require
new permission. Continue within the authorized scope and round budget until a
completion or stop condition below applies.

## Establish the campaign

For a new campaign, read the [repository standard](../../../research/repository.md)
and establish the independent local Git repository and initial question/state
commit before Prepare, experiments or proof attempts, including screening probes. Carry the skills, their assets, shared
`research/` specifications and the reviewer registration for this harness
([harness contract](../../../harness/README.md)) into that repository with
relative paths intact. The board repository retains only the question brief and
result metadata. The repository standard defines destination selection and what
to commit.

Before the first round, run a capability probe over everything the authorized
scope may reach and record it in `state.md`: Python and uv, the oracle solver,
Typst, Lean with Mathlib and Lake, and the external writing skill, each with its
actual version, provider or path, status, and the probe date. A capability that
is absent is recorded as pending and blocks only the stage that needs it; when the
environment changes mid-campaign, re-probe and record the delta instead of
relying on the earlier entry.

For a resumed campaign, read its README, local instructions, fixed question,
`state.md`, latest relevant review and evidence. Inspect Git status and the last
command outcome before repeating interrupted work. Check the capability probe and
re-probe anything it marks pending or that the environment may have changed since.
Continue the existing round count and testing foundation. Read other material when
an obligation needs it.

Read the shared [reduction contract](../../../research/reduction.md). The rule
contains F and G: legal forward construction and recovery of a valid source
output from every valid target output. Keep the question and acceptance criteria
fixed; a different theorem requires a new campaign.

## Work in the same conversation

Load a stage skill when its responsibility is needed:

| Responsibility | Skill and completion evidence |
|---|---|
| Testing foundation | [Prepare](../research-prepare/SKILL.md): independent oracles, encodings, injected cases and passing self-tests, committed before candidate construction |
| Construction and proof | [Propose](../research-propose/SKILL.md): executable F and G, general proof and worst-case time/encoding bounds |
| Executable verification | [Verify](../research-verify/SKILL.md): solve actual target instances independently and test recovered source outputs, including alternate valid target outputs |
| Independent assessment | [Review](../research-review/SKILL.md): separate correctness, novelty and significance judgments |
| Manuscript | [Write](../research-write/SKILL.md): reviewed Typst paper, figures where explanatory, reproducible commands and inspected PDF |
| Formal proof, when requested | [Formalize](../research-formalize/SKILL.md): explicit Lean statements, certificate checks and scoped verification claims |

A failure returns to the responsible work. Diagnose candidate defects, oracle
defects, proof gaps and execution failures separately. Record the reproducer,
expected/actual behavior and affected conclusions. Repair the cause and rerun
relevant checks; reuse unaffected results. Change an oracle expectation only
with a justification from the fixed definitions and an updated oracle self-test.
An algorithm defect does not require rebuilding the testing foundation.

After changing either map, run the prepared candidate suite and additional
verification before review. Proof-only changes require proof review; editorial
changes require compilation and inspection of affected pages. Preserve the
commands, inputs and candidate revision supporting reused evidence. Use finite
instance or search-family bounds, without solver, subprocess or campaign timeouts.
A harness-imposed limit that kills a run — a tool timeout, a stopped background
job, a closed session — is an execution failure: commit the partial state, record
it as an execution failure, and do not read it as an oracle answer or an
exhausted search family.

## Artifact ownership

The [repository standard](../../../research/repository.md#directory-ownership)
owns the directory layout and Git policy. Within `campaigns/<slug>/`:

- `question.md` fixes the target; `state.md` links the current claim, obligations,
  capability probe, round table, budget, checks, review and next action. The
  capability probe is a dated list of tool, version, provider or path, and
  status. The round table keeps one
  row per round with fixed columns — round id, the mechanism or standalone
  literature scope attempted, its first discriminating check, the outcome
  (supported, refuted, inconclusive or execution failure), and a link to
  `rounds/NNN/round.md` — so the authorized budget, the rounds used and the
  distinct mechanisms can be counted independently.
- `work/` holds the current contract, cases, checkers, algorithm, proof and paper.
  Each stage skill defines its deliverables.
- `rounds/NNN/round.md` records Plan / Evidence and diagnosis / Next action.
  Keep that round's experiment scripts, retained outputs and counterexamples
  alongside it; link implementation commits instead of copying whole workspaces.
- `work/evidence/<check-name>/` holds checks outside an exploratory round;
  `reviews/<review-name>/` holds each independent review and its checks.
- `formal/` holds formal proof sources and `formal/evidence/<check-name>/`.

Reusable findings live at repository-level `research/experience/`. The board
repository additionally keeps a local, uncommitted cross-question collection at
`research/experience/entries/`: read it in place, do not copy it into a campaign,
and treat presence there as no evidence
([experience format](../../../research/experience/README.md#local-shared-collection)).
Link detailed evidence from state and stage summaries rather than retelling it.
Preserve failed runs before repairs. For reproducible bulk outputs, follow the
repository standard's retention rules; keep unique observations and counterexamples.

## Research rounds and topic budget

Use the user's round allocation; if none is provided, disclose an initial budget
of three rounds. A round starts when committing to a construction hypothesis,
proof strategy or standalone literature investigation. Record its scope and first
discriminating check before executing it. A new mathematical mechanism or expanded
search family starts another round. Failed and abandoned attempts count.

Preparation, routine implementation/oracle repairs, editorial work and supporting
lookups stay with the work they serve. They do not consume artificial rounds.
An interrupted attempt resumes with its original scope and ID. A substantive
proof repair in review starts a round; correcting a transcription error does not.

At closure, record what was attempted, actual instance/solver/recovery counts,
evidence, diagnosis, remaining obligations and next decision. Record usage only
when measured. Complete experience extraction below, update `state.md` and commit.
Do not invent or retrospectively merge rounds. Label reconstructed records.
Round counts and independent mechanism counts must be reported separately. Each
round row names the mechanism attempted and the change that makes it a new round
rather than a repeat; closeout reports the authorized budget, the rounds used and
the distinct mechanisms read from that table.

Stop new discovery at budget exhaustion. A complete candidate may finish its
current checks, review and writing without an extra round if no new construction
or proof strategy is needed. Additional allocation extends the existing count.
A harness continuation budget, such as a DSH goal round limit, is a guardrail on
automatic continuation and not the research round count; report the two
separately and keep this table authoritative.

## Choose the next step

Choose the action that addresses the current uncertainty; these are options,
not a required sequence:

- **Continue:** develop or test the next unresolved construction or proof claim.
- **Investigate:** diagnose a failure or answer a focused literature question.
  Use Web and arXiv by default; record primary sources, theorem locations,
  search date, coverage gaps and what changes the decision.
- **Reconsider:** change the assumption or mechanism implicated by the evidence,
  preserving unaffected work. Parameter or seed changes alone are not new ideas.
- **Stop:** apply the budget and early-exit conditions below.

In the round plan, name the gap, proposed mechanism, relevant prior evidence,
first check and what its possible outcomes would establish. Search applicable
experience first. Prefer a check that changes a research decision to repeated
variations of an excluded approach. Reproducing a known result is evidence, not
discovery. Supporting lookups stay in the current round; a standalone literature
attempt declares a finite search scope and counts as a round.

## Learn from rounds

Use [research experience](../../../research/experience/README.md) for entry format,
retrieval and extraction. Before a round, search by mathematical structure and
assumptions; record which findings apply and why, or that no relevant match exists.

At closure, distinguish observation, supported or suspected cause, and consequence.
A failed test does not itself identify a cause; bounded UNSAT excludes only the
specified family. Add confirmed counterexamples to applicable regression tests.
Record **Experience extraction:** links to entries created/updated, or **none**
with a concrete reason. Save qualifying findings before starting the next round.
The check is required; a new entry per round is not.

At campaign closeout, check for missed findings, preserve contradictory evidence,
and report counts of distinct entries created, updated and pending with links.
Label retrospective extraction with its actual date. An entry's existence or use
is not evidence of improved discovery.

## Justify early exit

Before stopping for lack of progress while budget remains, retain an actual
construction or proof attempt, the failed assumption and what the evidence
excludes. Attempt a materially different mechanism or establish an obstruction.
If none can be formulated, investigate relevant adjacent literature and explain
why its mechanisms do not supply a testable next step. One failed gadget or a low
subjective success estimate alone is insufficient. Do not pad rounds with repeats.

Earlier stopping is appropriate for user instruction, exhausted budget, a concrete
external blocker, a completed result, or decisive evidence that the target fails
eligibility. Distinguish an incomplete investigation from an unpromising topic,
and an investment decision from an impossibility proof. For exploratory admission,
use the [screening criteria](../../../research/screening-method.md#exploratory-admission).
Record attempted mechanisms, partial results, remaining obligations and what new
evidence would justify resuming. Switch topics only within authorized scope.

## Independent review

When both maps, a candidate general proof and relevant passing checks exist,
spawn one independent reviewer whose charter is
[Research Review](../research-review/SKILL.md), using the reviewer registration
for this harness ([harness contract](../../../harness/README.md)). Supply the
fixed question, current artifact paths, a new review directory and any previous
findings with the repair summary. Use a fresh context: a spawned child, never a
fork of this conversation. Request an assessment without suggesting a verdict,
and keep the candidate unchanged during review.

The reviewer writes its own checks, without importing candidate implementations,
and cannot edit the candidate or spawn agents; the registration supplies whatever
the harness can enforce of that boundary, and a review records which mechanisms
were in force. Resolve concrete findings in the
main conversation. Request focused re-review after repairs; reuse unaffected
evidence. An advance review leads to writing. Material changes to the reviewed
construction or proof require renewed review. If independent review is unavailable,
report it as pending; self-review does not satisfy independent assessment.

## Recommend and report

Lead progress reports with the established result, remaining proof obligations,
main obstacle and recommended next action. Keep correctness, novelty and
significance separate. Describe prospects within the remaining budget as low,
medium, high or unknown, with evidence and explicitly uncalibrated judgment.
Keep earlier assessments so subsequent outcomes can be compared with them.

At handoff, include the repository path and latest commit, rounds used/remaining,
distinct mechanisms attempted, checks and their limits, experience counts and
links, and next action. Use actual evidence rather than a test-pass percentage
or an unsupported numerical probability of solving the problem.

## Completion and interruption

Use `ready_for_expert_review` only when executable F and G, their general proof,
relevant passing checks, an independent advance review and the compiled, visually
inspected Typst paper exist and agree. This status is an agent assessment, not
human certification. Track requested formal verification and pending independent
checks separately; completing the manuscript does not discharge them.

Use `stopped_without_discovery` for a supported stopping decision and record
partial results honestly. On interruption, commit the current state and resume
from it using the harness's session facilities. A missing tool blocks only the work that
requires it; report the missing capability and continue independent authorized
work. Creating a remote, publishing, updating the board or integrating a production
rule requires the corresponding authorization.
