#####################################################################
#                                                                   #
# /DummyIntermediateDevice.py                                       #
#                                                                   #
# Copyright 2013, Monash University                                 #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################

from __future__ import division, unicode_literals, print_function, absolute_import
from labscript_utils import PY2
if PY2:
    str = unicode

# This file represents a dummy labscript device for purposes of testing BLACS
# and labscript. The device is a Intermediate Device, and can be attached to
# a pseudoclock in labscript in order to test the pseudoclock behaviour
# without needing a real Intermediate Device.
#
# You can attach an arbitrary number of outputs to this device, however we
# currently only support outputs of type AnalogOut and DigitalOut. I would be
# easy to extend this is anyone needed further functionality.


from user_devices import labscript_device, BLACS_tab, BLACS_worker, runviewer_parser
from labscript import IntermediateDevice, DigitalOut, AnalogOut, config
import numpy as np
from labscript_devices.NI_DAQmx.utils import split_conn_DO, split_conn_AO
from labscript_utils import dedent



class DummyIntermediateDevice(IntermediateDevice):

    description = 'Dummy IntermediateDevice'
    clock_limit = 1e6

    # If this is updated, then you need to update generate_code to support whatever types you add
    allowed_children = [DigitalOut, AnalogOut]

    def __init__(self, name, parent_device, BLACS_connection='dummy_connection', **kwargs):
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
        #assert isinstance(device, AnalogOut) and isinstance(device, DigitalOut), "Device can only hande AnalogOut and DigitalOut"
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
        #group.create_dataset('OUTPUTS', compression=config.compression, data=out_table)
        group.create_dataset('AO', data=AO_table, compression=config.compression)


from blacs.device_base_class import DeviceTab
from blacs.tab_base_classes import Worker

@BLACS_tab
class DummyIntermediateDeviceTab(DeviceTab):
    def initialise_GUI(self):
        self.create_worker("main_worker",DummyIntermediateDeviceWorker,{})
        self.primary_worker = "main_worker"

class DummyIntermediateDeviceWorker(Worker):
    def init(self):
        pass

    def program_manual(self, front_panel_values):
        return front_panel_values

    def transition_to_buffered(self, device_name, h5file, initial_values, fresh):
        return initial_values

    def transition_to_manual(self,abort = False):
        return True

    def abort_transition_to_buffered(self):
        return self.transition_to_manual(True)

    def abort_buffered(self):
        return self.transition_to_manual(True)

    def shutdown(self):
        pass

@runviewer_parser
class DummyIntermediateDeviceParser(object):
    def __init__(self, path, device):
        self.path = path
        self.name = device.name
        self.device = device

    def get_traces(self, add_trace, clock=None):
        with h5py.File(self.path, 'r') as f:

            group = f['devices/' + self.name]

            if 'AO' in group:
                AO_table = group['AO'][:]
            else:
                AO_table = None

            if 'DO' in f['devices/%s' % self.name]:
                DO_table = group['DO'][:]
            else:
                DO_table = None

            props = properties.get(f, self.name, 'connection_table_properties')

            version = props.get('__version__', None)
            if version is None:
                msg = """Shot was compiled with the old version of the NI_DAQmx device
                    class. The new runviewer parser is not backward compatible with old
                    shot files. Either downgrade labscript_devices to 2.2.0 or less, or
                    recompile the shot with labscript_devices 2.3.0 or greater."""
                raise VersionException(dedent(msg))

            ports = props['ports']
            static_AO = props['static_AO']
            static_DO = props['static_DO']

        times, clock_value = clock[0], clock[1]

        clock_indices = np.where((clock_value[1:] - clock_value[:-1]) == 1)[0] + 1
        # If initial clock value is 1, then this counts as a rising edge (clock should
        # be 0 before experiment) but this is not picked up by the above code. So we
        # insert it!
        if clock_value[0] == 1:
            clock_indices = np.insert(clock_indices, 0, 0)
        clock_ticks = times[clock_indices]

        traces = {}

        if DO_table is not None:
            ports_in_use = DO_table.dtype.names
            for port_str in ports_in_use:
                for line in range(ports[port_str]["num_lines"]):
                    # Extract each digital value from the packed bits:
                    line_vals = (((1 << line) & DO_table[port_str]) != 0).astype(float)
                    if static_DO:
                        line_vals = np.full(len(clock_ticks), line_vals[0])
                    traces['%s/line%d' % (port_str, line)] = (clock_ticks, line_vals)

        if AO_table is not None:
            for chan in AO_table.dtype.names:
                vals = AO_table[chan]
                if static_AO:
                    vals = np.full(len(clock_ticks), vals[0])
                traces[chan] = (clock_ticks, vals)

        triggers = {}
        for channel_name, channel in self.device.child_list.items():
            if channel.parent_port in traces:
                trace = traces[channel.parent_port]
                if channel.device_class == 'Trigger':
                    triggers[channel_name] = trace
                add_trace(channel_name, trace, self.name, channel.parent_port)

        return triggers
