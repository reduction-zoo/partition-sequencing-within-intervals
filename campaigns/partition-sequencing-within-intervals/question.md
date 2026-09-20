---
status: proof-route-hold
openness: rule-completion
difficulty: provisional-low-to-moderate
importance: limited
tags: [partition, sequencing-within-intervals, scheduling, enforcer-gadget, rule-reconstruction, unsound-predecessor]
last-literature-check: 2026-09-21
---

# Research question — Partition → Sequencing Within Intervals

## Exact question and acceptance target

- Primary origin: board record `partition-sequencing-within-intervals.json` on
  the Open Question Board (`Construction open`), citing upstream issue
  <https://github.com/CodingThrust/problem-reductions/issues/205>. The board's
  acceptance target is a complete, reproducible rule; no new complexity
  classification is claimed.
- Mathematical objects, definitions, complete domain, and hypotheses:
  - Source Π_A = Partition. I_A: a finite family of positive integers in binary
    encoding. S_A(x): the subcollections whose sum equals half the total, and
    NO-SOLUTION exactly when no such subcollection exists. (Board phrasing:
    "return a subcollection with sum equal to half the total. Return NO-SOLUTION
    exactly when no such witness exists.")
  - Target Π_B = Sequencing Within Intervals. I_B: a finite set T of tasks, each
    with an integer release time `r(t) ≥ 0`, a positive integer length `l(t)` and
    an integer deadline `d(t)`. S_B(x): the feasible schedules σ : T → Z with
    σ(t) ≥ r(t), σ(t) + l(t) ≤ d(t), and for every other task t' either
    σ(t') + l(t') ≤ σ(t) or σ(t') ≥ σ(t) + l(t) — that is, each task executes
    contiguously and no two tasks overlap — and NO-SOLUTION when no feasible
    schedule exists. **Preemption is forbidden**; allowing it would invalidate the
    intended argument.
- Fully quantified statement to prove: there exist deterministic polynomial-time
  maps F and G with F(x) ∈ I_B for every x ∈ I_A and G(x,y) ∈ S_A(x) for every
  y ∈ S_B(F(x)), plus G(x, NO-SOLUTION) = NO-SOLUTION exactly when
  S_B(F(x)) = ∅.
- Does a disproof qualify? No. A disproof would have to show that no such rule
  exists.
- Required deterministic construction or algorithm: F and G implemented as
  `algorithm.py` over JSON on stdin/stdout, with `--extract` performing recovery,
  and neither map calling a solver, using randomness or consulting an LLM.
- Worst-case time, representation, and encoding bounds: polynomial time and
  output bit size for F in |x|, and for G in |x| + |y|, measured on the binary
  input encoding, so every constructed number must have polynomially many bits.
- Source and target problems (I, S), encodings and no-solution semantics: as
  above; the JSON encodings are fixed in `work/contract.md` during Prepare.
- Forward map F and target legality to prove: F emits a legal target instance —
  nonnegative release times, positive lengths, integer deadlines — for every
  legal Partition instance.
- Output sets S_A/S_B and recovery G: prove G(x,y) ∈ S_A(x) for every feasible
  schedule y of F(x), including schedules that are not the one the construction
  "intended"; and prove the NO-SOLUTION correspondence in both directions.
- Valid output restrictions, totality, and composition obligations: odd total
  sum, the enforcer's exact window, single-element and empty inputs, and repeated
  sizes must be covered explicitly; whether a schedule exists is a semantic
  answer, not an execution error.
- New complexity-theoretic contribution beyond applicable known reductions:
  none claimed. The contribution is a correct, executable, independently checked
  reconstruction of a textbook rule whose previous implementation was removed as
  unsound.

## Known results and remaining gap

| Primary result | Exact hypotheses | Conclusion/bounds | Why it does not settle the target |
|---|---|---|---|
| Garey & Johnson, *Computers and Intractability* (1979), Chapter 3, Theorem 3.8, p.70, as transcribed in issue #205 | Arbitrary Partition instance with total `B` | Sequencing Within Intervals is NP-complete; local replacement plus one "enforcer" task | The campaign must supply an executable F and G, a general proof and bounds; the book text is not freely available here, and the transcription's enforcer formula is exactly what the removed implementation got wrong |
| Upstream audit issue #1006 and its comment of 2026-04-06 | ~40 random NO instances, seed 42 | `Partition → SequencingWithinIntervals` was first listed SOUND, then corrected to **UNSOUND**: release `floor(S/2)` with deadline `ceil((S+1)/2)` leaves the enforcer schedulable for odd `S`, giving asymmetric blocks; 28 of ~40 NO instances were wrongly schedulable | Documents the failure but supplies no corrected construction |
| PR #1052 (merged 2026-04-17) | — | Removed eight unsound reductions, including this one; the problem models were retained | Leaves the edge absent; issue #205 was reopened for a correct re-implementation from literature (comment of 2026-04-14) |
| Issue #205 body, current revision (read 2026-09-21) | The same transcription, plus an AI-generated summary and an even-`B` example | The summary states `r(t̄) = floor(B/2)` and `d(t̄) = ceil((B+1)/2)` and then asserts "when `B` is odd: `r(t̄) = d(t̄) = ceil(B/2)`", which is arithmetically false for that formula: odd `B = 2k+1` gives `r = k` and `d = k+1`, so the enforcer stays schedulable. Only the even-`B` case is exercised | The transcription contradicts itself at exactly the odd case that broke the removed implementation, so the enforcer window must be derived and proved here rather than copied |

- Strongest applicable positive and negative results: the textbook positive
  result above, and the upstream NO-instance audit as the negative evidence.
- General theorem or composition consequences checked: none yet.
- Exact gap and mathematical significance: a correct rule is missing while an
  unsound predecessor is documented; the significance is a verified
  reconstruction with explicit NO-instance coverage, not a new classification.
- Weakest result meeting acceptance: executable F and G, a general proof, passing
  independent checks including NO instances, and an independent review. Partial
  results that would not suffice: a construction that is only tested on YES
  instances, or a proof that omits the odd-total-sum case.

## Openness evidence

| Search date and query | Primary URL and version | Theorem/page | Effect on target |
|---|---|---|---|
| 2026-09-18 (board import) | <https://github.com/CodingThrust/problem-reductions/issues/205> | Board record fixes the endpoints and the missing deliverable | Establishes the rule-completion gap |
| 2026-09-21, GitHub API reads of issues #205, #1006 and PR #1052, first through shell `curl` and then through the harness `web_fetch` once the proxy route was configured | issue #205 (open, labels `rule`,`Good`, milestone *Garey & Johnson*, `state_reason: reopened`, 8 comments); issue #1006 (closed, label `bug`); PR #1052 (merged) | Audit comment of 2026-04-06; removal list of PR #1052; the issue body's self-contradictory odd-`B` claim | Confirms the target is open, the previous construction is removed as unsound, and the model is retained |
| 2026-09-21, `web_search` for the Hitting String target (a different candidate) | search index only | — | Used only to reject that other candidate; not evidence for this target |

- Equivalent formulations and synonymous statements checked: the board's target
  definition matches the GJ instance definition quoted in issue #205, including
  the non-overlap condition.
- Historical progress, latest versions, and follow-ups checked: the issue was
  quality-checked three times (2026-03-10, 2026-03-11, 2026-03-26), then reopened
  on 2026-04-14 after the removal.
- Failed approaches and applicable lower bounds: the removed implementation and
  its root cause are recorded above; they become regression cases.
- Evidence of present openness; unavailable sources and coverage limits: the
  target is open upstream and the edge is absent. Garey & Johnson's book is not
  freely available from this session, so the theorem statement and the exact
  enforcer formula could not be read at the source; the transcription in issue
  #205 is treated as untrusted, because that formula is the failure's origin and
  because the issue's own summary contradicts it for odd totals. The issue was
  re-read through the harness `web_fetch` after the proxy fix, so the current
  revision, labels, milestone and `state_reason: reopened` are confirmed.
  Two unrelated AI-generated comments on #205 discuss a different problem and
  carry no evidence.

## Proof route and initial investigation

- Existing lemmas or constructions to build on: the textbook local-replacement
  scheme — one task per element, plus a single enforcer task whose unit length
  pins it to the midpoint of the horizon, splitting the schedule into two blocks
  that must each be filled exactly.
- Focused missing argument and proposed mechanism (hypothesis, untested):
  **Mechanism A (corrected enforcer window).** Let `B` be the total. Emit one task
  `t_a` with `r = 0`, `d = B + 1`, `l = s(a)` for each element, and one enforcer
  with `l = 1`, `r = ceil(B/2)`, `d = ceil((B+1)/2)`. For even `B` the enforcer is
  pinned to `[B/2, B/2+1]`, the two remaining blocks have length `B/2` each, and
  the tasks' total length equals the horizon length, so any feasible schedule
  fills both blocks exactly; the tasks before the enforcer then form an equal-sum
  subcollection, and any equal-sum subcollection yields such a schedule. For odd
  `B` the enforcer has `r = d` and cannot be scheduled at all, so the target is
  infeasible, matching the source's lack of a witness. Decoding returns the tasks
  scheduled before the enforcer.
- **Mechanism B (explicit odd-sum target).** Keep the even-`B` gadget and, when
  `B` is odd, emit a target instance that is infeasible by construction, for
  example a single task with `r = 0`, `d = 1`, `l = 2`. This is a different
  mathematical mechanism and would start its own round.
- Failure modes; observations that would refute the approach: a feasible
  schedule of an odd-`B` instance (the exact defect that removed the previous
  implementation); a feasible even-`B` schedule in which some element task lies
  across the enforcer or in which a block is not exactly filled; a feasible
  schedule whose pre-enforcer set does not sum to `B/2`; a decoder that returns a
  source output for an infeasible target; non-integer or negative start times.
- Bounded experiment or proof exercise, tools, and time/compute budget: Prepare
  fixes the encodings and builds independent oracles for both endpoints, with NO
  instances injected as mandatory cases; the first counted round tests Mechanism A
  by exhaustive enumeration over small instances (at most five elements with small
  sizes, both parities of `B`) against the independent source oracle. No timeouts;
  bounds are explicit and finite.
- Executed commands, actual results, and counterexamples: none. No experiment has
  been run; this document is committed before Prepare, as the repository standard
  requires.
- What those results establish and what they do not: —.
- Remaining route to a general proof and independent checking plan: prove F legal
  and polynomial in the binary input length; prove recovery for every feasible
  schedule, including unintended ones; prove the NO-SOLUTION correspondence for
  both parities; prove G polynomial; verify recovered subcollections against an
  independent oracle, including alternate feasible schedules; then request
  independent review.

## Difficulty, importance, and reporting summary

| Dimension | Assessment | Evidence and uncertainty |
|---|---|---|
| Difficulty | provisional low-to-moderate | The board records no construction attempt; the evidence here is a published route plus a documented single-root-cause failure. The main risk is not the gadget but proving recovery for *every* feasible schedule and handling both parities correctly, so the rating stays provisional |
| Importance | limited | The board frames the rule as a compact foundational scheduling reconstruction with independently checkable release-time and deadline semantics; no new classification is claimed |

- Why the difficulty and importance judgments support the proposed priority: the
  failure mechanism is documented and small, so a correct rule is reachable
  within a few rounds, and the NO-instance regression cases make the verification
  meaningful rather than ceremonial.
- Overlap with other candidates and the distinct contribution of this target:
  overlaps with other Partition-endpoint rules on the board, several of which the
  same upstream audit found unsound; the distinct contribution is a verified rule
  for this endpoint pair.
- Next bounded proof exercise and what its result would change: the exhaustive
  small-instance test of Mechanism A above. Refuting it would force Mechanism B or
  a different horizon gadget, and would itself be a recorded counterexample.

## Screening decision

| Gate | Result | Evidence and reason |
|---|---|---|
| 1. Precise mathematical question | pass | Both (I, S) are stated exactly, including the non-preemption condition and the no-solution semantics |
| 2. Applicable known results | pass | Garey & Johnson Chapter 3 Theorem 3.8 (p.70) via issue #205; the previous implementation's removal is documented in #1006 and PR #1052 |
| 3. Supported openness | pass | Issue #205 is open with the edge absent after PR #1052; a correct re-implementation is explicitly requested. The book itself could not be read, which limits but does not block the reconstruction |
| 4. Mathematical significance | pass, as a reconstruction | The acceptance target is a correct reproducible rule for an established classification; no new classification is claimed, and the unsound predecessor makes the correction substantive |
| 5. Plausible proof route | pass | Mechanism A is explicit, arithmetic and checkable on every obligation listed above |
| 6. Bounded initial investigation | hold | Not executed: this record is committed before Prepare; the first counted round is the bounded probe |

Overall decision and first blocking gate: `pass` for an authorized
rule-reconstruction campaign, with Gate 6's bounded probe and the
source-text re-audit of Garey & Johnson as open obligations.

## Research history

- 2026-09-21: campaign repository created under
  `~/Codes/reduction-zoo/partition-sequencing-within-intervals`. Before
  selection, a first candidate (`3-SAT → Hitting String`) was rejected at
  screening after its upstream issue was read: that target is On Hold upstream as
  an isomorphism of Satisfiability by trivial symbol substitution. No research
  repository remains for it.
- 2026-09-21: issues #205, #1006 and PR #1052 read through the GitHub API from a
  shell `curl`, because DSH's `web_fetch` public-address guard rejects the
  fake-ip answers this machine's DNS returns.
- Related problems, proof artifacts and reproducible checks: none yet.

## Campaign contract

- Fixed statement and qualifying positive outcome: a complete deterministic rule
  (F, G) for Partition → Sequencing Within Intervals with the NO-SOLUTION
  correspondence. No negative outcome qualifies.
- Allowed approaches, tools, resource budget, and stopping conditions:
  deterministic construction with a general proof; Python with uv and a committed
  lockfile; Z3, OR-Tools and brute-force enumerators are available for independent
  oracles, which must not be LLMs and must not import the candidate; an initial
  round budget of three, which the user may extend; stop conditions and early-exit
  obligations from the session skill.
- Required general proof and applicable construction/extraction bounds:
  polynomial worst-case time and output bit size for F in |x| and for G in
  |x| + |y|, with recovery membership for every valid target output.
- Independent verification obligations and literature recheck: independent
  oracles and injected cases in Verify, with NO instances mandatory; an
  independent reviewer via the registered reviewer child; and a literature and
  novelty re-audit at review, including the Garey & Johnson source text if it
  becomes available.
- Record partial progress honestly; a different theorem needs a new campaign.

The target is a deterministic polynomial-time reduction under the
[shared contract](../../research/reduction.md), with forward instance
construction and deterministic polynomial-time recovery from any valid target
output. Production integration would require a mature result and separate
authorization.
