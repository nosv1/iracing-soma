# Session notes

Claude's notes for this repo. Cross-project context lives in the hub:
[nosv1/nosv1](https://github.com/nosv1/nosv1).

## Where things stand

**2026-10-10:** repo created (scaffolding only: this file, CLAUDE.md, README, .gitignore). No code.

**2026-10-11:**

- Stack decided: all Python. C++ SDK was cloned, read, then removed (C++ practice goes elsewhere,
  e.g. otto). pyirsdk in `env/` venv (Python 3.10). pyirsdk tutorials + vars table in
  [docs/irsdk/](irsdk/).
- TTS: Piper (CPU), voice `en_GB-southern_english_female-low` in `voices/` (gitignored).
- LLM: Ollama 0.40.3, `llama3.2:3b` and `llama3.1:8b` pulled.
- **GPU contention test done** ([bench/gpu_contention.py](../bench/gpu_contention.py), run
  `bench/runs/20261011-190912`, untracked). VR on Quest via Link at 72 Hz, big AI grid:
  - iRacing held 72 fps in every phase, incl. nonstop 8B generation.
  - Headroom (Oculus HUD): ~70% baseline, ~60% 3B continuous, ~50% 8B continuous.
    Occasional 72→70 dips also occur at baseline.
  - VRAM is the limit: 8.7 GB baseline, 11.4 GB with 3B, 14.0 GB with 8B (of 16).
  - TTFT ~0.03–0.05 s, 3B ~190 tok/s, 8B ~100 tok/s. One 15 s cold first request in the dry run,
    not reproduced; may need a warm-up call at session start.
  - With a one-line prompt, 3B invents facts badly; 8B mostly faithful but still embellishes.
- Project setup: Python 3.14 `.venv`, uv (`uv sync` / `uv add`, `uv.lock` committed), package at
  `src/soma/` installed editable. Ruff + mypy as dev deps. Ollama context default is 4096
  (models support 128K); ~8K fits either model in VRAM.
- Prompt playground: [bench/prompt_play.py](../bench/prompt_play.py) (`ollama.chat`, examples as
  prior turns). Learned: small models copy surface text of examples (quotes, numbers), so vary
  example values and keep each example's reply consistent with its facts; ambiguous keys
  (`position`, `driver`) get misread.

### Design direction (2026-10-11, pinned)

- Fixed-shape reports (caught call) start as **templates**: LLM phrasing needs examples + check +
  template fallback anyway, so templates are less work. Add LLM phrasing only if it feels robotic.
- Every fact handed to the voice carries **what to do about it** (fuel short → save X% or box by
  lap N), computed in code. No problem-without-a-solution messages.
- The LLM's real job: an engineer who **wants to succeed**. Inputs = goal + code-computed
  projections (laps to catch, catchable before flag, position if passed); LLM picks what matters
  and the tone. Open: where the goal comes from (driver-set vs inferred), first projection
  (laps-to-catch), how it resets targets when the goal slips.
- Example pool: keyed by event, only relevant examples per call, stored as data so it doubles as
  the eval set.

## Next

0. His, parked: review items left from 2026-10-11. `iRacing` wrapper leaks `ir.ir` and never
   calls `check_iracing()`; failed connect is silent (`Car(idx=None)`); keep caught-call logic
   pure (snapshots in, result out) so it's testable against replays.
1. His: caught-call detection (line crossing detected from `CarIdxLapDistPct` wrap; see
   `git show 282c4a7:irsdk/irsdk_lapTiming/lapTiming.cpp`, `processLapInfo`). Template voice.
2. His: first projection (laps to catch car ahead), then goal-aware LLM call.
3. His: numbers/facts check; decide digits-from-LLM + code spells numbers for Piper.
4. Eval harness over the example pool, 3B vs 8B, temperature sweep. (Tooling, fair for me.)
5. Telemetry recorder + replay for desk testing.
