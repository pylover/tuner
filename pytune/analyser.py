from threading import Thread
import abc

from kivy.logger import Logger
import numpy as np

from pytune.inputs import MicrophoneReader
from pytune.common import singleton, Event
from pytune import config
import pytune.algorithms as alg


@singleton
class Analyser(object):
    """
    This class would be singleton and run on another thread, until the stop method called.
    Main role of this object is to detect the musical pitch(Note) from input: (file|microphone)
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, data_callback=None, pitch_callback=None):
        self.counter = 0
        self._thread = Thread(target=self.start)

        self.data_received = Event()
        self.pitch_detected = Event()
        self.pitch_buffer = None

        if callable(data_callback):
            self.data_received += data_callback
        if callable(pitch_callback):
            self.pitch_detected += pitch_callback

        self._create_reader()
        self._thread.start()

    def _create_reader(self):
        self.reader = MicrophoneReader()

    def start(self):
        self.reader.start(self._onread)

    def stop(self):
        self.reader.close()
        self._thread.join(timeout=5)

    def detect_pitch(self, data):
        try:
            # freq=  alg.freq_from_fft(data,config.listen.samplerate)
            # freq=  alg.freq_from_crossings(data,config.listen.samplerate)
            freq = alg.freq_from_autocorr(data, config.listen.samplerate)
            # freq=  alg.freq_from_hps(data,config.listen.samplerate)
            if freq is None or np.isnan(freq):
                return

            self.pitch_detected(self, freq)
        except IndexError as ex:
            Logger.exception(ex.message)

    def _onread(self, data):
        self.counter += 1
        self.data_received(self, data, self.counter)

        if self.pitch_buffer is not None:
            if len(self.pitch_buffer) >= config.pitch_detection.chunk:
                self.detect_pitch(self.pitch_buffer)
                self.pitch_buffer = None
            else:
                self.pitch_buffer = np.concatenate((self.pitch_buffer, data))

        elif np.max(data) >= config.pitch_detection.threshold:
            self.pitch_buffer = data


if __name__ == '__main__':
    detector = Analyser()
    detector.start()
    import time

    print('Sleeping !!!! OzOzo')
    time.sleep(1)
    detector.stop()
