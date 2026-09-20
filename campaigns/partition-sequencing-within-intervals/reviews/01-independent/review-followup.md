# Follow-up review — repair of review 01 findings F1–F4

Reviewer: fresh-context DSH `subagent` spawned by the campaign parent agent with
the review charter instructions. Review directory:
`campaigns/partition-sequencing-within-intervals/reviews/01-independent/`.
Repository: `/Users/xiweipan/Codes/reduction-zoo/partition-sequencing-within-intervals`,
branch `main`. Previous review: `reviews/01-independent/review.md` (state
`9653daa`, decision ADVANCE, findings F1–F4). Repair commit: `1d2b5ae`
("Record independent review 01 and repair its four findings"). This is a scoped
follow-up: it judges the repair of F1–F4 and reuses review 01's unaffected
evidence rather than repeating it.

## Decision

**ADVANCE** — the repaired proof is eligible for expert review and for the Write
stage. F1, F2 and F3 are correctly and completely repaired; F4 is correctly
recorded as a non-theorem integration caveat; no repair weakened a claim, and the
theorem statement and its quantifiers are unchanged. One new, non-load-bearing
provenance overclaim (F5) is recorded below; it does not touch the theorem, the
polynomial obligation or the significance judgment, and I do not treat it as
blocking. It can be fixed in one sentence at the Write stage.

## Isolation mechanisms actually in force for this follow-up

| Mechanism | In force? | Evidence |
|---|---|---|
| Fresh context, no inherited conversation | yes | I am a `subagent` started by the parent with the follow-up charter; no proposer turns were visible |
| Registered reviewer tool / `toolFilter.deny` | **no** | no `research_reviewer` tool and no tool filter; the standard tool catalog is present. I spawned no agents and sent no messages |
| Delegation depth cap around the reviewer | **no** | no depth refusal is installed; non-nesting is an instruction I followed, not an enforced boundary |
| Write confinement to the review directory | **no** (instruction only) | file policy is `danger-full-access`; the sandbox does not restrict writes. I wrote only this file plus a scratch script outside the repository |
| Separate model route | **no** | no provider/model pin; the runtime reports the same `deepseek-flash` route family as the session |
| Candidate/tests/evidence immutability | checked, instruction-backed | see the hash table in §3 |

These mechanisms are **instruction-only** for this follow-up, and none of them is
evidence for or against correctness. The mathematical judgment below rests only
on the current files, the arithmetic I recomputed, and the source fetches.

## 1. Per-finding disposition

**F1 — integrality premise in Lemma 3's measure step: correctly and completely
repaired.** `work/proof.md:61-68`. The repair adds exactly the missing premise:
"Here every start and length is an integer, so every task interval has integer
endpoints; the complement of their finite union inside `[0, m) ∪ [m+1, 2m+1]`
would then be a finite union of intervals with integer endpoints, and any
non-empty such complement has measure at least `1`. The complement has measure
`0`, so it is empty and the elements occupy both blocks exactly." Checked myself:
(i) the premise is *guaranteed*, not assumed — `contract.md:22-31` requires
integer `r/l/d`, `algorithm.py:31-34` emits integer values, and `proof.md:11-14`
requires integer `σ_i`; (ii) the closure is valid because the ambient set already
starts and ends at integers (`0`, `m`, `m+1`, `2m+1`), so an integer-endpoint
cover's complement is exactly a union of integer-endpoint intervals; (iii) the
claim "non-empty such complement has measure at least 1" is the correct
integrality fact; (iv) I stress-tested the engine independently of any start-time
integrality premise on all pairwise-disjoint integer-endpoint families inside
`S = [0,m) ∪ [m+1,2m+1]` for `m = 1..5`: every family with total length `2m`
covers `S` exactly (25 cases), and all 2 016 non-covering disjoint families have
complement measure `≥ 1` (no complement of measure strictly between 0 and 1
exists). The lemma remains universally quantified over *all* feasible schedules,
so this is not a weakened claim.

**F2 — recovery output bit size: correctly and completely repaired.**
`work/proof.md:98-102`. The false "`O(n)` integer comparisons and `O(n)` output
bits" is replaced by "`O(n log B)` bit operations, because each comparison touches
numbers of bit length `O(log B)`" and "its output lists up to `n` indices, each of
bit length `Θ(log n)`, so the output is `Θ(n log n)` bits in the worst case (the
subset of all indices)". Checked: under `contract.md:12-15`/`26-27` a witness is a
strictly increasing index list, each index needs `Θ(log n)` bits, and the full
subset is a genuine valid output of the rule (e.g. `sizes=[1,2,3]` →
`subset [0,1,2]`, verified by running the unchanged candidate), so `Θ(n log n)` is
a tight worst case; `n·⌈log n⌉` is also `O(|x|)` since `|x| = Θ(n log B)`, so the
polynomial obligation still holds. Both bounds are now *weaker numerically* than
the old text, i.e. the repair strengthens the statement rather than overclaiming,
and I recomputed the growth at `n = 10, 1000, 20000` (worst-case output bits 25,
8 977, 267 233 against the `n log n` bound 40, 10 000, 300 000; forward output bits
growing as `n·log B`). The `Θ` is only ever used as an upper bound in `O(...)`
contexts, so no new overclaim arises.

**F3 — provenance attribution: correctly and completely repaired.**
`work/proof.md:37-47` (and the scope paragraph `work/proof.md:110-117`). The
overclaim "The current issue text repeats that false reading" is gone. The repair
now (a) locates the floor reading in "the issue's AI-generated summary and in the
removed implementation (PR #1052's deleted text used `h = ⌊S/2⌋` with enforcer
`r = h`, `d = h + 1`)" and (b) presents the ceiling as forced by the quoted text
itself, (c) states "Mechanism A is therefore the textbook window transcribed
correctly, not a correction of the textbook". I verified this against the live
source: the GitHub API body of issue #205 (fetched 2026-09-21) contains the
warning-tagged "Unverified: AI-generated summary" with `r(t̄) = ⌊B/2⌋`,
`d(t̄) = ⌈(B+1)/2⌉`, while the quoted theorem text uses `r(t̄) = [B/2]`,
`d(t̄) = [(B+1)/2]` and asserts "Since B is even, r(t̄) = B/2 and
d(t̄) = r(t̄) + 1". I recomputed the bracket rule for all `B = 2..100`: the floor
convention fails the even-`B` assertion (never gives `d = r+1`), the ceiling
convention satisfies it, and only the ceiling convention makes the odd-`B` line
`r(t̄) = d(t̄)` true. So the repair's attribution and its derivation are correct.
The repaired scope paragraph no longer misattributes the defect to the textbook,
so the novelty framing F3 protected is intact.

**F4 — integration caveat: correctly recorded, and correctly scoped outside the
theorem.** `work/proof.md:119-126`. The caveat is stated as "recorded but not part
of the theorem", names the released model `problemreductions 0.6.0`, states the
precise failing assertion `r + l ≤ d`, offers the two escapes (mechanism B or a
model change), and closes with "This does not affect `G(x, y) ∈ S_A(x)` for the
fixed endpoints". I re-verified both source claims from review 01:
`docs.rs/crate/problemreductions/0.6.0/.../sequencing_within_intervals.rs` (HTTP
200) still `assert!(sum <= deadlines[i], "… time window is empty")` in `new`
(i.e. panics on `r+l > d`), while upstream `main`
(`raw.githubusercontent.com/CodingThrust/problem-reductions/main/...`) now returns
`Ok(0)` from `start_slot_count` when `latest_start < release` and documents "If
this range is empty, the instance is infeasible". Odd `B` gives `r̄ = d̄ = ⌈B/2⌉`
(verified: `B = 11` → `r̄ = 6`, `d̄ = 6`), so the caveat is real and the theorem is
untouched by it. No escape is needed for the fixed JSON encoding.

**No repair weakened a claim.** `proof.md:71-74` (theorem statement) and
`proof.md:107-117` are unchanged in substance between `9653daa` and `1d2b5ae`; the
scope paragraph still claims only "the textbook local-replacement plus enforcer
gadget … with … the recovery obligation proved for every valid target output",
still claims no originality, and `proof.md:128-131` still declares malformed
target solutions out of scope. F2's numbers grew (honest weakening of a bound),
F1 added a true premise, F3 corrected an attribution; nothing became stronger than
what the argument supports except the point recorded as F5.

## 2. New finding

**F5 — the repaired provenance sentence presents a derived reading as a fact
about the source text (minor; provenance framing only).**
Location: `work/proof.md:42-45` — "The quoted Garey & Johnson text is
self-consistent and already forces the ceiling: for even `B` it asserts
`d(t̄) = r(t̄) + 1` with `r(t̄) = [B/2]`, which requires `[(B+1)/2] = B/2 + 1`,
that is `[x] = ⌈x⌉`; for odd `B` both brackets then round up and `r(t̄) = d(t̄)`."

Missing premise: the quotation never defines the bracket operation `x ↦ [x]`, and
the Garey & Johnson book remains unavailable (review 01 §2 could not fetch it), so
"that is `[x] = ⌈x⌉`" is not a reading of the source notation but an inference
that the quoted *formulas* are mutually consistent only under the rounding-up
convention. The inference itself is correct — I verified computationally that only
`[x] = ⌈x⌉` satisfies the three constraints for all `B = 2..100` — but as written
the sentence asserts the bracket semantics as established fact. (Same drafting
point: "both brackets then round up" misdescribes `r(t̄)`, which under either
convention is already an integer for odd `B`; the conclusion `r(t̄) = d(t̄)` is
nevertheless correct.) Severity: the claim carries no theorem content — the
corrected window is independently re-derived in Lemma 2, and the scope paragraph
only uses the textbook as the origin of the gadget — so nothing downstream depends
on it. Required correction for the Write stage: reword to say that the quoted
formulas are mutually consistent only under `[x] = ⌈x⌉`, without asserting that
reading as verified source notation. This does **not** warrant a revise decision
and does not affect the advance.

## 3. Unchanged candidate/tests/evidence (so review 01's results still apply)

`git diff --name-status 9653daa 1d2b5ae` lists exactly five paths: the three new
`reviews/01-independent/` files, `state.md`, and `work/proof.md`. The candidate,
the prepared suite, the verification script and every evidence file are byte-identical
across the two commits and in the worktree (Git blob hashes compared three ways):

| Path | 9653daa | 1d2b5ae | worktree |
|---|---|---|---|
| `work/algorithm.py` | identical | identical | identical |
| `work/check.py` | identical | identical | identical |
| `work/verify.py` | identical | identical | identical |
| `work/cases.json` | identical | identical | identical |
| `work/contract.md` | identical | identical | identical |
| `work/preparation.md` | identical | identical | identical |
| `work/verification.md` | identical | identical | identical |
| `work/evidence/verification-run.txt` | identical | identical | identical |

`git status --porcelain` was empty before I wrote this file. Consequently review
01's executed evidence still stands and is reused here: the implementation ↔
construction agreement on 2 810 instances; the exhaustive confirmation over
2 721 small instances / 378 670 valid target schedules that the enforcer is pinned
and `Σ_{i∈W} s_i = B/2`; the feasibility ↔ witness correspondence for both
parities; the candidate-recovery agreement on 420 reviewer-constructed schedules
plus 280 `no_solution` answers; and the retained campaign suites
(`rounds/001/candidate-suite.txt`, `work/evidence/verification-run.txt`). The
`n ≤ 7` enumeration bound and the campaigns' own bit-length disclaimers
(`preparation.md:70-75`, `verification.md:50-68`) are unchanged and still the
honest limits of the finite evidence.

## 4. Correctness/novelty/significance after the repair (reusing evidence)

- **Correctness — still supported.** The theorem (`proof.md:71-89`) and its
  quantifiers are unchanged; the only proof text that changed is Lemma 2's
  provenance paragraph, Lemma 3's closure step, the recovery-bounds paragraph and
  the scope/limits sections. The three repaired passages were the only defects
  review 01 found, and §1 above verifies each repair and its arithmetic. The
  recovery map is still proved for *every* valid target output, including the
  `no_solution` case and schedules not intended by the gadget.
- **Novelty — unchanged.** The repaired text no longer misattributes the defect to
  the textbook and still claims no new classification; the theorem remains Garey &
  Johnson `[SS1]` Theorem 3.8, as the upstream `main` model documentation also
  states (re-fetched, HTTP 200: "This is problem SS1 from Garey & Johnson (1979),
  NP-complete via Theorem 3.8"). F5 is a provenance nuance and not a novelty
  claim.
- **Significance — unchanged.** The board's reconstruction criteria are still met
  for the same reason as review 01: executable deterministic F and G, a general
  proof, negative-instance coverage, and the recovery obligation for every valid
  target output as the addition over GJ's decision proof. F4 remains an honest
  portability limit, now recorded in the document itself rather than only in the
  review.

## 5. Checks run for this follow-up

Script: `/tmp/followup_checks.py` (scratch, outside the repository; imports
neither `algorithm.py`, `check.py` nor `verify.py`). Command:
`python3 /tmp/followup_checks.py`.

- **F1 engine, integrality-independent.** All pairwise-disjoint integer-endpoint
  interval families (size 1–3) inside `[0,m) ∪ [m+1,2m+1]` for `m = 1..5`:
  25 families with total length `2m` occupy both blocks exactly; all 2 016
  non-covering families have complement measure `≥ 1`. No counterexample to the
  closure step, and no dependence on an integrality premise for the *starts*.
- **F2 arithmetic.** Recomputed worst-case recovery output bits at
  `n = 10/1000/20000` (25 / 8 977 / 267 233, all `≤ n⌈log n⌉ = 40 / 10 000 /
  300 000`) and the forward output growth `n·log B`; both within `|x|` and
  `|x| + |y|` polynomially.
- **F3 bracket rule.** For every `B = 2..100`: floor fails the quoted even-`B`
  assertion `d(t̄) = r(t̄) + 1`, ceiling satisfies it, and only ceiling makes the
  odd-`B` line `r(t̄) = d(t̄)` true.
- **Candidate spot checks** (unchanged code, independent of the repairs, to
  confirm recovery still emits the tight worst-case subset and the negative
  answer): `{"sizes":[1,2,3]}` → enforcer `{r:3,l:1,d:4}`; the explicit schedule
  `start [0,1,0,3]` → `{"subset":[0,1,2]}`; `{"no_solution":true}` →
  `{"no_solution":true}`.
- **F4 source re-verification.** `web_fetch` of the 0.6.0 docs.rs source (panic on
  `r+l > d`) and of upstream `main` (`start_slot_count` → `Ok(0)`); both HTTP 200
  on 2026-09-21.
- **Provenance/attribution source.** `web_fetch` of the GitHub API issue #205 body
  (HTTP 200) to confirm the floor reading sits in the warning-tagged AI summary
  and that the quoted text uses `[B/2]`, `[(B+1)/2]` with
  `d(t̄) = r(t̄) + 1` for even `B`.
- **Immutability.** The three-way blob-hash table in §3, plus
  `git diff --name-status 9653daa 1d2b5ae`.

## 6. What I could not check

- The Garey & Johnson book text itself (page 70, the bracket definition, the
  exact wording of Theorem 3.8) is still not available here, so F5's point stands
  unresolved and the ceiling convention remains established by re-derivation, not
  by the source.
- The Lenstra–Rinnooy Kan–Brucker pointer in review 01 §2 remains unconfirmed at
  source; it is not used by the repaired passages.
- Above `n = 7` the recovery claim still rests on the general proof, not on
  enumeration, exactly as review 01 recorded.
- No formal proof assistant was used; F1's closure step is checked by the argument
  above plus the exhaustive engine probe, not by a machine-checked proof.
