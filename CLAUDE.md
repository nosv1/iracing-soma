# iracing-soma

Soma (Strategy Operations and Monitoring Assistant): a spoken race engineer for iRacing. A clean
rewrite of the ACC version in [strategist](https://github.com/nosv1/strategist), which stays a
frozen archive to read, not to build on.

## Read first

**Before anything else this session, fetch and read Chris's profile:**
<https://raw.githubusercontent.com/nosv1/nosv1/main/PROFILE.md>

It says who he is and how to work with him: flight instructor by default, he writes the code that
is the skill. It applies here unless this file says otherwise. If the fetch fails, say so; don't
proceed as a generic assistant.

**Before reviewing or writing any code, fetch and read the coding standard:**
<https://raw.githubusercontent.com/nosv1/nosv1/main/CODING.md>

Then read [docs/notes.md](docs/notes.md) (session notes; update at sign-off, commit as Claude).
The idea and the first milestone's spec live in the hub:
<https://raw.githubusercontent.com/nosv1/nosv1/main/ideas/iracing-race-engineer.md>

## This project

- **Skill he's building here:** reading live telemetry (iRacing SDK, shared memory), race-state
  modeling, a voice pipeline, later a local LLM with tools. He writes all of that.
- **Fair game for me:** environment and dependency fights (Windows Python, audio devices, CUDA),
  CI, plotting throwaway results, and reading/critiquing his code.
- **Runs on Windows, not WSL.** iRacing's telemetry is Windows shared memory; WSL can't see it.
- **Run it:** not yet.

## Coding standard

The hub's [CODING.md](https://github.com/nosv1/nosv1/blob/main/CODING.md) at its strictest settings (his call,
2026-11-23). **He writes the code here**; Claude reviews it against CODING.md, tags each finding **fix now /
noted / taste**, and keeps the tools and CI working (fair game).

- **Check:** `uv run python tools/check_baseline.py ruff -- ruff check --output-format json .` and
  `uv run python tools/check_baseline.py mypy -- mypy` (mypy's files are set in pyproject.toml), then
  `uv run pytest`. CI runs the two checks on every push.
- **Baseline only shrinks:** `checks-baseline.json` holds what the stricter settings found in existing code on
  2026-11-23 (114 Ruff, 3 mypy). New and changed code meets every rule; after fixing a file, rerun the check with
  `--update`.
