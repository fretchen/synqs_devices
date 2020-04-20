"""The sample file to be run in runmanager.

This is the minimal sample that you can load from runmanager to see if your
code is working properly.
"""

from labscript import start, stop, ClockLine

from labscript_devices.DummyPseudoclock.labscript_devices import DummyPseudoclock
from user_devices.dummy_device.labscript_devices import DummyDevice

# pylint: disable= E0602

# the clockline is always needed to have the experiment run in runmanager
DummyPseudoclock("dummy_pseudoclock")
ClockLine(
    name="dummy_clockline",
    pseudoclock=dummy_pseudoclock.pseudoclock,
    connection="flag 0",
)

# the device, which can only set some value and that's it.
DummyDevice(name="dummy_device_0")


dummy_device_0.update_value(9)

if __name__ == "__main__":
    start()
    stop(1)
