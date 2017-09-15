'''
Created on Jan 22, 2013

@author: vahid
'''
from kivy.app import App


class PyTuneApp(App):
    
    def __init__(self,*args,**kwargs):
        App.__init__(self,*args,**kwargs)
        
        
#    def on_start(self,*args,**kwargs):
#        App.on_start(self,*args,**kwargs)
        
    def on_stop(self,*args,**kwargs):
        from pytune.analyser import Analyser
        App.on_stop(self,*args,**kwargs)
        Analyser().stop()
        
        