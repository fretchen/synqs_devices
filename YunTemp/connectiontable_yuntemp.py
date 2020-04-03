"""The sample file to be run in runmanager.

This is the minimal sample that you can load from runmanager to see if your code is working properly.
"""

from labscript import start, stop

from user_devices.YunTemp.labscript_devices import YunTemp

YunTemp(
    name="temp_control_0", target="http://129.206.182.60/", usern='root', passw=None
)

start()
stop(1)
