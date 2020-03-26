"""The module to access the YunTemp within the shots.

The YunTemp exposes the properties of temperature control.
"""
from labscript import Device, set_passed_properties


class YunTemp(Device):
    description = "Yun Temperature Control"

    # This decorator declares that some keyword arguments should be saved to the
    # connection table, so that BLACS can read them:
    @set_passed_properties({"connection_table_properties": ["target"]})
    def __init__(self, name, target="localhost", port=5001, **kwargs):
        Device.__init__(self, name=name, parent_device=None, connection=None, **kwargs)
        self.start_commands = []
        self.stop_commands = []
        # The existence of this attribute is how BLACS knows it needs to make a tab for
        # this device:
        self.BLACS_connection = target
