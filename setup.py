import re
from os.path import join, dirname
from setuptools import setup, find_packages

# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'tuner', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

dependencies = [
    'kivy',
    'pymlconf',
    'kivy',
    'pyaudio',
    'numpy',
    'scipy',
    'pygame'
]

setup(
    name="tuner",
    description="Musical instrument tuner using Kivy.",
    version=package_version,
    author="Vahid Mardani",
    url="http://github.com/pylover/tuner",
    author_email="vahid.mardani@gmail.com",
    long_description=open('README.md').read(),
    install_requires=dependencies,
    packages=find_packages(),
    package_data={
        'tuner': [
            'data/*.yaml',
            'gui/*.kv',
            'gui/styles/*.kv'
        ]
    },
    # data_files=[('', ['tuner/data/*.yaml'])],
    entry_points={
        'console_scripts': [
            'tuner = tuner:main'
        ]
    }
)
