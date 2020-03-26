"""The file that generates the GUI for the YunTemp.

"""

from blacs.device_base_class import DeviceTab


class YunTempTab(DeviceTab):
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
        analog_props = {
            "setpoint": {
                "base_unit": "V",
                "min": 0.0,
                "max": 500.0,
                "step": 1.0,
                "decimals": 1,
            },
            "P": {
                "base_unit": "V",
                "min": 0.0,
                "max": 500.0,
                "step": 1.0,
                "decimals": 1,
            },
            "I": {
                "base_unit": "V",
                "min": 0.0,
                "max": 500.0,
                "step": 1.0,
                "decimals": 1,
            },
        }

        # Create the output objects
        self.create_analog_outputs(analog_props)

        # Create widgets for output objects
        dds_widgets, ao_widgets, do_widgets = self.auto_create_widgets()

        # and auto place the widgets in the UI
        self.auto_place_widgets(ao_widgets)

    def initialise_workers(self):
        """Connects the Tab to the worker.

        Reads out the ip adress of the Yun.
        Sets the Worker and initializes the properties of the GUI.
        """
        connection_object = self.settings["connection_table"].find_by_name(
            self.device_name
        )

        # Store the target port to be used
        blacs_connection = str(connection_object.BLACS_connection)

        self.target = blacs_connection

        # Create and set the primary worker
        self.create_worker(
            "main_worker",
            "user_devices.YunTemp.blacs_workers.YunTempWorker",
            {"target": self.target},
        )
        self.primary_worker = "main_worker"

        # Set the capabilities of this device
        self.supports_remote_value_check(True)
        self.supports_smart_programming(True)
