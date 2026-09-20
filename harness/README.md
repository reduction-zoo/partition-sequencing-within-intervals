# Harness contract

The AutoResearch skills describe responsibilities, evidence and stopping rules.
They are harness-neutral: they assume the capabilities below and leave session,
delegation and reviewer registration to the harness that runs them. This
directory holds those registrations. Codex and DSH are both supported; a new
harness is added by supplying the same registration, not by rewriting a skill.

Keep every skill, specification and template harness-neutral. A harness name
belongs in this directory or in an example, never in a rule the research depends on.

## Required capabilities

| Capability | Why the flow needs it | Codex | DSH |
|---|---|---|---|
| Load `.agents/skills` from the project root | The skills are the flow's instructions | native | `dsh-skill-filesystem` (project root = nearest `.git`) |
| Read the repository instructions (`AGENTS.md`) | Local research contract | native | `dsh-agent-instructions` |
| Filesystem, shell, Git, `uv` | Campaign repository, rounds, commits, locked environments | yes | yes |
| Web and arXiv access | Openness and novelty checks | yes | `web_search`, `web_fetch` |
| One persistent session with a finite round budget | The campaign is one continuous conversation | conversation | session, plus goal rounds as a guardrail |
| An independent subagent with a fresh context | Review must not inherit the proposer's reasoning | native subagents | `subagent` (`spawn`); `subagent_fork` is not acceptable for review |
| A reviewer registration fixing charter and limits | See below | `.codex/agents/research-reviewer.toml` | `harness/dsh/presets/research/agent.cordis.yml` |
| Typst, Lean/Mathlib/Lake, [`sci-brain:how-to-technical-writing`](https://github.com/QuantumBFS/sci-brain/tree/main/skills/how-to-technical-writing) | Write and Formalize | environment | environment (skill roots) |

A missing capability blocks only the work that needs it: report it as pending
work, never as a successful check. Missing review is never replaced by
self-review, and a missing solver is never replaced by an LLM oracle.

## Reviewer registration

Both registrations are thin wrappers. The reviewer's charter is
[Research Review](../.agents/skills/research-review/SKILL.md); the registration
only decides how the reviewer is started and what it may touch. A registration
must provide:

1. a fresh context, with no inherited conversation;
2. no ability to modify the candidate, the prepared tests or earlier evidence;
3. no ability to delegate to further agents;
4. writes confined to the review directory the parent assigns;
5. optionally, a different model route than the proposer's, recorded in `review.md`.

- **Codex** reads `.codex/agents/research-reviewer.toml`, whose
  `developer_instructions` point at the same charter.
- **DSH** mounts a second `tool-subagent` instance named `research_reviewer` in
  the `research` agent preset. Its `persona` carries the same pointer,
  `toolFilter.deny` removes every agent-spawning tool, and `maxDepth: 1` makes
  nesting structurally impossible: the parent may start the reviewer, and the
  reviewer may start nothing. See [harness/dsh](dsh/README.md).

Instructions alone are the weakest form of this contract. Prefer a harness
mechanism (tool denial, a depth cap, a sandbox) whenever one exists, and state in
`review.md` which mechanisms were actually in force.

## Session workspace and file policy

The repository standard puts the campaign repository outside the board repository.
A harness that bounds writes by the session workspace therefore needs one of:

- the campaign repository as the session's workspace root (recommended: the copied
  `.agents/skills` and local `AGENTS.md` then load from the campaign repository), or
- an explicit grant covering the destination, or
- a wider file policy for that session, which the user authorizes deliberately.

Reading the board to choose a question and writing the campaign are separate
sessions when the harness cannot cover both paths at once. Record the boundary in
the campaign README rather than discovering it at the first denied write.

## Budgets and interruptions

The round table in the campaign's `state.md` is authoritative for research
rounds. A harness continuation budget (for example DSH goal rounds) only limits
automatic continuation: it is a guardrail, not the round count, and the two
numbers are reported separately.

A harness-imposed execution limit that kills a run — a tool timeout, a stopped
background job, a closed session — is an execution failure. Record it as such,
after committing the partial state; it is not an oracle answer and it does not
exhaust a search family. Do not convert harness limits into research conclusions.
