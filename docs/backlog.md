# Backlog

Chris's ideas, captured raw. Not prioritized, not specced; expand when picked up.

- **Spotter**: car left / right / clear calls.
- **Flag announcements**: speak flag changes.
  - **Time until intercept on a local yellow**: how long until I reach the yellow.
- **Which split am I in**: answer on request.
- **Race-distance milestones**: call out when laps left halves: halfway, quarter to go, and so
  on.
  - **Trap, timed races**: laps left is an estimate from the leader's pace, so it can move. A
    milestone could fire twice or get skipped; needs a rule.
- **Repair time**: how long the repair will take, before committing to the pit. Already on the
  question list in [notes.md](notes.md) with the vars to check (`PitRepairLeft`,
  `PitOptRepairLeft`, fast repair). `EngineWarnings` also has repairs-needed bits (`0x0080`
  mandatory, `0x0100` optional): may say "damaged" on track even if the times don't fill in yet.
- **Oil pressure warning**: speak it when the warning light comes on. `EngineWarnings & 0x0004`
  (pyirsdk `EngineWarnings.oil_pressure_warning`); `OilPress` (bar) is there for the trend.
  Needs a "what to do" (short shift? box?), and a check that it doesn't fire falsely on session
  start (OblivionsPeak hit that with its engine warnings).
- **Water temp in the draft (ovals)**: bump drafting blocks the radiator, temp climbs fast. Call
  it from the rate of rise, before the light: "temps climbing, get some air", maybe with time to
  the warning at the current rate. `WaterTemp` (C); light is `EngineWarnings & 0x0001`. Unknown:
  the threshold per car, and how fast it cools in clean air.
- **Start reaction time**: green flag → my reaction, for standing and rolling starts.
  - Green: the `SessionFlags` green bit, or `SessionState` changing to racing (check which is
    first). Reaction: `Throttle` onset is probably cleaner than a jump in `Speed`, which lags.
  - The 10 Hz recordings are too coarse (100 ms steps against a ~200–500 ms reaction). Live
    60 Hz is 17 ms. Or record at 60 Hz around the start (ties into the fps config below).
- **Braking smoothness**: a reading on how smooth my braking is.
  - Open: smooth how? Spiky application, a ragged release (trail braking), or pumping mid-zone.
    Each is a different measure; pick one first.
  - `Brake` / `BrakeRaw` (0–1), `BrakeABSactive`, `LongAccel` (`LongAccel_ST` is 360 Hz). Pedal
    traces need more than 10 Hz: live 60 Hz, or record faster (fps config below).
  - Needs a "what to do", and when to say it (after the corner? end of lap? on request?).
- **Watch my splits**: running alone, chasing or managing, I want to know how my laps look
  without a dash that shows a projected lap.
  - Projected lap ≈ reference lap + live delta: `LapDeltaToBestLap`,
    `LapDeltaToSessionBestLap`, `LapDeltaToOptimalLap`, `LapDeltaToSessionLastlLap` (sic), each
    with an `_OK` valid flag and a `_DD` rate. `LapCurrentLapTime` is the F3-box estimate.
  - Open: which reference (my best, last lap, session best), and what it says: projected lap,
    up/down vs reference, trend over the last few laps.
- **"Keep me posted on X"**: tell Soma to watch something more or less often, by voice.
  - Shape: a watch list, topic → how often (every lap, every sector, only on change, stop).
    Splits above would be the first topic.
  - Fits the router: "keep me posted on lap times" → a function call with topic + cadence.
  - Ties to per-key cooldowns on callouts (OblivionsPeak's `CalloutManager`, in notes.md).
- **Radio effects**: make Soma sound like team radio, not a clean TTS voice.
  - Usual recipe: band-pass (roughly 300–3000 Hz), a little distortion/compression, light
    static, a click or squelch at the start and end of each line.
  - Lives in `Speaker`, between `synthesize` and `play`: Piper chunks are NumPy arrays, so the
    filter is array in, array out (SciPy has the filters). Pre-render the click once.
  - Watch for added latency (spotter calls later), and readability: radio filtering makes
    speech harder to understand, so keep it mild or make it switchable.
- **Config file**: settings out of `main.py`, starting with recorded fps.
- **Ruff N802 on `iRacing` names** (`recorder.py`): keep the casing and silence ruff. Either a
  per-line `# noqa: N802`, or once in `pyproject.toml` under `[tool.ruff.lint.pep8-naming]`.
  A noqa comment above the line didn't work; ask why.
