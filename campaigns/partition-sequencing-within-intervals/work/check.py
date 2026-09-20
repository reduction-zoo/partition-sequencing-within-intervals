#!/usr/bin/env python3
"""Independent oracles and validators for Partition -> Sequencing Within Intervals.

This file is the campaign's testing foundation. It must not import, copy or
invoke the candidate reduction: the candidate is always executed as a separate
process by ``--candidate``.

Endpoints (see ``contract.md``):

* Source, Partition:      ``{"sizes": [s_1, ..., s_n]}``
* Source output:          ``{"subset": [i, ...]}`` or ``{"no_solution": true}``
* Target, Sequencing:     ``{"tasks": [{"r": r, "l": l, "d": d}, ...]}``
* Target output:          ``{"start": [s_1, ..., s_n]}`` or ``{"no_solution": true}``

Oracle design
-------------

* Source, conclusive: subset-sum dynamic programming decides existence and
  reconstructs one witness exactly. Exhaustive enumeration of all ``2^n``
  subsets (small ``n``) independently lists every witness and cross-checks the
  dynamic program.
* Target, conclusive: the subset dynamic program ``f[mask]`` = minimum possible
  completion time of exactly the tasks in ``mask`` decides feasibility, because
  for a fixed task set completing earlier is never worse (exchange argument).
  OR-Tools CP-SAT encodes the same instance independently with ``AddNoOverlap``
  and must agree; a missing solver or an "unknown" status is reported, never
  treated as NO. Every schedule returned by either route is re-validated against
  the definition in this file.

No check uses wall-clock timeouts. Negative decisions are accepted only from the
conclusive dynamic programs (and CP-SAT's INFEASIBLE status).
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path

CASES_PATH = Path(__file__).resolve().parent / "cases.json"
WITNESS_CAP = 8  # distinct valid target outputs tested per constructed instance
PERMUTATION_LIMIT = 8  # tasks; above this, witnesses come from a capped DFS


# --------------------------------------------------------------------------
# Source oracle: Partition
# --------------------------------------------------------------------------


def source_instance_problem(instance: object) -> str | None:
    """Return why ``instance`` is not a legal source instance, else None."""
    if not isinstance(instance, dict):
        return "source instance must be a JSON object"
    extra = set(instance) - {"sizes"}
    if extra:
        return f"source instance has unknown keys {sorted(extra)}"
    sizes = instance.get("sizes")
    if not isinstance(sizes, list) or not sizes:
        return "sizes must be a non-empty list"
    for index, size in enumerate(sizes):
        if isinstance(size, bool) or not isinstance(size, int):
            return f"sizes[{index}] must be an integer"
        if size < 1:
            return f"sizes[{index}] must be positive"
    return None


def source_output_format_problem(instance: dict, output: object) -> str | None:
    """Structural validation of a purported source output, without the oracle."""
    if not isinstance(output, dict):
        return "source output must be a JSON object"
    keys = set(output)
    if keys == {"subset"}:
        subset = output["subset"]
        if not isinstance(subset, list):
            return "subset must be a list"
        sizes = instance["sizes"]
        previous = -1
        for position, index in enumerate(subset):
            if isinstance(index, bool) or not isinstance(index, int):
                return f"subset[{position}] must be an integer"
            if index <= previous:
                return f"subset is not strictly increasing at position {position}"
            if not 0 <= index < len(sizes):
                return f"subset index {index} is out of range"
            previous = index
        return None
    if keys == {"no_solution"}:
        if output["no_solution"] is not True:
            return "no_solution must be true when present"
        return None
    return f"source output must carry exactly one of subset/no_solution, got {sorted(keys)}"


def source_witness_problem(instance: dict, subset: list[int]) -> str | None:
    """Validate a claimed witness against the definition (sum = half the total)."""
    sizes = instance["sizes"]
    chosen = sum(sizes[index] for index in subset)
    half = sum(sizes)
    if 2 * chosen != half:
        return f"subset sums to {chosen}, which is not half of the total {half}"
    return None


def source_enumerate_witnesses(instance: dict) -> list[list[int]]:
    """Every witness, by exhaustive enumeration. Finite bound: at most 20 items."""
    sizes = instance["sizes"]
    if len(sizes) > 20:
        raise ValueError("exhaustive source enumeration is bounded to 20 items")
    half, total = divmod(sum(sizes), 2)
    witnesses: list[list[int]] = []
    for mask in range(1 << len(sizes)):
        if total:
            break  # odd total: no witness can exist
        chosen = [index for index in range(len(sizes)) if mask >> index & 1]
        if sum(sizes[index] for index in chosen) == half:
            witnesses.append(chosen)
    return witnesses


def source_solve(instance: dict) -> tuple[bool, list[int] | None]:
    """Decide source feasibility conclusively and reconstruct one witness.

    Subset-sum dynamic programming over reachable sums: an exact decision
    procedure, independent of any candidate.
    """
    sizes = instance["sizes"]
    half, remainder = divmod(sum(sizes), 2)
    if remainder:
        return False, None
    # reachable[sum] = index of an item that first reached this sum, plus parent
    reachable: dict[int, tuple[int, int]] = {0: (-1, -1)}
    for index, size in enumerate(sizes):
        for current in sorted(reachable, reverse=True):
            target = current + size
            if target <= half and target not in reachable:
                reachable[target] = (index, current)
    if half not in reachable:
        return False, None
    subset: list[int] = []
    current = half
    while current > 0:
        index, parent = reachable[current]
        subset.append(index)
        current = parent
    subset.sort()
    return True, subset


# --------------------------------------------------------------------------
# Target oracle: Sequencing Within Intervals
# --------------------------------------------------------------------------


def target_instance_problem(instance: object) -> str | None:
    """Return why ``instance`` is not a legal target instance, else None."""
    if not isinstance(instance, dict):
        return "target instance must be a JSON object"
    extra = set(instance) - {"tasks"}
    if extra:
        return f"target instance has unknown keys {sorted(extra)}"
    tasks = instance.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return "tasks must be a non-empty list"
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            return f"tasks[{index}] must be an object"
        extra = set(task) - {"r", "l", "d"}
        if extra:
            return f"tasks[{index}] has unknown keys {sorted(extra)}"
        for key in ("r", "l", "d"):
            if key not in task:
                return f"tasks[{index}] is missing {key}"
            value = task[key]
            if isinstance(value, bool) or not isinstance(value, int):
                return f"tasks[{index}].{key} must be an integer"
        if task["r"] < 0:
            return f"tasks[{index}].r must be nonnegative"
        if task["l"] < 1:
            return f"tasks[{index}].l must be positive"
        if task["d"] < 1:
            return f"tasks[{index}].d must be positive"
    return None


def target_output_format_problem(instance: dict, output: object) -> str | None:
    """Structural validation of a purported schedule, without solving."""
    if not isinstance(output, dict):
        return "target output must be a JSON object"
    keys = set(output)
    if keys == {"start"}:
        starts = output["start"]
        if not isinstance(starts, list):
            return "start must be a list"
        if len(starts) != len(instance["tasks"]):
            return f"start has {len(starts)} entries for {len(instance['tasks'])} tasks"
        for index, start in enumerate(starts):
            if isinstance(start, bool) or not isinstance(start, int):
                return f"start[{index}] must be an integer"
            if start < 0:
                return f"start[{index}] must be nonnegative"
        return None
    if keys == {"no_solution"}:
        if output["no_solution"] is not True:
            return "no_solution must be true when present"
        return None
    return f"target output must carry exactly one of start/no_solution, got {sorted(keys)}"


def target_schedule_problem(instance: dict, starts: list[int]) -> str | None:
    """Validate one schedule against the definition: windows and non-overlap."""
    tasks = instance["tasks"]
    for index, (task, start) in enumerate(zip(tasks, starts)):
        if start < task["r"]:
            return f"tasks[{index}] starts at {start}, before its release {task['r']}"
        if start + task["l"] > task["d"]:
            return (
                f"tasks[{index}] ends at {start + task['l']}, "
                f"after its deadline {task['d']}"
            )
    for left, right in itertools.combinations(range(len(tasks)), 2):
        left_start, left_length = starts[left], tasks[left]["l"]
        right_start, right_length = starts[right], tasks[right]["l"]
        if not (
            left_start + left_length <= right_start
            or right_start + right_length <= left_start
        ):
            return f"tasks[{left}] and tasks[{right}] overlap"
    return None


def target_solve_dp(instance: dict) -> tuple[bool, list[int] | None]:
    """Decide target feasibility conclusively by a subset dynamic program.

    ``best[mask]`` is the minimum completion time of exactly the tasks in
    ``mask``. For a fixed task set, completing earlier never hurts, so the
    minimum over last tasks is exact; a finite ``best[full]`` is a witness.
    """
    tasks = instance["tasks"]
    count = len(tasks)
    infinity = None
    best: list[int | None] = [infinity] * (1 << count)
    parent: list[int | None] = [None] * (1 << count)
    best[0] = 0
    for mask in range(1 << count):
        current = best[mask]
        if current is None:
            continue
        for index in range(count):
            if mask >> index & 1:
                continue
            task = tasks[index]
            start = max(task["r"], current)
            if start + task["l"] > task["d"]:
                continue
            end = start + task["l"]
            following = mask | 1 << index
            if best[following] is None or end < best[following]:
                best[following] = end
                parent[following] = index
    full = (1 << count) - 1
    if best[full] is None:
        return False, None
    order: list[int] = []
    mask = full
    while mask:
        index = parent[mask]
        assert index is not None
        order.append(index)
        mask ^= 1 << index
    order.reverse()
    starts = [0] * count
    current = 0
    for index in order:
        task = tasks[index]
        start = max(task["r"], current)
        starts[index] = start
        current = start + task["l"]
    return True, starts


def cpsat_available() -> tuple[bool, str]:
    """Whether the independent CP-SAT route can run, with its version."""
    try:
        from ortools.sat.python import cp_model  # noqa: F401
        import ortools

        return True, getattr(ortools, "__version__", "unknown")
    except Exception as error:  # pragma: no cover - reported, never silent
        return False, f"{type(error).__name__}: {error}"


def target_solve_cpsat(instance: dict) -> tuple[str, list[int] | None]:
    """Independently decide target feasibility with OR-Tools CP-SAT.

    Returns ``("feasible"|"infeasible"|"unknown"|"unavailable", starts)``. The
    encoding adds a start variable per task with its window and one
    ``AddNoOverlap`` over the intervals.
    """
    try:
        from ortools.sat.python import cp_model
    except Exception:
        return "unavailable", None
    tasks = instance["tasks"]
    model = cp_model.CpModel()
    starts: list[object] = []
    intervals: list[object] = []
    for index, task in enumerate(tasks):
        upper = max(task["d"], task["r"] + task["l"])
        start = model.NewIntVar(0, upper, f"start_{index}")
        model.Add(start >= task["r"])
        end = model.NewIntVar(0, upper, f"end_{index}")
        model.Add(end == start + task["l"])
        model.Add(end <= task["d"])
        intervals.append(model.NewIntervalVar(start, task["l"], end, f"task_{index}"))
        starts.append(start)
    model.AddNoOverlap(intervals)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return "feasible", [int(solver.Value(start)) for start in starts]
    if status == cp_model.INFEASIBLE:
        return "infeasible", None
    return "unknown", None


def target_witnesses(instance: dict, cap: int = WITNESS_CAP) -> list[list[int]]:
    """Distinct valid target outputs, deterministically, at most ``cap``.

    Small instances use every permutation with the earliest-start rule (which is
    optimal per fixed order); larger ones use a lexicographic depth-first search
    capped at ``cap`` orders. Each returned schedule is re-validated. Feasibility
    itself is decided by the dynamic program, not by this enumeration.
    """
    tasks = instance["tasks"]
    count = len(tasks)
    found: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()

    def record(starts: list[int]) -> None:
        key = tuple(starts)
        if key in seen:
            return
        if target_schedule_problem(instance, starts) is None:
            seen.add(key)
            found.append(starts)

    if count <= PERMUTATION_LIMIT:
        for order in itertools.permutations(range(count)):
            starts = [0] * count
            current = 0
            ok = True
            for index in order:
                task = tasks[index]
                start = max(task["r"], current)
                if start + task["l"] > task["d"]:
                    ok = False
                    break
                starts[index] = start
                current = start + task["l"]
            if ok:
                record(starts)
            if len(found) >= cap:
                break
    else:
        def search(mask: int, current: int, starts: list[int]) -> None:
            if len(found) >= cap:
                return
            if mask == (1 << count) - 1:
                record(list(starts))
                return
            for index in range(count):
                if mask >> index & 1:
                    continue
                task = tasks[index]
                start = max(task["r"], current)
                if start + task["l"] > task["d"]:
                    continue
                starts[index] = start
                search(mask | 1 << index, start + task["l"], starts)
                if len(found) >= cap:
                    return

        search(0, 0, [0] * count)

    # Additional valid outputs that only differ by starting some task later.
    for starts in list(found):
        for index in range(count):
            for extra in range(1, cap + 1):
                if len(found) >= cap:
                    break
                candidate = list(starts)
                candidate[index] += extra
                record(candidate)
    return found[:cap]


# --------------------------------------------------------------------------
# Self-test fixtures
# --------------------------------------------------------------------------

SOURCE_SELF_CASES = [
    # (sizes, has_solution, one witness or None, why it is hand-checkable)
    ([1, 1], True, [0], "half of 2 is 1, one item of size 1"),
    ([4], False, None, "half of 4 is 2, no subset of a single size-4 item"),
    ([1, 2], False, None, "total 3 is odd"),
    ([1, 1, 4], False, None, "total 6, half 3, no subset sums to 3"),
    ([1, 2, 3], True, [2], "the item of size 3 is half of 6"),
    ([3, 1, 2, 4], True, [0, 2], "3 + 2 = 5, half of 10"),
    ([2, 2, 2, 2], True, [0, 1], "2 + 2 = 4, half of 8"),
    ([1, 1, 1, 5], False, None, "total 8, half 4, subsets 1,2,3,5,6,7,8"),
]

TARGET_SELF_CASES = [
    # (tasks, feasible, why it is hand-checkable)
    ([{"r": 0, "l": 1, "d": 1}], True, "the only task fits its window"),
    ([{"r": 0, "l": 2, "d": 1}], False, "the task cannot fit at all"),
    (
        [
            {"r": 0, "l": 2, "d": 3},
            {"r": 0, "l": 2, "d": 3},
            {"r": 1, "l": 1, "d": 2},
        ],
        False,
        "the length-1 task at [1,2) leaves two blocks of length 1 for length-2 tasks",
    ),
    (
        [
            {"r": 0, "l": 1, "d": 2},
            {"r": 1, "l": 1, "d": 3},
        ],
        True,
        "two unit tasks in disjoint windows",
    ),
    (
        [
            {"r": 0, "l": 3, "d": 11},
            {"r": 0, "l": 1, "d": 11},
            {"r": 0, "l": 2, "d": 11},
            {"r": 0, "l": 4, "d": 11},
            {"r": 5, "l": 1, "d": 6},
        ],
        True,
        "the textbook even-total gadget: enforcer pinned at [5,6)",
    ),
    (
        [
            {"r": 0, "l": 1, "d": 8},
            {"r": 0, "l": 2, "d": 8},
            {"r": 0, "l": 4, "d": 8},
            {"r": 4, "l": 1, "d": 4},
        ],
        False,
        "odd-total gadget with the corrected enforcer (r = d = 4) is unschedulable",
    ),
]


def _check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def run_self_test() -> int:
    failures: list[str] = []
    notes: list[str] = []

    print("== source oracle: exhaustive enumeration versus dynamic programming ==")
    for sizes, expected, witness, why in SOURCE_SELF_CASES:
        instance = {"sizes": sizes}
        problem = source_instance_problem(instance)
        _check(problem is None, f"{sizes}: instance rejected: {problem}", failures)
        has_solution, found = source_solve(instance)
        _check(
            has_solution == expected,
            f"{sizes}: dynamic program answered {has_solution}, expected {expected} ({why})",
            failures,
        )
        if witness is not None:
            _check(
                source_witness_problem(instance, witness) is None,
                f"{sizes}: stored witness {witness} is invalid",
                failures,
            )
        enumerated = source_enumerate_witnesses(instance)
        _check(
            bool(enumerated) == expected,
            f"{sizes}: exhaustive enumeration disagrees with the expectation",
            failures,
        )
        if expected:
            _check(
                found is not None and found in enumerated,
                f"{sizes}: dynamic-program witness {found} is not among the enumerated ones",
                failures,
            )
        print(f"  {sizes}: expected={expected} dp={has_solution} witness={found} witnesses={len(enumerated)}")

    print("== target oracle: dynamic program versus CP-SAT ==")
    available, version = cpsat_available()
    notes.append(f"CP-SAT available={available} version={version}")
    for tasks, expected, why in TARGET_SELF_CASES:
        instance = {"tasks": tasks}
        problem = target_instance_problem(instance)
        _check(problem is None, f"{tasks}: instance rejected: {problem}", failures)
        feasible, starts = target_solve_dp(instance)
        _check(
            feasible == expected,
            f"{tasks}: dynamic program answered {feasible}, expected {expected} ({why})",
            failures,
        )
        if starts is not None:
            _check(
                target_schedule_problem(instance, starts) is None,
                f"{tasks}: dynamic-program schedule {starts} is invalid",
                failures,
            )
        status, cpsat_starts = target_solve_cpsat(instance)
        if status == "unavailable":
            print(f"  {tasks}: CP-SAT unavailable, dynamic program only")
        else:
            _check(
                (status == "feasible") == expected,
                f"{tasks}: CP-SAT answered {status}, expected {expected}",
                failures,
            )
            if cpsat_starts is not None:
                _check(
                    target_schedule_problem(instance, cpsat_starts) is None,
                    f"{tasks}: CP-SAT schedule {cpsat_starts} is invalid",
                    failures,
                )
        print(f"  {tasks}: expected={expected} dp={feasible} {starts} cpsat={status} {cpsat_starts}")

    print("== deliberately incorrect fixtures must be rejected ==")
    yes_instance = {"sizes": [3, 1, 2, 4]}
    no_instance = {"sizes": [1, 1, 4]}
    bad_source_outputs = [
        (yes_instance, {"subset": [0, 1]}, "wrong sum: 3 + 1 = 4 is not half of 10"),
        (yes_instance, {"subset": [0, 0]}, "duplicate index"),
        (yes_instance, {"subset": [0, 9]}, "index out of range"),
        (yes_instance, {"subset": [2, 0]}, "not strictly increasing"),
        (yes_instance, {"subset": [0, 2], "no_solution": True}, "both keys"),
        (yes_instance, {}, "neither key"),
        (yes_instance, {"subset": "0"}, "wrong type"),
    ]
    for instance, output, why in bad_source_outputs:
        problem = source_output_format_problem(instance, output)
        extra = None
        if problem is None and "subset" in output:
            extra = source_witness_problem(instance, output["subset"])
        _check(problem is not None or extra is not None, f"accepted bad source output ({why}): {output}", failures)
        print(f"  rejected ({why}): {problem or extra}")

    yes_target = {"tasks": [{"r": 0, "l": 1, "d": 2}, {"r": 1, "l": 1, "d": 3}]}
    bad_target_outputs = [
        (yes_target, {"start": [1, 1]}, "overlap at time 1"),
        ({"tasks": [{"r": 0, "l": 1, "d": 1}]}, {"start": [1]}, "the task ends after its deadline"),
        (yes_target, {"start": [-1, 2]}, "negative start"),
        (yes_target, {"start": [0]}, "wrong length"),
        (yes_target, {"start": [0, 1], "no_solution": True}, "both keys"),
        (yes_target, {}, "neither key"),
    ]
    for instance, output, why in bad_target_outputs:
        problem = target_output_format_problem(instance, output)
        extra = None
        if problem is None and "start" in output:
            extra = target_schedule_problem(instance, output["start"])
        _check(problem is not None or extra is not None, f"accepted bad target output ({why}): {output}", failures)
        print(f"  rejected ({why}): {problem or extra}")

    print("== stored cases must agree with the oracles ==")
    cases = json.loads(CASES_PATH.read_text())
    for case in cases["cases"]:
        instance = case["instance"]
        has_solution, witness = source_solve(instance)
        _check(
            has_solution == case["expect"]["has_solution"],
            f"{case['name']}: stored expectation disagrees with the source oracle",
            failures,
        )
        for stored in case["expect"]["witnesses"]:
            _check(
                source_witness_problem(instance, stored) is None,
                f"{case['name']}: stored witness {stored} is invalid",
                failures,
            )
        if not case["expect"]["has_solution"]:
            _check(
                source_enumerate_witnesses(instance) == [],
                f"{case['name']}: exhaustive enumeration found a witness for a NO case",
                failures,
            )
    print(f"  {len(cases['cases'])} stored cases agree")

    print()
    for note in notes:
        print(f"note: {note}")
    if failures:
        print(f"\nSELF-TEST FAILED with {len(failures)} problem(s):")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("\nSELF-TEST PASSED")
    return 0


# --------------------------------------------------------------------------
# Candidate harness
# --------------------------------------------------------------------------


def run_candidate(path: Path, payload: object, extract: bool) -> tuple[int, str, str]:
    """Run the candidate as a separate process; return exit code, stdout, stderr."""
    command = [sys.executable, str(path)]
    if extract:
        command.append("--extract")
    completed = subprocess.run(
        command,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def run_candidate_suite(path: Path) -> int:
    failures: list[str] = []
    cases = json.loads(CASES_PATH.read_text())["cases"]
    print(f"candidate: {path}")
    total_outputs = 0
    for case in cases:
        name = case["name"]
        instance = case["instance"]
        expected = case["expect"]["has_solution"]
        code, stdout, stderr = run_candidate(path, instance, extract=False)
        if code != 0:
            failures.append(f"{name}: forward map exited {code}: {stderr.strip()[:200]}")
            print(f"  {name}: FORWARD FAILED")
            continue
        try:
            target = json.loads(stdout)
        except json.JSONDecodeError as error:
            failures.append(f"{name}: forward map printed invalid JSON: {error}")
            continue
        problem = target_instance_problem(target)
        if problem is not None:
            failures.append(f"{name}: illegal target instance: {problem}")
            continue
        feasible, starts = target_solve_dp(instance=target)
        status, _ = target_solve_cpsat(target)
        if status not in ("unavailable", "unknown"):
            if (status == "feasible") != feasible:
                failures.append(
                    f"{name}: target oracles disagree (dp={feasible}, cpsat={status})"
                )
        if feasible != expected:
            failures.append(
                f"{name}: target feasibility {feasible} does not match source feasibility {expected}"
            )
        witnesses = target_witnesses(target) if feasible else []
        if not feasible:
            witnesses = [None]  # the only valid target output is NO-SOLUTION
        checked = 0
        for witness in witnesses:
            target_output = (
                {"no_solution": True} if witness is None else {"start": witness}
            )
            code, stdout, stderr = run_candidate(
                path, {"source": instance, "target_solution": target_output}, extract=True
            )
            if code != 0:
                failures.append(f"{name}: recovery exited {code}: {stderr.strip()[:200]}")
                continue
            try:
                recovered = json.loads(stdout)
            except json.JSONDecodeError as error:
                failures.append(f"{name}: recovery printed invalid JSON: {error}")
                continue
            format_problem = source_output_format_problem(instance, recovered)
            if format_problem is not None:
                failures.append(f"{name}: malformed recovered source output: {format_problem}")
                continue
            if not expected:
                if "no_solution" not in recovered:
                    failures.append(
                        f"{name}: unsolvable source but recovery returned {recovered}"
                    )
                checked += 1
                continue
            if "subset" not in recovered:
                failures.append(
                    f"{name}: solvable source but recovery returned NO-SOLUTION for target output {target_output}"
                )
                continue
            witness_problem = source_witness_problem(instance, recovered["subset"])
            if witness_problem is not None:
                failures.append(f"{name}: invalid recovered witness: {witness_problem}")
            checked += 1
        total_outputs += checked
        print(
            f"  {name}: source={'YES' if expected else 'NO'} target_feasible={feasible} "
            f"target_outputs_tested={checked}"
        )
    print()
    print(f"instances={len(cases)} target_outputs_tested={total_outputs}")
    if failures:
        print(f"\nCANDIDATE SUITE FAILED with {len(failures)} problem(s):")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("\nCANDIDATE SUITE PASSED")
    return 0


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true", help="run oracle and fixture checks")
    group.add_argument("--candidate", type=Path, help="run the complete rule against every case")
    arguments = parser.parse_args()
    if arguments.self_test:
        return run_self_test()
    available, version = cpsat_available()
    print(f"CP-SAT available={available} version={version}")
    return run_candidate_suite(arguments.candidate)


if __name__ == "__main__":
    sys.exit(main())
