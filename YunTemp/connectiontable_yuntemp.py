
from labscript import *

from labscript_devices import CustomArduinoDevice
from labscript_devices.DummyPseudoclock.labscript_device import DummyPseudoclock

DummyPseudoclock(name='clock_0')
CustomArduinoDevice(name='arduino_0', parent_device=clock_0.clockline,
    com_port="/dev/ttys004")

if __name__ == '__main__':
    start()
    stop(1)