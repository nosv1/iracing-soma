import json
import threading
from datetime import datetime
from pathlib import Path
from queue import Queue

from soma.iracing import iRacing
from soma.irsdk_vars import SESSION_TICK


class Recorder:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.q: Queue[dict] = Queue()  # iRacing frames
        self.STOP = object()

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.prev_session_info_update = -1
        self.prev_session_tick = -1

        self.t = threading.Thread(target=self.writer)
        self.t.start()

    def record_iRacing_session_yaml(self, ir: iRacing):
        cur_session_info_update = ir.ir.session_info_update
        if self.prev_session_info_update == cur_session_info_update:
            return
        self.prev_session_info_update = cur_session_info_update

        h = ir.ir._header
        yaml_bytes = bytes(
            ir.ir._shared_mem[
                h.session_info_offset : h.session_info_offset + h.session_info_len
            ]
        ).rstrip(b"\x00")
        with open(
            f"{self.output_dir / str(datetime.now().timestamp())}-session.yaml", "wb"
        ) as f:
            f.write(yaml_bytes)

    def queue_iRacing_frame(self, ir: iRacing):
        cur_session_tick = ir.ir[SESSION_TICK]
        if self.prev_session_tick == cur_session_tick:
            return
        self.prev_session_tick = cur_session_tick

        ir.ir.freeze_var_buffer_latest()
        self.q.put(json.dumps({name: ir.ir[name] for name in ir.ir.var_headers_names}))

    def writer(self):
        with open(f"{self.output_dir / str(datetime.now().timestamp())}.txt", "a") as f:
            while True:
                item = self.q.get()
                if item is self.STOP:
                    break
                f.write(f"{item}\n")
