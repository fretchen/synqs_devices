"""The temperature control module based on the Arduino Yun.

  Typical usage example:

  YunTemp(name="temp_control_0")
"""

import sys

if sys.version_info < (3, 6):
    raise RuntimeError("YunTemp strongly prefers Python 3.6+")
