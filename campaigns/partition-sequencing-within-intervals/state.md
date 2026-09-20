# Campaign state — Partition → Sequencing Within Intervals

## Fixed target

`campaigns/partition-sequencing-within-intervals/question.md` is immutable. A
different theorem is a new campaign.

## Authorization and budget

- Authorized by the user on 2026-09-21: pick one construction-open rule from the
  board and open a campaign under `~/Codes/reduction-zoo`.
- Research round budget: **3**, the session default disclosed because the user
  gave no number. Only the user extends it.
- Any harness continuation budget (for example a DSH goal round limit or an
  auto-continuation cap) is a guardrail and never the research round count; the
  round table below is authoritative.

## Capability probe (2026-09-21)

| Capability | Actual version / provider | Path | Status |
|---|---|---|---|
| python3 | 3.14.7 | `/opt/homebrew/bin/python3` | ok |
| uv | 0.12.7 | `~/.local/bin/uv` | ok |
| git | 2.55.0, identity `Xiwei Pan` | `/opt/homebrew/bin/git` | ok |
| z3 | 5.1.0 (binary and Python module) | `/opt/homebrew/bin/z3` | ok |
| ortools | 9.15.6755 | Python module | ok |
| networkx / numpy / scipy / pulp | 3.6.1 / 2.5.3 / 1.17.1 / 3.3.0 | Python modules | ok |
| ripgrep | 15.2.0 | `/opt/homebrew/bin/rg` | ok |
| typst | 0.15.1 | `/opt/homebrew/bin/typst` | ok |
| PDF rasterizers | pdftoppm, pdftocairo, gs | `/opt/homebrew/bin` | ok |
| lean / lake | 4.34.0 / 5.0.0 | `~/.elan/bin` | ok |
| Comparator / nanoda / lean4checker | absent | — | pending; blocks final formal certification only |
| `sci-brain:how-to-technical-writing` | installed skill | `~/.agents/skills/how-to-technical-writing` | ok |
| `web_fetch` for primary sources | blocked | — | machine DNS runs in Shadowrocket fake-ip mode, so hostnames answer with RFC 2544 addresses (198.18.0.0/15) and DSH's public-fetch guard rejects them. `$DSH_HOME/.env` now sets `HTTP_PROXY`/`HTTPS_PROXY=http://127.0.0.1:1082`; takes effect after a DSH restart. Until then use shell `curl`, which routes through the system proxy |
| Primary-source access via shell `curl` | works (HTTP 200) | — | used to read issues #205, #1006 and PR #1052 on 2026-09-21 |
| Reviewer registration | DSH `research` preset, tool `research_reviewer` | `harness/dsh/presets/research` | installed; mount not yet observed in a session |

Re-probe when the environment changes and record the delta here rather than
relying on this table. The DSH restart is itself such a change: re-probe
`web_fetch` afterwards.

## Round table

| Round | Mechanism / standalone literature scope | First discriminating check | Outcome | Record |
|---|---|---|---|---|
| — | — | — | — | no rounds yet |

Planned mechanisms, each a separate round if counted: **A** corrected enforcer
window (`r = ceil(B/2)`); **B** explicit odd-sum infeasible target with the
even-`B` gadget retained. A parameter or seed change is not a new row.

## Artifacts

- `question.md` fixed; route hypotheses A and B recorded and untested.
- `work/` empty. `rounds/` empty. `reviews/` empty. `formal/` absent: no
  formalization is requested.

## Checks

None yet. Prepare owns the first testing foundation: `work/contract.md`,
`work/cases.json`, `work/check.py` with `--self-test` and `--candidate`, plus the
committed lockfile once Python is used. Cases must include NO instances for both
parities of the total, because that is the failure the removed implementation
exhibited.

## Review

None. Independent review will use the `research_reviewer` child of the DSH
`research` preset once a complete candidate with a general proof exists.

## Next action

Prepare: fix the JSON encodings of both endpoints in `contract.md`, implement the
independent source and target oracles with injected YES and NO cases, make
`check.py --self-test` pass and commit the testing foundation. Round 1 then tests
Mechanism A by exhaustive enumeration over small instances. No round may start
before that commit, and the campaign session must run with this repository as its
workspace.
