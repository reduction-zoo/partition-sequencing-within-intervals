# Preparation report — testing foundation

Status: **complete and committed before any candidate was constructed.** This
report establishes no reduction correctness claim; it only describes the oracles,
their checks and their limits.

## Files

| File | Role |
|---|---|
| `contract.md` | Both encodings, legal-instance constraints, candidate command contract, validity predicates |
| `cases.json` | 16 injected source instances with hand-checkable ground truth |
| `check.py` | Independent source and target oracles, validators, `--self-test`, `--candidate PATH` |
| `../../pyproject.toml`, `../../uv.lock` | Locked Python project (CPython 3.12.11, `ortools==9.15.6755`) |

## Oracles

**Source (Partition).** Subset-sum dynamic programming decides existence and
reconstructs one witness: exact, conclusive, independent of any candidate. For
instances with at most 20 items, exhaustive enumeration of all `2^n` subsets
lists every witness and cross-checks the dynamic program. Witnesses are validated
directly against the definition (`Σ = B/2`), not against the encoding used to
find them.

**Target (Sequencing Within Intervals).** Two independent exact methods:

1. Subset dynamic programming, `best[mask]` = minimum possible completion time of
   exactly the tasks in `mask`. Completing a fixed task set earlier is never
   worse (exchange argument), so a finite `best[full]` decides feasibility and
   reconstructs a schedule. `O(2^n · n)`, conclusive.
2. OR-Tools CP-SAT: one start variable per task with its window, one
   `AddNoOverlap` over the intervals. `OPTIMAL`/`FEASIBLE` yields a schedule,
   `INFEASIBLE` is a conclusive negative, and any other status is recorded as
   `unknown` — never as NO. If the solver is unavailable the run reports
   `unavailable` rather than silently degrading.

Both methods must agree in `--self-test`; schedules from either route are
re-validated by `target_schedule_problem`. Alternate valid target outputs are
enumerated deterministically: every permutation with the earliest-start rule for
instances of at most 8 tasks (optimal per fixed order), a lexicographic
depth-first search capped at 8 orders above that, plus schedules that differ by
starting a task later. The cap is explicit and finite.

## Commands and results

```sh
uv sync --locked
uv run --locked python campaigns/partition-sequencing-within-intervals/work/check.py --self-test
```

Result (2026-09-21): **SELF-TEST PASSED**.

- 8 hand-checkable source cases: the dynamic program, the exhaustive enumeration
  and the stored expectation agree, and every stored witness validates.
- 6 hand-checkable target cases: the subset dynamic program and CP-SAT agree on
  both feasible and infeasible instances, including the even-total textbook
  gadget and the odd-total gadget with the corrected enforcer window.
- 18 deliberately incorrect fixtures are rejected: wrong subset sum, duplicate
  and out-of-range indices, non-increasing indices, both/neither output keys,
  wrong value types, overlapping tasks, a task past its deadline, a negative
  start, and a schedule of the wrong length.
- 16 stored cases agree with the source oracle.

Solver reconciliation with the campaign capability probe: the probe recorded
OR-Tools 9.15.6755 on the host; the locked project pins the same version.

## Coverage and limits

- Source cases: `n <= 8`; exhaustive source cross-check is bounded to `n <= 20`.
- Target witness enumeration: at most 8 distinct valid outputs per constructed
  instance; permutation enumeration bounded to 8 tasks.
- Infeasibility is accepted only from the exact dynamic programs or CP-SAT's
  `INFEASIBLE`; `unknown` and `unavailable` are reported, never read as NO.
- No solver, subprocess, shell or wall-clock timeouts are used anywhere.
- JSON integers are unbounded, so nothing here checks the *bit-length* bounds
  that the forward map must respect; those stay a proof obligation.
- The foundation cannot show that the candidate's construction is correct; it can
  only refute a candidate that fails the tested outputs.

## Change log

- 2026-09-21, before the foundation commit: one self-test fixture mislabelled a
  legal schedule (`{"start": [0, 2]}` on tasks with windows `[0,3]` and `[1,3]`)
  as deadline-violating. The fixture was replaced with a single-task instance
  that genuinely ends after its deadline. No expectation derived from the problem
  definitions changed; the corrected fixture is stricter only in that it now
  names a real violation.
