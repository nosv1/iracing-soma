import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from queue import Queue

from soma.iracing import iRacing
from soma.irsdk_vars import SESSION_TICK

logger = logging.getLogger(__file__)


class Recorder:
    def __init__(self, output_dir: Path, iracing_fps: int, recorded_fps: int = 10):
        self.init_time = datetime.now().strftime("%Y%m%d-%H%M%S")

        self._output_dir = output_dir / self.init_time
        self._yaml_history_dir = self._output_dir / "yaml_history"

        # iracing outputs at 60 fps,
        # the recorder can decide how often each of those frames gets recorded
        # 60 / 10 = 6 frames between recorded frames
        self._tick_delay = iracing_fps / recorded_fps

        self.q: Queue[str] = Queue()  # iRacing frames, json dumps
        # append this to the queue to stop the thread
        self.STOP = "STOP"

        self._output_dir.mkdir(parents=True, exist_ok=False)
        self._yaml_history_dir.mkdir(parents=True, exist_ok=False)
        # {str(tick_number): str(file_name)}]}
        self._yaml_idx: dict[str, str] = {}

        self._prev_session_info_update = -1
        self._prev_recorded_tick = 0
        self._cur_session_tick = lambda ir: ir.ir[SESSION_TICK]

        self._t = threading.Thread(target=self.writer)
        self._t.start()
        logger.info(
            "Recorder initialized:\n" f"\tFrames recorded per second={recorded_fps}"
        )

    @property
    def next_recorded_tick(self):
        return self._tick_delay + self._prev_recorded_tick

    def update_yaml_idx(self, cur_tick: int, filename: str):
        self._yaml_idx[str(cur_tick)] = filename
        with open(self._yaml_history_dir / "index.json", "w+") as f:
            json.dump(self._yaml_idx, f, indent=4)

    def record_iRacing_session_yaml(self, ir: iRacing):
        # only record the session if there's been an update
        cur_session_info_update = ir.ir.session_info_update
        if self._prev_session_info_update == cur_session_info_update:
            return
        self._prev_session_info_update = cur_session_info_update

        h = ir.ir._header
        yaml_bytes = bytes(
            ir.ir._shared_mem[
                h.session_info_offset : h.session_info_offset + h.session_info_len
            ]
        ).rstrip(b"\x00")
        cur_tick = self._cur_session_tick(ir)
        filename = f"{cur_tick:07}-{datetime.now().timestamp()}.yaml"

        # write yaml file
        with open(
            self._yaml_history_dir / filename,
            "wb",
        ) as f:
            f.write(yaml_bytes)

        # update the index
        self.update_yaml_idx(cur_tick, filename)

    def queue_iRacing_frame(self, ir: iRacing) -> bool:
        """returns bool on whether or not the frame was queued for recording"""
        # only queue the frame if enough ticks have passed
        cur_session_tick = self._cur_session_tick(ir)
        if cur_session_tick < self._prev_recorded_tick:
            self._prev_recorded_tick = cur_session_tick
            logger.info("Reset previous recorded tick")

        if cur_session_tick < self.next_recorded_tick:
            return False

        self._prev_recorded_tick = cur_session_tick

        self.q.put(json.dumps({name: ir.ir[name] for name in ir.ir.var_headers_names}))
        return True

    def handle_new_tick(self, ir: iRacing):
        queued = self.queue_iRacing_frame(ir)
        if queued:
            self.record_iRacing_session_yaml(ir)

    def writer(self):
        with open(self._output_dir / "frames.txt", "a") as f:
            while True:
                item = self.q.get()
                if item is self.STOP:
                    break
                f.write(f"{item}\n")
