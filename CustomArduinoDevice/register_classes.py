from labscript_devices import register_classes

register_classes(
    'CustomArduinoDevice',
    BLACS_tab='user_devices.CustomArduinoDevice.blacs_tabs.CustomArduinoDeviceTab',
    runviewer_parser=None,
)
