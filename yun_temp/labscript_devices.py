"""The module to access the YunTemp within the shots.

The YunTemp exposes the properties of temperature control.
"""

import requests
from labscript import Device, set_passed_properties


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
        self, name, target="http://129.206.182.60/", usern="root", passw=None, **kwargs
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
        self.timeout = 10
        self.target = target
        # do we still need this part here ?
        addr = self.target + "arduino/read/all/"
        try:
            proxies = {
                "http": None,
                "https": None,
            }
            req = requests.get(
                addr, auth=(usern, passw), timeout=self.timeout, proxies=proxies,
            )
        except ConnectionError:
            print("No connection")
        html_text = req.text
        lines = html_text.split("<br />")
        ard_str = lines[1]
        vals = ard_str.split(",")
        self.value = vals[1]
        self.BLACS_connection = {"target": target, "usern": usern, "passw": passw}

    def generate_code(self, hdf5_file):
        """Packs the recorded temperature value into the hdf5 file (into device properties).

        Args:
            hdf5_file: used file format
        """
        Device.generate_code(self, hdf5_file)
        self.init_device_group(hdf5_file)
        self.set_property(
            "Temperature", float(self.value), location="device_properties"
        )
