"""The sample file to be run in runmanager.

This is the minimal sample that you can load from runmanager to see if your code is working properly.
"""

from labscript import *

from user_devices.YunTemp.labscript_devices import YunTemp

YunTemp(name="temp_control_0", com_port="/dev/ttys004" )

start()
stop(1)
