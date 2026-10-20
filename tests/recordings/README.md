# Test recordings

Fixtures in the recorder's format (`frames.txt` + `yaml_history/`), read with `Loader`.

| Fixture | What | Made by |
| --- | --- | --- |
| `valid` | small recording, cp1252 driver name, YAML switch at tick 630 | hand |
| `yaml_tick_without_frame` | a YAML tick with no matching frame (loader must raise) | hand |
| `laps` | 2 cars at constant speed, 4 s laps, known crossings and deltas | hand |
| `laps_p2` | `laps` with the player at P2 | hand |
| `laps_p3` | 3 cars, player P3, sorted delta order differs from position order | hand |
| `rolling_start` | 10-20 race, 70–230 s: rolling start through the end of lap 2 | `trim_recording.py` |

## Cutting a fixture from a real recording

Full recordings live in `recordings/` (gitignored, hundreds of MB). `trim_recording.py`
keeps one session's frames within a time window, and only the frame variables that
`src/soma` reads, so the fixture stays a few MB.

```
uv run python tests/recordings/trim_recording.py <full recording> <fixture dir> \
    --session <SessionNum> --start <SessionTime s> --end <SessionTime s>
```

`rolling_start` was made with:

```
uv run python tests/recordings/trim_recording.py \
    recordings/20261020-120232 tests/recordings/rolling_start \
    --session 2 --start 70 --end 230
```

**Regenerate when code reads a new variable** (a `KeyError` in a test on this fixture).
The fixture dir must not exist; delete it first. Then check the laps still match (they
should: only columns are added).
