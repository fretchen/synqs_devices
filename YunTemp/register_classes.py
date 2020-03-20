"""Register the YunTemp to blacs.

This is boilerplate and should be only minimally changed.
"""

from labscript_devices import register_classes

register_classes(
    "YunTemp",
    BLACS_tab="user_devices.YunTemp.blacs_tabs.YunTempTab",
    runviewer_parser=None,
)
