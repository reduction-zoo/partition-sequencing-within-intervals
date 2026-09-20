# Screening open research questions

The objective is to resolve open mathematical questions through original
deterministic algorithms, reductions, and their proofs. Research results,
proof attempts, counterexamples, and verification evidence belong in each
independent question repository. Existing production models, edges, and overheads do not define the
research agenda. Every selected question must nevertheless target an original
deterministic polynomial-time reduction algorithm. Existing
library interfaces and immediate integration value are not
mathematical admission requirements; new endpoint problems are allowed.
Actual production changes are a separately authorized later step.

Write every research artifact in English. Literature-based selection uses the
board's `website/questions/<slug>.json` and its question-record template. Search
existing records before adding one; retain dated literature evidence and coverage
in the existing fields. Follow the [repository boundary](repository.md#selection-and-research-boundary)
before writing tests, searching constructions or attempting a proof, including
screening probes. The independent repository uses [question.md](question.md) for
its fixed campaign question and owns all subsequent research history.
A screening decision supports an attempt; it does not establish a theorem or
guarantee that a problem is solvable within the budget.

## Generate candidates from mathematical literature

Start with explicitly stated open questions or conjectures in primary papers,
and precise gaps between established theorems. For an inferred gap, explain
which results leave it unresolved; absence of a search result is insufficient.
Prefer directions where existing techniques approach the target closely enough
to identify a focused missing argument. Do not select a subject merely because
it is called parameterized complexity, or because a library lacks an edge.

Use Web and arXiv by default. Search the field, synonymous and equivalent
formulations, historical progress, and negative results. Hugging Face paper
search is supplementary when relevant. For each promising direction:

1. Read the original question and definitions in the primary source.
2. Trace subsequent versions, journal publications, and follow-up results.
3. Compare the exact hypotheses and conclusions of the strongest known results.
4. Identify one unresolved statement and a concrete possible proof mechanism.

Current-library overhead optimization is not the present selection objective.
Implementations of known constructions may become separate production tasks;
they do not qualify as discoveries here.

## Apply six gates in order

Record `pass`, `hold`, or `reject`, with evidence in the screening assessment.
Stop at the first blocking gate; mark later gates `not assessed`. Missing decisive
evidence means hold. These judgments are not additional website status fields.
A literature-backed board question may have an untested route; all six gates
are required for the evidence-backed moderate-difficulty shortlist, not listing.

### Gate 1 — Precise mathematical question

Fix the objects, complete input domain, quantifiers, hypotheses, and conclusion.
Distinguish proving a conjecture from settling it in either direction. Specify
in advance whether a counterexample or a negative theorem qualifies as success.
Specify Π_A = (I_A, S_A) and Π_B = (I_B, S_B), finite input/output encodings,
resource bounds and the valid-output semantics from the [reduction contract](reduction.md).
Seek a deterministic pair (F, G) proving that every valid output of F(x) recovers
an output in S_A(x). State no-solution behavior explicitly. Decision, search and
exact optimization problems are eligible. For optimization S(x) consists of all
optimal solutions; do not replace this with threshold feasibility unless that is
the selected question. Neither a bijection nor equal objective values is required.
The construction and recovery algorithms must not call a solver themselves.

Pass a precise open target whose positive result is a reduction algorithm under
the stated notion. Hold unspecified endpoints, preservation conditions, or
resource bounds. A completed construction is the research goal, not an admission
prerequisite. Structural lemmas may support it, but a standalone structural
conjecture without a reduction target does not qualify. A proved impossibility
under the fixed notion may be a qualifying negative outcome if specified in
advance; it is not itself a reduction algorithm. Library API compatibility and
solution extraction beyond the chosen definition are later implementation concerns.

### Gate 2 — Applicable known results

Compare primary theorems under matching hypotheses, representations, and
semantics. Record strongest applicable algorithms, constructions, lower bounds,
and general results that could imply the target. Substitute parameters through
compositions; account for numeric growth and witness premises when applicable.

Pass a precise difference from cited results. Hold an unexamined decisive
implication. Reject a target already established by known results. A known
counterexample rejects a request to prove that false statement; it also means
that a request to settle the statement is already resolved.

### Gate 3 — Supported openness

Search exact statements, aliases, equivalent formulations, updates, precursors,
and failed approaches. Read theorem statements and relevant proofs rather than
relying on abstracts. Record search dates, actual queries, primary URLs,
versions, theorem/page locations, and the effect of each result.

Pass only with evidence that the exact question remains unresolved within the
recorded coverage. Hold inaccessible decisive sources, empty-search evidence,
or missing update checks. Reject known or immediately implied answers. A pass
is not proof that no unpublished or overlooked solution exists.

### Gate 4 — Mathematical significance

Explain what resolving the question would establish: a new structural fact,
constructive mechanism, algorithmic guarantee, or boundary of possibility.
Specify the weakest result that meets the question's acceptance criteria.

Pass a substantive mathematical contribution. Hold unsupported significance.
Reject porting, bookkeeping, or direct reuse of known results presented as
novel research. A known generic SAT/ILP encoding can be a valid reduction while
failing research novelty; do not conflate these judgments. Explain the new
complexity-theoretic consequence without requiring immediate library utility.

### Gate 5 — Plausible proof route

Identify the strongest usable lemmas, the precise remaining obstacle, and at
least one mechanism for overcoming it. Explain why the work appears focused
rather than dependent on several unrelated breakthroughs. Name likely failure
modes and what evidence would invalidate the approach.

Pass a concrete route to a general argument. Hold an unexplored mechanism.
Exclude from the moderate-difficulty shortlist a target whose only route is
unstructured search or an unrelated major breakthrough. This is a feasibility
judgment, not a mathematical impossibility claim.

### Gate 6 — Bounded initial investigation

This gate is research. Establish the independent repository and commit the fixed
question and starting state before the probe, following [repository.md](repository.md).
Use the session round budget and records; retain failures in this same repository
whether or not the question is admitted to the shortlist.

Specify a finite construction family or a bounded proof exercise, resource
limits, exact checks, and the observation sought. Execute the initial
investigation before admitting a candidate to the moderate-difficulty shortlist.
Record what happened and what remains uncertain. A useful outcome may be a
proved intermediate lemma or a counterexample narrowing the approach; successful
small instances are not required and do not establish a general result.

Pass when actual evidence supports a remaining proof route and independent
verification is feasible. Hold an unexecuted or inconclusive investigation.
Reject this approach when the experiment refutes it; keep the mathematical
question's status separate. Exhausting bounded synthesis excludes only its
stated family. A changed target needs a separately screened candidate.

## Reporting difficulty and importance

Report these two dimensions separately, using the evidence from Gates 4–6.
They are research judgments, not theorem claims or additional admission gates.

- **Difficulty:** low means a concrete route has only localized remaining proof
  obligations supported by investigation; moderate means a focused new gadget or
  lemma is needed and bounded work supports a plausible route; high means major
  obstacles or several unsupported mechanisms remain. Use uncertain when the
  investigation cannot support a rating. Assess discovery and proof difficulty,
  not the runtime of the resulting reduction or the size of an example gadget.
  Name the main obstacle, relevant failed attempts and what would change the
  assessment. Do not infer moderate difficulty merely from a one-parameter gap,
  a short problem statement or successful small instances. Do not invent success
  probabilities or completion times without evidence.
- **Importance:** high requires a clearly justified broad consequence, such as
  completing a natural classification or establishing a broadly applicable new
  reduction mechanism; moderate can resolve a substantive named boundary or open
  case; limited describes a narrow consequence without demonstrated broader reach.
  Use uncertain when significance has not been established. State the precise
  mathematical consequence, its scope and why existing results do not imply it.
  Explicit mention as an open problem is evidence of interest, not automatically
  high importance. A new library edge, a different NP-complete source, or generic
  encodability alone does not establish research significance.

Attach the supporting facts and uncertainty to each rating. Use not assessed
when an earlier gate blocked assessment. Recommendations must explain the
tradeoff: an accessible candidate need not be the most important one, and an
important candidate may remain too difficult to admit. Do not hide either
dimension behind a combined score. Label holds separately from admitted topics,
and account for overlap before claiming multiple contributions or ranking topics.

## Exploratory admission

For an authorized exploratory campaign, distinguish research eligibility
from route readiness. Gates 1–4 still establish the exact target,
known-result boundary, supported openness and significance. Gates 5–6 may remain
on hold when opening an exploratory campaign: finding and testing a mechanism
is its work, not a prerequisite. Preserve those assessments honestly; do not
relabel the topic as an all-pass moderate-difficulty candidate.

For definition or literature holds, resolve the specific missing premise using
primary sources and record the outcome on the existing card. Such work is not
an algorithm-discovery round or a new proof. If it remains externally blocked,
state the missing source or definition; do not classify the mathematical route
as exhausted. Known-result and scope exclusions remain outside the exploration
queue unless contrary evidence changes their classification.

Once eligible, establish the repository and initial commit before Prepare, then
establish tests and make substantive construction
attempts under the existing round budget. A failed screening baseline alone
cannot discharge this obligation. Apply the Research Session
[exit assessment](../.agents/skills/research-session/SKILL.md#justify-early-exit)
before stopping for lack of progress. Report actual mechanisms and evidence,
not just rounds or an uncalibrated probability. Never relabel historical probes
as newly executed rounds or restart their unchanged search families.

## Selection and proof campaign

Only all-pass candidates enter the moderate-difficulty shortlist. The authorized
exploratory admission above is a separate admission path. Rank by mathematical
significance, strength of openness evidence, and specificity of the proof route.
Group overlapping candidates; do not fill a quota with cosmetic variants or
holds. Return fewer than ten if fewer qualify. The next milestone is one
supported candidate followed by a real proof attempt.

Reuse the repository and campaign established for the initial investigation.
For exploratory admission without a prior probe, create them and commit the
question before Prepare. Carry the literature evidence into the campaign question
and establish the testing foundation, then conduct counted
research rounds under [Research Session](../.agents/skills/research-session/SKILL.md#research-rounds-and-topic-budget).
Propose and Verify share the main conversation; complete candidates receive
independent review before writing. Record the finite round allocation before
starting, and return to topic selection when the allocation is exhausted or the
Research Session exit assessment supports stopping. Do not repeat screening at each round.
New assumptions or conflicting literature require targeted checks during research.
The review stage assesses novelty and significance of the actual theorem proved.

During discovery, develop a general proof and deterministic construction where
applicable. Preserve failed approaches, counterexamples, and exact commands.
Do not weaken the question to obtain success. Review correctness, novelty, and
significance separately; checkers must not import candidate implementations.
Finite checks and agreement between agents cannot replace proof.

A completed result must meet the fixed statement, supply general reasoning and
applicable time/encoding bounds, survive independent checks, and undergo a fresh
literature review. Report intermediate lemmas as partial results. No qualifying
result is an honest campaign outcome. Keep research in the independent question repository; consider
production integration only after a result is mature and separately authorized.
