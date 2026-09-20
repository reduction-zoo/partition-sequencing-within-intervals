# Independent review 01 — Partition → Sequencing Within Intervals

Reviewer: fresh-context DSH `subagent` spawned by the campaign parent agent with
the review instructions. Review directory:
`campaigns/partition-sequencing-within-intervals/reviews/01-independent/`.
Repository state reviewed: commit `9653daa`, branch `main`; candidate
`work/algorithm.py` verified unchanged since `3a4c545`
(`git diff --stat 3a4c545 9653daa -- …/work/algorithm.py` is empty).

## Decision

**ADVANCE** — eligible for expert review. Correctness is supported by the general
proof and by my own exhaustive independent checks; the mathematical content is a
known textbook result and the campaign claims no new classification; the rule
meets the board's fixed acceptance criteria. Two sentence-level corrections and
one integration caveat are recorded below as F1–F4. They do not change any
mathematical claim or the polynomial-bound obligation, but F2 and F3 should be
fixed before the write/formalize stage.

## Isolation mechanisms actually in force

| Mechanism | In force? | Evidence in this session |
|---|---|---|
| Fresh context, no inherited conversation | yes | I am a `subagent` (spawn provider) started by the parent with these instructions; no proposer turns were visible to me |
| Registered `research_reviewer` tool / `toolFilter.deny` | **no** | the session runs the standard preset (`state.md:91-94`); `subagent`, `subagent_fork`, `workflow`, `send_message`, `list_agents`, `interrupt_agent` and `ask_user_question` are all present in my tool catalog. I spawned no agents and sent no messages |
| Delegation depth cap (`maxDepth`) around the reviewer | **no** | no depth refusal was installed for this session; structural non-nesting is an instruction I followed, not an enforced boundary |
| Write confinement to the review directory | **no** (instruction only) | file policy is `danger-full-access`; the sandbox does not restrict writes. I wrote only inside `reviews/01-independent/`; `git status --porcelain` shows only `?? campaigns/partition-sequencing-within-intervals/reviews/` |
| Separate model route | **no** | no `agentOptions.provider/model` pin; the runtime reports the `deepseek-flash` route, the same harness route family as the session |
| Candidate/tests/evidence immutability | enforced only by instruction | I read them; the `git status` output above is the evidence that nothing was modified |

None of the above is evidence for or against correctness. Agent agreement and
confidence are not evidence; only the files and the checks below count.

## 1. Correctness judgment — supported

**Rule audited.** `work/algorithm.py:27-35` (`build_target`) emits one element task
`{r:0, l:s_i, d:B+1}` per size and one enforcer `{r:(B+1)//2, l:1, d:(B+2)//2}`,
i.e. `r̄ = ⌈B/2⌉`, `d̄ = ⌈(B+1)/2⌉`, exactly as stated in `work/proof.md:3-9`.
`work/algorithm.py:38-47` (`recover`) returns `{i < n : start_i < start_n}` or
`{"no_solution": true}`. Both maps are stateless, deterministic, import only
`json`/`sys`, and call no solver.

**Obligation checked.** For every legal `x` (`contract.md:9-11`: non-empty list of
positive integers) and every valid target output `y ∈ S_B(F(x))`
(`contract.md:22-31`), `G(x,y) ∈ S_A(x)` (`contract.md:57-59`).

**What is sound, with locations.**

- *Legality of F for every legal input.* Element tasks have `r=0`, `l=s_i≥1`,
  `d=B+1≥2`; the enforcer has `r̄≥1`, `l̄=1`, `d̄≥1`. Holds for all legal `x`.
  `proof.md:16-23` (Lemma 1) states this correctly, including the `O(n log B)`
  output bound, which is right for F.
- *The enforcer is pinned.* `proof.md:25-35` (Lemma 2): for `B=2m`,
  `r̄=d̄-1=m` forces `σ̄=m`; for `B=2m+1`, `r̄=d̄=m+1` forces `σ̄≥m+1` and
  `σ̄+1≤m+1`, i.e. no feasible start. Both arithmetics are correct.
- *Recovery for every valid target output, not only the intended one.*
  `proof.md:43-58` (Lemma 3): when `B=2m`, the enforcer occupies `[m,m+1)` and all
  task intervals lie in `[0,B+1]`; the elements are disjoint with total length
  `2m` equal to the measure of `[0,m)∪[m+1,2m+1]`, so the union covers that set
  and the pre-enforcer elements have total length `m`. Hence
  `Σ_{i∈W} s_i = B/2` for **every** feasible schedule, and `W` is a valid
  Partition witness. This is the strongest part of the candidate and it is the
  obligation the removed implementation failed. My check 3 enumerated 378 670
  valid schedules over 2 721 source instances and every one satisfies
  `sum(W)=B/2` (output quoted below).
- *Both parities and the NO-SOLUTION correspondence.* Odd `B`: F is infeasible
  (Lemma 2) and `S_A(x)=∅`. Even `B` without a witness: any feasible schedule
  would give a witness by Lemma 3, so F is infeasible; with a witness, the
  explicit contiguous schedule in `proof.md:67-74` is feasible, so the two sides
  agree. The theorem and its final paragraph (`proof.md:60-83`) quantify over all
  legal `x` and all `y ∈ S_B(F(x))`.
- *Determinism, runtime, encoding size.* F: `n+1` tasks, `O(n log B)` output bits,
  one pass over the input. G: one pass over `n+1` integer starts, no state.
  Polynomial in `|x|` and `|x|+|y|` respectively. My check 6 re-ran both maps on
  identical inputs (equal outputs) and measured output growth at `n=10, 1000,
  20000`.
- *Implementation ↔ construction correspondence.* My check 1 compared the
  candidate's forward JSON to my own re-implementation of the stated
  construction, field for field, on 2 810 instances: identical in every case. The
  enforcer-by-index assumption `enforcer = len(sizes)` in `algorithm.py:44`
  matches the append order in `algorithm.py:33-34`.

**Findings (all minor; none breaks a mathematical claim).**

**F1 — Lemma 3's measure step needs the integrality premise.**
Location: `work/proof.md:55-58`. Missing premise: the intervals have integer
endpoints (integer starts and integer lengths), so the complement of their finite
union inside `[0,m)∪[m+1,2m+1]` is a finite union of integer-endpoint intervals
and any non-empty such complement has measure at least 1, not 0. Without that
premise "covers the set up to a null set" does not literally imply "occupy
`[0,m)` exactly". The conclusion is nevertheless true and I found no
counterexample; required correction is a one-sentence clarification, not a change
of argument.

**F2 — recovery output bit size is understated by a `log n` factor.**
Location: `work/proof.md:87-88`: "`O(n)` integer comparisons and `O(n)` output
bits". Under the fixed encoding (`contract.md:12-15`, `26-27`) a subset is a list
of up to `n` indices, and each index needs `Θ(log n)` bits, so the output is
`Θ(n log n)` bits in the worst case (subset = all indices) and the comparison work
is `O(n log B)` bit operations. The obligation (polynomial output length) still
holds, so this is a false bound, not a failed obligation. Required correction:
restate as `O(n log n)` output bits and `O(n log B)` bit operations. My scaling
note (`independent-checks.txt:8-10`) is consistent with the `n·log(values)` growth.

**F3 — the provenance sentence overstates what the issue text says.**
Location: `work/proof.md:41` ("The current issue text repeats that false reading")
and `work/proof.md:96-99` ("corrected at the enforcer window"). The quoted Garey &
Johnson text inside issue #205 is *self-consistent* and forces the ceiling:
it asserts for even `B` that `d(t̄)=r(t̄)+1` with `r(t̄)=[B/2]`, which requires
`[(B+1)/2]=B/2+1`, i.e. `[x]=⌈x⌉`; for odd `B` both values then round up and
`r(t̄)=d(t̄)`. The floor reading appears only in the AI-generated summary
(warning-tagged, issue #205 body) and in the removed implementation (PR #1052's
deleted paper text used `h = floor(S/2)`, enforcer `r=h`, `d=h+1`). So mechanism A
is the *textbook* window transcribed correctly, not a correction of the textbook.
Required correction: attribute the defect to the summary and the removed
implementation. This affects the framing of novelty, not the rule.

**F4 — integration caveat (not a defect against the fixed question).**
The odd-`B` target gives the enforcer `r̄=d̄`, i.e. `r̄+l̄>d̄`. This is a legal
instance under the fixed question (`question.md:25-32`) and under the campaign's
encoding (`contract.md:23-25`), and upstream `main` now accepts an empty window as
an infeasible instance. But the *released* upstream model
`problemreductions 0.6.0` (2026-09-02) asserts `r(i)+l(i) ≤ d(i)` in
`SequencingWithinIntervals::new` and cannot represent it — see
<https://docs.rs/crate/problemreductions/0.6.0/source/src/models/misc/sequencing_within_intervals.rs>
(panics) versus
<https://raw.githubusercontent.com/CodingThrust/problem-reductions/main/src/models/misc/sequencing_within_intervals.rs>
(`start_slot_count` returns `Ok(0)`). Missing premise for anyone registering this
rule against the released crate: either mechanism B (explicit infeasible target)
or a model change. Does not affect `G(x,y) ∈ S_A(x)` for the fixed endpoints.

**Boundary observations.** Empty `sizes` is outside `I_A` (`contract.md:9-11`),
but the rule still behaves: `{"sizes": []}` → `{"tasks":[{"r":0,"l":1,"d":1}]}`
and its schedule `[0]` → `{"subset": []}` with sum `0 = B/2`, so the omission is
benign. I did not test malformed/out-of-domain inputs beyond this, and the proof
declares them out of scope (`proof.md:102-105`).

## Independent checks run (not a rerun of the campaign suites)

Script: `reviews/01-independent/independent_checks.py` (imports neither
`algorithm.py` nor `check.py` nor `verify.py`; the candidate is executed only as a
subprocess). Command and full transcript:
`uv run --locked python campaigns/partition-sequencing-within-intervals/reviews/01-independent/independent_checks.py`
→ `reviews/01-independent/independent-checks.txt`, `REVIEWER CHECKS PASSED`.

- **check2 (completeness of the enumeration route).** For five tiny instances, an
  unrestricted DFS over all start tuples inside `[0,B+1]` produces exactly the
  same schedule set as my permutation enumeration. This validates the argument
  that every valid schedule is a no-idle contiguous filling, so the enumeration
  below really is over *all* valid target outputs.
- **check1 (implementation ↔ construction).** 2 810 instances (all `n≤4` with
  values 1–5; all `n=5` with 1–4; all `n=6` with 1–3; all `n=7` with 1–2; random
  and extreme cases incl. `[10^9,10^9]`, `[10^12,1]`, `[1]*12`): candidate
  forward output equals my re-implementation of `proof.md`'s construction in every
  case.
- **check3 (recovery for every valid output).** 2 721 instances exhaustively
  enumerated: **378 670** valid target schedules, every one with the enforcer at
  `B/2` and `sum(W) = B/2`.
- **check4 (correspondence).** On the same exhaustive set, target feasibility
  equals source witness existence for both parities (odd totals and even-total
  no-witness cases are infeasible; witness cases are feasible).
- **check5 (candidate recovery).** 420 reviewer-constructed valid schedules
  (including reversed and shuffled block orders, so not only the intended
  schedule) — candidate output matched my own `W` in all 420; 280 `no_solution`
  answers were returned for the 280 infeasible instances.
- **check6.** Both maps are deterministic across repeated invocations; output
  value bit length grows as expected with `n`.

Transcript:

```
instances: 2810 (exhaustive: 2721)
note: check2: unrestricted search equals permutation enumeration on 5 tiny instances
note: check1: forward output equals stated construction on 2810 instances
note: check3: all 378670 valid schedules over 2721 exhaustively enumerated instances have sum(W) = B/2
note: check5: candidate recovery matched reviewer W on 420 schedules and 280 no_solution answers
note: scale n=10: max value bits=11, fields=33, approx output bits=363
note: scale n=1000: max value bits=25, fields=3003, approx output bits=75075
note: scale n=20000: max value bits=33, fields=60003, approx output bits=1980099
forward subprocess calls: 2812
recovery subprocess calls: 702
REVIEWER CHECKS PASSED
```

I read, but did not rerun, the campaign's own retained evidence
(`rounds/001/candidate-suite.txt`: 16 instances / 59 outputs; `work/evidence/verification-run.txt`:
52 instances / 153 outputs) and the preparation/verification limit statements
(`preparation.md:75-76`, `verification.md:50-68`), which correctly disclaim
bit-length and all-output coverage. My checks close the all-output gap only up to
`n≤7`; above that the general proof, not enumeration, carries the claim.

## 2. Novelty judgment — no new theorem; known textbook result

Search date: **2026-09-21 (local, UTC+8; 2026-09-20 UTC)**, via `web_fetch` of the
GitHub REST API and `web_search` from this shell (the campaign's proxy note,
`AGENTS.md:47-51`, was already applied, so `web_fetch` succeeded with HTTP 200).

The theorem actually proved is the NP-completeness of Garey & Johnson problem
**[SS1] Sequencing Within Intervals** by reduction from Partition; the recovery
map is the immediate decoding of that same proof.

- **Verified.** Issue #205's quoted proof text is Garey & Johnson, *Computers and
  Intractability* (1979), Chapter 3, Theorem 3.8: it gives the `[SS1]`
  INSTANCE/QUESTION definition, the element tasks `r=0, d=B+1, l=s(a)`, the
  enforcer, and the equal-block correctness argument — the same theorem now
  proved here. <https://github.com/CodingThrust/problem-reductions/issues/205>
  (state `open`, `state_reason: reopened`, labels `rule`/`Good`, milestone *Garey &
  Johnson*, 8 comments — all confirmed).
- **Verified.** The upstream project's own current model documentation states the
  classification: "This is problem SS1 from Garey & Johnson (1979), NP-complete
  via Theorem 3.8."
  <https://docs.rs/problemreductions/latest/problemreductions/models/misc/struct.SequencingWithinIntervals.html>
  and the same comment in the current source,
  <https://raw.githubusercontent.com/CodingThrust/problem-reductions/main/src/models/misc/sequencing_within_intervals.rs>.
- **Verified provenance of the gap.** PR #1052, "fix: remove 8 unsound
  reductions, fix 8 buggy rules (#1006)", merged 2026-04-17, lists
  `Partition → SequencingWithinIntervals` among the eight removed edges and its
  deleted paper entry used `h = floor(S/2)` with enforcer `r=h, d=h+1`.
  <https://github.com/CodingThrust/problem-reductions/pull/1052>; the correction
  to UNSOUND is issue #1006's comment of 2026-04-06 ("28 of ~40 tested NO
  instances", seed 42). <https://github.com/CodingThrust/problem-reductions/issues/1006>
  The campaign's provenance rows in `question.md:62-69` are accurate on these
  points.
- **Verified openness of the edge.** The upstream `main` tree (1 481 paths,
  `truncated:false`) contains `sequencingwithinintervals_ilp.rs`,
  `threepartition_sequencingwithreleasetimesanddeadlines.rs` and
  `partition_sequencingtominimizetartytaskweight.rs`, but **no**
  `partition_sequencingwithinintervals.rs`; issue #205 is open and requests a
  correct reconstruction.
- **Equivalent known formulation.** Non-preemptive single-machine feasibility with
  release dates and deadlines is `1|r_j|L_max ≤ 0`, NP-complete in the ordinary
  sense; the standard citation is Lenstra, Rinnooy Kan & Brucker, *Complexity of
  machine scheduling problems*, Annals of Discrete Mathematics 1 (1977) 343–362.
- **Could not verify.** (a) The Garey & Johnson book itself is not freely
  available here, so the exact theorem number (3.8), page (70) and the bracket
  notation `[x]` are taken from the issue quotation, not from the source text; the
  internal-consistency argument in F3 is what pins `[x]=⌈x⌉`. (b) The primary
  Lenstra–Rinnooy Kan–Brucker paper was not reachable; only secondary records were
  found, so that pointer is unconfirmed at source. (c) I found no source that
  states the decoding step (pre-enforcer tasks) as a separate result; it is
  implicit in GJ's decision proof, so this is not evidence of novelty.
- **Conclusion.** The mathematical content is fully known and the recovery step is
  folklore; there is no new theorem, no new equivalent formulation, and no new
  complexity classification. The campaign already claims none
  (`question.md:57-60`, `proof.md:93-100`), which is the correct scope.

## 3. Significance judgment — meets the fixed acceptance criteria as a reconstruction

Board record (board repository, outside this campaign):
`/Users/xiweipan/Codes/autoresearch-gadgets/website/questions/partition-sequencing-within-intervals.json`,
category `Construction open`. Its `required_result` asks for deterministic
polynomial-time F and G with legal target construction and recovery for every
valid target output including NO-SOLUTION; its `acceptance` asks for executable
construction and recovery, a general proof over all legal inputs and target
outputs, worst-case polynomial time and encoding-size bounds, citation of the
proof used, and small positive **and negative** instances checked with independent
solvers. It explicitly does **not** require a new classification.

Concrete contribution, separating reconstruction from classification:

- **Reconstruction, complete and executable.** F and G are implemented as one
  deterministic stateless rule (`algorithm.py`), the construction matches the
  textbook gadget exactly (check 1), and the proof covers both parities plus the
  two-way NO-SOLUTION correspondence. This is what the board asked for, and it is
  the first such rule for this edge after PR #1052 removed the unsound one
  (upstream tree confirmed edge-absent).
- **The real mathematical addition over GJ.** Lemma 3 proves recovery membership
  for *every* valid target schedule, including schedules unrelated to the one the
  gadget "intends". GJ's Theorem 3.8 as quoted argues only the decision
  equivalence; it does not state the decoder obligation that the reduction
  contract imposes. This is a small but genuine strengthening, and it is exactly
  the obligation the unsound predecessor violated.
- **Negative-instance coverage.** Odd totals and even-total no-witness cases are
  both exercised and both produce infeasible targets (`cases.json`,
  `rounds/001/candidate-suite.txt`, `verification-run.txt`), which is the failure
  mode the audit found upstream. My exhaustive enumeration confirms the
  correspondence on all 2 721 small instances.
- **Not a classification.** No new complexity result is claimed and none is
  present; the closest known result, GJ Theorem 3.8, already gives the
  classification, and `1|r_j|L_max` gives an equivalent formulation. Importance
  should therefore be reported as "verified reconstruction", not as a new
  classification, which is what the campaign and the board say.
- **Scope shapers.** F4 (released-crate empty-window assertion) and the `n≤7`
  enumeration bound are the honest limits of portability and of the finite
  evidence; neither undercuts the fixed acceptance criteria.

## Required corrections before the write/formalize stage

1. `work/proof.md:87-88` — replace "`O(n)` output bits" with `O(n log n)` output
   bits (and `O(n log B)` bit operations). (F2)
2. `work/proof.md:41` and `work/proof.md:96-99` — attribute the `floor` defect to
   the AI-generated issue summary and the removed implementation, and present
   mechanism A as the faithful textbook window; add one clause to
   `work/proof.md:55-58` noting the integrality step. (F3, F1)
3. Optional, for the parent's integration planning: record F4 (released
   `problemreductions 0.6.0` rejects `r+l>d`) so a later registration uses
   mechanism B or an updated model.

Nothing above blocks expert review of the rule as it stands against the fixed
question.
