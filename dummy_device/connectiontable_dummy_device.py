"""The sample file to be run in runmanager.

This is the minimal sample that you can load from runmanager to see if your
code is working properly.
"""

from labscript import start, stop

from user_devices.dummy_device.labscript_devices import DummyDevice

DummyDevice(name="dummy_device_0")

start()
stop(1)
