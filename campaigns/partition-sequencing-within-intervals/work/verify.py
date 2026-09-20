#!/usr/bin/env python3
"""Independent verification of the Partition -> Sequencing Within Intervals rule.

Deliberately independent of the testing foundation: this file imports neither
``check.py`` nor ``algorithm.py``, and both endpoints are solved here by
different algorithms than the prepared checker uses.

| Endpoint | `check.py` | this file |
|---|---|---|
| Source oracle | subset-sum dynamic programming | exhaustive enumeration of all combinations |
| Source validator | `source_witness_problem` | `source_output_ok`, written here |
| Target oracle | subset dynamic programming + CP-SAT `AddNoOverlap` | permutation enumeration + a pairwise-disjunctive CP-SAT model |
| Target validator | `target_schedule_problem` | `schedule_ok`, written here |

The candidate is always executed as a subprocess through its documented command
contract. Mismatches are written as reproducers under `work/evidence/`.

Usage:  python verify.py --candidate PATH
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import subprocess
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parent
EVIDENCE = WORK / "evidence"
SEED = 20260921
OUTPUT_CAP = 12  # distinct valid target outputs tested per constructed instance
PERMUTATION_LIMIT = 8  # tasks; above this the target oracle falls back to CP-SAT only


# --------------------------------------------------------------------------
# Source: Partition, by exhaustive combination enumeration
# --------------------------------------------------------------------------


def source_witnesses(sizes: list[int]) -> list[list[int]]:
    """Every subcollection summing to half the total, by enumerating combinations."""
    half, remainder = divmod(sum(sizes), 2)
    if remainder:
        return []
    found: list[list[int]] = []
    for size in range(len(sizes) + 1):
        for combination in itertools.combinations(range(len(sizes)), size):
            if sum(sizes[index] for index in combination) == half:
                found.append(list(combination))
    return found


def source_output_ok(sizes: list[int], output: object) -> str | None:
    """Why a purported source output is invalid, else None. Written here."""
    if not isinstance(output, dict):
        return "output is not an object"
    keys = set(output)
    if keys == {"no_solution"} and output["no_solution"] is True:
        return None
    if keys != {"subset"}:
        return f"expected exactly one key, got {sorted(keys)}"
    subset = output["subset"]
    if not isinstance(subset, list):
        return "subset is not a list"
    if any(not isinstance(index, int) or isinstance(index, bool) for index in subset):
        return "subset holds a non-integer"
    if len(set(subset)) != len(subset):
        return "subset repeats an index"
    if any(not 0 <= index < len(sizes) for index in subset):
        return "subset index out of range"
    if sum(sizes[index] for index in subset) != sum(sizes) / 2:
        return "subset does not sum to half the total"
    return None


def source_truth(sizes: list[int]) -> bool:
    """Whether the source instance has any valid output."""
    return bool(source_witnesses(sizes))


# --------------------------------------------------------------------------
# Target: Sequencing Within Intervals, by permutations and by a pairwise model
# --------------------------------------------------------------------------


def schedule_ok(tasks: list[dict], starts: list[int]) -> str | None:
    """Why a purported schedule is invalid, else None. Written here."""
    if not isinstance(starts, list) or len(starts) != len(tasks):
        return "start list has the wrong length"
    if any(not isinstance(start, int) or isinstance(start, bool) for start in starts):
        return "start holds a non-integer"
    for index, (task, start) in enumerate(zip(tasks, starts)):
        if start < task["r"] or start + task["l"] > task["d"]:
            return f"task {index} violates its window"
    for first, second in itertools.combinations(range(len(tasks)), 2):
        end_first = starts[first] + tasks[first]["l"]
        end_second = starts[second] + tasks[second]["l"]
        if not (end_first <= starts[second] or end_second <= starts[first]):
            return f"tasks {first} and {second} overlap"
    return None


def target_schedules_by_permutation(tasks: list[dict]) -> list[list[int]]:
    """Every distinct feasible schedule found by trying all task orders.

    For a fixed order, starting each task as early as possible is optimal, so an
    order that fails under this rule admits no feasible schedule in that order.
    Feasibility of the whole instance is the disjunction over orders; this is
    exact for at most 8 tasks (the caller checks the bound).
    """
    count = len(tasks)
    found: dict[tuple[int, ...], list[int]] = {}
    for order in itertools.permutations(range(count)):
        starts = [0] * count
        current = 0
        for index in order:
            start = max(tasks[index]["r"], current)
            if start + tasks[index]["l"] > tasks[index]["d"]:
                break
            starts[index] = start
            current = start + tasks[index]["l"]
        else:
            found.setdefault(tuple(starts), starts)
    return list(found.values())


def target_cpsat_pairwise(tasks: list[dict]) -> tuple[str, list[int] | None]:
    """Decide target feasibility with a pairwise-disjunctive CP-SAT model.

    Different encoding from `check.py`: no `AddNoOverlap`, instead one boolean
    per task pair ordering the two tasks, which is the definition read literally.
    """
    try:
        from ortools.sat.python import cp_model
    except Exception as error:  # pragma: no cover - reported, never silent
        return f"unavailable ({type(error).__name__})", None
    model = cp_model.CpModel()
    count = len(tasks)
    starts = []
    for index, task in enumerate(tasks):
        upper = max(task["d"], task["r"] + task["l"])
        start = model.NewIntVar(0, upper, f"s{index}")
        model.Add(start >= task["r"])
        model.Add(start <= task["d"] - task["l"])
        starts.append(start)
    for first, second in itertools.combinations(range(count), 2):
        before = model.NewBoolVar(f"before_{first}_{second}")
        model.Add(starts[first] + tasks[first]["l"] <= starts[second]).OnlyEnforceIf(before)
        model.Add(starts[second] + tasks[second]["l"] <= starts[first]).OnlyEnforceIf(before.Not())
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return "feasible", [int(solver.Value(start)) for start in starts]
    if status == cp_model.INFEASIBLE:
        return "infeasible", None
    return "unknown", None


def target_truth(tasks: list[dict]) -> tuple[bool | None, str]:
    """Feasibility from the two independent routes, demanding agreement."""
    status, starts = target_cpsat_pairwise(tasks)
    permutation: list[list[int]] | None = None
    if len(tasks) <= PERMUTATION_LIMIT:
        permutation = target_schedules_by_permutation(tasks)
    if status == "feasible":
        problem = schedule_ok(tasks, starts) if starts is not None else "no schedule returned"
        if problem is not None:
            return None, f"CP-SAT returned an invalid schedule: {problem}"
    if permutation is not None:
        permutation_feasible = bool(permutation)
        if status in ("feasible", "infeasible") and (status == "feasible") != permutation_feasible:
            return None, f"oracles disagree: cpsat={status} permutations={permutation_feasible}"
        return permutation_feasible, "permutations"
    if status in ("feasible", "infeasible"):
        return status == "feasible", "cpsat"
    return None, status


def target_outputs(tasks: list[dict], feasible: bool) -> list[dict]:
    """Valid target outputs to test, capped; NO-SOLUTION when infeasible."""
    if not feasible:
        return [{"no_solution": True}]
    schedules: list[list[int]] = []
    if len(tasks) <= PERMUTATION_LIMIT:
        schedules = target_schedules_by_permutation(tasks)
    else:
        status, starts = target_cpsat_pairwise(tasks)
        if starts is not None:
            schedules = [starts]
    # Add schedules that differ by starting one task later.
    for schedule in list(schedules):
        for index in range(len(tasks)):
            for extra in (1, 2):
                candidate = list(schedule)
                candidate[index] += extra
                if schedule_ok(tasks, candidate) is None:
                    schedules.append(candidate)
    unique: dict[tuple[int, ...], list[int]] = {}
    for schedule in schedules:
        unique.setdefault(tuple(schedule), schedule)
    return [{"start": schedule} for schedule in list(unique.values())[:OUTPUT_CAP]]


# --------------------------------------------------------------------------
# Instance families, including degenerate and large-value cases
# --------------------------------------------------------------------------


def generated_instances() -> list[tuple[str, list[int]]]:
    instances: list[tuple[str, list[int]]] = [
        ("degenerate-single-one", [1]),
        ("degenerate-single-two", [2]),
        ("degenerate-two-ones", [1, 1]),
        ("degenerate-large-equal", [10**9, 10**9]),
        ("degenerate-large-no", [10**9, 10**9 - 1]),
        ("degenerate-unbalanced", [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        ("degenerate-one-huge-one-small", [10**12, 1]),
        ("near-half-off-by-one", [5, 5, 5, 5, 5]),
        ("duplicates-heavy", [4, 4, 4, 4, 4, 4, 4]),
        ("powers-of-two", [1, 2, 4, 8, 16, 32]),
        ("consecutive-nine", list(range(1, 10))),
        ("two-large-coprime", [999_983, 999_979]),
    ]
    rng = random.Random(SEED)
    for index in range(40):
        count = rng.randint(1, 7)
        sizes = [rng.randint(1, 12) for _ in range(count)]
        instances.append((f"random-{index:02d}", sizes))
    return instances


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------


def call_candidate(path: Path, payload: object, extract: bool) -> tuple[int, str, str]:
    command = [sys.executable, str(path)] + (["--extract"] if extract else [])
    completed = subprocess.run(command, input=json.dumps(payload), capture_output=True, text=True)
    return completed.returncode, completed.stdout, completed.stderr


def save_reproducer(name: str, payload: object) -> Path:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    path = EVIDENCE / f"verify-{name}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    arguments = parser.parse_args()
    candidate = arguments.candidate
    failures: list[str] = []
    instances = 0
    outputs_tested = 0
    no_solution_outputs = 0
    schedule_outputs = 0

    print(f"candidate: {candidate}")
    print(f"seed for generated instances: {SEED}")
    for name, sizes in generated_instances():
        instances += 1
        source = {"sizes": sizes}
        witnesses = source_witnesses(sizes)
        expected = bool(witnesses)
        code, stdout, stderr = call_candidate(candidate, source, extract=False)
        if code != 0:
            failures.append(f"{name}: forward map exited {code} ({stderr.strip()[:160]})")
            save_reproducer(f"{name}-forward", {"source": source, "stderr": stderr})
            continue
        try:
            target = json.loads(stdout)
        except json.JSONDecodeError as error:
            failures.append(f"{name}: forward map printed invalid JSON ({error})")
            save_reproducer(f"{name}-forward-json", {"source": source, "stdout": stdout})
            continue
        tasks = target.get("tasks") if isinstance(target, dict) else None
        if not isinstance(tasks, list) or not tasks:
            failures.append(f"{name}: constructed target has no task list")
            save_reproducer(f"{name}-target", {"source": source, "target": target})
            continue

        feasible, route = target_truth(tasks)
        if feasible is None:
            failures.append(f"{name}: target oracles inconclusive ({route})")
            save_reproducer(f"{name}-inconclusive", {"source": source, "target": target})
            continue
        if feasible != expected:
            failures.append(
                f"{name}: correspondence broken, source_has_output={expected} target_feasible={feasible}"
            )
            save_reproducer(
                f"{name}-correspondence",
                {"source": source, "target": target, "witnesses": witnesses[:5]},
            )
            continue

        tested_here = 0
        for target_output in target_outputs(tasks, feasible):
            code, stdout, stderr = call_candidate(
                candidate, {"source": source, "target_solution": target_output}, extract=True
            )
            if code != 0:
                failures.append(f"{name}: recovery exited {code} ({stderr.strip()[:160]})")
                save_reproducer(
                    f"{name}-recovery-error",
                    {"source": source, "target": target, "target_solution": target_output, "stderr": stderr},
                )
                continue
            try:
                recovered = json.loads(stdout)
            except json.JSONDecodeError as error:
                failures.append(f"{name}: recovery printed invalid JSON ({error})")
                save_reproducer(
                    f"{name}-recovery-json",
                    {"source": source, "target": target, "target_solution": target_output, "stdout": stdout},
                )
                continue
            problem = source_output_ok(sizes, recovered)
            if problem is not None:
                failures.append(f"{name}: recovered output invalid ({problem})")
                save_reproducer(
                    f"{name}-recovered",
                    {
                        "source": source,
                        "target": target,
                        "target_solution": target_output,
                        "recovered": recovered,
                        "problem": problem,
                    },
                )
                continue
            if not expected and "no_solution" not in recovered:
                failures.append(f"{name}: unsolvable source, recovery returned a witness")
            if expected and "subset" not in recovered:
                failures.append(f"{name}: solvable source, recovery returned NO-SOLUTION")
            if "no_solution" in target_output:
                no_solution_outputs += 1
            else:
                schedule_outputs += 1
            tested_here += 1
        outputs_tested += tested_here
        print(f"  {name}: sizes={sizes} source={'YES' if expected else 'NO'} "
              f"target={feasible} route={route} outputs={tested_here}")

    print()
    print(f"instances={instances} target_outputs={outputs_tested} "
          f"schedules={schedule_outputs} no_solution_answers={no_solution_outputs}")
    if failures:
        print(f"\nVERIFICATION FAILED with {len(failures)} problem(s):")
        for failure in failures:
            print(f"  - {failure}")
        print(f"reproducers under {EVIDENCE}")
        return 1
    print("\nVERIFICATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
