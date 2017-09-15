


import fnmatch
import os
import re
import kivy
from .gui.app import PyTuneApp
from ._config import config

__version__ = '1.0.0'
kivy.require('1.5.1') 

rootdir = os.path.abspath(os.path.dirname(__file__))
stylesdir = os.path.join(rootdir,'gui','styles')
configfile = os.path.join(rootdir,'config.ini')



def start():
    from kivy.config import Config as KivyConfig
    from kivy.lang import Builder
    from kivy.logger import Logger
    
    KivyConfig.set('graphics', 'width', config.width)
    KivyConfig.set('graphics', 'height', config.height)

    #Config.read('config.ini')
    for root, _dirs, files in os.walk(stylesdir):
        files = [os.path.join(root, f) for f in files if re.match(fnmatch.translate('*.kv'),f)]
        for f in files:
            Logger.debug('loading style file: %s' % f)
            Builder.load_file(f)
    PyTuneApp().run()
    
    

__all__ = ['__version__',
           'config'
           'PyTuneApp']