import logging
import threading
from queue import Queue

import sounddevice
from piper import PiperVoice

logger = logging.getLogger(__file__)


class Speaker:
    def __init__(self, voice: PiperVoice, use_thread: bool = True):
        self.voice = voice
        self.q: Queue[str] = Queue()
        # append this to the queue to stop the thread
        self.STOP = "STOP"

        self._use_thread: bool = use_thread
        if self._use_thread:
            self._t = threading.Thread(target=self.speaker)
            self._t.start()

        self.add_to_queue("Speaker initialized")

    def add_to_queue(self, text: str):
        self.q.put(text)
        if not self._use_thread:
            self.speaker()

    def speaker(self):
        while self._use_thread or not self.q.empty():
            item = self.q.get()
            if item is self.STOP:
                break
            logger.info(f"Speaking:\n{item}")
            chunk_array = self.voice.synthesize(item)

            for chunk in chunk_array:
                sounddevice.play(chunk.audio_float_array, chunk.sample_rate)
                sounddevice.wait()

    def stop(self):
        self.q.put(self.STOP)
        if self._use_thread:
            self._t.join()
