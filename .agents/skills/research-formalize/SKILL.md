---
name: research-formalize
description: Formalize an existing reduction proof or selected lemmas in Lean, audit its assumptions, and independently check certificates against the intended statements.
---

# Research Formalize

Turn an existing mathematical argument into a reproducible proof certificate.
Work in the persistent research conversation using Lean 4, Mathlib and Lake;
use Comparator for final statement matching and independent checking. Do not
build a runner, proof-search framework or session manager. Formalization does
not establish novelty, significance or correspondence to executable Python.

Read the shared [reduction contract](../../../research/reduction.md): problems
are (I, S), and the rule is (F, G) with recovery from every valid target output.

## Scope and statements

Read the campaign question, current proof, algorithm, witness contract and latest
review. Reuse any existing formalization. State the authorized target: selected
lemmas, the mathematical reduction, resource bounds, or implementation agreement.
A partial target is legitimate but cannot certify the entire result. Do not
restart discovery or expand to other campaigns without applicable authorization.

Write the intended definitions and theorem signatures before constructing proofs.
For reductions, preserve the source/target (I, S) definitions, legal construction
and recovery membership for all legal inputs and every valid encoded target
output. Preserve optimality and special-answer semantics where specified.
Check dimensions, number domains, quantifiers, degenerate cases and the meaning
of norms or other overloaded notation. Keep rational input encoding distinct
from real existential feasibility and from finite witness encoding.

Maintain a separate trusted challenge containing the intended statements and
their definitions. Its imports and build configuration are part of the trusted
boundary. Check these against the question, independently of whether a proof
compiles. Do not let proof repairs silently change the challenge, replace a
substantive claim with a hypothesis, or assume a convenient property of witnesses.
A necessary statement correction must be explained and checked against the fixed
question; a different theorem belongs to a different campaign. Comparator
matching does not establish that a human's intended problem was encoded correctly.
Avoid definition holes for the languages, feasibility predicates and resource model.

## Formalization loop

Choose a proof obligation that resolves the current mathematical risk. Reuse
Mathlib declarations after checking their actual hypotheses. Develop the lemma,
read Lean's feedback, and repair the proof or add the missing auxiliary lemma.
Prefer a completed general argument over many easy identities or bounded cases.

Classify unresolved work as a false statement or counterexample, missing premise,
mathematical proof gap, library gap, elaboration problem, or tool/environment
failure. A failed tactic does not refute a theorem. A numerical or solver check
may guide a repair but is not a formal proof unless its certificate is checked.
Never add an axiom or weaken a quantifier to close a goal.

Record the implicated obligation, diagnosis and next action in the campaign's
existing records. Reuse unaffected proofs and tests. A substantive mathematical
repair returns to propose/review; syntax repairs and formalization work alone do
not count as new discovery rounds. Respect the authorized scope and budget;
stop with named unresolved obligations when exhausted or externally blocked.
Do not impose wall-clock timeouts or start unbounded/background proof searches.

## Certificate acceptance

Consult the installed tool versions, reconciled with the campaign's capability
probe, and the current official documentation before
configuring checks; do not copy version-specific commands from memory.

1. Build with Lake and inspect diagnostics. Audit the transitive axiom dependencies
   of every claimed result with `#print axioms`. Only the standard foundational
   axioms `propext`, `Classical.choice` and `Quot.sound` are permitted. Reject
   `sorryAx`, custom mathematical axioms and native-computation axioms. A source
   search for `sorry` alone is insufficient. Draft holes may remain in unfinished
   work, but no accepted result may depend on them. Challenge placeholders are
   specifications, never accepted proof evidence.
2. Recheck built proofs using `lean4checker --fresh` where supported. Keep this
   distinct from an independent kernel implementation.
3. For final certification, use Comparator against the trusted challenge in a
   separate clean verification environment with its supported sandbox. Enable an
   independent external checker such as nanoda, and enforce the same axiom allowlist.
   Use the official tools and configuration; do not substitute a development fake
   sandbox or treat an unavailable checker as a pass. Record remaining checks as
   pending if the required environment is unavailable.

A successful certificate establishes only the statements actually checked under
the declared foundations and toolchain assumptions. Human review still owns the
meaning of the challenge and its referenced definitions. Formal proof authorship,
agent agreement and compilation success alone are not certification.

## Reduction and implementation obligations

Keep four scopes separate: selected lemmas; legal construction and complete
output-recovery correctness; polynomial time and encoding size of F and G;
executable implementation agreement. Establish operation counts and output bit
lengths from each construction using the shared contract's input-length measures.
Small output size alone is not polynomial runtime. A complete written complexity
argument is valid evidence, not a missing result merely because it is not encoded
in Lean. Formalize resource bounds in an explicit cost model when requested.

A Lean model of an algorithm does not verify the existing implementation. Retain
injected-instance tests as implementation evidence. To claim implementation
agreement, prove the executable function meets the specification or provide a
checked correspondence to it; differential tests alone do not suffice. Do not
replace the production implementation as a side effect of proof formalization.

## Artifacts and reporting

Use `formal/` at the campaign root, alongside `work/`, for the standard Lake project, trusted
challenge, proof sources and Comparator configuration. Create only needed files.
Retain toolchain/dependency versions through standard project files. Save commands,
working directory and raw build/axiom/checker outputs under
`formal/evidence/<check-name>/`, preserving failed evidence before repair reruns.
Do not create implementation hashes, duplicate manuscripts or progress databases.

In `state.md`, link paper lemmas to Lean declaration names and evidence. Report
which of the four scopes above passed, which are partial or unattempted, all
remaining assumptions, and the next unresolved obligation. Do not express progress
as a percentage of lemmas. An existing `ready_for_expert_review` label is not a
formal certificate. Only claim full formal reduction verification when the complete
reduction and resource obligations pass; report implementation agreement separately.

## Tool references

- [Lean proof validation](https://lean-lang.org/doc/reference/latest/ValidatingProofs/):
  axiom auditing, kernel replay and remaining trust assumptions.
- [Comparator](https://github.com/leanprover/comparator): trusted challenges,
  statement comparison, sandbox requirements and external checkers.
- [Mathlib documentation](https://leanprover-community.github.io/mathlib4_docs/):
  find existing definitions and lemmas before adding replacements.
