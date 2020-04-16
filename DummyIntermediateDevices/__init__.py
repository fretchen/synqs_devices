"""A dummy for just some device, which simply puts out some super simplistic values.

  Typical usage example:

  DummyDevice(name="dummy_device_0")
"""

from __future__ import division, unicode_literals, print_function, absolute_import
from labscript_utils import PY2

if PY2:
    str = unicode
