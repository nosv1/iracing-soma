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
