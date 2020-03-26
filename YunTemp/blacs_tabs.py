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
        # self.create_dds_outputs(dds_prop)
        self.create_analog_outputs(analog_props)

        # Create widgets for output objects
        dds_widgets, ao_widgets, do_widgets = self.auto_create_widgets()

        # and auto place the widgets in the UI
        self.auto_place_widgets(ao_widgets)

    def initialise_workers(self):
        """Connects the Tab to the worker.

        Not sure about the details to be honest.

        Args:
            self: Anything else?

        Returns:
            Nothing really. Just does the binding.
        """
        connection_object = self.settings["connection_table"].find_by_name(
            self.device_name
        )
        #conn_properties = connection_object.properties

        # Store the COM port to be used

        blacs_connection = str(connection_object.BLACS_connection);

        print(connection_object.BLACS_connection);
        print('I AM HERE!!!!!!!!!!!!');
        self.target = blacs_connection;
        #if "," in blacs_connection:
        #    self.target, port = blacs_connection.split(",")
        #    print(self.target)
        #    self.port = int(port)
        #else:
        #   self.target = blacs_connection
        #    self.port = 5001

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
