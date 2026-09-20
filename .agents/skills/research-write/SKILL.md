---
name: research-write
description: Write and inspect a Typst paper from a reviewed reduction proof and its reproduction evidence.
---

# Research Write

Prepare an English manuscript and reproducible instructions for the reviewed
reduction result without introducing new mathematical claims.

Read the shared [reduction contract](../../../research/reduction.md): problems
are (I, S), and the rule is (F, G) with recovery from every valid target output.

## Inputs and boundary

Read the question, candidate proof, implementation, test reports and the latest
independent review report.
Treat the reviewed theorem and construction as the scope. Do not edit the
candidate, prepared tests, independent checks or previous reviews.

## Required writing method

Load and apply `sci-brain:how-to-technical-writing` before drafting and again for
the final language pass. Its source is
[sci-brain/skills/how-to-technical-writing](https://github.com/QuantumBFS/sci-brain/tree/main/skills/how-to-technical-writing);
resolve it through the available-skills catalog, and install it from that source
when the harness has no such skill. If it remains unavailable, report the missing
dependency rather than silently skipping it.
Apply its notation and figure guidance to the mathematical argument. Edit the manuscript directly while preserving mathematical claims and
qualifications. A substantive proof change requires
renewed independent review. Repair in the
main conversation and request review again before completing the paper.

## Paper structure and figures

Write a research paper for a complexity-theory reader, not a campaign completion
report. Start with the problem's significance, the closest known results, the
precise gap and the new contribution. Present the main theorem and construction
idea early, then develop definitions, lemmas, the reduction and its proof.
Close with the result's implications and limits. Keep command transcripts,
agent decisions, repair history and local paths out of the main mathematical
narrative; put essential experimental and reproduction details in appendices.

Use a restrained single-column mathematical-paper layout when no venue is given.
Do not imply conformity to an unnamed venue or publication readiness from layout
alone. Use consistent theorem/proof treatment, mathematical notation, numbered
cross-references, captions and a complete reference list. Do not invent authors.

For graph-gadget reductions, include structural vector figures that explain the
rigid gadget, its composition and the clause attachment when these mechanisms
are used. For other reductions, illustrate the construction where it materially
helps the reader. Never add decorative figures or a quota of unrelated images.
Draw exact graph figures from explicit vertices and edges; check their adjacency,
ports, labels and degree counts against the construction. Mark schematic drawings
and omitted edges explicitly. Use legible labels and grayscale-safe distinctions.
Introduce every figure in the text and provide a self-contained caption explaining
its symbols and the property used in the proof. Save vector assets in `figures/`.

## Deliverables

Read [the manuscript skeleton](assets/manuscript.typ) and copy it with
[the report layout](assets/report.typ) into the assigned output directory.
Write `manuscript.typ`, using `report.typ`, and compile `manuscript.pdf`.
Replace all instructional placeholder text with the reviewed result. Adapt the
section structure to the argument; retain exact definitions, the deterministic
forward algorithm, backward output recovery, complete proofs and bounds for both,
verification, related work and reproduction. Present construction and solution
recovery as one rule; state the recovery premise for every valid target output.
Include both command modes in the reproduction appendix.
Author the report directly in Typst from the reviewed research artifacts. Use
native math for every mathematical expression, including inline variables,
subscripts, sets, relations and bounds; reserve raw blocks for executable code.
Do not use a Markdown conversion as the finished report. Check attachment scope
explicitly, for example `N_(G)(v)` for a neighborhood indexed by G. Use verified
references for citations.
Do not create a parallel Markdown manuscript or reproduction report.

Include reproduction prerequisites, including the tool versions from the
campaign's capability probe, artifact paths, commands and their actual
results in the report. Refer to existing implementations rather than copying an
alternative algorithm. Never add solver, subprocess, shell or wrapper timeouts.
Keep finite instance-size limits explicit. If existing checks contain timeouts,
record the conflict and return to the responsible testing skill in this
conversation for repair; do not silently claim compliance.

Run `typst compile manuscript.typ manuscript.pdf`. Inspect every rendered PDF page for
clipped text, incorrect formula scope, unreadable notation, broken tables and
page breaks separating a formula from its setup. Compile again
after any source edit. Preserve verification results and compilation diagnostics.
Distinguish finite checks from proof and retain the reviewed certainty and
novelty qualifications. Do not invent authorship, affiliation or acceptance.

## Completion and repair

Complete writing only after the technical-writing pass, figure checks and page-by-page
PDF inspection, when the paper and reproduction appendix are complete and
consistent with the reviewed result. Fix editorial defects within this stage.
Reuse existing passing algorithm checks for editorial changes. If an algorithm
or proof change is needed, record the precise gap and repair it in the main
conversation; update affected checks and obtain renewed independent review.
Stop if the reviewed result cannot be supported. Do not publish, submit, or modify the production library.
