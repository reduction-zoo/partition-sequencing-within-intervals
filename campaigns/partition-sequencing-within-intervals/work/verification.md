# Verification report — independent re-implementation

Tested candidate: `work/algorithm.py` at commit `3a4c545` (mechanism A,
corrected enforcer window). The candidate was not modified during verification.

## Independence

`verify.py` imports neither `check.py` nor `algorithm.py` and solves both
endpoints with different algorithms than the prepared checker:

| Endpoint | `check.py` | `verify.py` |
|---|---|---|
| Source oracle | subset-sum dynamic programming | exhaustive enumeration of all combinations |
| Source validator | `source_witness_problem` | `source_output_ok` |
| Target oracle | subset dynamic program plus CP-SAT `AddNoOverlap` | permutation enumeration for at most 8 tasks plus a pairwise-disjunctive CP-SAT model |
| Target validator | `target_schedule_problem` | `schedule_ok` |

The candidate is executed only through its documented command contract, as a
subprocess, with the source instance or `{"source", "target_solution"}` on stdin.
Whenever the permutation route applies, it must agree with CP-SAT on feasibility;
disagreement is reported as an oracle defect rather than resolved silently.

## Command and result

```sh
uv run --locked python campaigns/partition-sequencing-within-intervals/work/verify.py \
  --candidate campaigns/partition-sequencing-within-intervals/work/algorithm.py
```

Retained output: `work/evidence/verification-run.txt`. Result:
**VERIFICATION PASSED**.

Instance coverage: **52** source instances — 12 hand-chosen degenerate or
extreme cases plus 40 deterministic pseudo-random instances (`random.Random`,
seed `20260921`, 1–7 items with sizes 1–12). Degenerate cases include a single
item, equal large items (`10^9`), a huge-plus-tiny total, ten unit items, powers
of two, nine consecutive integers and two large coprime values.

Output coverage: **153** distinct valid target outputs fed through recovery —
113 feasible schedules and 40 `no_solution` answers, each with the recovered
source output validated against the independent source oracle. Coverage is
reported separately from instance coverage because a feasible constructed target
admits many valid outputs and each was exercised on its own.

Every case satisfied the two-way correspondence: the constructed target was
feasible exactly when the source instance had a witness. No mismatch, no oracle
disagreement, no candidate execution error and no malformed output occurred, so
no reproducer file was written.

## Coverage limits and untested domains

- Instance sizes: source `n <= 7` for generated cases and `n = 10` for one
  degenerate case; larger `n` is untested.
- Target outputs: at most 12 distinct valid outputs per constructed instance; the
  set of all valid outputs is not enumerated.
- Feasibility above 8 tasks rests on CP-SAT alone (no permutation cross-check).
- Values: integers up to `10^12`; nothing checks the polynomial *bit-length*
  bound the proof claims, and nothing here bounds runtime.
- The generated family samples small random instances; it cannot establish that
  the construction is correct for all legal inputs — that is `work/proof.md`'s
  obligation, not this report's.
- Consistency between the implementation and the stated construction was
  inspected by reading `algorithm.py` against `proof.md`: `F` emits one window
  `[0, B+1]` task per element plus the enforcer at `r = ceil(B/2)`,
  `d = ceil((B+1)/2)`; `G` reads the enforcer at index `n` and returns the
  elements with smaller start time. The implementation adds no state, no
  randomness and no solver call. No size-growth concern was found beyond the
  documented `O(n log B)` encoding, which the proof argues is polynomial.
