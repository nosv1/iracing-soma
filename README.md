# iracing-soma

Soma — Strategy Operations and Monitoring Assistant. A spoken race engineer for iRacing.

Successor to the ACC version in [strategist](https://github.com/nosv1/strategist).

## What it does

Nothing yet. First milestone: at each start/finish crossing, call out the same-class car ahead
you gained the most time on — "Caught Smith by 0.8 seconds."

## Running it

Windows only (iRacing telemetry is Windows shared memory). Python 3.14.

Needs [uv](https://docs.astral.sh/uv/) (`winget install astral-sh.uv`).

```bat
uv sync
uv run python -m piper.download_voices --download-dir voices en_GB-southern_english_female-low
uv run main.py
uv run ruff check .
```

Add a dependency with `uv add <pkg>` (or `uv add --dev <pkg>` for tooling).

## What I learned

## What broke
