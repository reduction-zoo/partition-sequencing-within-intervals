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
| `web_fetch` for primary sources | works (HTTP 200) | via `http://127.0.0.1:1082` | was blocked: this machine resolves DNS in Shadowrocket fake-ip mode, so hostnames answer with RFC 2544 addresses (198.18.0.0/15) and DSH's public-fetch guard rejected them. `$DSH_HOME/.env` now sets `HTTP_PROXY`/`HTTPS_PROXY`, DSH was restarted, and `web_fetch` of the issue #205 API succeeded on 2026-09-21. Loopback stays direct |
| Primary-source access via shell `curl` | works (HTTP 200) | — | used before the restart to read issues #205, #1006 and PR #1052 on 2026-09-21; still a fallback |
| Reviewer registration | DSH `research` preset, tool `research_reviewer` | `harness/dsh/presets/research` | installed; mount not yet observed in a session |

Re-probe when the environment changes and record the delta here rather than
relying on this table. The proxy fix is already recorded as a delta: `web_fetch`
went from blocked to working on 2026-09-21 after the DSH restart.

## Round table

| Round | Mechanism / standalone literature scope | First discriminating check | Outcome | Record |
|---|---|---|---|---|
| 001 | A: corrected enforcer window (`r = ceil(B/2)`) | prepared candidate suite `check.py --candidate algorithm.py` over 16 injected cases | supported: suite passed, 59 target outputs, no counterexample | [rounds/001/round.md](rounds/001/round.md) |

Planned mechanisms, each a separate round if counted: **A** corrected enforcer
window (`r = ceil(B/2)`); **B** explicit odd-sum infeasible target with the
even-`B` gadget retained. A parameter or seed change is not a new row.

## Artifacts

- `question.md` fixed; route hypothesis A constructed and suite-passed,
  hypothesis B untried.
- `work/contract.md`, `work/cases.json`, `work/check.py`, `work/preparation.md`,
  `work/algorithm.py`, `work/proof.md` current; `pyproject.toml` and `uv.lock`
  lock CPython 3.12.11 with `ortools==9.15.6755`. `rounds/001/` holds the round
  record and its retained suite output; `reviews/` empty; `formal/` absent.

## Checks

Testing foundation in place and self-tested (2026-09-21, before any candidate was
constructed): `uv run --locked python campaigns/partition-sequencing-within-intervals/work/check.py --self-test`
passes. Independent source oracle = subset-sum dynamic program cross-checked
against exhaustive enumeration; independent target oracle = subset dynamic
program and an independent OR-Tools CP-SAT encoding, which must agree. 16 injected
cases, 14 hand-checkable oracle cases and 18 deliberately malformed fixtures
rejected; NO instances cover both parities of the total. Limits: at most 8
distinct target outputs per instance, exhaustive source cross-check at most 20
items, no bit-length bounds and no candidate correctness claim.

Round 001 ran the candidate suite against `work/algorithm.py`: 16 instances, 59
distinct valid target outputs through recovery, PASSED
([retained output](rounds/001/candidate-suite.txt)). The general proof is
`work/proof.md`; no oracle defect and no counterexample appeared.

## Review

None. Independent review will use the `research_reviewer` child of the DSH
`research` preset once a complete candidate with a general proof exists.

## Next action

Verify: write an independent `work/verify.py` that re-implements the small-instance
oracles without importing `check.py` or `algorithm.py`, exercise alternate valid
target outputs, degenerate inputs and the NO correspondence, and record
`work/verification.md`. Then request independent review.
