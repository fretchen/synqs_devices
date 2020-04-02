"""The module to access the YunTemp within the shots.

The YunTemp exposes the properties of temperature control.
"""

from labscript import Device, set_passed_properties
import requests


class YunTemp(Device):
    """ The device class which we interact with in our experiment files.

    Attributes:
        description: What the device is meant for.
    """

    description = "Yun Temperature Control"

    # This decorator declares that some keyword arguments should be saved to the
    # connection table, so that BLACS can read them:
    @set_passed_properties(
        {"connection_table_properties": ["target", "usern", "passw"]}
    )
    def __init__(
        self, name, target="http://127.0.0.1:5001/", usern=None, passw=None, **kwargs
    ):
        """ Initialize the device itself.

        Args:
            name:   Name presented in Blacs.
            target: The ip adress of the arduino including the port he listens on.
            usern:  The username for accessing the webapi of the arduino
            passw:  The password associated.
        """
        Device.__init__(self, name=name, parent_device=None, connection=None, **kwargs)
        self.value = 0
        self.timeout = 1
        self.target = target
        # do we still need this part here ?
        try:
            proxies = {
                "http": None,
                "https": None,
            }
            r = requests.get(
                self.temp_http_str(),
                auth=(usern, passw),
                timeout=self.timeout,
                proxies=proxies,
            )
        except ConnectionError:
            print("No connection")
            return 0, 0
        html_text = r.text
        lines = html_text.split("<br />")
        ard_str = lines[1]
        vals = ard_str.split(",")
        self.value = vals[1]
        self.BLACS_connection = {"target": target, "usern": usern, "passw": passw}

    def temp_http_str(self):
        return self.target + "arduino/read/all/"

    def generate_code(self, hdf5_file):
        """Packs the recorded temperature value into the hdf5 file (into device properties).

        Args:
            hdf5_file: used file format
        """
        Device.generate_code(self, hdf5_file)
        group = self.init_device_group(hdf5_file)
        self.set_property(
            "Temperature", float(self.value), location="device_properties"
        )
