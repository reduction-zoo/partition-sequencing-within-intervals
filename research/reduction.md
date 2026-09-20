# Reduction contract

A computational problem is a pair Π = (I, S). The set I contains its legal,
finitely encoded instances. For each x in I, S(x) is the set of valid, finitely
encoded outputs. A solver may return any member of S(x).

For a decision problem, S(x) contains the correct YES or NO answer. For a search
problem, it contains the valid witnesses. For an exact optimization problem,
S(x) = OPT(x), the set of all optimal solutions, not merely feasible solutions
or objective values. An optimal-value problem can be defined separately.

Specify behavior on instances with no witness or no optimum. Either restrict I
to instances for which the requested output exists, or include explicit valid
outputs such as NO-SOLUTION or INFEASIBLE where appropriate. On the admitted
input domain, S(x) must be nonempty. This prevents a correctness claim from
holding vacuously when the target solver has no valid output. Special outputs
are semantic answers, not solver execution errors. Unknown is not an answer.

## One rule, two algorithms

A reduction from Π_A to Π_B consists of deterministic polynomial-time algorithms:

- F maps each x in I_A to a legal instance F(x) in I_B.
- G maps the source instance x and a valid target output y to a source output.

The correctness obligation is

$$
\forall x\in I_A,\quad\forall y\in S_B(F(x)),\quad
G(x,y)\in S_A(x).
$$

Thus any correct solver for B yields a correct solver for A: construct F(x),
solve that instance, and apply G to its output and x. F and G do not themselves
call a solver or depend on runtime randomness or LLM decisions. The rule need
not preserve objective values, enumerate all source solutions or give a bijection.
For optimization, every optimal target solution must recover an optimal source
solution, including ties. No guarantee for nonoptimal target solutions is implied.
For decision problems, decode either answer through G; do not require the raw
source and target answers to agree unless the specific theorem requires it.

Measure F in |x| and G in |x| + |y|, using the specified finite encodings. Prove
polynomial worst-case runtime and output length for both maps. Account for the
bit cost of arithmetic. Exact real outputs require an explicit representation;
abstract real coordinates alone do not define an executable contract.

## Evidence

Testing injects x, executes F, independently obtains y in S_B(F(x)), executes G,
and checks membership in S_A(x). Compare the recovered answer with independent
source ground truth. For optimization, check feasibility and global optimality,
including alternate target optima. For decisions, test YES and NO; for search,
test distinct witnesses and the specified no-solution behavior. Do not compare
raw answers or objective values across different problems without a proved reason.

A general proof establishes output legality and the recovery implication for all
legal inputs and all valid target outputs. Finite tests, formal statement checking,
implementation agreement, novelty and significance are separate evidence scopes.
Existing question-specific claims remain fixed when adopting this contract.

## Literature context

This instance-map and solution-decoder structure is established in complexity
theory. Fenner et al., *Complements of Multivalued Functions*, Definition 2.2,
define metric many-one reducibility through polynomial preprocessing and
postprocessing whose possible outputs refine the source multivalued function.
The definition includes domain conditions. We call the contract above simply
“reduction”; no new reduction name or acronym is introduced.

- https://cse.sc.edu/~fenner/papers/coNPMV.pdf
- https://www.cs.ox.ac.uk/people/paul.goldberg/papers/STOC2021-FGHS.pdf

Primary sources checked 2026-09-17. The second reference is a concrete use of
search reductions in the complexity of gradient descent, not a claim that
stationary points are global optima.
