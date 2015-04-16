# setup-ftpd.py - for ftpd.py --> ftpd.exe
from distutils.core import setup
import py2exe

setup(name='ftpd',scripts=['ftpd.py'])
