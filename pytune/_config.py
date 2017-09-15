'''
Created on Jan 26, 2013

@author: vahid
'''

from pymlconf import ConfigManager
from os import path
import pyaudio
root_dir = path.abspath(path.join(path.dirname(__file__),'..'))


config = ConfigManager(

    init_value={
        'width': 480,
        'height': 640,
        'samples_dir': path.join(root_dir,'samples'),
        #'chunk_size': 44032 / 8,
        'listen':{
            'chunk': 1024,
            'channels': 1,
            'samplerate': 44100,
            'format': pyaudio.paInt16
        },
        'pitch_detection': {
            'threshold': 32768 / 4,
            'chunk': 1024 * 5
            }
        }
)

#*    fft        crossings    autocorr    hps
#1    50.06 Hz    73.01 Hz    50.11 Hz    4.15 Hz

#*    fft        crossings    autocorr    hps
#1    50.15 Hz    71.86 Hz    50.12 Hz    13.13 Hz
#2    50.19 Hz    73.90 Hz    50.11 Hz    12.80 Hz

#*    fft        crossings    autocorr    hps
#1    49.92 Hz    71.00 Hz    50.13 Hz    19.01 Hz
#2    49.99 Hz    74.68 Hz    50.13 Hz    17.41 Hz
#3    50.07 Hz    79.31 Hz    50.12 Hz    18.54 Hz
#4    49.99 Hz    70.33 Hz    50.12 Hz    21.50 Hz

#*    fft        crossings    autocorr    hps
#1    49.23 Hz    70.05 Hz    50.19 Hz    33.13 Hz
#2    50.20 Hz    75.19 Hz    50.17 Hz    32.79 Hz
#3    56.74 Hz    70.31 Hz    50.26 Hz    33.16 Hz
#4    51.17 Hz    75.35 Hz    50.25 Hz    31.65 Hz
#5    47.74 Hz    100.59 Hz   50.23 Hz    30.64 Hz
#6    49.52 Hz    66.78 Hz    50.12 Hz    31.73 Hz
#7    51.70 Hz    80.38 Hz    50.15 Hz    31.38 Hz
#8    51.48 Hz    64.77 Hz    50.15 Hz    31.94 Hz