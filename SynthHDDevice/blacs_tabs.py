"""The file that generates the GUI for the SynthHD.

As it has no GUI this is just the barebones connection.

"""

from blacs.device_base_class import DeviceTab


class SynthHDDeviceTab(DeviceTab):
    """The class behind the GUI. It inherits from DeviceTab.


    Attributes:
        settings: Not sure here.
        worker: Not sure here.
    """

    def initialise_workers(self):

        # Look up the COM port and baud rate in the connection table:
        connection_table = self.settings["connection_table"]
        device = connection_table.find_by_name(self.device_name)

        com_port = device.properties["com_port"]
        baud_rate = device.properties["baud_rate"]

        # Start a worker process with our worker class, and pass it the com port and
        # baud rate, which it will need:
        self.create_worker(
            "main_worker",
            "synqs_devices.SynthHDDevice.blacs_workers.SynthHDWorker",
            {"com_port": com_port, "baud_rate": baud_rate},
        )
        self.primary_worker = "main_worker"
