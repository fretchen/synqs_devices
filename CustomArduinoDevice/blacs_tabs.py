"""The file that generates the GUI for the CustomArduinoDevice.

We only have a blank GUI. So it really just binds to the worker here.
"""
from blacs.device_base_class import DeviceTab


class CustomArduinoDeviceTab(DeviceTab):
    """The class behind the GUI. It inherits from DeviceTab.


    Attributes:
        settings: Not sure here.
        worker: Not sure here.
    """

    def initialise_workers(self):
        """Connects the Tab to the worker.

        Not sure about the details to be honest.

        Args:
            self: Anything else?

        Returns:
            Nothing really. Just does the binding.
        """
        # Look up the COM port and baud rate in the connection table:
        connection_table = self.settings["connection_table"]
        device = connection_table.find_by_name(self.device_name)

        com_port = device.properties["com_port"]
        baud_rate = device.properties["baud_rate"]

        # Start a worker process with our worker class, and pass it the com port and
        # baud rate, which it will need:
        self.create_worker(
            "main_worker",
            "user_devices.CustomArduinoDevice.blacs_workers.CustomArduinoDeviceWorker",
            {"com_port": com_port, "baud_rate": baud_rate},
        )
        self.primary_worker = "main_worker"
