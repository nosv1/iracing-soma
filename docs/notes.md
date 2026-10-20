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
expected laps left; expected laps of fuel; am I being caught; **how long to repair** (added
10-14: know the cost before committing to the pit entry). Notes from discussion:

- Every "expected" is a modeling choice that's his: fuel = fuel ÷ avg burn over which laps
  (exclude pit/out/yellow?); laps left in a timed race follows the leader's pace (check
  `SessionLapsRemainEx` first); finish position needs everyone's pace + pending stops — do last.
  Each states its method ("on last 5 laps' burn").
- "Am I being caught?" is the caught-call projection reversed; pure laps-to-catch gets both.
- "Laps left" vs "fuel laps" is a real ambiguity → candidate for a combined fuel-vs-race
  function: "12 to go, fuel for 11. Save 10%, or box lap 8." Templates suffice.
- Repair time: `PitRepairLeft` (mandatory, s) and `PitOptRepairLeft` (optional, s), plus
  `FastRepairAvailable` (255 = unlimited) / `FastRepairUsed`. Unverified: whether they're
  populated on track before pitting (OblivionsPeak's engineer reads `PitRepairLeft` on track to
  detect damage, which suggests yes) and how repair time stacks with fuel/tyre service. Check
  both in a recording with damage. The action is his call: mandatory-only vs + optional vs fast
  repair, priced against pit lane loss and laps left ("45 s required, 30 more optional; fast
  repair available").

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

### 2026-10-14 (morning): first race recorded

- Recorder fixed up and committed (`be8ad51`): 10 Hz via `SessionTick` delta (60 Hz confirmed:
  header `tick_rate` 60, 60 ticks/s measured), JSON lines, freeze/unfreeze once per loop in
  `main`, `Driver` constructors fixed. Uncommitted: STOP-file shutdown in `main.py` (mine, at his
  request: create `<record dir>/STOP`, checked ~1 Hz, loop breaks so `finally` flushes), his
  latest `recorder.py` (tick-reset handling, `exist_ok=False`).
- **First recording** (online, practice → qualify → 12-min race, `recordings/`, gitignored):
  15,674 frames, all valid JSON, 326 MB raw (~20.8 KB/frame; gzip measured ~10–12x on track).
  Final `session.yaml` has official race results. He moved it to
  `recordings/20261014-110000/`. I also snapshotted every YAML version externally (his recorder
  overwrites one file): `yaml_history/`, 172 files, renamed `<SessionTick>-<hash>.yaml` (tick
  the YAML took effect, estimated from wall-clock snapshot time, ~1 s; aligned to the frames'
  `SessionNum` changes) + `index.json` with original names. Loader rule: newest YAML with
  tick <= frame tick.
- Seen: `SessionTime` **resets per session** (139 → 1014 s over ~26 min wall). Timeline across
  sessions needs `SessionNum` + `SessionTime` or `SessionTick`. **`SessionTick` is continuous**
  across all three sessions: every frame gap exactly 6, no resets, no drops.
- `SessionInfoUpdate` is a shared-memory header counter (`ir.session_info_update`), **not** a
  telemetry var, so it is not in the frames. Record it into each frame to pair YAML exactly.
- I ran it in the background while he raced in VR, with spoken status via Piper
  (`en_GB-alan-medium`, now in `voices/`): only on session/flag change, stall, crash. He liked
  it. Lessons for Soma: silence = OK; short templates were enough; load the voice once (per-line
  model load cost ~9 s).

### 2026-10-14 (midday): loader design, his

He's building replay (`src/soma/loader.py`, started). Where he landed (his reasoning, coached):
the **frame dict is the interface**. `Session`/`Car`/`Driver` take a frame instead of `ir.ir`,
so nothing downstream knows live vs replay, and the `ir.ir` leak goes away. Loader reads
`frames.txt` one line at a time (generator + `yield`, `json.loads` per line), never the whole
file. Open, his call:

- Frames lack YAML sections (`DriverInfo`). Option A: a `Snapshot(frame, yaml)` with
  `__getitem__` that mirrors pyirsdk's lookup (frame first, then YAML), so `x[KEY]` code stays.
  Option B: pass frame and YAML separately; explicit, more signature churn.
- Live mode must build the same frame; only when `SessionTick` moves, as the recorder does.

### 2026-10-14 (evening): prior art, open source

- He's considering making Soma open source. Googling turned up
  [OblivionsPeak/ai-race-engineer](https://github.com/OblivionsPeak/ai-race-engineer): one
  6.5K-line file, 61 of 66 commits Claude co-authored, cloud LLM through the author's backend
  (login, 50 queries/day), no license, no record/replay. Its fix log ("false meatball/engine
  warning on session start", "CarLeftRight shifted by one") shows bugs a replay would catch.
  Worth borrowing as ideas, not code: its callout list (meatball `SessionFlags & 0x40000`, new
  `EngineWarnings` bits, `PitRepairLeft` rising, sector deltas from
  `LapDeltaToSessionBestLap`), absorbing flags present on connect / first on-track, and per-key
  cooldowns on callouts (`CalloutManager`).
- Open: the license (MIT vs GPL), his call, no rush.

### 2026-10-14 (evening): connection, loader done, tests

- **Connection:** `connect()` retries `startup()` with backoff capped at 30 s (he flipped
  max/min once); main loop does `disconnect()` → `connect()` on drop, so pyirsdk's cached var
  headers reset. `startup()` = one attempt (HTTP sim-status + 32 ms data-valid wait), not a
  background process. Known: STOP can't fire while `connect()` blocks (Ctrl+C still flushes).
- **Recorder:** per-run timestamped folder, YAML history `yaml_history/<tick>-<ts>.yaml` +
  `index.json`. **Requirement (his): every YAML tick is a recorded frame tick**; YAML is checked
  only on ticks a frame is recorded (`handle_new_tick`). First recording's `index.json` rewritten
  to his flat `{tick: file}` (string keys); `recorder.py` should write the same.
- **YAML is cp1252**: raw `yaml.safe_load` fails on all 172 files (`Å` byte), `.decode("cp1252")`
  first parses all. pyirsdk `_parse_yaml` (irsdk.py:647) does more sanitizing (quotes in names,
  leading commas); look there if a lobby breaks parsing.
- **Loader done:** `snapshots()` generator, exact-tick YAML pairing, raises
  `CorruptRecordingsError` if index ticks are left unmatched; `Snapshot.__getitem__` frame then
  YAML. Real recording: 15,674 snapshots (his run; temp count code since removed).
- **Tests:** pytest, fixture recordings in `tests/recordings/` (`valid`, `yaml_tick_without_frame`;
  cp1252 name; YAML switch at 630). 4 green. Taught: generator body runs only when consumed;
  asserts behind `if` pass vacuously → consume in a fixture, flat asserts.
- **mypy clean** on `main.py src tests` (stubs for yaml, `irsdk`/`sounddevice` ignored). It found
  4 real bugs. `possibly-undefined` is opt-in; enabling it would have caught the replay `ir` crash.
- Ideas go in [backlog.md](backlog.md) (his, raw, unprioritized).

### 2026-10-15: live/replay split, shared fixtures

- His: `main` split into two loops (record vs live stream, `13d1efc`); cars/drivers now dicts
  keyed by car idx (`1bd03bd`). Not checked by me whether replay runs end to end.
- Fixtures moved to `tests/conftest.py` (`a9540d0`): `recordings_path`, `valid_loader`,
  `valid_snapshots_dict`, `valid_driver_dict`. Taught: don't import fixtures from test modules
  (dependency chain isn't visible, couples files); conftest is auto-discovered.
- State at sign-off: 5 tests green, `uv run mypy main.py src tests` clean, ruff 6 left
  (E501 ×2 `loader.py:59-60`, N802 ×2 `recorder.py` `iRacing` names, 2 unsafe-fix). Run checks
  via `uv run`; bare `python -m mypy` hit another env and gave false `import-untyped`.

### 2026-10-16: second recording, caught call started

- **Second recording** `recordings/20261016-164405/` (gitignored): 3 sessions, race green
  16:59, checkered 17:14 (~15 min). 17,466 frames, all valid JSON, 218 YAML, 375 MB. Ran via a
  scratchpad watcher (spoken status, northern male voice); STOP file shut it down clean (exit 0).
  Live `Session.from_frame` survived 30 min without throwing (says nothing about its values).
- **Line-crossing math, his,** worked on paper first:
  `t_cross = t1 − p1 · (t1 − t0) / (p1 + 1 − p0)` (linear interpolation across the wrap; same
  answer from either side). He tried to skip it ("frames have `SessionTime`"); worked through
  why not: frame time is 0–100 ms late per car at 10 Hz, so on the fixture the un-interpolated
  delta gap is 0.100 vs a true 0.154 (35% off). Live 60 Hz is ≤17 ms late, but one code path.
- **`CarIdxLastLapTime` is official per-car timing** (seen populated for the whole field, `-1`
  for some laps, e.g. car 4 with a best but no last; cause unverified). Delta gap over a lap =
  difference of the two lap times, no interpolation needed. Absolute gap (laps-to-catch) still
  needs interpolated crossing times. Use lap times as the check on his crossings in real data.
- **Fixture `tests/recordings/crossings/`** (mine, uncommitted): 2 cars at constant speed,
  4 s laps, 50 frames. Car 0 crosses 0.388 / 4.388, car 1 0.769231 / 4.615385; gap 0.381231 →
  0.227385, **delta 0.153846**; `CarIdxLastLapTime` 4.0 / 3.846154 from the frame after each
  car's 2nd crossing, `-1` before. Generator lives in the session scratchpad only (will be lost;
  regenerate or move into `tests/` if the fixture needs to change).
- Added to `irsdk_vars.py`: `CAR_IDX_LAP_COMPLETED`, `CAR_IDX_LAP_DIST_PCT`,
  `CAR_IDX_ON_PIT_ROAD`, `CAR_IDX_TRACK_SURFACE`, `CAR_IDX_LAST_LAP_TIME`.
- Taught: `from_<source>` alternative constructors are idiomatic (keep plain `__init__` for
  tests); redundancy is the smell (`from_car_idx_frame(car_idx, frame)`, `Lap.create_lap`).
  `typing.Protocol` for `IRSDK | Snapshot`; he moved `Snapshot` to `snapshot.py`. Ticks = frame
  ID (int, unique, continuous); `SessionTime` = the math (float, resets per session).
- **His WIP (uncommitted), state at sign-off:** `Lap`, `Car.get_delta_gap_after_lap`,
  `Session.update_session`, tick dedupe in `handle_frame`. Untested (`test_crossings.py` is a
  `pass`). mypy 4 errors (`Lap.from_frame` missing `@classmethod`, `field(default=list)`,
  `update_car` missing `frame`, `Lap | None` append). Reviewed, fix now: laps don't survive
  frames (new `Car` each frame), crossing time not interpolated, guard on `laps_completed`
  not `len(laps)`. Noted: `laps[-2]` pairs by list position (mismatch between the two cars'
  crossings, lapped cars), any backwards pct counts as a lap (garage `-1`, tows), sign
  convention (+0.154 for self=0, other=1) undocumented.
- **His redesign, landed at sign-off:** one persistent `Car` per idx owning its laps, updated in
  place; previous frame kept as cheap scalars (`prev_lap_dist`, `prev_session_time`), no
  `old_car` chain.

### 2026-10-17: backlog, oval priorities

- Backlog grew (all in [backlog.md](backlog.md)): laps-left milestones (timed-race trap noted),
  repair time, start reaction time, oil pressure warning, water temp in the draft. Pyirsdk
  `EngineWarnings` bits checked: `0x0001` water temp, `0x0004` oil pressure, `0x0080` / `0x0100`
  mandatory / optional repairs needed (possible on-track damage signal).
- Both recordings: repair vars present, always 0.0 (no damage taken). Still unverified whether
  they populate before the pit box.
- **Priority signal (his):** he races ovals a fair amount; caught call matters less there.
  Repair time + spotter would let him use Soma in oval races sooner. He runs DRE now and wants
  to switch: plan is to note which DRE calls he'd miss and build those first.
- **Open, his call (parked, he was tired):** reorder Next around that. My suggestion: crossing
  test green → damage recording → live loop + repair-time call (first in-race feature, forces
  the live + voice pipeline) → spotter (latency; pre-render clips; ask what it beats iRacing's
  built-in on) → caught call for road. And a `docs/dre-calls.md` list (call, trigger, oval/road,
  would-miss), offered, not made.
- His plan for next session: test the function from 10-16 (`get_delta_gap_after_lap`) before
  the persistent-`Car` refactor. Low-energy path: build `Car`s with hand-made `laps` directly
  (plain `__init__`), no update loop needed.
- **Reminder (his ask):** when he's tired or hits a checkpoint, remind him to consider starting
  [otto](https://github.com/nosv1/otto-the-robot). Reminded at the delta checkpoint; he chose
  the voice line first. Still open.

### 2026-10-17 (evening): lap detection + delta tested (`7d7cc60`)

- His: persistent-`Car` redesign landed. `soma/handler.py` `handle_frame(session, frame)` builds
  a throwaway `Session.from_frame`, skips duplicate ticks, then
  `Session.handle_frame` → `Car.handle_frame` updates persistent cars in place
  ("handle_frame → update_x" is his template). Lap = `laps_completed` up **and** pct wraps.
  `estimate_lap_timestamp` takes prev/cur scalars (no `old_car`). `main` calls the same handler.
- Bug he found via fixture: crossing denominator written `p1 − (1 − p0)` instead of
  `p1 + (1 − p0)`; gave 0.4158 vs 0.388, plausible-looking, lap-count test passed anyway. Only
  known-answer asserts caught it. Also found the `laps[lap_to_compare]` off-by-one himself.
- Tests: fixture `tests/recordings/laps/` (his; same numbers as the old scratch `crossings`,
  which is gone). Module-scoped `laps_session` fixture, parametrized timestamp test, delta test.
  8 green, mypy clean, ruff 10 (6 auto-fixable unused imports, incl. `PiperVoice` in
  `handler.py`, `IRSDK` in `session.py`).
- Taught: `pp`, `pp locals()`, `display`, `interact`, `pytest --pdb`; `approx` goes on the
  expected side (bool raises); `zip` truncates silently; rounded expected values vs default
  `rel=1e-6` (use `2/13`, `10/13`, `60/13`, or `abs=`); parametrize reruns fixtures → module
  scope + ScopeMismatch.
- Delta = self lap time − other lap time (= `CarIdxLastLapTime` difference): `+` means self
  was slower, consistent whoever leads. He keeps it caller-relative, favors "relative to the
  leading car" later. His docstring still says "+ = further apart", false when self leads
  (his own test: +0.154 while closing). Noted, not fixed.
- Open, fix now (before voice): 0 laps → index −1 → `laps[-2]` `IndexError`; guard misses it.
  Edge tests (0/0, 1/1, unequal counts; a `car_with_laps(idx, timestamps)` helper makes each one
  line) parked in a TODO by him; the guard fix itself is not optional before voice.
- His loop is copied 3× (live, replay, test fixture); he dislikes it. Root is the parked
  live/replay unification (live as a generator yielding snapshots). He can't picture it yet;
  parked, not a priority.

### 2026-10-18 (morning): events, delta gaps ahead

- Backlog: braking smoothness, watch my splits (projected lap from `LapDeltaTo*`), "keep me
  posted on X" (topic → cadence watch list, a router call). `irsdk_vars.py` gained the vars the
  backlog names (`e43a74b`, mine).
- **Design problem (his):** a lap-based announcement needs "player + new lap", but
  `Car.handle_frame` detected the lap and returned `None`, so the fact was lost. Car shouldn't
  know it's the player (session owns `player_car_idx`). He rejected ACC's global queue (hidden
  coupling, breaks "snapshots in, event out") and chose **events stored on the car**:
  `car.events: list[Event]` (`soma/event.py`, `Enum`, `CAR_NEW_LAP`), cleared in
  `Car.handle_frame`; `handler.handle_events(session)` reads them per car after
  `Session.handle_frame`.
- Known hole, his call to leave: cars missing from the new frame skip `handle_frame`, so their
  events are never cleared → stale `NEW_LAP` re-read every frame. He wants proof of what a
  disconnect looks like first. Check: a car with `CarIdxPosition` > 0 → 0 mid-race in either
  recording. Clearing all cars' events before the loop fixes it regardless.
- His WIP (uncommitted): `CarDeltaGap`, `Car.get_delta_gaps_ahead(cars, positions)` (cars in
  positions 1..P−1, sorted by delta), `handle_events` with a `breakpoint()`,
  `test_sorted_delta_gaps` (no assert yet). Fixture `tests/recordings/laps_p2/` (mine): `laps`
  with `PlayerCarIdx` 1 (P2). Result at sign-off: `[CarDeltaGap(car_idx=0, delta_gap=-0.15385)]`,
  the expected −2/13. Noted: `get_delta_gaps_ahead` has no return type; `update_session` never
  refreshes `player_car_idx`.
- Taught: module-scoped generator fixtures are consumed once (`snapshots_with_laps_iterator`
  is empty after `laps_session`); he switched to a fresh `loader.snapshots()`. Single test:
  `uv run pytest tests/test_laps.py::name`, `-k`, `-s`, `-x`.

### 2026-10-18 (evening): Soma speaks; caught call checked on a real race

- **First spoken output** (his): `Speaker` (queue + thread, Piper), `handle_events` builds the
  caught call ("Caught P5 by 0.2 seconds / Gap is 1.3 seconds..."). Tests: `laps_p3` fixture
  (mine; 3 cars, player P3, sorted order ≠ position order), sorted-gaps and caught-call tests.
  Backlog: radio effects.
- **Live run aborted, replay instead.** Started live with a watcher; he stopped it. A silent replay
  of `20261016-164405` crashed in qualifying (`KeyError`, stale `session.positions` from the first
  frame). He fixed positions, then laps carrying over between sessions (`SessionTime` resets →
  312 s deltas). Lesson (his): replay the recordings before going live.
- **Checked against official times:** all 4 race calls match `CarIdxLastLapTime` differences keyed
  by lap number (−0.238, −0.367, −0.276, −0.070 → said 0.2, 0.4, 0.3, 0.1). I first said calls 2–4
  were wrong; that check read a stale value (below).
- **`CarIdxLastLapTime` posts late:** 1.1 s min, ~1.8 s median after the crossing, every car,
  both recordings; on the crossing frame it still holds the previous lap. `LapLastLapTime`,
  `LapCurrentLapTime` reset and `CarIdxLastLapTime` change on the same frame (player, 11/11
  laps); reset value = time since the real crossing (728.133 − 2.182 = 725.951 vs his
  interpolated 725.969). Posted value = his crossing diff (median 0.0000, ~85% within 10 ms).
  So `Lap.lap_time_s` (read at crossing) is one lap stale; timestamps are right.
- **Edge cases found in recordings, not handled:** pit-lane start makes `CarIdxLapCompleted` go
  0→1→0→1 with a pct wrap in pit lane (10-14 car 9; likely double-counted lap); car not in world
  flickers laps/pct/last to −1 and back (10-16 car 4); pct slightly < 0 at the line (4 frames).
- Open: lap pairing by list index vs lap number (late joiners, lapped cars); "Gap is 8.3 s" in
  the last call unverified; whether a 0.07 s/lap gain on a car 8 s up is worth calling; fake
  speaker for tests (`test_caught_call` speaks aloud, needs gitignored `voices/`, no assert).
- Scratch tools (session scratchpad, will be lost): `replay_dry.py` (prints calls per tick),
  `replay_check2.py` (calls vs official lap-keyed deltas), `lastlap_lag.py`. Empty folder
  `recordings/20261018-174349/` left from the aborted live run.
- His WIP uncommitted at sign-off: `main.py`, `car.py`, `handler.py`, `lap.py`, `session.py`,
  `test_laps.py` (incl. a `breakpoint()` in `handle_events`).

### 2026-10-19: first live race, silent; server switch found

- **Live run** with recording, `recordings/20261019-175649/` (gitignored, 437 MB, 210 YAML, all
  valid JSON): practice server → race server → full race at Oulton, P20 → P7. Ran under a
  scratchpad crash watcher (speaks only on non-zero exit); no crash, STOP exit 0. Short false
  start `recordings/20261019-175431/` (6 MB) left for him to keep or delete. I removed the
  `breakpoint()` from `handle_events` at his request (in his uncommitted `handler.py`).
- **Soma never spoke** past "Speaker initialized". Two bugs, both his, both fix now:
  1. iRacing moved him to the race server while connected: `SessionTick` reset (83673 → 59711)
     and **`PlayerCarIdx` 35 → 18**. `update_session` never refreshed `player_car_idx`, so Soma
     watched an empty slot all race. He has since added the refresh (uncommitted).
  2. `len(car.laps) <= 1` counted sessions once `laps` became `{session_num: [Lap]}`; race-only
     driving = 1 forever. Diagnostic replay with the idx forced to 18: all 11 race laps blocked
     there, 9 of them had a gain to call. He changed it to `len(car.laps[car.session_num])`.
- **Server identity** (in [irsdk_vars.md](irsdk/irsdk_vars.md)): `WeekendInfo.SessionID`,
  `SubSessionID`, `EventType` all change on the switch. `EventType` is the server's event, not
  the current session (race server says Race during its practice); current session =
  `Sessions[SessionNum].SessionType`. Lineup is per event (practice server: 0 Practice; race
  server: 0 Practice, 1 Lone Qualify, 2 Race). YAML lagged the telemetry switch by 54 ticks.
- Constants added to `irsdk_vars.py` (mine); lap fixtures `laps`, `laps_p2`, `laps_p3` gained
  `WeekendInfo` + `SessionInfo` (one Race session, SessionNum 0) so `Session.from_frame` can
  read them.
- **His WIP at sign-off (uncommitted):** `SessionType(StrEnum)` with `is_practice` /
  `is_qualifying` / `is_race` (taught: value lookup `SessionType("Race")`, `_missing_` →
  `UNKNOWN`; `@dataclass` on an enum makes it unhashable; `!r` = repr, `{v:!r}` is a format
  spec and raised inside `_missing_`, fixed). `Session.from_frame` reads `WeekendInfo` and
  `Sessions[SessionNum].SessionType`. At sign-off: 10 green, mypy clean, ruff 8 (old). Still no
  test for an unknown type → `UNKNOWN`. `CURRENT_SESSION_NUM` added (`71797d4`).
- Noted, not fixed: cars from the old server persist in `session.cars` (idx reuse across
  servers); recorder `index.json` keyed by tick alone collides across a tick reset (today's two
  servers didn't collide only because their ticks fell on different steps of the 6-tick spacing).
- Ideas: race-control voice for session/flag changes (`en_US-norman-medium`, downloaded to
  `voices/`; heartbeat that Soma is alive; absorb flags present on connect; `sounddevice.play`
  is one global stream, two `Speaker` threads cut each other off). Backlog: voice
  personalities, tester warnings (log file + spoken once + shutdown list).
- pytest warnings (57): `sounddevice` uses `.shape =`, deprecated in NumPy 2.5. Not ours; gone
  once tests use a fake speaker.

### 2026-10-20: event facts, red test stubs

- **Workflow (his):** a red `pytest.fail("TODO: input -> expected")` stub left at sign-off gives
  next session an immediate start without blocking the sign-off. I create stub files when a test
  is identified; he writes the bodies. `5df0e2d` (mine): `test_car.py` (delta gap: no laps either
  car, self has no laps, unequal counts), server-switch `player_car_idx`, YAML tick ⊂ frame ticks.
  Real bug behind one: `get_last_shared_completed_lap` checks only `other` has laps this session;
  self without → `KeyError`.
- **Facts, his:** `handle_events(session)` returns `list[EventFact]` (`event_fact.py`:
  `GapFact`, `CaughtFact` with nested `GapFact`, `event: ClassVar[str]`, `to_json`, `to_str`);
  speaking moved to `handle_event_facts(facts, speaker)`. No speaker in tests now. Shared loop
  steps pulled into `do_stuff()` (live + replay). He dropped subject/verb/object/adjunct for one
  dataclass per event: named typed fields, raw numbers (round when spoken), car resolved to a
  position for the line. Taught: dataclass inheritance (parent fields first, default-ordering
  `TypeError`, `kw_only`), `ClassVar`.
- Ruff: `extend-ignore-names = ["*iRacing*"]` (his commit `1244752`); 4 E501 left.
- Morning WIP landed (`b1cd935`): `test_caught_call` asserts per field with approx. Noted, open:
  `do_stuff` `session` param vs mypy; `Packet` wraps only `Session`; possible duplicate
  car-ahead `GapFact` when the car ahead is the caught car.
- Open: hub spec ([ideas/iracing-race-engineer.md](https://github.com/nosv1/nosv1/blob/main/ideas/iracing-race-engineer.md))
  still describes the live code fallback (dropped 10-13); offered to fix, no answer yet.

### 2026-10-20 (midday): Soma speaks live; race start, lap times

- **Two live races, Soma speaking** (recording on): `recordings/20261020-112829/` (14,830 frames)
  and `recordings/20261020-120232/` (9,058 frames, wheel came off; also the source of the
  `rolling_start` fixture). Both all valid JSON, STOP exit 0. He liked the speed after the
  line ("fast beats slow"). STOP file is `recordings/STOP` (`main.py` logs the path), not the run
  folder.
- **Bad calls heard:** "Caught P8 by 60.9 s", "Caught P9 by 7.4 s" (race 1; cause unknown, stubs
  in `test_caught_outliers.py`), "Caught P2 by 1.9 s" (race 2, cause found: the rolling-start
  crossing counted as a lap).
- **Race start, his fix:** `CarIdxLapCompleted` is −1 until the car first crosses; at the green
  it goes −1 → 0 with a pct wrap. He guarded on the old count ≥ 0 (renamed to "did finish lap").
  Also ignores tows / not-in-world flicker (−1 → n). `CarIdxLapCompleted` **resets per session**
  (checked in 3 recordings); his `event_laps_completed` name is misleading.
- **Lap times, his:** from his own crossings (this − previous timestamp); lap 1 = `None`.
  `CarIdxLastLapTime` was read at the crossing and was one lap stale (posts 1–2 s late, 10-18).
  His timings match official: median 0.0000 s, ~85% within 10 ms **at 10 Hz** (his comment said
  60 Hz; check it was fixed). Official lap 1 of a rolling start (72.01) ≠ his crossing diff
  (65.2): iRacing seems to time it from about the green; unverified.
- **Fixture `rolling_start`** (mine, `4d2adec`): race session 70–230 s, only the frame keys
  `src/soma` reads, 3.5 MB from 184 MB; laps match the full recording for all 12 cars.
  `tests/recordings/trim_recording.py` regenerates it; [tests/recordings/README.md](../tests/recordings/README.md)
  lists fixtures + the command. Rerun it when code reads a new var (e.g. `SessionFlags`).
- **Damage, answered:** on-track damage shows as `EngineWarnings` 0x80 / 0x100 (mandatory /
  optional repair), ~3 s before the incident count rose. `PitRepairLeft` / `PitOptRepairLeft`
  stayed 0.0 on track and on pit road; maybe only in the box (recording stopped before it).
- **HUD goal (his):** remove the whole HUD; each element is a call that speaks up or is asked.
  [hud.md](hud.md) (mine) lists them with source vars; priority + done are his. Vars added to
  `irsdk_vars.py`, all checked present in a real frame.
- **Flags, started (his):** `SessionFlags` is a bitfield; test bits with `&`, "turned on" =
  `new & ~old`. His plan: a `SessionFlag(IntFlag)` from the `irsdk.Flags` values (unknown bits
  are kept, no `_missing_` needed). `CarIdxSessionFlags` holds only per-car flags (meatball,
  black-flag warning, servicible) for every car, never track flags; player's bits mirror
  `SessionFlags` (backlog).
- Tests: stubs for delta-gap edges, server switch, YAML ticks, race start, outliers. Safety
  rating 2.36: sports car races, survive lap 1. Audio: set the headset as default output
  before starting Soma; switching mid-run untested (mine to test).
- Otto: Gazebo Fuel back; Depot model cached in WSL, setup gotcha committed there (`e015156`).

## Next

**Reordered 10-16:** a week in, no caught-call code yet. The list had polish ahead of the
feature (my ordering). Caught call goes first, against the replay loop as it stands.

0. Pre-sim habit: `uv run pytest`, `uv run mypy main.py src tests`, `uv run ruff check`.
1. His: **caught-call detection**, against the loader/replay loop as is. Redesign + delta test
   done 10-17 (`7d7cc60`). **Speaks 10-18**, calls correct on the 10-16 race. **Spoke live
   10-20.** **Next:** flags (race control voice, `SessionFlag`), then find the cause of the 60 s /
   7 s catches in `20261020-112829` (replay at those calls).
   Old plan, for reference: fix the
   0-laps guard, then a template voice line for the
   delta (load voice once; speaking blocks the loop; decide when it fires). Mini sectors after the line works. Keep it pure (snapshots in, event
   out) so it runs against recordings. Reference once he has his own:
   `git show 282c4a7:irsdk/irsdk_lapTiming/lapTiming.cpp`, `processLapInfo` (line crossing
   from `CarIdxLapDistPct` wrap).
2. His: explore the recording as (1) needs it. Open: `CarIdxPosition` on the grid before green,
   what `CarIdxF2Time` holds, YAML `ClassPosition` base.
3. **Parked until the caught call works** (not blocking it):
   - Live/replay unification: both sources yield `Snapshot`, one `for snapshot in source` loop;
     STOP during reconnect. Matters when running live; shape it from what the detector needs.
   - Verify replay end to end on the real recording (do this when (1) first runs).
   - Ruff leftovers, `possibly-undefined` in mypy config.
   - Recorder `index.json` → `{tick: file}`; gzip; recorder tests (stub in
     `tests/test_recorder.py`: every YAML tick is a frame tick); loader test nits (ticks as
     ordered list to catch dupes, fixture hint `dict[int, ...]`); `ir.disconnect()` on exit.
4. His: function signatures for the question list above, then 5–8 radio-style variants per
   question as `question → expected call` (incl. ambiguous ones → `clarify`). His spec.
5. Mine once (4) exists: router eval harness, 3B vs 8B; score correct call, correct `none`,
   correct `clarify` separately.
6. His: first projection (laps to catch), numbers/facts check.
