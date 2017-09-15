import math

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.app import App

from tuner.configuration import settings


class Spectrum(Widget):
    lines = NumericProperty(32)
    lw = NumericProperty(1)
    buffer = ListProperty()
    color = ListProperty([0, 1, 0, 1])

    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        App.get_running_app().analyser.add_data_callback(self.on_data_received)
        self.buffer = [0] * self.lines
        self._max = 0

    def on_data_received(self, data, frameno):
        counter = 0
        downsampling_rate = settings.listen.chunk / 4
        result = []
        thrshld = .01
        bag = 0.0
        for i in data / 2:
            bag += abs(i)
            counter += 1
            if counter % downsampling_rate == 0:
                ff = math.log(bag / downsampling_rate * 9.0 / 32768.0 + 1, 10)
                if ff < thrshld:
                    ff = 0.0
                result.append(ff)

                bag = 0.0
        self.buffer = self.buffer[4:] + result

    def getpoints(self, data, index):
        x = self.x + self.width / self.lines * index
        if not self.buffer:
            return x, self.y, x, self.y
        power = self.buffer[index] * self.height / 2
        return x, self.center_y - power, x, self.center_y + power
