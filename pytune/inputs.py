'''
Created on Feb 13, 2013

@author: vahid
'''

import abc
from pytune import config
import pyaudio
import numpy as np

class AudioReader(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        pass
    
    def start(self,callback):
        assert callable(callback), "Invalid Callback"
        self.callback = callback
        self._start()
    
    def close(self):
        self._close()
        self.callback = None

    def _callback(self,*args,**kwargs):
        if self.callback:
            self.callback(*args,**kwargs)

    @abc.abstractmethod
    def _start(self):
        pass

    @abc.abstractmethod
    def _close(self):
        pass
    

class MicrophoneReader(AudioReader):
    
    def __init__(self):
        self.__stop_flag = False # there are just a boolean for flag, Bingo! atomic operations does not requires high-level lock objects.
        
    def _start(self):
        p = pyaudio.PyAudio()
    
        
        try:
            stream = p.open(format=config.listen.format,
                        channels=config.listen.channels,
                        rate=config.listen.samplerate,
                        input=True,
                        frames_per_buffer=config.listen.chunk)
            
            while not self.__stop_flag:
                data = stream.read(config.listen.chunk)
                self._callback(np.fromstring(data,dtype=np.int16))
        except:
            stream.close()
            raise
            
    
    def _close(self):
        self.__stop_flag = True
