"""Cut a test fixture out of a full recording.

Keeps frames of one session within [start, end] seconds of SessionTime, and only the
frame keys that soma's code reads (the irsdk_vars constants used outside
irsdk_vars.py), so fixtures stay small. YAML snapshots inside the window are copied;
the one in effect at the window's first frame is re-keyed to that frame's tick, since
the loader requires every YAML tick to be a frame tick.

If code starts reading a new var, the fixture won't have it: re-run this on the full
recording (kept in the gitignored recordings/).

    uv run python tests/recordings/trim_recording.py \
        recordings/20261020-120232 tests/recordings/rolling_start \
        --session 2 --start 70 --end 230
"""

import argparse
import json
import re
import shutil
from pathlib import Path

from soma import irsdk_vars

SRC_DIR = Path(irsdk_vars.__file__).parent


def used_keys() -> set[str]:
    code = "\n".join(
        p.read_text(encoding="utf-8")
        for p in SRC_DIR.glob("*.py")
        if p.name != "irsdk_vars.py"
    )
    return {
        value
        for name, value in vars(irsdk_vars).items()
        if name.isupper() and isinstance(value, str) and re.search(rf"\b{name}\b", code)
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=Path)
    parser.add_argument("dst", type=Path)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--start", type=float, required=True)
    parser.add_argument("--end", type=float, required=True)
    args = parser.parse_args()

    keys = used_keys() | {irsdk_vars.SESSION_TICK}
    index: dict[str, str] = json.loads(
        (args.src / "yaml_history" / "index.json").read_text()
    )
    yaml_ticks = sorted(int(t) for t in index)

    kept_ticks: list[int] = []
    (args.dst / "yaml_history").mkdir(parents=True, exist_ok=False)
    with (
        open(args.src / "frames.txt", encoding="utf-8") as f_in,
        open(args.dst / "frames.txt", "w", encoding="utf-8") as f_out,
    ):
        for line in f_in:
            frame = json.loads(line)
            if frame[irsdk_vars.SESSION_NUM] != args.session:
                continue
            if not args.start <= frame[irsdk_vars.SESSION_TIME] <= args.end:
                continue
            f_out.write(json.dumps({k: frame[k] for k in keys if k in frame}) + "\n")
            kept_ticks.append(frame[irsdk_vars.SESSION_TICK])

    first, last = kept_ticks[0], kept_ticks[-1]
    new_index: dict[str, str] = {}
    # (source tick, tick in the fixture): the YAML in effect moves to the first frame
    in_effect = max(t for t in yaml_ticks if t <= first)
    pairs = [(in_effect, first)] + [(t, t) for t in yaml_ticks if first < t <= last]
    for src_tick, dst_tick in pairs:
        src_name = index[str(src_tick)]
        dst_name = f"{dst_tick:07d}-{src_name.split('-', 1)[1]}"
        shutil.copy(
            args.src / "yaml_history" / src_name, args.dst / "yaml_history" / dst_name
        )
        new_index[str(dst_tick)] = dst_name
    (args.dst / "yaml_history" / "index.json").write_text(
        json.dumps(new_index, indent=4)
    )

    print(f"{len(kept_ticks)} frames, ticks {first}..{last}, {len(new_index)} YAML")
    print(f"{len(keys)} keys: {sorted(keys)}")


if __name__ == "__main__":
    main()
