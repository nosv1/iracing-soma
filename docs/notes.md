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
- (Superseded 10-13 by the router role below; kept as a later option.) The LLM's real job: an
  engineer who **wants to succeed**. Inputs = goal + code-computed
  projections (laps to catch, catchable before flag, position if passed); LLM picks what matters
  and the tone. Open: where the goal comes from (driver-set vs inferred), first projection
  (laps-to-catch), how it resets targets when the goal slips.
- Example pool: keyed by event, only relevant examples per call, stored as data so it doubles as
  the eval set.

### LLM role narrowed (2026-10-13, brainstorm, pinned)

He doesn't trust 3B/8B to write code, and he's right: live code generation can't be checked
mid-race. Rule: an LLM job is OK only if code can cheaply check its output.

- **No live code fallback.** Unknown question → "don't have that" + log it. He writes the new
  built-in from the log between sessions (promotion loop kept, minus generated code). Hub spec
  still describes the fallback; update it there.
- **LLM = router.** Spoken question → `{"fn", "args"}`, `none`, or `{"clarify": [candidates]}`.
  Code validates fn/args. On `clarify`, code (not the LLM) asks "fuel or race?" from the
  candidate list; one pending question is the only cross-turn state. Prefer answering both when
  they fit in one line ("12 to go, fuel for 14") over asking; asking costs a second exchange.
- **Functions return facts + action** (pinned rule above); each ships a template sentence. LLM
  phrasing is an optional layer behind the numbers check, deferred.
- **Parameterize by car**: `gap_to(car)`, `best_lap(car)`; "leader"/"ahead"/"behind"/name are
  args. Hard part is arg resolution (names, car numbers, Whisper mishearing) — open whether the
  LLM resolves or passes the raw phrase to code matching against the driver list.

His first questions: gap to leader; best lap; leader best lap; expected finish position;
expected laps left; expected laps of fuel; am I being caught. Notes from discussion:

- Every "expected" is a modeling choice that's his: fuel = fuel ÷ avg burn over which laps
  (exclude pit/out/yellow?); laps left in a timed race follows the leader's pace (check
  `SessionLapsRemainEx` first); finish position needs everyone's pace + pending stops — do last.
  Each states its method ("on last 5 laps' burn").
- "Am I being caught?" is the caught-call projection reversed; pure laps-to-catch gets both.
- "Laps left" vs "fuel laps" is a real ambiguity → candidate for a combined fuel-vs-race
  function: "12 to go, fuel for 11. Save 10%, or box lap 8." Templates suffice.

### 2026-10-13 (evening): recorder first, started

Reordered: the recorder jumped to the front; everything else (caught call, projections, router
eval) needs real race data to test against.

- `check_iracing()` (tutorial copy) axed; `iRacing` now has bare `connect()` / `disconnect()`.
- [docs/irsdk/irsdk_vars.md](irsdk/irsdk_vars.md) gained a session-info (YAML) section, built
  from a live dump, plus observed facts: `CarIdx*` arrays are **72** wide, pace car idx 64;
  `CarIdxPosition` 0 = empty slot / unscored, -1 = slots 64–71; YAML `ClassPosition` looks
  0-based (verify multiclass). `ir[key]` falls back from telemetry vars to YAML sections.
- His recorder (uncommitted, WIP): `main.py -r [DIR]` (default `./recordings`, gitignored),
  `Recorder` = queue + one non-daemon writer thread + sentinel, stopped in `finally`. Per tick it
  freezes and queues `{name: ir[name] for all vars}`; saves raw YAML bytes on
  `session_info_update` change. Also WIP: `Session`, `Driver` (`@classmethod` constructors).
- He thinks it records; not yet verified or tested.

## Next

0. His, review of the WIP recorder before trusting a recording:
   - [bug] Main loop has no pacing: it spins, queueing the same tick many times (~300 vars each).
     File size and queue memory grow fast. Wait for a new tick (`SessionTick` changed) or sleep.
   - [bug] `while ir.state.is_ir_connected` never goes false: `connect()` sets True without
     checking `startup()`'s return, and nothing rechecks `ir.is_connected`. Only Ctrl+C exits.
   - [design] Frames written as Python `repr` (`f"{item}"`); JSON lines would be loadable by
     anything. Decide the format before recording much.
   - [bug] `Driver.drivers_from_irsdk`: needs `(cls, ir)`; YAML nesting is
     `ir['DriverInfo']['Drivers']`, code has it inside out.
   - [nit] `disconnect()` logs "Connected"; `Session.session_time` is a float.
1. His: tests for the recorder (round-trip: record → load → same values) and a replay source
   with the same interface as the live wrapper.
2. His: caught-call detection (line crossing from `CarIdxLapDistPct` wrap; see
   `git show 282c4a7:irsdk/irsdk_lapTiming/lapTiming.cpp`, `processLapInfo`). Template voice.
   Keep it pure (frames in, event out) so it runs against recordings.
3. His: function signatures for the question list above, then 5–8 radio-style variants per
   question as `question → expected call` (incl. ambiguous ones → `clarify`). His spec.
4. Mine once (3) exists: router eval harness, 3B vs 8B; score correct call, correct `none`,
   correct `clarify` separately.
5. His: first projection (laps to catch), numbers/facts check.
