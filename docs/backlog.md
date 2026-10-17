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
  `PitOptRepairLeft`, fast repair).
- **Start reaction time**: green flag → my reaction, for standing and rolling starts.
  - Green: the `SessionFlags` green bit, or `SessionState` changing to racing (check which is
    first). Reaction: `Throttle` onset is probably cleaner than a jump in `Speed`, which lags.
  - The 10 Hz recordings are too coarse (100 ms steps against a ~200–500 ms reaction). Live
    60 Hz is 17 ms. Or record at 60 Hz around the start (ties into the fps config below).
- **Config file**: settings out of `main.py`, starting with recorded fps.
- **Ruff N802 on `iRacing` names** (`recorder.py`): keep the casing and silence ruff. Either a
  per-line `# noqa: N802`, or once in `pyproject.toml` under `[tool.ruff.lint.pep8-naming]`.
  A noqa comment above the line didn't work; ask why.
