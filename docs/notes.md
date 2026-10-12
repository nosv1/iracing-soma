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
- Chris's main.py / src/ are scratch, untracked until real development starts.

## Next

1. His: Soma's prompt (few-shot, structured facts in) + a numbers/facts check.
2. Eval: fixed set of 20–30 fact cases, run both models with his prompt, score with his check.
   Pick 3B if it passes, else 8B. Model name as one setting. (Harness = tooling, fair for me.)
3. His: caught-call detection (line crossing detected from `CarIdxLapDistPct` wrap; see
   iRacing's lapTiming sample logic).
4. Telemetry recorder + replay for desk testing.
