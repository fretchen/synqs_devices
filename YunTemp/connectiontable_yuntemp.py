from labscript import *

from user_devices.CustomArduinoDevice.labscript_devices import CustomArduinoDevice
from labscript_devices.DummyPseudoclock.labscript_devices import DummyPseudoclock

DummyPseudoclock(name='clock_0')
CustomArduinoDevice('arduino_0', com_port="/dev/ttys004")

#if __name__ == '__main__':
start()
stop(1)
