import abc

import numpy as np
import pyaudio

from tuner.configuration import settings


class AudioReader(object, metaclass=abc.ABCMeta):
    def __init__(self, callback):
        self.callback = callback

    def _callback(self, *args, **kwargs):
        if self.callback:
            self.callback(*args, **kwargs)

    @abc.abstractmethod
    def open(self):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class MicrophoneReader(AudioReader):
    stream = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio = pyaudio.PyAudio()
        # there are just a boolean for flag, Bingo! atomic operations does not requires high-level lock objects.
        self._stop_flag = False

    def open(self):
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=settings.listen.channels,
            rate=settings.listen.samplerate,
            input=True,
            frames_per_buffer=settings.listen.chunk
        )

    def start(self):
        while not self._stop_flag:
            data = self.stream.read(settings.listen.chunk)
            self._callback(np.fromstring(data, dtype=np.int16))

    def stop(self):
        # This method will be called within another thread.
        self._stop_flag = True

    def close(self):
        self.stream.close()

