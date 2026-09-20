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

This is where the removed upstream implementation went wrong. Writing the release
time as `⌊B/2⌋` gives, for `B = 2m+1`, `σ̄ ≥ m` and `σ̄ ≤ m`, so the enforcer
remains schedulable and the two remaining blocks have unequal lengths `m` and
`m+1`. The floor reading appears in the issue's AI-generated summary and in the
removed implementation (PR #1052's deleted text used `h = ⌊S/2⌋` with enforcer
`r = h`, `d = h + 1`). The quoted Garey & Johnson text is self-consistent and
already forces the ceiling: for even `B` it asserts `d(t̄) = r(t̄) + 1` with
`r(t̄) = [B/2]`, which requires `[(B+1)/2] = B/2 + 1`, that is `[x] = ⌈x⌉`; for odd
`B` both brackets then round up and `r(t̄) = d(t̄)`. Mechanism A is therefore the
textbook window transcribed correctly, not a correction of the textbook, and the
window used here is re-derived above rather than copied.

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
to a null set. Here every start and length is an integer, so every task interval
has integer endpoints; the complement of their finite union inside
`[0, m) ∪ [m+1, 2m+1]` would then be a finite union of intervals with integer
endpoints, and any non-empty such complement has measure at least `1`. The
complement has measure `0`, so it is empty and the elements occupy both blocks
exactly. Hence there is no idle time in either block, and the elements
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

`G` reads `σ̄` once and compares the `n` element start times against it:
`O(n log B)` bit operations, because each comparison touches numbers of bit
length `O(log B)`. Its output lists up to `n` indices, each of bit length
`Θ(log n)`, so the output is `Θ(n log n)` bits in the worst case (the subset of
all indices). Both quantities are polynomial in `|x| + |y|`. `G`
reconstructs everything from `source` and `target_solution` (the enforcer is the
task that `F` appends, so its position is `n`), so separate process invocations
behave identically and no memory of the forward run is required.

## Scope of the claim

This argument covers every legal source instance and every valid target output
for the fixed endpoints and encodings of `contract.md`. It does not claim
originality: the construction is the textbook local-replacement plus enforcer
gadget — Garey & Johnson problem `[SS1]`, Chapter 3, Theorem 3.8, whose
classification as NP-complete via that theorem the upstream model documentation
also states — with the textbook window (`[x] = ⌈x⌉`) re-derived here and the
recovery obligation proved for every valid target output. Finite tests in
`check.py` and `verify.py` are evidence about this implementation, not a
substitute for the argument above.

One integration caveat is recorded but not part of the theorem. For odd `B` the
enforcer is released at `r̄ = d̄`, i.e. `r̄ + l̄ > d̄`. That is a legal instance under
the fixed question and under `contract.md`, and upstream `main` now treats such a
task as an infeasible windowless instance; but the released upstream model
`problemreductions 0.6.0` asserts `r + l ≤ d` in its constructor and cannot
represent it. Registering this rule against that release would need mechanism B
(an explicitly infeasible target built from satisfiable windows) or a model
change. This does not affect `G(x, y) ∈ S_A(x)` for the fixed endpoints.

One boundary worth stating: `G` is defined for valid target outputs. Given a
malformed `target_solution` that violates the target predicate — for instance a
schedule placing the enforcer off its pinned slot — `G` makes no promise, exactly
as the reduction contract specifies.
