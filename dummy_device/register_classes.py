"""Register the YunTemp to blacs.

This is boilerplate and should be only minimally changed.
"""

from labscript_devices import register_classes

register_classes(
    "DummyDevice",
    BLACS_tab="user_devices.dummy_device.blacs_tabs.DummyDeviceTab",
    runviewer_parser=None,
)
