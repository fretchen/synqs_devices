from labscript import *

# from user_devices.dummy_device.labscript_devices import DummyDevice
from labscript_devices.DummyPseudoclock.labscript_devices import DummyPseudoclock
from user_devices.DummyIntermediateDevices.labscript_devices import (
    DummyIntermediateDevice,
)

# from user_devices.DummyIntermediateDevice import DummyIntermediateDevice

DummyPseudoclock("dummy_pseudoclock")
ClockLine(
    name="dummy_clockline",
    pseudoclock=dummy_pseudoclock.pseudoclock,
    connection="flag 0",
)

# DummyDevice(name="dummy_device_0", parent_device=dummy_clockline)
DummyIntermediateDevice(name="dummy_intermediate_device", parent_device=dummy_clockline)
AnalogOut(name="AO1", parent_device=dummy_intermediate_device, connection="ao0")
AnalogOut(name="AO2", parent_device=dummy_intermediate_device, connection="ao1")
# DigitalOut(name="dummy_DO1", parent_device=dummy_intermediate_device, connection="dummy_connection")


start()
t = 0
t += 2
AO1.constant(t, value=2)
t += 1
# dummy_DO1.go_high(t)
# t+=1
# dummy_DO1.go_low(t)
# t+=1
AO2.constant(t, value=5)
stop(t + 2)
