from labscript import *

from user_devices.CustomArduinoDevice.labscript_devices import CustomArduinoDevice

CustomArduinoDevice("arduino_0", com_port="/dev/ttys004")

start()
stop(1)
