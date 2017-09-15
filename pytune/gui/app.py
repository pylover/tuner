from kivy.app import App
from pytune.analyser import Analyser


class PyTuneApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyser = Analyser()

    def on_start(self):
        self.analyser.start()
        App.on_start(self)

    def on_stop(self):
        App.on_stop(self)
        self.analyser.stop()
