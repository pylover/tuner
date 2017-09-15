#! /usr/bin/env python



cent = 1
chromatic_interval = 100 * cent
octave = cent * 1200
octave = chromatic_interval * 12
savart = cent / 4

shoor = [
    (25.00, 'C'),
    (25.00, 'C#'),
    (12.50, 'D<'),
    (12.50, 'D'),
    (25.00, 'D#'),
    (12.50, 'E<'),
    (12.50, 'E'),
    (25.00, 'F'),
    (12.50, 'F>'),
    (12.50, 'F#'),
    (12.50, 'G<'),
    (12.50, 'G'),
    (25.00, 'G#'),
    (12.50, 'A<'),
    (12.50, 'A'),
    (25.00, 'A#'),
    (12.50, 'B<'),
    (12.50, 'B'),
]
class NoteTable(object):
    mincent = -6900
    maxcent = 5800
    def __init__(self,intervals,format='cent'):
        self.format = format
        self.table = [] # [cent,octave,number,name]
        cursor = self.mincent - self.__get_cents(intervals[0][0])
        icursor = 0
        counter = 0
        while cursor < self.maxcent:
            cursor += self.__get_cents( intervals[icursor][0])
            octave = counter % len(intervals)
            self.table.append([
                cursor,
                octave,
                counter,
                intervals[icursor][1]])
            icursor = icursor + 1 if icursor < len(intervals)-1 else 0
    def __get_cents(self,val):
        if self.format == 'cent':
            return val
        elif self.format == 'savart':
            return val * 4.0
        else:
            raise Exception('invalid format: %s' % self.format)
        
    def find(self,cent):
        candidate = self.table[0]
        candidate_abs = 999999.9
        for row in self.table[1:]:
            absdiff = abs(row[0] - cent) 
            candidate[0] - cent
            if  < :
                candidate = row
            elif row[0] - cent == candidate[0] - cent:
                return row
            elif row[0] - cent > candidate[0] - cent:
                break;
        return candidate
    
class PerisanNote(object):
    def __init__(self,freq,la=440.0):
        self.frequency = float(freq)
        self.la = la

    @property
    def name(self):
        return 'NaN'

    def __repr__(self):
        return self.name

if __name__ == '__main__':
    #A = PersianNote(440)
    #print A
    t = NoteTable(shoor,format='savart')
    for row in t.self.table[:]:
        print row
