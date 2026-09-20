# Local research instructions

This repository is one AutoResearch campaign for the fixed question in
`campaigns/partition-sequencing-within-intervals/question.md`. It is not the
website board: the board repository's website-only `AGENTS.md` does not apply
here.

Run the workflow from [research-session](.agents/skills/research-session/SKILL.md)
and read the shared [reduction contract](research/reduction.md). Load Prepare,
Propose, Verify, Review, Write and Formalize only when their responsibility is
needed. Keep the question and acceptance criteria fixed; a different theorem is a
new campaign.

- Write all repository content in English.
- Keep algorithms, proofs, tests, round records and reviews under
  `campaigns/partition-sequencing-within-intervals/`. Follow
  [research/repository.md](research/repository.md) for layout, artifact
  ownership and the Git policy: create no research artifact before the initial
  commit, commit the testing foundation before constructing a candidate, commit
  every completed round including failures, and never rewrite or fabricate
  history.
- Derive oracles from the problem definitions, prefer a mature solver, and never
  let the oracle import the candidate. Unknown, numerical ambiguity and
  execution failure are not NO. **Infeasible (NO) instances are mandatory test
  cases here**: the removed upstream implementation passed YES-instance tests and
  failed NO instances.
- Use finite instance or search-family bounds. Never add solver, subprocess,
  shell or wrapper timeouts, and never add wall-clock limits to a check.
- A harness-imposed limit that kills a run is an execution failure to record,
  not an oracle answer.
- Missing capability is reported as pending work, never as a successful check.
- Reusable findings go in `research/experience/`. The board repository keeps a
  local, uncommitted cross-question collection at
  `/Users/xiweipan/Codes/autoresearch-gadgets/research/experience/entries/`:
  read it there, do not copy it into this repository, and treat presence there
  as no evidence.

## Harness

This campaign runs under DSH. The reviewer registration is
[harness/dsh](harness/dsh/README.md); the independent reviewer is the
`research_reviewer` child of the `research` agent preset, installed at
`$DSH_HOME/.agent-presets/research` and selected when the campaign session starts
(a session cannot change preset after it has produced anything). Codex would
instead read `.codex/agents/research-reviewer.toml`.

Network note: this machine resolves DNS in a fake-ip range, so DSH's
`web_fetch` public-address guard rejects hostnames until DSH runs with
`HTTP_PROXY`/`HTTPS_PROXY` set (see `$DSH_HOME/.env`). Until DSH is restarted
with that file in force, fetch primary sources with `curl` from the shell, which
routes through the system proxy, and record the method used.
