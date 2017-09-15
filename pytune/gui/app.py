
from kivy.app import App
from pytune.analyser import Analyser


class PyTuneApp(App):
    def __init__(self, *args, **kwargs):
        App.__init__(self, *args, **kwargs)
        self.analyser = Analyser()

    #    def on_start(self,*args,**kwargs):
    #        App.on_start(self,*args,**kwargs)

    def on_stop(self, *args, **kwargs):
        App.on_stop(self, *args, **kwargs)
        self.analyser.stop()
