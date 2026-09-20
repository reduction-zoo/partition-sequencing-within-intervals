# Research experience

Keep one descriptive English Markdown file per reusable finding. Use ordinary
repository search to retrieve entries by structure and assumptions, for example:

```sh
rg -n -i 'YOUR_STRUCTURE_OR_ASSUMPTION' research/experience
```

## Local shared collection

The board repository keeps findings that may generalize across questions in a
local, Git-ignored collection at `research/experience/entries/`. A campaign
repository has no such directory: its local instructions record the board
repository's absolute path, and the collection is read there rather than copied.
Entries use the format below, but no admission rule is defined yet: presence
shows only that someone judged a finding possibly reusable. It is not reviewed
evidence, nothing in it is shared or published, and no standard is claimed for it.

A campaign whose writes are confined to its own directory keeps proposed entries
there and records this collection as the intended destination; promotion happens
later in a session whose workspace is the board repository. Because Git does not
track the collection, back it up separately.

Each entry states its claim, exact applicability and exclusions, evidence type
(counterexample, finite-family exclusion, general lemma or hypothesis), review
status, originating rounds and supporting files, and consequence for future
construction. It ends with a use history linking later rounds and their observed
effects. A new entry may have no subsequent uses. Record uncertainty explicitly.

Round records own observations and reflection; this directory owns only findings
that can change a future construction or research decision. Check for extraction at every round closure under
[Research Session](../../.agents/skills/research-session/SKILL.md#learn-from-rounds).
Save a qualifying finding when its applicability can be stated; otherwise record
the reason in the round. Do not require one entry per round.
Literature-derived techniques can use the same format, with primary-source
locations and a clear distinction between published facts and local deductions.

Use these short sections in each entry: **Claim and applicability**, **Evidence
and status**, **Consequence for search**, and **Use history**. Include descriptive
tags for repository search. Link the original proof, counterexample or experiment;
do not copy the full round report, raw data or bibliography. Search existing
entries first and extend the same finding rather than creating one per use.
Use history links the later round and states whether application helped, failed
or remained inconclusive; the detailed outcome stays in that round. Record in
the consuming round which finding was used and which premises were checked.

Update the relevant entry in place. Retain contradictory evidence and clearly
mark a retracted or superseded claim; do not silently leave it available for use.
Check cited evidence before applying a finding. Independent review of a candidate
must check any inherited mathematical premises on which it relies.

The collection contains research findings, not stage instructions or a transcript
archive. Keep detailed experiments in their originating campaigns and preserve
referenced evidence during cleanup. At the end of a round that used a finding,
append the round link and observed effect to its use history. Separate preventing
a known failure from producing a valid new rule. If an unresolved causal question
could change the next action, use a focused diagnostic or literature check within
the round scope; mark unresolved causes explicitly.

When writes are restricted to a campaign directory, keep proposed experience
entries there and record their intended destination as pending. At closeout,
count distinct files created, updated and pending, excluding this README. Check
that cited evidence exists; retrospective extraction must use its actual date. A lesson's existence or use does not establish
novelty, correctness or a measured improvement in discovery.

The workflow adapts [CEGIS's counterexample constraints](https://people.csail.mit.edu/asolar/SynthesisCourse2020/Lecture10.htm),
[ExpeL's experience extraction and retrieval](https://arxiv.org/html/2308.10144v3),
and [ACE's incremental experience updates](https://arxiv.org/html/2510.04618v3).
Their results do not establish effectiveness on open reduction research;
that requires comparison under matched research and computational budgets.
