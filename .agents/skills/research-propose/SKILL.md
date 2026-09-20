---
name: research-propose
description: Construct or repair a reduction and its solution-recovery algorithm, using prepared tests and a general proof.
---

# Research Propose

Construct an original deterministic polynomial-time reduction for the fixed
campaign question, delivering forward instance construction and backward witness
recovery as two parts of one rule. Use the prepared test harness throughout discovery.

Read the shared [reduction contract](../../../research/reduction.md): problems
are (I, S), and the rule is (F, G) with recovery from every valid target output.

## Inputs and boundary

Read `contract.md`, `preparation.md`, the question, and previous counterexamples
and reviews. Keep the prepared oracles, encodings and expected answers unchanged.
If testing machinery is wrong, preserve the reproducer, return to the prepare
responsibility in this conversation, and justify the repair from the problem
definitions. Never change tests to accommodate the candidate or weaken the question.

## One rule, two algorithms

Specify Π_A = (I_A, S_A) and Π_B = (I_B, S_B) using the shared contract.
Deliver F(x) in I_B and G(x,y) satisfying G(x,y) in S_A(x) for every legal x
and every y in S_B(F(x)). Construction and recovery are one rule.

For decisions, G decodes both YES and NO. For search, it handles any valid witness
and the specified no-solution answer. For optimization, it recovers an optimal
source solution from every optimal target solution, including ties; feasibility
alone does not suffice. Do not assume symmetry, canonical form, rationality or
optimality unless the target output contract supplies that premise. Prove any
normalization used by the decoder. No bijection or objective equality is required.

Prove polynomial runtime and encoding size for F in |x| and G in |x| + |y|.
G must decode the construction, not solve the source through exponential search
or an oracle. Reconstruct any metadata deterministically from x; both command
modes must work across fresh process invocations without hidden state.

## Deliverables and feedback

Follow the round definition and budget in
[Research Session](../research-session/SKILL.md#research-rounds-and-topic-budget).
Declare the current hypothesis and finite scope before experimentation. Close
the round with evidence, a cause analysis and the
[experience extraction decision](../research-session/SKILL.md#learn-from-rounds)
before changing the construction
family or proof strategy. Testing preparation and routine repairs remain reusable
across rounds; a round need not reach a complete candidate to count.
Use [Choose the next step](../research-session/SKILL.md#choose-the-next-step)
to continue, investigate, reconsider an earlier choice or stop as evidence warrants.

Before a local gadget search, sketch how its interface would participate in the
full construction and recovery, marking unresolved composition assumptions.
Check restrictive premises against the relevant known examples. Once a local
interface works, test its proposed composition before enlarging the local search
unless a specific remaining local defect justifies that work.

Keep the current `algorithm.py` and `proof.md` in `work/` under the
[artifact ownership rules](../research-session/SKILL.md#artifact-ownership).
Until a full candidate exists, keep local experiments in their round directories.
The proof must specify legal construction, recovery correctness for every valid
target output, gadget composition where applicable, and worst-case time
and output bit-size bounds for both maps. Implement both command modes in
`algorithm.py`: the default forward map and `--extract` for witness recovery, as
defined in the prepared contract. Neither algorithm may use runtime randomness
or LLM decisions. A proof of recoverability without executable recovery is incomplete.

As soon as a candidate can execute, run `python3 check.py --candidate algorithm.py`.
For each injected source instance, the harness runs the forward map, solves the
actual target independently, passes its valid output to the backward map, and
checks the recovered output against the source contract and independent ground
truth. For optimization, this includes global optimality; for decisions, both
YES and NO outputs go through recovery. The rule passes only when this full loop passes. Use concrete failures to revise the construction or recovery
and run the affected checks again. Record commands,
results, failed approaches, unresolved lemmas and useful constraints in the
current `round.md`, linking its raw evidence instead of duplicating it.
Preserve counterexamples for later attempts. A bounded synthesis failure excludes
only its stated construction family. Check new literature dependencies as they arise.

## Completion and repair

Continue to verification in the same conversation with executable forward and
backward maps and a candidate general proof. Preserve counterexamples before
repairing either algorithm or its proof. Do not restart the testing foundation
for a candidate defect. Request independent review only after the complete rule
passes the relevant checks and no acknowledged proof lemma remains unresolved.
Record a supported reason when abandoning the search. Tests do not establish proof.
