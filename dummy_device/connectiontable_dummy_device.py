"""The sample file to be run in runmanager.

This is the minimal sample that you can load from runmanager to see if your
code is working properly.
"""

from labscript import *

from labscript_devices.DummyPseudoclock.labscript_devices import DummyPseudoclock
from user_devices.dummy_device.labscript_devices import DummyDevice
DummyPseudoclock("dummy_pseudoclock")
ClockLine(
    name="dummy_clockline",
    pseudoclock=dummy_pseudoclock.pseudoclock,
    connection="flag 0",
)

DummyDevice(name="dummy_device_0")
dummy_device_0.update_value(9)

if __name__ == "__main__":
    start()
    stop(1)
