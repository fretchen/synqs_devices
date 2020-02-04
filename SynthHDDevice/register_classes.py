from labscript_devices import register_classes

register_classes(
    'SynthHDDevice',
    BLACS_tab='synqs_devices.SynthHDDevice.blacs_tabs.SynthHDDeviceTab',
    runviewer_parser=None,
)
