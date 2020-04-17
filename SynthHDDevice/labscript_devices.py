"""The module to access the SynthHD within the shots.

The SynthHD exposes the SynthHD by windfreak to labscript.
"""


import numpy as np
import h5py

from labscript import Device, set_passed_properties


class SynthHDDevice(Device):
    """A labscript device to send commands to SynthHD at the beginning and end of
    shots"""

    # This decorator declares that some keyword arguments should be saved to the
    # connection table, so that BLACS can read them:
    @set_passed_properties({"connection_table_properties": ["com_port", "baud_rate"]})
    def __init__(self, name, com_port="COM1", baud_rate=115200, **kwargs):
        """Initialize the device.

        TODO: somehow baud_rate is never used.
        """
        Device.__init__(self, name=name, parent_device=None, connection=None, **kwargs)
        self.start_commands = []
        # self.stop_commands = []
        # The existence of this attribute is how BLACS knows it needs to make a tab for
        # this device:
        self.BLACS_connection = com_port

    def add_start_command(self, command):
        """Add a serial command that should be send at the start of the experiment"""
        if not isinstance(command, bytes):
            raise TypeError("command must be a bytestring")
        self.start_commands.append(command)

    def generate_code(self, hdf5_file):
        # Convert the lists of commands into numpy arrays and save them to the shot file
        # as HDF5 datasets within our device's group:
        vlenbytes = h5py.special_dtype(vlen=bytes)
        start_commands = np.array(self.start_commands, dtype=vlenbytes)
        # stop_commands = np.array(self.stop_commands, dtype=vlenbytes)
        group = self.init_device_group(hdf5_file)
        if self.start_commands:
            group.create_dataset("START_COMMANDS", data=start_commands)
        # if self.stop_commands:
        # group.create_dataset('STOP_COMMANDS', data=stop_commands)
