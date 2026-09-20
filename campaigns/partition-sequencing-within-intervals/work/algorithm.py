#!/usr/bin/env python3
"""Partition -> Sequencing Within Intervals: one rule, two deterministic maps.

Forward map (default mode) reads one source instance and writes one target
instance. Recovery map (``--extract``) reads ``{"source": …, "target_solution": …}``
and writes one source output. Neither map calls a solver, uses randomness or
consults an LLM, and neither depends on state kept from an earlier invocation.

Construction (mechanism A):

* one task per element:  ``r = 0``, ``l = s_i``, ``d = B + 1`` with ``B = Σ s_i``
* one enforcer task:     ``r = ceil(B/2)``, ``l = 1``, ``d = ceil((B+1)/2)``

For even ``B`` the enforcer is pinned to ``[B/2, B/2 + 1)`` and the elements must
fill both sides exactly; for odd ``B`` the enforcer has ``r = d`` and no feasible
schedule exists. Recovery reports the element tasks scheduled before the enforcer.

See ``proof.md`` for the general argument and bounds.
"""

from __future__ import annotations

import json
import sys


def build_target(source: dict) -> dict:
    """Forward map F: a Partition instance to a Sequencing instance."""
    sizes = source["sizes"]
    total = sum(sizes)
    enforcer_release = (total + 1) // 2  # ceil(B/2)
    enforcer_deadline = (total + 2) // 2  # ceil((B+1)/2)
    tasks = [{"r": 0, "l": size, "d": total + 1} for size in sizes]
    tasks.append({"r": enforcer_release, "l": 1, "d": enforcer_deadline})
    return {"tasks": tasks}


def recover(source: dict, target_solution: dict) -> dict:
    """Recovery map G: a source instance and a valid target output to a source output."""
    sizes = source["sizes"]
    if "no_solution" in target_solution:
        return {"no_solution": True}
    starts = target_solution["start"]
    enforcer = len(sizes)  # the enforcer is the task appended by F
    enforcer_start = starts[enforcer]
    before = [index for index in range(len(sizes)) if starts[index] < enforcer_start]
    return {"subset": before}


def main(argv: list[str]) -> int:
    extract = False
    for argument in argv[1:]:
        if argument == "--extract":
            extract = True
        else:
            print(f"unknown argument {argument!r}", file=sys.stderr)
            return 2
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        print(f"input is not valid JSON: {error}", file=sys.stderr)
        return 1
    try:
        if extract:
            result = recover(payload["source"], payload["target_solution"])
        else:
            result = build_target(payload)
    except (KeyError, TypeError) as error:
        print(f"malformed input: {type(error).__name__}: {error}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
