"""Register the YunTemp to blacs.

This is boilerplate and should be only minimally changed.
"""

from labscript_devices import register_classes

register_classes(
    "DummyIntermediateDevice",
    BLACS_tab="user_devices.DummyIntermediateDevices.blacs_tabs.DummyIntermediateDeviceTab",
    runviewer_parser="user_devices.DummyIntermediateDevices.runviewer_parsers.DummyIntermediateDeviceParser",
)
