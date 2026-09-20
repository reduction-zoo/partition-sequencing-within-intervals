# Test contract — Partition → Sequencing Within Intervals

Fixed for this campaign. Both endpoints, their encodings and the candidate
command contract are part of the tested interface; changing any of them requires
re-preparing the testing foundation.

## Source, Π_A = Partition

- **I_A**: a finite family of positive integers, `{"sizes": [s_1, …, s_n]}` with
  `n >= 1` and every `s_i >= 1`. Values are JSON integers, i.e. binary encodings
  whose bit length is the input size measure.
- **S_A(x)**: every subcollection whose sum equals half the total
  `B = Σ s_i`, each witness encoded as `{"subset": [i_1 < i_2 < …]}`
  (strictly increasing item indices), or `{"no_solution": true}` when no such
  subcollection exists. A negative answer is a semantic answer, not an error.
- **Validity predicate** (`check.py: source_witness_problem`): the indices are
  strictly increasing and in range, and `Σ_{i ∈ subset} s_i = B / 2`. Because
  sizes are positive, `B` must be even for any witness to exist.

## Target, Π_B = Sequencing Within Intervals

- **I_B**: a finite set of tasks, `{"tasks": [{"r": …, "l": …, "d": …}, …]}` with
  `n >= 1`, integer `r >= 0`, integer `l >= 1` and integer `d >= 1`. A task with
  `d < r + l` is a legal instance that happens to be infeasible; it must be
  accepted as input.
- **S_B(x)**: every feasible schedule, encoded as `{"start": [σ_1, …, σ_n]}` with
  each `σ_i` a nonnegative integer, or `{"no_solution": true}`.
- **Validity predicate** (`check.py: target_schedule_problem`): for every task,
  `σ_i >= r_i` and `σ_i + l_i <= d_i`; and for every pair `i ≠ j`, either
  `σ_i + l_i <= σ_j` or `σ_j + l_j <= σ_i`. Task `i` executes contiguously on
  `[σ_i, σ_i + l_i)`; **preemption is not part of this problem**.

## Candidate command contract

`algorithm.py` must implement both maps as one rule, with no randomness, no
solver call and no LLM decision inside either map, and no state shared between
separate process invocations.

| Command | stdin | stdout |
|---|---|---|
| `python3 algorithm.py` | one source instance JSON object | one target instance JSON object |
| `python3 algorithm.py --extract` | `{"source": <source instance>, "target_solution": <target output>}` | one source output JSON object |

- Diagnostics go to stderr; any execution failure exits nonzero.
- The forward map must never read the target solution, and the recovery map must
  reconstruct everything it needs from `source` plus `target_solution`.
- Only one of the two output keys may appear in an output object; both or neither
  is malformed.
- `target_solution` is always a valid target output for the instance the
  candidate itself produced, including `{"no_solution": true}`.
- Output numbers are JSON integers. Polynomial worst-case time and output bit
  length for both maps are proof obligations of the Propose stage, not things
  `check.py` can establish.

## Correctness obligation tested here

For every source instance `x` in `I_A` and every valid target output
`y ∈ S_B(F(x))`, `G(x, y)` must lie in `S_A(x)`. The harness therefore tests each
one of up to eight distinct valid target outputs per constructed instance,
including `{"no_solution": true}` when the constructed target is infeasible, and
checks the recovered source output against independently established source
ground truth.
