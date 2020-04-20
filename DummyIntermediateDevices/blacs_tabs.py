"""The file that generates the GUI for the YunTemp.

"""
from blacs.device_base_class import DeviceTab


class DummyIntermediateDeviceTab(DeviceTab):
    def initialise_GUI(self):
        self.create_worker(
            "main_worker",
            "user_devices.DummyIntermediateDevices.blacs_workers.DummyIntermediateDeviceWorker",
        )
        self.primary_worker = "main_worker"
