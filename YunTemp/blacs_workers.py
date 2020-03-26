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
        self.shot_file = None

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
        #print(
            #self.connection.is_open
        #)  # check whether the port is open. Displays True in the BLACS device tab
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

        # this is when the hardware communication begins. It's important to reset the arduino here.
        self.reset_connection(self.connection)

        self.shot_file = h5_file
        with h5py.File(self.shot_file, "r") as f:
            group = f[f"devices/{self.device_name}"]
            if "START_COMMANDS" in group:
                start_commands = group["START_COMMANDS"][:]
            else:
                start_commands = None
        # It is polite to close the shot file (by exiting the 'with' block) before
        # communicating with the hardware, because other processes cannot open the file
        # whilst we still have it open
        for command in start_commands:
            print(f"sending command: {repr(command)}")

            self.connection.write(command)
            # self.connection.flush()
            # this command is written in Experiment.py, which is fetched here and actually written onto the arduino
            # you will see this in the BLACS device tab. It's nothing but the string that we should send to the arduino
            # inorder to control the DDS

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
        # Read commands from the shot file and send them to the device
        with h5py.File(self.shot_file, "r") as f:
            group = f[f"devices/{self.device_name}"]
            if "STOP_COMMANDS" in group:
                stop_commands = group["STOP_COMMANDS"][:]
            else:
                stop_commands = None
        for command in stop_commands:
            print(f"sending command: {repr(command)}")
            self.connection.write(command)

        # Forget the shot file:
        self.shot_file = None

        # This is expected by BLACS to indicate success:
        return True

    def shutdown(self):
        """ Called when BLACS closes.
        """
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
        call_string  = self.target + 'arduino/read/all/';
        r = requests.get(call_string);
        print(r.text)

        # now we need to parse the values from r.text  into the output_values.
        current_output_values = {"setpoint": 0.0, "P": 0.0, "I": 0.0}
        return current_output_values
