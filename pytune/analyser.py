from threading import Thread
import abc

from kivy.logger import Logger
import numpy as np

from pytune.inputs import MicrophoneReader
from pytune.configuration import settings, init as init_config
import pytune.algorithms as alg


class Analyser:
    """
    This class would be singleton and run on another thread, until the stop method called.
    Main role of this object is to detect the musical pitch(Note) from input: (file|microphone)
    """
    __metaclass__ = abc.ABCMeta
    __reader_factory__ = MicrophoneReader

    def __init__(self, data_callback=None, pitch_callback=None):
        self.counter = 0
        self.data_received = data_callback
        self.pitch_detected = pitch_callback
        self.pitch_buffer = None
        self.reader = self.__reader_factory__(self._onread)
        self._thread = Thread(target=self.listen)

    def listen(self):
        self.reader.open()
        # This call will blocks the current thread.
        self.reader.start()

    def start(self):
        self._thread.start()

    def stop(self):
        self.reader.stop()
        self._thread.join(timeout=5)
        self.reader.close()

    def detect_pitch(self, data):
        try:
            # freq=  alg.freq_from_fft(data,settings.listen.samplerate)
            # freq=  alg.freq_from_crossings(data,settings.listen.samplerate)
            freq = alg.freq_from_autocorr(data, settings.listen.samplerate)
            # freq=  alg.freq_from_hps(data,settings.listen.samplerate)
            if freq is None or np.isnan(freq):
                return

            self.pitch_detected(freq)
        except IndexError as ex:
            Logger.exception(ex.message)

    def _onread(self, data):
        self.counter += 1
        if self.data_received:
            self.data_received(data, self.counter)

        if self.pitch_detected is not None and self.pitch_buffer is not None:
            if len(self.pitch_buffer) >= settings.pitch_detection.chunk:
                self.detect_pitch(self.pitch_buffer)
                self.pitch_buffer = None
            else:
                self.pitch_buffer = np.concatenate((self.pitch_buffer, data))

        elif np.max(data) >= settings.pitch_detection.threshold:
            self.pitch_buffer = data


if __name__ == '__main__':
    init_config()

    def ondata(data, index):
        print(index, data)

    detector = Analyser(data_callback=ondata)
    try:
        detector.start()
    except KeyboardInterrupt:
        detector.stop()
