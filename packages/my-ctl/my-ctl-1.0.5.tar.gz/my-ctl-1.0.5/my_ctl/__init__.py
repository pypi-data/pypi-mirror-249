import importlib
import os
import sys

from .my_ctl import *

# MODULE REGISTER
globals().update(importlib.import_module('my_ctl').__dict__)

# STATIC PATH
if sys.platform.startswith('linux'):
	os.environ['MY_CTL_STATIC'] = os.path.dirname(os.path.abspath(__file__))