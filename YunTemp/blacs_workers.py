"""
This is where BLACS really connects to the hardware. Everything elso is just sending it here.
"""

import serial
import time
import labscript_utils.h5_lock
import h5py
from blacs.tab_base_classes import Worker
import requests
import sys
from userlib.user_devices.YunTemp.helpers.yuntemp import *


class YunTempWorker(Worker):
    """The class behind the Worker. It inherits from Worker.


    Attributes:
        connection: Not sure here.
        shot_file: Not sure here.
    """

    def init(self):
        """Initialize the Worker.

        Initializes the IP socket and resets everything properly. Do NOT
        rename it to __init__ . There is something specific about Blacs that remains
        a bit mystical to me.
        """
        # Each shot, we will remember the shot file for the duration of that shot
        self.timeout = 1
        self.shot_file = None

    def __repr__(self):
        """Nice printing format for the YunTempWorker.
        """
        ret_str = "<YunTempWorker {}".format(self.target) + ">"
        return ret_str

    def reset_connection(self, ip):

        """ Reset connection.

        This function, when called resets the arduino. Please be aware that the serial port should be open before you call this function.
        It resets Arduino DUE, and clears everything in its input and reads fresh from the arduino. The arduino when ready for the string
        to be written for the ramps displays 'Arduino ready', which is displayed in the device in BLACS. If you don't see this, check your code.

        Args:
            ser: The serial connection to the Arduino.

        Returns:
            Nothing really.
        """
        # print(
        # self.connection.is_open
        # )  # check whether the port is open. Displays True in the BLACS device tab
        ser.setRTS(True)
        ser.setDTR(True)
        time.sleep(0.1)
        ser.setRTS(False)
        ser.setDTR(False)
        ser.reset_input_buffer()

        line = ser.readline()
        ard_str = line[0:-2]
        print(ard_str)

    # We don't use this method but it needs to be defined:
    def program_manual(self, values):
        """ Required - But a dummy we do not use.

        Not sure how to do this one properly.

        Args:
            values: Not sure here.

        Returns:
            Empty dict.
        """
        return {}

    def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
        """ Required - Read commands from the shot file and send them to the device.

        Not sure about the right description here.

        Args:
            device_name: Not sure here.
            h5_file: Not sure here.
            initial_values: Not sure here.
            fresh: Not sure here.

        Returns:
            Empty dict.
        """

        # This is expected by BLACS, we should return the final values that numerical
        # channels have from th shot - for us we have no channels so this is an empty
        # dictionary
        return {}

    def transition_to_manual(self):
        """ Required - Not sure what it does.

        Not sure about the right description here.

        Returns:
            Empty dict.
        """

        # This is expected by BLACS to indicate success:
        return True

    def shutdown(self):
        """ Called when BLACS closes.
        """

        # does this make any sense for us ???
        self.connection.close()

    def abort_buffered(self):
        """ Called when BLACS closes.

        Called when a shot is aborted. We may or may not want to run
        transition_to_manual in this case. If not, then this method should do whatever
        else it needs to, and then return True. It should make sure to clear any state
        were storing about this shot (e.g. it should set self.shot_file = None)
        """
        return self.transition_to_manual()

    def abort_transition_to_buffered(self):
        """ This is called if transition_to_buffered fails with an exception or returns False.

        Returns:
            True, which indicates success.
        """
        # Forget the shot file:
        self.shot_file = None
        return True  # Indicates success

    def check_remote_values(self):
        """ Called when remote values are checked.


        Returns:
            dictionary of remote values, keyed by hardware channel name.
        """
        # Dummy
        try:
            proxies = {
                "http": None,
                "https": None,
            }
            r = requests.get(
                self.temp_http_str(), timeout=self.timeout, proxies=proxies
            )
        except ConnectionError:
            print("No connection")
            return 0, 0
        html_text = r.text
        lines = html_text.split("<br />")
        ard_str = lines[1]

        vals = ard_str.split(",")
        if len(vals) == 7:
            setpoint = vals[0]
            value = vals[1]
            error = vals[2]
            output = vals[3]
            gain = vals[4]
            integral = vals[5]
            sp_vals = vals[6].split("\r")
            diff = sp_vals[0]
        print("I AM HERE!!!!!!!!!!!!")
        print(ard_str)
        print(value)
        current_output_values = {
            "setpoint": float(setpoint),
            "P": float(gain),
            "I": float(integral),
        }
        return current_output_values

    """ The following stuff come from the DeviceControlServer code and more precisely
    from the WebTempControl model. So no guarantee  that it works right now ...
    """

    def temp_http_str(self):
        return self.target + "arduino/read/all/"

    def temp_field_str(self):
        return "read_wtc" + str(self.id)

    def conn_str(self):
        return "conn_wtc" + str(self.id)

    def startstop_str(self):
        return "start" + str(self.id)

    def is_open(self):
        """ Test if the serial connection is open
        """

        try:
            proxies = {
                "http": None,
                "https": None,
            }
            r = requests.get(self.http_str(), timeout=self.timeout, proxies=proxies)
            return True
        except ConnectionError:
            return False

    def set_setpoint(self):
        """Outdated....
        """
        try:
            set_str = "/arduino/write/setpoint/" + str(self.setpoint) + "/"
            addr = self.http_str() + set_str
            proxies = {
                "http": None,
                "https": None,
            }
            r = requests.get(addr, timeout=self.timeout, proxies=proxies)
            return r.ok
        except ConnectionError:
            return False

    def set_gain(self):
        try:
            proxies = {
                "http": None,
                "https": None,
            }

            set_str = "/arduino/write/gain/" + str(self.gain) + "/"
            addr = self.http_str() + set_str
            r = requests.get(addr, timeout=self.timeout, proxies=proxies)
            return r.ok
        except ConnectionError:
            return False

    def set_integral(self):
        try:
            proxies = {
                "http": None,
                "https": None,
            }
            set_str = "/arduino/write/integral/" + str(self.integral) + "/"
            addr = self.http_str() + set_str
            r = requests.get(addr, timeout=self.timeout, proxies=proxies)
            return r.ok
        except ConnectionError:
            return False

    def set_differential(self):
        try:
            proxies = {
                "http": None,
                "https": None,
            }
            set_str = "/arduino/write/differential/" + str(self.diff) + "/"
            addr = self.http_str() + set_str
            r = requests.get(addr, timeout=self.timeout, proxies=proxies)
            return r.ok
        except ConnectionError:
            return False
