import math

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty
from kivy.animation import Animation
from kivy.app import App
from tuner.notation import Note


class AnalogDisplay(Widget):
    value = NumericProperty(0)
    padding = NumericProperty(70)
    needle_length = NumericProperty(0.0)
    guide_length = NumericProperty(16)
    subguide_length = NumericProperty(12)
    guide_width = NumericProperty(3)
    subguide_width = NumericProperty(1)
    minvalue = NumericProperty(30)
    maxvalue = NumericProperty(150)
    notes = ListProperty()
    la = NumericProperty(440)

    def __init__(self, **kwargs):
        Widget.__init__(self, **kwargs)
        App.get_running_app().analyser.add_pitch_detect_callback(self.on_pitch_detected)
        self.bind(la=self.on_la_changed)

    def on_la_changed(self, *args, **kwargs):
        pass

    def on_pitch_detected(self, freq):
        note = Note(frequency=freq, lafreq=self.la)
        self.notes = [note.walk(-1), note, note.walk(1)]
        val = note.distance + 1.0
        expect_max = self.maxvalue - self.minvalue
        expect_value = val * expect_max / 2 + self.minvalue
        Animation(value=expect_value, transition='out_back', duration=.5).start(self)

    def calc_needle_points(self, pos, size, padding, needle_length, value):
        y = pos[1] + padding
        rad = math.radians(value)
        return \
            self.center_x, \
            y, \
            self.center_x - math.cos(rad) * needle_length, \
            y + math.sin(rad) * needle_length

    def calc_label_positions(self, degree, length, pos, size):
        y = pos[1] + self.padding
        rad = math.radians(degree)
        sinrad = math.sin(rad)
        cosrad = math.cos(rad)
        # hypoend = self.needle_length + length
        hypostart = self.needle_length + self.padding / 2.0
        return \
            self.center_x - cosrad * hypostart, \
            y + sinrad * hypostart

    def calc_guidelines(self, degree, length, val, pos, size):
        # TODO: remove val
        y = pos[1] + self.padding
        rad = math.radians(degree)
        sinrad = math.sin(rad)
        cosrad = math.cos(rad)
        hypoend = self.needle_length + length
        hypostart = self.needle_length + self.padding / 2.0
        return \
            self.center_x - cosrad * hypostart, \
            y + sinrad * hypostart, \
            self.center_x - cosrad * hypoend, \
            y + sinrad * hypoend
