# Research repository standard

Each selected question is investigated in its own Git repository from the start.
The board repository distributes question briefs and reusable skills; it does not
host campaign execution or proof artifacts. Write repository content in English.

## Selection and research boundary

During literature-based selection, keep each retained question in the board's
`website/questions/<slug>.json`, using its existing template. Record definitions,
importance, difficulty, dated literature evidence and coverage there. Reading
papers, comparing known theorems and proposing a route do not require a separate
research repository. An untested route must remain identified as untested.

Before writing tests, searching constructions or attempting a new proof, create
the independent repository and initial commit below. This includes a small probe
used to assess a candidate during screening. Reuse the same repository if the
question is selected for further work. Keep unsuccessful attempts there too.
The board remains the question catalog; synchronize supported assessments and
solution metadata without copying research logs or adding screening-only fields.

## Start before Prepare

Use the user's chosen location outside the board repository. Before creating
files, resolve the destination path and confirm it is neither the board repository
nor a directory inside it; a nested `.git` does not satisfy this requirement.
If no location is supplied, use a sibling directory of the board repository,
named after the question's stable slug. State the chosen path before creating it.
If that path already exists, inspect it; resume only if it belongs to the same
question, otherwise ask for a different destination. The board stores these
reusable instructions, not the research repositories themselves.

Create the question directory and initialize a local repository with `git init -b main` before writing tests, searching constructions or attempting a proof. Confirm that `git rev-parse --show-toplevel` identifies that directory,
not a parent repository. If resuming an existing repository, inspect its status
and history and continue there without reinitializing it.

Before the first research attempt or Prepare, make an initial commit containing
the README, applicable local
instructions, `.gitignore`, the fixed campaign question and initial `state.md`.
Record the accepted scope, round budget and starting evidence. The README names
the question and links to the campaign state. Copy the research skills (including their assets), `research/` specifications
and the reviewer registration for the harness in use (`harness/`; for Codex,
`.codex/agents/research-reviewer.toml`) with their relative paths intact. Do not
copy the board repository's local `research/experience/entries/` collection:
campaigns read it in place, and the destination's local instructions record the
board repository's absolute path so it can be found. Write local research
instructions from the fixed question and shared reduction contract; the board
repository's website-only AGENTS.md does not belong in the new project. A missing Git identity or failed commit is a concrete setup
blocker: resolve it before starting experiments; do not invent an identity.

Run the campaign from a session whose workspace is this repository, or grant it
explicitly when the harness bounds writes by the session workspace. The copied
skills and local instructions then load from this repository, which is also the
Git root the harness discovers. See the
[harness contract](../harness/README.md#session-workspace-and-file-policy).

A remote is not required to begin. Research authorization includes local commits;
it does not by itself authorize GitHub creation or publication.

## Directory ownership

Use the existing campaign layout; paths below are relative to the repository root.
Create directories only when there is content for them.

| Path | Contents |
|---|---|
| `README.md` | Question, current claim and verification scope, links to proof/history, reproduction commands |
| `AGENTS.md` | Local research instructions |
| `pyproject.toml`, `uv.lock` | Python dependencies and locked environment, added when Python is first used |
| `campaigns/<slug>/question.md`, `state.md` | Fixed target and current progress |
| `campaigns/<slug>/work/` | Current construction, recovery, tests, proof and Typst manuscript |
| `campaigns/<slug>/rounds/`, `reviews/` | Attempt records, retained evidence and independent reviews |
| `campaigns/<slug>/formal/` | Lean sources and formal-check evidence, separate from `work/` |
| `research/experience/` | Reusable findings linked to their originating evidence |

The [session skill](../.agents/skills/research-session/SKILL.md#artifact-ownership)
defines files within each campaign. On completion, update the README to expose
the final artifacts in place. Do not copy the entire campaign into another
`history/` tree or create a new repository merely to present the result. Existing
archives may keep their established layout; new work continues their real history.

## Commit as research proceeds

Commit the prepared testing foundation before constructing a candidate. Commit
each completed round, including failed and inconclusive attempts, after recording
its evidence, diagnosis and reusable findings. Commit independent reviews,
substantive proof repairs and formal-check results when recorded. If a session
ends during a round, save its current state in a clearly described partial commit;
this does not count as a completed round.

Stage only campaign-related changes and inspect the staged diff. Before replacing
an implementation cited by evidence, commit it and reference its commit and path
from the round record. Preserve any uncommitted reproducer inputs. Git supplies
implementation history; do not duplicate the full workspace in every round.
Keep experiment scripts and unique evidence with the round that produced them.

Do not squash, amend away or fabricate research history to make a campaign look
successful. Repository creation at the end cannot reconstruct missing history.
An imported campaign must identify itself as an import with only the history
actually retained. Rewriting existing commits requires an explicit request.

## What belongs in Git

Commit source code, proofs, question definitions, test inputs, dependency locks,
commands, compact result logs, reviews and irreplaceable evidence. Retain failure
records and counterexamples, even when they invalidate a proposed result.
A reviewed manuscript PDF may accompany its Typst source for direct reading.

Exclude `.venv/`, Python bytecode, Lean dependency/build caches and reproducible
bulk outputs such as expanded target graphs. Add explicit ignore patterns for
those outputs. For each omitted artifact, retain its exact input, generator
revision, dependency lock, working directory and command; record seeds where
applicable and whether randomness can change the result. A fresh checkout must
support reconstruction without a sibling research repository or the old session.
Do not exclude unique observations or solver certificates merely because they
are large. Decide how to preserve such evidence before publishing.

Manage Python with uv, commit `uv.lock`, and document `uv sync --locked` and the
actual test commands. Local environments can be deleted after use and rebuilt.
Before pushing, inspect all commits to be pushed for inadvertently tracked bulk
outputs; adding an ignore rule does not remove already committed files.

## GitHub and the board

When remote creation is authorized, create a private repository unless the user
requests public visibility, and push the existing local history. Use a stable
question slug and a README that states the exact result and remaining checks.
For a history-and-proof archive, disable Issues, Discussions, Wiki and Actions
where applicable. Do not add contribution workflows or automatic deployment.

Record a solution on the board with its repository URL, full result commit,
model/version, date and documented verification scope. A repository or passing
finite test suite does not make a result Verified. Follow the board's acceptance
rules and keep pending independent checks explicit.
