# DSH harness setup

`presets/research/` holds one DSH agent preset for the AutoResearch flow:

- `agent.cordis.yml` — the composition, derived from the shipped `standard`
  preset of DSH 0.1.5-rc.2;
- `preset.yml` — its display name and description in the preset picker.

It differs from `standard` in four ways:

1. the persona names a research agent rather than a coding agent;
2. every delegation tool carries `maxDepth: 1`, so the parent may start one
   level of child and no child may start another;
3. a second `tool-subagent` instance, `research_reviewer`, carries the reviewer
   charter from `.agents/skills/research-review/SKILL.md`, is denied every tool
   that could reach or start another agent, and cannot nest;
4. no `tool-ralph` row, because a fresh child per round contradicts this flow's
   single persistent session.

`workflow` stays mounted: `find-open-problems` legitimately fans out across
candidate records, and a workflow run is not the campaign conversation.

## Install

Choose one of these. Only one should be active for the id `research`.

**Copy into the writable preset root.** Discovery skips a preset directory that
is a symbolic link, so copy rather than link; re-copy after editing this
repository.

```sh
mkdir -p "$DSH_HOME/.agent-presets"
cp -R harness/dsh/presets/research "$DSH_HOME/.agent-presets/research"
```

**Or keep this checkout as the live source.** Add the directory as a
`system`-trust preset root in `$DSH_HOME/cordis.patch.yml` (or the profile's own
`cordis.patch.yml`). A patch replaces the targeted row's whole `config`, so the
existing `default` must be restated, and `trust: system` keeps the writable
`<dshHome>/.agent-presets` root as the target for presets you author in the app:

```yaml
- id: agent-presets
  config:
    default: standard
    roots:
      - path: /absolute/path/to/autoresearch-gadgets/harness/dsh/presets
        trust: system
```

Either way the preset appears in the preset picker of a new session. A session
cannot switch preset once it has produced anything, so choose `Research` when
the session starts, or set the default for new sessions in
`$DSH_HOME/settings.yaml`:

```yaml
agent-presets:
  default: research
```

## Use it for a campaign

Start the campaign session with the campaign repository as the working
directory. DSH loads `AGENTS.md` and `.agents/skills` from that repository, and
under `workspace-write` the session workspace is the only writable root, so the
board session that selects a question and the campaign session that researches
it are usually two sessions. See the [harness contract](../README.md#session-workspace-and-file-policy).

`research_reviewer` is the reviewer registration. Give it the fixed question,
the current artifact paths, a new review directory under `reviews/`, and the
previous findings when review follows a repair. It runs as a continuable child,
so a follow-up review can steer the same reviewer — which the review charter
asks for — and the parent is told when a run settles.

To review on a different model than the proposer, pin the route on that row:

```yaml
    - id: tool-subagent-research-reviewer
      name: '@deepseek-ai/dsh-tool-subagent'
      config:
        provider: spawn
        toolName: research_reviewer
        backgroundMode: continuable
        maxDepth: 1
        agentOptions:
          provider: <provider id>
          model: <model id>
        # …persona and toolFilter as in the composition
```

Record the route actually used in `review.md`; a different model is not by
itself independence.

## Limits

- `toolFilter` is name-level. The reviewer keeps `write` and `edit` because it
  must author `review.md`; "write only in the assigned review directory" stays an
  instruction, while delegation is refused structurally.
- A preset is a snapshot. DSH has no "standard plus one change" layer, so
  re-derive `agent.cordis.yml` after a DSH upgrade from the installed
  `@deepseek-ai/dsh-agent-presets/presets/standard/agent.cordis.yml`.
- A running session keeps the composition it started with. Changing the
  composition file affects the next session, not the current one.

## Verification status

Checked against DSH 0.1.5-rc.2: the composition parses, is a top-level list of
named rows, every named plugin resolves, the roster reports no `broken` verdict,
and `--dump-config --patch` accepts the `roots` snippet above without losing
`default`. Mounting the preset and the reviewer's tool filter are asserted from
the shipped `standard` composition plus the `dsh-subagent` source, not from a
live research session; the first campaign should confirm three observations: the
session offers `research_reviewer`, the reviewer's tool list has no `subagent`,
`subagent_fork`, `workflow`, `send_message`, `list_agents`, `interrupt_agent` or
`ask_user_question`, and a nested spawn attempt is refused for exceeding
`maxDepth`.
