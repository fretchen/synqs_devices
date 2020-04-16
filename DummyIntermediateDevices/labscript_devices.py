"""The module to access the YunTemp within the shots.

The YunTemp exposes the properties of temperature control.
"""

from labscript import Device
from labscript_devices import (
    labscript_device,
    BLACS_tab,
    BLACS_worker,
    runviewer_parser,
)
from labscript import IntermediateDevice, DigitalOut, AnalogOut, config
import numpy as np
from labscript_devices.NI_DAQmx.utils import split_conn_DO, split_conn_AO
from labscript_utils import dedent


class DummyIntermediateDevice(IntermediateDevice):

    description = "Dummy IntermediateDevice"
    clock_limit = 1e6

    # If this is updated, then you need to update generate_code to support whatever types you add
    allowed_children = [DigitalOut, AnalogOut]

    def __init__(
        self, name, parent_device, BLACS_connection="dummy_connection", **kwargs
    ):
        self.BLACS_connection = BLACS_connection
        IntermediateDevice.__init__(self, name, parent_device, **kwargs)
        self.value = 0

    def update_value(self, val):
        """Allows us to update the value of the dummy device.

        Args:
            val: Some value we would like to set there.
        """
        self.value = val

    def add_device(self, device):
        """Error checking for adding a child device"""
        # Verify static/dynamic outputs compatible with configuration:
        # assert isinstance(device, AnalogOut) and isinstance(device, DigitalOut), "Device can only hande AnalogOut and DigitalOut"
        IntermediateDevice.add_device(self, device)

    def _make_analog_out_table(self, analogs, times):
        """Collect analog output data and create the output array"""
        if not analogs:
            return None
        n_timepoints = len(times)
        connections = sorted(analogs, key=split_conn_AO)
        dtypes = [(c, np.float32) for c in connections]
        analog_out_table = np.empty(n_timepoints, dtype=dtypes)
        for connection, output in analogs.items():
            analog_out_table[connection] = output.raw_output
        return analog_out_table

    def generate_code(self, hdf5_file):
        IntermediateDevice.generate_code(self, hdf5_file)
        group = self.init_device_group(hdf5_file)

        clockline = self.parent_device
        pseudoclock = clockline.parent_device
        times = pseudoclock.times[clockline]

        # out_table = np.empty((len(times),len(self.child_devices)), dtype=np.float32)
        # determine dtypes
        dtypes = []
        for device in self.child_devices:
            if isinstance(device, DigitalOut):
                device_dtype = np.int8
            elif isinstance(device, AnalogOut):
                device_dtype = np.float64
            dtypes.append((device.name, device_dtype))

        # create dataset
        analogs = {}
        out_table = np.zeros(len(times), dtype=dtypes)
        for device in self.child_devices:
            out_table[device.name][:] = device.raw_output
            if isinstance(device, AnalogOut):
                analogs[device.connection] = device

        times = clockline.parent_device.times[clockline]
        print(times)
        AO_table = self._make_analog_out_table(analogs, times)
        print(AO_table)
        # group.create_dataset('OUTPUTS', compression=config.compression, data=out_table)
        group.create_dataset("AO", data=AO_table, compression=config.compression)
