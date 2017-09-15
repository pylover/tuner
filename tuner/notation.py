import math

MIDI_TABLE = {0: 'C',
              1: 'C#',
              2: 'D',
              3: 'D#',
              4: 'E',
              5: 'F',
              6: 'F#',
              7: 'G',
              8: 'G#',
              9: 'A',
              10: 'A#',
              11: 'B',
              12: 'C'}


class units:
    midi = 'midinumber'
    cents = 'cents'
    savart = 'savart'


class Note:
    def __init__(self, frequency=None, midi_number=None, lafreq=440.0):
        assert (frequency is not None) ^ (midi_number is not None), 'one of frequency or midi_number must be passed'
        self.la = lafreq
        self.frequency = frequency if frequency else (2.0 ** ((midi_number - 69.0) / 12.0)) * self.la

    @property
    def accurate(self):
        return math.log(self.frequency / self.la, 2) * 12.0 + 69.0

    @property
    def midinumber(self):
        return int(round(self.accurate))

    @property
    def distance(self):
        return self.accurate - self.midinumber

    @property
    def name(self):
        return MIDI_TABLE[self.midinumber % 12]

    @property
    def octave(self):
        return self.midinumber / 12

    @property
    def fullname(self):
        return '%s%.2F' % (self.name, self.octave)

    def walk(self, step=1, unit=units.midi):
        return Note(midi_number=self.midinumber + step, lafreq=self.la)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '%s%s%s' % (self.name, self.octave, '(%.2F)' % self.distance if self.distance else '')


class PersianNote(Note):
    pass


if __name__ == '__main__':
    n = Note(880)
    print(n)
    for i in range(-14, 14):
        print(n.walk(i))
