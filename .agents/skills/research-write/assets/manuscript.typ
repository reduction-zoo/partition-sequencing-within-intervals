#import "report.typ": research-report
#show: research-report.with(
  title: "Title of the reduction theorem",
  date: "YYYY-MM-DD",
  status: "Working manuscript",
)

#heading(numbering: none)[Abstract]
State the problem, new construction, theorem and main complexity bounds.

= Introduction
Explain why the problem matters, what the closest results establish, what gap
remains and what the reduction contributes. State the main theorem and idea.

= Preliminaries
Define the source and target instance domains, valid-output sets, finite encodings
and no-solution semantics. For exact optimization, valid outputs are global optima.

= Construction
Give the deterministic forward reduction and backward output-recovery algorithm,
with structural vector figures. Introduce each
figure in the text, label the interfaces and explain omissions in its caption.

= Correctness
State and prove the supporting lemmas and composition. Establish legal target
construction $F(x) in I_B$ for every $x in I_A$, and prove
$ y in S_B(F(x)) ==> G(x,y) in S_A(x) $
for every legal source input and every valid target output. Include special
answers, alternate optimal solutions and the problem's exact output semantics.

= Complexity
Prove worst-case running-time and output encoding-size bounds for $F$ in the
source encoding length and for $G$ in the combined source and target-output length.

= Conclusion
State the classification consequence and the limitations of the result.

#heading(numbering: none)[References]
Give complete, verified primary-source references with theorem locations in text.

#pagebreak()
#set heading(numbering: "A.")
#counter(heading).update(0)
= Verification and reproducibility
Report finite evidence separately from proof. Give prerequisites and reproduction
commands, with finite instance-size bounds and no timeouts. Keep operational
history in the campaign records rather than the paper's main narrative.
