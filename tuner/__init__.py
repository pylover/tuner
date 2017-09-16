import fnmatch
import os
import re

from kivy.config import Config as KivyConfig
from kivy.lang import Builder
from kivy.logger import Logger

from .gui.app import TunerApp
from .configuration import settings, init as init_config

__version__ = '1.0.0b2'

rootdir = os.path.abspath(os.path.dirname(__file__))
stylesdir = os.path.join(rootdir, 'gui', 'styles')
configfile = os.path.join(rootdir, 'config.ini')


def main():
    init_config()
    KivyConfig.set('graphics', 'width', settings.width)
    KivyConfig.set('graphics', 'height', settings.height)

    for root, _dirs, files in os.walk(stylesdir):
        files = [os.path.join(root, f) for f in files if re.match(fnmatch.translate('*.kv'), f)]
        for f in files:
            Logger.debug('loading style file: %s' % f)
            Builder.load_file(f)
    TunerApp().run()
