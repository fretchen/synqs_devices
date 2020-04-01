"""The module to access the YunTemp within the shots.

The YunTemp exposes the properties of temperature control.
"""
import h5py
from labscript import Device, set_passed_properties
import requests
from userlib.user_devices.YunTemp.helpers.yuntemp import *


class YunTemp(Device):
    description = "Yun Temperature Control"

    # This decorator declares that some keyword arguments should be saved to the
    # connection table, so that BLACS can read them:
    @set_passed_properties({"connection_table_properties": ["target"]})
    def __init__(self, name, target="http://127.0.0.1:5001/", **kwargs):
        Device.__init__(self, name=name, parent_device=None, connection=None, **kwargs)
        self.value = 0
        self.timeout = 1
        self.target = target

        try:
            proxies = {
                "http": None,
                "https": None,
            }
            r = requests.get(
                self.temp_http_str(), auth = (usern, passw), timeout = self.timeout, proxies=proxies
            )
        except ConnectionError:
            print("No connection")
            return 0, 0
        html_text = r.text
        lines = html_text.split("<br />")
        ard_str = lines[1]
        vals = ard_str.split(",")
        self.value    =  vals[1]
        self.BLACS_connection = target

    def temp_http_str(self):
        return self.target + "arduino/read/all/"

    def generate_code(self, hdf5_file):
        """Packs the recorded temperature value into the hdf5 file (into device properties)

        Attributes:
            hdf5_file: used file format
        """
        Device.generate_code(self, hdf5_file)
        group = self.init_device_group(hdf5_file)
        self.set_property('Temperature', float(self.value), location='device_properties')
