#!/usr/bin/env python3
"""Reviewer's independent checks for Partition -> Sequencing Within Intervals.

Written from the problem definitions in work/contract.md and the construction in
work/proof.md. This file does NOT import work/algorithm.py, work/check.py or
work/verify.py and reuses none of their helpers. The candidate is executed only
as a subprocess through its documented command contract.

Checks:
  1. implementation-vs-spec: candidate forward output equals the stated
     construction, field for field, on every enumerated instance;
  2. completeness cross-check: on tiny instances, an unrestricted search over
     start tuples is compared with the permutation enumeration, confirming that
     every valid target schedule is a no-idle contiguous filling;
  3. exhaustive schedule enumeration (small n): for every enumerated instance ALL
     valid target schedules (every permutation of the n+1 tasks) are enumerated
     and the reviewer recomputes W = {i < n : start_i < start_enforcer}, checking
     sum(W) = B/2 in each of them;
  4. correspondence: target feasible iff the source has a witness, both parities;
  5. candidate recovery on reviewer-constructed valid schedules (diverse block
     orders) and on no_solution answers, compared against the reviewer's own W;
  6. determinism and empirical output-bit-length scaling.
"""

from __future__ import annotations

import itertools
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parents[1] / "work" / "algorithm.py"

RECOVERY_CAP = 700
FORWARD_CALLS = 0
RECOVERY_CALLS = 0


# ---------------------------------------------------------------------------
# Stated construction, re-implemented from proof.md
# ---------------------------------------------------------------------------


def f_spec(sizes: list[int]) -> dict:
    total = sum(sizes)
    tasks = [{"r": 0, "l": s, "d": total + 1} for s in sizes]
    tasks.append({"r": -(-total // 2), "l": 1, "d": -(-(total + 1) // 2)})
    return {"tasks": tasks}


def g_spec(sizes: list[int], starts: list[int]) -> list[int]:
    n = len(sizes)
    return [i for i in range(n) if starts[i] < starts[n]]


def source_witnesses(sizes: list[int]) -> list[list[int]]:
    half, rem = divmod(sum(sizes), 2)
    if rem:
        return []
    out = []
    for k in range(len(sizes) + 1):
        for combo in itertools.combinations(range(len(sizes)), k):
            if sum(sizes[i] for i in combo) == half:
                out.append(list(combo))
    return out


# ---------------------------------------------------------------------------
# Reviewer's own validator and schedule enumeration
# ---------------------------------------------------------------------------


def schedule_ok(tasks: list[dict], starts: list[int]) -> bool:
    if len(starts) != len(tasks):
        return False
    for task, start in zip(tasks, starts):
        if not isinstance(start, int):
            return False
        if start < task["r"] or start + task["l"] > task["d"]:
            return False
    for a, b in itertools.combinations(range(len(tasks)), 2):
        if not (
            starts[a] + tasks[a]["l"] <= starts[b]
            or starts[b] + tasks[b]["l"] <= starts[a]
        ):
            return False
    return True


def schedules_by_permutation(tasks: list[dict]) -> list[list[int]]:
    """All no-idle schedules: place each permutation of the tasks from time 0.

    For a legal constructed instance with even total the union of the task
    intervals is contained in [0, B+1], has measure B+1 equal to the total task
    length, and the tasks are pairwise disjoint; hence the union is exactly
    [0, B+1] and every valid schedule is such a contiguous filling. Check 2
    confirms this on tiny instances by an unrestricted search.
    """
    count = len(tasks)
    found = []
    seen = set()
    for order in itertools.permutations(range(count)):
        starts = [0] * count
        cursor = 0
        ok = True
        for index in order:
            task = tasks[index]
            start = cursor if cursor >= task["r"] else task["r"]
            if start + task["l"] > task["d"]:
                ok = False
                break
            starts[index] = start
            cursor = start + task["l"]
        if ok:
            key = tuple(starts)
            if key not in seen and schedule_ok(tasks, starts):
                seen.add(key)
                found.append(starts)
    return found


def schedules_by_full_search(tasks: list[dict], horizon: int) -> list[list[int]]:
    """Every start tuple in [0, horizon] satisfying the predicate, by DFS."""
    order = sorted(range(len(tasks)), key=lambda i: -tasks[i]["l"])
    starts: list = [None] * len(tasks)
    out: list[list[int]] = []

    def rec(pos: int) -> None:
        if pos == len(order):
            out.append([int(s) for s in starts])
            return
        index = order[pos]
        task = tasks[index]
        for start in range(task["r"], task["d"] - task["l"] + 1):
            if start + task["l"] - 1 > horizon:
                continue
            good = True
            for other in range(len(tasks)):
                if starts[other] is None:
                    continue
                o_start = starts[other]
                o_len = tasks[other]["l"]
                if not (start + task["l"] <= o_start or o_start + o_len <= start):
                    good = False
                    break
            if good:
                starts[index] = start
                rec(pos + 1)
                starts[index] = None

    rec(0)
    return out


def reviewer_schedules(sizes: list[int], limit: int = 3) -> list[list[int]]:
    """Valid target schedules built by the reviewer from the block lemma.

    Uses a witness W summing to B/2: place W contiguously from 0, the enforcer at
    B/2, and the complement contiguously from B/2+1. Several block orders are
    produced so recovery is exercised on schedules other than the intended one.
    """
    witnesses = source_witnesses(sizes)
    if not witnesses:
        return []
    n = len(sizes)
    total = sum(sizes)
    half = total // 2
    witness = witnesses[0]
    complement = [i for i in range(n) if i not in set(witness)]
    rng = random.Random(1234 + n + total)
    orders = []
    for left in (witness, list(reversed(witness))):
        for right in (complement, list(reversed(complement))):
            orders.append(list(left) + list(right))
    shuffled_left = list(witness)
    rng.shuffle(shuffled_left)
    shuffled_right = list(complement)
    rng.shuffle(shuffled_right)
    orders.append(shuffled_left + shuffled_right)

    tasks = f_spec(sizes)["tasks"]
    out = []
    for order in orders[:limit]:
        prefix, rest = order[: len(witness)], order[len(witness):]
        starts = [0] * (n + 1)
        cursor = 0
        for index in prefix:
            starts[index] = cursor
            cursor += sizes[index]
        starts[n] = half
        cursor = half + 1
        for index in rest:
            starts[index] = cursor
            cursor += sizes[index]
        if schedule_ok(tasks, starts):
            out.append(starts)
    return out


# ---------------------------------------------------------------------------
# Candidate invocation
# ---------------------------------------------------------------------------


def call(payload: object, extract: bool) -> dict:
    global FORWARD_CALLS, RECOVERY_CALLS
    command = [sys.executable, str(CANDIDATE)] + (["--extract"] if extract else [])
    done = subprocess.run(
        command, input=json.dumps(payload), capture_output=True, text=True
    )
    if done.returncode != 0:
        raise RuntimeError(f"candidate exited {done.returncode}: {done.stderr.strip()}")
    if extract:
        RECOVERY_CALLS += 1
    else:
        FORWARD_CALLS += 1
    return json.loads(done.stdout)


# ---------------------------------------------------------------------------
# Instance families
# ---------------------------------------------------------------------------


def families() -> list[tuple[list[int], bool]]:
    """(sizes, exhaustive) pairs; exhaustive means all valid schedules enumerated."""
    out: list[tuple[list[int], bool]] = []
    for n in range(1, 5):
        out.extend((list(t), True) for t in itertools.product(range(1, 6), repeat=n))
    out.extend((list(t), True) for t in itertools.product(range(1, 5), repeat=5))
    out.extend((list(t), True) for t in itertools.product(range(1, 4), repeat=6))
    out.extend((list(t), True) for t in itertools.product(range(1, 3), repeat=7))
    rng = random.Random(424242)
    for _ in range(60):
        n = rng.randint(1, 7)
        out.append(([rng.randint(1, 6) for _ in range(n)], True))
    # Larger n and extreme values: forward-map and sampled-recovery checks only.
    out.extend([
        ([10**9, 10**9], False),
        ([10**9, 10**9 - 1], False),
        ([10**12, 1], False),
        ([1] * 12, False),
        ([7, 7], False),
        ([5, 5, 3, 3, 2], False),
        ([1, 2, 4], False),
        ([3, 3, 3], False),
        ([1, 1, 4], False),
    ])
    for _ in range(80):
        n = rng.randint(8, 14)
        out.append(([rng.randint(1, 9) for _ in range(n)], False))
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def main() -> int:
    failures: list[str] = []
    notes: list[str] = []
    instances = families()
    print(f"candidate: {CANDIDATE}")
    print(
        f"instances: {len(instances)} "
        f"(exhaustive: {sum(1 for _, e in instances if e)})",
        flush=True,
    )

    # ---- check 2: tiny unrestricted search vs permutation enumeration -------
    for sizes in [[1, 1], [3, 1, 2, 4], [1, 1, 4], [2, 2, 2, 2], [1, 2, 4]]:
        target = f_spec(sizes)
        full = {tuple(s) for s in schedules_by_full_search(target["tasks"], sum(sizes) + 1)}
        perm = {tuple(s) for s in schedules_by_permutation(target["tasks"])}
        if full != perm:
            failures.append(
                f"check2 {sizes}: unrestricted search {len(full)} vs permutation {len(perm)}"
            )
    notes.append("check2: unrestricted search equals permutation enumeration on 5 tiny instances")

    # ---- checks 1, 3, 4, 5 --------------------------------------------------
    total_schedules = 0
    exhaustive_instances = 0
    recovery_tested = 0
    no_solution_tested = 0
    for sizes, exhaustive in instances:
        target = f_spec(sizes)
        candidate_target = call({"sizes": sizes}, extract=False)
        if candidate_target != target:
            failures.append(
                f"check1 {sizes}: candidate forward {candidate_target} != stated {target}"
            )
            continue
        half, _ = divmod(sum(sizes), 2)
        expected = bool(source_witnesses(sizes))

        if exhaustive:
            exhaustive_instances += 1
            schedules = schedules_by_permutation(target["tasks"])
            total_schedules += len(schedules)
            if bool(schedules) != expected:
                failures.append(
                    f"check4 {sizes}: target feasible={bool(schedules)}, source witness={expected}"
                )
            for starts in schedules:
                if starts[len(sizes)] != half:
                    failures.append(f"check3 {sizes}: enforcer not pinned at {half}: {starts}")
                    break
                chosen = g_spec(sizes, starts)
                if sum(sizes[i] for i in chosen) != half:
                    failures.append(
                        f"check3 {sizes}: W={chosen} sums to {sum(sizes[i] for i in chosen)} "
                        f"not {half}; schedule {starts}"
                    )
                    break

        if RECOVERY_CALLS < RECOVERY_CAP:
            if expected:
                for starts in reviewer_schedules(sizes):
                    if RECOVERY_CALLS >= RECOVERY_CAP:
                        break
                    got = call(
                        {"source": {"sizes": sizes}, "target_solution": {"start": starts}},
                        extract=True,
                    )
                    want = g_spec(sizes, starts)
                    recovery_tested += 1
                    if got != {"subset": want}:
                        failures.append(
                            f"check5 {sizes}: recovery {got} != reviewer W {want} for {starts}"
                        )
                    if sum(sizes[i] for i in want) != half:
                        failures.append(f"check5 {sizes}: recovered W {want} not half-sum")
            else:
                got = call(
                    {"source": {"sizes": sizes},
                     "target_solution": {"no_solution": True}},
                    extract=True,
                )
                no_solution_tested += 1
                if got != {"no_solution": True}:
                    failures.append(f"check5 {sizes}: no_solution target gave {got}")

    notes.append(f"check1: forward output equals stated construction on {len(instances)} instances")
    notes.append(
        f"check3: all {total_schedules} valid schedules over {exhaustive_instances} "
        f"exhaustively enumerated instances have sum(W) = B/2"
    )
    notes.append(
        f"check5: candidate recovery matched reviewer W on {recovery_tested} schedules "
        f"and {no_solution_tested} no_solution answers"
    )

    # ---- check 6: determinism and bit-length scaling -----------------------
    if call({"sizes": [3, 1, 2, 4]}, extract=False) != call({"sizes": [3, 1, 2, 4]}, extract=False):
        failures.append("check6: forward map is not deterministic")
    payload = {"source": {"sizes": [3, 1, 2, 4]}, "target_solution": {"start": [0, 3, 4, 5, 2]}}
    if call(payload, extract=True) != call(payload, extract=True):
        failures.append("check6: recovery map is not deterministic")

    for n in (10, 1000, 20000):
        sizes = [1 + (i * 37) % 10**6 for i in range(n)]
        target = f_spec(sizes)
        bits = max(len(bin(v)) - 2 for task in target["tasks"] for v in task.values())
        notes.append(
            f"scale n={n}: max value bits={bits}, fields={len(target['tasks']) * 3}, "
            f"approx output bits={bits * len(target['tasks']) * 3}"
        )

    print()
    for note in notes:
        print("note:", note)
    print(f"forward subprocess calls: {FORWARD_CALLS}")
    print(f"recovery subprocess calls: {RECOVERY_CALLS}")
    if failures:
        print(f"\nREVIEWER CHECKS FAILED with {len(failures)} problem(s):")
        for failure in failures[:40]:
            print("  -", failure)
        return 1
    print("\nREVIEWER CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
