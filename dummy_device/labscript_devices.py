"""The module to access the YunTemp within the shots.

The YunTemp exposes the properties of temperature control.
"""

from labscript import Device


class DummyDevice(Device):
    """ The device class which we interact with in our experiment files.

    Attributes:
        description: What the device is meant for.
    """

    description = "Dummy Device"

    def __init__(self, name, **kwargs):
        """ Initialize the device itself.

        Args:
            name:   Name presented in Blacs.
        """
        # pylint: disable=C0103
        Device.__init__(self, name=name, parent_device=None, connection=None, **kwargs)
        self.value = 0
        # needs to be defined to compile, perhaps a specific value is is required
        # for correct behaviour
        self.BLACS_connection = {}

    def update_value(self, val):
        """Allows us to update the value of the dummy device.

        Args:
            val: Some value we would like to set there.
        """
        self.value = val

    def generate_code(self, hdf5_file):
        """Packs the recorded temperature value into the hdf5 file (into device properties).

        Args:
            hdf5_file: used file format
        """
        Device.generate_code(self, hdf5_file)
        self.init_device_group(hdf5_file)
        self.set_property("Value", float(self.value), location="device_properties")
