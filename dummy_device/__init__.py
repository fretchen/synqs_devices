"""A dummy for just some device, which simply puts out some super simplistic values.

  Typical usage example:

  DummyDevice(name="dummy_device_0")
  dummy_device_0.update_value(9)
"""

import sys

if sys.version_info < (3, 6):
    raise RuntimeError("YunTemp strongly prefers Python 3.6+")
