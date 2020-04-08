"""The file that generates the GUI for the YunTemp.

"""
import ast
from blacs.device_base_class import DeviceTab


class DummyDeviceTab(DeviceTab):
    """The class behind the GUI. It inherits from DeviceTab.


    Attributes:
        settings: Not sure here.
        worker: Not sure here.
    """

    def initialise_GUI(self):
        """Define the layout of the tab.

        Returns:
            Nothing really. Just sets things up.
        """
        pass

    def initialise_workers(self):
        """Connects the Tab to the worker.

        Reads out the ip adress of the Yun.
        Sets the Worker and initializes the properties of the GUI.
        """
        # Create and set the primary worker
        self.create_worker(
            "main_worker", "user_devices.dummy_device.blacs_workers.DummyDeviceWorker",
        )
        self.primary_worker = "main_worker"

        # Set the capabilities of this device
        self.supports_remote_value_check(False)
        self.supports_smart_programming(True)
