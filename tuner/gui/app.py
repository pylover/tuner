from kivy.app import App
from tuner.analyser import Analyser


class TunerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyser = Analyser()

    def on_start(self):
        self.analyser.start()
        App.on_start(self)

    def on_stop(self):
        App.on_stop(self)
        self.analyser.stop()
