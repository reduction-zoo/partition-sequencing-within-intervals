# Partition → Sequencing Within Intervals

An independent AutoResearch campaign for one fixed reduction rule: reconstruct,
prove and independently verify deterministic polynomial-time maps `F` and `G`
between an equal-sum partition instance and a non-preemptive single-machine
sequencing instance with release times and deadlines.

- Fixed question and acceptance target:
  [campaigns/partition-sequencing-within-intervals/question.md](campaigns/partition-sequencing-within-intervals/question.md)
- Current progress, budget, capability probe and round table:
  [campaigns/partition-sequencing-within-intervals/state.md](campaigns/partition-sequencing-within-intervals/state.md)
- Workflow: [research-session](.agents/skills/research-session/SKILL.md) over the
  [reduction contract](research/reduction.md); repository layout and Git policy in
  [research/repository.md](research/repository.md)
- Provenance: the board record
  `partition-sequencing-within-intervals.json` in
  `/Users/xiweipan/Codes/autoresearch-gadgets/website/questions/`, which cites
  upstream issue <https://github.com/CodingThrust/problem-reductions/issues/205>

## Why this target

The upstream project **removed** this reduction as mathematically unsound
(PR #1052, merged 2026-04-17, following the audit in issue #1006): with the
enforcer task's release time written as `floor(S/2)`, odd total sums produce
asymmetric time blocks, so 28 of about 40 tested NO instances were wrongly
schedulable. The problem model was retained and the rule is open again, to be
re-implemented correctly from the literature (issue #205, comment of
2026-04-14). The deliverable is therefore a *correct and independently checked*
rule, not a new complexity classification.

## Status

Complete, reviewed reconstruction, awaiting expert review. The rule is
executable (`work/algorithm.py`), the general argument is `work/proof.md`, the
testing foundation and its self-test are in `work/check.py` and
`work/preparation.md`, independent verification is in `work/verify.py` and
`work/verification.md`, the independent reviews are under
`reviews/01-independent/`, and the compiled manuscript is
`work/manuscript.pdf` (source `work/manuscript.typ`).

Claim: for every legal Partition instance and every valid Sequencing Within
Intervals output of the constructed instance, recovery returns a subcollection
summing to half the total; the target is infeasible exactly when the source has no
witness. The classification is the known textbook result; the contribution is the
rule, its recovery obligation and finite evidence including infeasible instances.

Model provenance: produced by a DSH agent session on the `deepseek-flash`
route, whose catalog name in the harness is `DeepSeek-V41-Flash`.

Remaining checks: expert review. Not claimed: novelty of the classification, and
an empty-window representation compatible with the released upstream model
`problemreductions 0.6.0` (recorded in `work/proof.md`).

## Layout

| Path | Contents |
|---|---|
| `campaigns/partition-sequencing-within-intervals/question.md` | Fixed target, definitions, literature evidence, screening gates, campaign contract |
| `campaigns/partition-sequencing-within-intervals/state.md` | Claim, obligations, capability probe, round table, budget, next action |
| `campaigns/partition-sequencing-within-intervals/work/` | Current contract, cases, checkers, algorithm, proof and manuscript |
| `campaigns/partition-sequencing-within-intervals/rounds/` | One record per round with its scripts and retained evidence |
| `campaigns/partition-sequencing-within-intervals/reviews/` | Independent reviews and their checks |
| `research/experience/` | Reusable findings from this campaign |
| `harness/`, `.codex/`, `.agents/skills/` | Harness reviewer registration, reviewer configuration and the research skills |

## Reproduction

No Python project exists yet; `pyproject.toml` and `uv.lock` are added when the
testing foundation first uses Python, after which every command runs as:

```sh
uv sync --locked
uv run --locked python check.py --self-test
uv run --locked python check.py --candidate algorithm.py
```

The tool versions this machine actually provides are recorded in the capability
probe in `state.md`.
