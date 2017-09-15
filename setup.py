
import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'pytune', '__init__.py')) as v_file:
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
    name="pytune",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid.mardani@gmail.com",
    long_description=open('README.md').read(),
    install_requires=dependencies,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pytune = pytune:main'
        ]
    }
)
