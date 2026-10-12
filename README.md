# iracing-soma

Soma — Strategy Operations and Monitoring Assistant. A spoken race engineer for iRacing.

Successor to the ACC version in [strategist](https://github.com/nosv1/strategist).

## What it does

Nothing yet. First milestone: at each start/finish crossing, call out the same-class car ahead
you gained the most time on — "Caught Smith by 0.8 seconds."

## Running it

Windows only (iRacing telemetry is Windows shared memory). Python 3.14.

```bat
python3.14 -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
.venv\Scripts\python -m piper.download_voices --download-dir voices en_GB-southern_english_female-low
.venv\Scripts\ruff check .
```

## What I learned

## What broke
