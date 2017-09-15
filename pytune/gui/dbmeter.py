import math

import numpy as np
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.app import App


class DecibelMeter(Widget):
    value = NumericProperty(45)
    padding = NumericProperty(70)
    max = NumericProperty(1.0)

    def __init__(self, **kw):
        Widget.__init__(self, **kw)
        App.get_running_app().analyser.add_data_callback(self.on_data_received)

    def on_data_received(self, data, frameno):
        peak = np.max(np.abs(data))
        peak = math.log(abs((peak - 1) / 32768.0 * 9.0 + 1), 10)
        self.value = peak
