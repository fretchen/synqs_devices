"""This is where BLACS really connects to the hardware.

Everything elso is just sending it here.
"""

import serial
import h5py

from blacs.tab_base_classes import Worker


class SynthHDWorker(Worker):
    """The class behind the Output Worker. It inherits from Worker.


    Attributes:
    """

    def __init__(self):
        """Initialize the Worker.

        Initializes the serial connections and resets everything properly. Should be
        called init instead of __init__. At least, this is how it is in all the other
        devices.
        """
        # Make a serial connection to the device. The com port and buad rate which
        # were passed to us from the BLACS tab are now available as instance attributes

        # every time the device is restarted in BLACS,we reset the arduino after opening the
        # serial port; this is a peculiar nature of our setup.
        # Note that this reset when called here, doesn't run in every shot.
        self.connection = serial.Serial(self.com_port, baudrate=self.baud_rate)

        # Could send and receive data here to confirm the device is working and do
        # any initial setup that is not related to any particular shot.

        # Each shot, we will remember the shot file for the duration of that shot
        self.shot_file = None

    # We don't use this method but it needs to be defined:
    def program_manual(self, front_panel_values):
        """Required - Performans manual updates from BLACS front panel.

        Attributes:
            front_panel_values: Not sure where they come from.

        Returns:
            dict: Which are the values the Arduino gives us back after we programmed it.
        """
        # pylint: disable= W0613, R0201
        return {}

    def transition_to_buffered(self, device_name, h5_file, initial_values, fresh):
        """Read commands from the shot file and send them to the device.

        This is when the hardware communication begins. It's important to reset the arduino here.

        Args:
            device_name: Not sure here.
            h5_file: Not sure here.
            initial_values: Not sure here.
            fresh: Not sure here.

        Returns:
            Empty dict.
        """
        # pylint: disable= W0613

        self.shot_file = h5_file
        with h5py.File(self.shot_file, "r") as file:
            group = file[f"devices/{self.device_name}"]
            if "START_COMMANDS" in group:
                start_commands = group["START_COMMANDS"][:]
            else:
                start_commands = None
        # It is polite to close the shot file (by exiting the 'with' block) before
        # communicating with the hardware, because other processes cannot open the file
        # whilst we still have it open
        print(self.connection.is_open)
        for command in start_commands:
            print(f"sending command: {repr(command)}")
            self.connection.write(command)
            # self.connection.flush()
            # this command is written in Experiment.py, which is fetched here and
            # actually written onto the arduino you will see this in the BLACS device
            # tab. It's nothing but the string that we should send to the arduino
            # inorder to control the DDS

        # This is expected by BLACS, we should return the final values that numerical
        # channels have from th shot - for us we have no channels so this is an empty
        # dictionary
        return {}

    def transition_to_manual(self):
        """
        # Read commands from the shot file and send them to the device
        with h5py.File(self.shot_file, 'r') as f:
            group = f[f'devices/{self.device_name}']
            if 'STOP_COMMANDS' in group:
                stop_commands = group['STOP_COMMANDS'][:]
            else:
                stop_commands = None
        for command in stop_commands:
            print(f"sending command: {repr(command)}")
            self.connection.write(command)
        """
        # Forget the shot file:
        self.shot_file = None
        # self.connection.close()
        # This is expected by BLACS to indicate success:
        return True

    def shutdown(self):
        """Called when BLACS closes.
        """
        self.connection.close()

    def abort_buffered(self):
        """ Called when a shot is aborted.

        We may or may not want to run transition_to_manual in this case. If not,
        then this method should do whatever else it needs to, and then return True.
        It should make sure to clear any state were storing about this shot
        (e.g. it should set self.shot_file = None)

        Returns:
            boolean: indicate that it was successful.
        """
        return self.transition_to_manual()

    def abort_transition_to_buffered(self):
        """ called if transition_to_buffered fails with an exception or returns False.
        """
        # Forget the shot file:
        self.shot_file = None
        return True  # Indicates success
