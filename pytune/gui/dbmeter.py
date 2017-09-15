'''
Created on Jan 28, 2013

@author: vahid
'''

from kivy.uix.widget import Widget 
from kivy.properties import NumericProperty
from pytune.analyser import Analyser
import numpy as np 
import math

class DecibelMeter(Widget):
    value = NumericProperty(45)
    padding = NumericProperty(70)
    max = NumericProperty(1.0)
    
    def __init__(self,*args,**kw):
        Widget.__init__(self,*args,**kw)
        Analyser().data_received += self.on_data_received
        
    def on_data_received(self,sender,data,frameno):
        peak = np.max(np.abs(data))
        peak = math.log(abs((peak-1) / 32768.0 * 9.0 + 1),10)
        self.value = peak
    
        
