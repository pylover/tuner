from threading import Thread
import abc

from kivy.logger import Logger
import numpy as np

from tuner.inputs import MicrophoneReader
from tuner.configuration import settings, init as init_config
import tuner.algorithms as alg


class Analyser:
    """
    This class would be singleton and run on another thread, until the stop method called.
    Main role of this object is to detect the musical pitch(Note) from input: (file|microphone)
    """
    __metaclass__ = abc.ABCMeta
    __reader_factory__ = MicrophoneReader

    def __init__(self):
        self.counter = 0
        self.data_callbacks = []
        self.pitch_callbacks = []
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
            # freq = alg.freq_from_fft(data,settings.listen.samplerate)
            # freq = alg.freq_from_crossings(data,settings.listen.samplerate)
            freq = alg.freq_from_autocorr(data, settings.listen.samplerate)
            # freq = alg.freq_from_hps(data,settings.listen.samplerate)
            if freq is None or np.isnan(freq):
                return

            for c in self.pitch_callbacks:
                c(freq)
        except IndexError as ex:
            Logger.exception(ex)

    def _onread(self, data):
        self.counter += 1
        if self.data_callbacks:
            for c in self.data_callbacks:
                c(data, self.counter)

        if self.pitch_callbacks and self.pitch_buffer is not None:
            if len(self.pitch_buffer) >= settings.pitch_detection.chunk:
                self.detect_pitch(self.pitch_buffer)
                self.pitch_buffer = None
            else:
                self.pitch_buffer = np.concatenate((self.pitch_buffer, data))

        elif np.max(data) >= settings.pitch_detection.threshold:
            self.pitch_buffer = data

    def add_data_callback(self, callback):
        self.data_callbacks.append(callback)

    def add_pitch_detect_callback(self, callback):
        self.pitch_callbacks.append(callback)


if __name__ == '__main__':
    init_config()

    def ondata(data, index):
        print(index, data)

    def onpitch(freq):
        print('PITCH: ', freq)

    detector = Analyser()
    # detector.add_data_callback(ondata)
    detector.add_pitch_detect_callback(onpitch)
    try:
        detector.start()
    except KeyboardInterrupt:
        detector.stop()
