"""The file that binds really to the Arno Tower.

This is where BLACS really connects to the hardware. Everything elso is just sending it here.
"""
import serial
import time
import labscript_utils.h5_lock
import h5py
from blacs.tab_base_classes import Worker


class CustomArduinoDeviceWorker(Worker):
    """The class behind the Worker. It inherits from Worker.


    Attributes:
        connection: Not sure here.
        shot_file: Not sure here.
    """

    def init(self):
        """Initialize the Worker.

        Initializes ther serial port and resets everything properly.
        """
        # Make a serial connection to the device. The com port and buad rate which
        # were passed to us from the BLACS tab are now available as instance attributes
        self.connection = serial.Serial(
            self.com_port, baudrate=self.baud_rate, timeout=0.1
        )
        ser = self.connection

        # every time the device is restarted in BLACS,we reset the arduino after opening the serial port; this is a peculiar nature of our setup.
        # Note that this reset when called here, doesn't run in every shot.
        self.reset_connection(ser)

        # Could send and receive data here to confirm the device is working and do
        # any initial setup that is not related to any particular shot.

        # Each shot, we will remember the shot file for the duration of that shot
        self.shot_file = None

    def reset_connection(self, ser):
        """ Reset connection.

        This function, when called resets the arduino. Please be aware that the serial port should be open before you call this function.
        It resets Arduino DUE, and clears everything in its input and reads fresh from the arduino. The arduino when ready for the string
        to be written for the ramps displays 'Arduino ready', which is displayed in the device in BLACS. If you don't see this, check your code.

        Args:
            ser: The serial connection to the Arduino.

        Returns:
            Nothing really.
        """
        print(
            self.connection.is_open
        )  # check whether the port is open. Displays True in the BLACS device tab
        ser.setRTS(True)
        ser.setDTR(True)
        time.sleep(0.1)
        ser.setRTS(False)
        ser.setDTR(False)
        ser.reset_input_buffer()

        line = ser.readline()
        ard_str = line[0:-2]
        print(ard_str)

    def check_remote_values(self):
        """Queries device for current output settings.

        Not sure about the details here.

        Returns:
            results as a dictionary to update the BLACS tab.
        """
        results = {}
        return results

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
        # This is called if transition_to_buffered fails with an exception or returns
        # False.
        # Forget the shot file:
        self.shot_file = None
        return True  # Indicates success
