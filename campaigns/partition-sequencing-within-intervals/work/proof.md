# Proof — Partition → Sequencing Within Intervals

Notation. A source instance is `x = (s_1, …, s_n)` with `n ≥ 1` and every
`s_i ≥ 1`; write `B = Σ_{i=1}^{n} s_i`. The rule is

- **F**: tasks `T_1, …, T_n` with `r_i = 0`, `l_i = s_i`, `d_i = B + 1`, plus one
  enforcer task `T̄` with `r̄ = ⌈B/2⌉`, `l̄ = 1`, `d̄ = ⌈(B+1)/2⌉`;
- **G**: if the target output is `no_solution`, return `no_solution`; otherwise
  return `W = { i : σ_i < σ̄ }`, the element tasks scheduled before the enforcer.

Recall the target predicate: a schedule `σ` is feasible when `σ_j ≥ r_j`,
`σ_j + l_j ≤ d_j` for every task, and no two tasks overlap, i.e.
`σ_j + l_j ≤ σ_k` or `σ_k + l_k ≤ σ_j` for every pair. Preemption is not part of
the problem: a task occupies the contiguous interval `[σ_j, σ_j + l_j)`.

## Lemma 1 (F is a legal, polynomial-size construction)

Every emitted task has integer `r ≥ 0`, integer `l ≥ 1` and integer `d ≥ 1`:
element tasks inherit `s_i ≥ 1` and `B + 1 ≥ 2`; the enforcer has
`l̄ = 1`, `r̄ = ⌈B/2⌉ ≥ 1` and `d̄ = ⌈(B+1)/2⌉ ≥ 1`. The construction performs
`n + 1` tasks' worth of integer arithmetic on numbers of bit length
`O(log B)`, so its runtime is `O(n log B)` and its output has
`O(n log B)` bits — polynomial in the input length `|x| = Θ(n + log B)`.

## Lemma 2 (the enforcer is pinned exactly when `B` is even)

In any feasible schedule of `F(x)`:

- if `B = 2m` then `σ̄ = m`;
- if `B = 2m + 1` then no feasible schedule exists.

*Proof.* The enforcer's own constraints are `σ̄ ≥ ⌈B/2⌉` and `σ̄ + 1 ≤ ⌈(B+1)/2⌉`.
For `B = 2m`: `⌈B/2⌉ = m` and `⌈(B+1)/2⌉ = m + 1`, so `σ̄ ≥ m` and `σ̄ ≤ m`, hence
`σ̄ = m`. For `B = 2m + 1`: `⌈B/2⌉ = m + 1` and `⌈(B+1)/2⌉ = m + 1`, so `σ̄ ≥ m+1`
and `σ̄ ≤ m`, a contradiction. ∎

This is precisely where the removed upstream implementation failed. Writing the
release time as `⌊B/2⌋` gives, for `B = 2m+1`, `σ̄ ≥ m` and `σ̄ ≤ m`, so the
enforcer remains schedulable and the two remaining blocks have unequal lengths
`m` and `m+1`. The current issue text repeats that false reading; the window used
here is derived above, not copied.

## Lemma 3 (even case: the elements fill both sides exactly)

Let `B = 2m` and let `σ` be a feasible schedule. Then every element task lies
entirely in `[0, m)` or entirely in `[m+1, 2m+1]`, and

    Σ_{i ∈ W} s_i = m = B/2    where W = { i : σ_i < m }.

*Proof.* By Lemma 2, `σ̄ = m`, so the enforcer occupies `[m, m+1)`. No element
task overlaps it, so each element interval lies inside
`[0, m) ∪ [m+1, 2m+1]`; in particular no element spans the enforcer. Each element
window is `[0, B+1] = [0, 2m+1]`, and the union `[0,m) ∪ [m+1,2m+1]` has measure
`2m`. The element tasks are pairwise disjoint and their total length is
`Σ s_i = B = 2m`, which equals that measure. A disjoint family contained in a
measurable set, whose total measure equals the set's measure, covers the set up
to a null set. Hence there is no idle time in either block, and the elements
starting before `m` occupy `[0, m)` exactly, so their lengths sum to `m`. ∎

## Theorem (the rule is correct)

For every legal source instance `x` and every valid target output
`y ∈ S_B(F(x))`, the recovered value `G(x, y)` lies in `S_A(x)`.

*Proof.* Let `x` be legal and let `y ∈ S_B(F(x))` be valid.

*Case 1: `y = no_solution`.* Then `S_B(F(x)) = ∅`. Suppose `x` had a witness `A'`
with `Σ_{i ∈ A'} s_i = B/2`. Then `B = 2m` is even. Schedule the tasks of `A'`
contiguously in increasing index order starting at time `0`, the enforcer at
`m`, and the remaining element tasks contiguously after it ending at `2m+1`.
Every element ends by `2m + 1 = B + 1 = d_i` and starts no earlier than `0 = r_i`;
the enforcer lies in `[m, m+1)`, inside its window by Lemma 2's computation.
No two tasks overlap. So the schedule is feasible and `S_B(F(x)) ≠ ∅`, a
contradiction. Hence `S_A(x) = ∅` and `G(x, y) = no_solution ∈ S_A(x)`.

*Case 2: `y = σ` is a schedule.* By Lemma 2, `B = 2m` is even and `σ̄ = m`. Lemma
3 gives `Σ_{i ∈ W} s_i = m = B/2`, so `W` is a subcollection whose sum is half
the total; `G(x, y) = W ∈ S_A(x)`. ∎

The two directions above also show that the negative answer is not vacuous: a
witness of `x` always yields a feasible schedule of `F(x)` (the construction used
in Case 1), so infeasibility of the target happens exactly when the source has no
witness.

## Recovery is polynomial and stateless

`G` reads `σ̄` once and compares the `n` element start times against it: `O(n)`
integer comparisons and `O(n)` output bits, hence polynomial in `|x| + |y|`. It
reconstructs everything from `source` and `target_solution` (the enforcer is the
task that `F` appends, so its position is `n`), so separate process invocations
behave identically and no memory of the forward run is required.

## Scope of the claim

This argument covers every legal source instance and every valid target output
for the fixed endpoints and encodings of `contract.md`. It does not claim
originality: the construction is the textbook local-replacement plus enforcer
gadget (Garey & Johnson, Chapter 3, Theorem 3.8, as cited upstream), corrected at
the enforcer window and re-derived here. Finite tests in `check.py` are evidence
about this implementation, not a substitute for the argument above.

One boundary worth stating: `G` is defined for valid target outputs. Given a
malformed `target_solution` that violates the target predicate — for instance a
schedule placing the enforcer off its pinned slot — `G` makes no promise, exactly
as the reduction contract specifies.
