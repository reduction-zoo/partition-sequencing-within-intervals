---
name: research-prepare
description: Build and validate independent test oracles and injected cases before constructing a reduction.
---

# Research Prepare

Build the testing foundation for the fixed reduction question before a
candidate is constructed. First confirm that the independent local Git repository
and its initial question/state commit exist, following the
[repository standard](../../../research/repository.md#start-before-prepare).
Read the campaign question and previous test failures.

Read the shared [reduction contract](../../../research/reduction.md): problems
are (I, S), and the rule is (F, G) with recovery from every valid target output.

## Inputs and boundary

Use the source and target (I, S) definitions, not a proposed reduction,
to derive independent solution oracles. Write only in the assigned output directory.
Preserve previous evidence. Do not construct a candidate reduction in this stage.
During repairs, reuse the existing testing foundation and counterexamples;
repair it only with an explanation grounded in the fixed problem definitions.

## Oracle implementation policy

Prioritize correctness and inspectable encodings over solver performance. First
use a suitable mature open-source solver, such as Z3, OR-Tools CP-SAT, a SAT
solver or an ILP solver. Prefer an already available solver when it fits the
problem; do not benchmark every backend or build a solver-selection framework.
Derive constraints directly from the problem definition and explain why feasible
assignments correspond to feasible witnesses in both directions; for optimization,
also encode and independently check the objective and optimality. These solvers are
test oracles, not part of the candidate reduction algorithm.

If suitable solvers cannot handle the required formulation, explain why and
implement a simple textbook algorithm, such as exhaustive enumeration,
backtracking or dynamic programming, over an explicit finite test domain.
A tiny exhaustive implementation is also appropriate for cross-checking an
encoding. Avoid custom solver machinery, parameter tuning and performance
engineering; choose a smaller, explicitly reported test domain when necessary.

Validate returned witnesses directly against the problem definition, independently
of the solver encoding. Accept a negative decision only from a conclusive check of its predicate, and
INFEASIBLE only from a conclusive infeasibility result;
unknown, numerical ambiguity or execution failure is not NO. For ILP, account
for numerical tolerances and check discrete witnesses exactly. Record the solver,
version, encoding, result-status interpretation and any correctness limitations
in `preparation.md`, and reconcile the solver version with the campaign's
capability probe.

## Deliverables

Keep the reusable files below in `work/`. Follow
[artifact ownership](../research-session/SKILL.md#artifact-ownership) for raw
evidence: use the current round when repairing within one, otherwise a named
`work/evidence/` directory. `preparation.md` describes the current foundation
and links to the checks supporting it; preserve superseded test evidence.

- `contract.md`: source and target JSON encodings, legal-instance constraints,
  and the candidate command contract. `algorithm.py` reads one source instance
  as JSON from stdin and writes one target instance as JSON to stdout; diagnostics
  go to stderr and execution errors produce a nonzero exit code. Define source
  and target output encodings and independent validity predicates as well.
  `python3 algorithm.py --extract` reads a JSON object with keys `source` and
  `target_solution`, and writes one valid source output as JSON. The source value uses
  the forward input encoding. Recovery may reconstruct metadata from the source;
  it cannot depend on memory retained by the earlier forward subprocess.
- `cases.json`: source cases with independently established valid outputs or
  optimal values. Cover YES/NO decisions, distinct search witnesses, optimization
  ties and the specified infeasible/no-solution behavior where applicable.
- `check.py`: independent source/target solvers and output validators. Validate
  both feasibility and exact optimality for optimization, using small exhaustive
  checks or conclusive certificates. Do not import candidates or use an LLM oracle.
- `preparation.md`: oracle checks, commands, results, domain and size coverage,
  unresolved limitations, and reasons for any changes to previous test expectations.

Provide `python3 check.py --self-test` for hand-verifiable cases, stored ground
truth, and deliberately incorrect outputs/recovery fixtures. Confirm that wrong
answers, suboptimal solutions and malformed outputs are detected.

Provide `python3 check.py --candidate PATH` to execute F for each injected source
instance, solve the actual target independently, pass each obtained valid output
to `--extract`, and check the recovered output against S_A(x). For decisions,
exercise both YES and NO through G. For optimization, verify the recovered
objective against the independently established source optimum, not the target
objective. Test alternate target optima. For search, exercise distinct valid
witnesses and explicit no-solution outputs where defined. Do not restrict tests
to outputs supplied by the candidate or skip recovery for special valid answers.
Exit nonzero on mismatch, invalid output or execution failure. Record finite
instance/output coverage, seeds and reproducible evidence. Unknown or numerical
ambiguity cannot establish a valid oracle answer. Choose finite size bounds;
do not introduce wall-clock timeouts.

## Completion and repair

Run the self-test after establishing or changing the testing foundation. Commit
the prepared foundation and its evidence before constructing a candidate. Continue
to construction in the same conversation when it passes and its finite coverage
is explicit. Repair test defects here, preserving evidence and explaining changed
expectations. Record a concrete blocker if preparation cannot be completed.
Do not emit a stage verdict or create a new session. Preparation establishes no
reduction correctness claim.
