"""This is where BLACS really connects to the hardware.

Everything elso is just sending it here.
"""

import requests
from blacs.tab_base_classes import Worker


class DummyDeviceWorker(Worker):
    """The class behind the Output Worker. It inherits from Worker.


    Attributes:
        connection: Not sure here.
        shot_file: Not sure here.
    """

    shot_file = None
    timeout = 10

    def init(self):
        """Initialize the Worker.

        Initializes the IP socket and resets everything properly. Do NOT
        rename it to __init__ . There is something specific about Blacs that remains
        a bit mystical to me.
        """
        # Each shot, we will remember the shot file for the duration of that shot
        self.timeout = 10
        self.shot_file = None

    def __repr__(self):
        """Nice printing format for the YunTempWorker.

        Returns:
            ret_str: a string that is some key information about the worker.
        """
        ret_str = "<DummyDevice {}".format(self.target) + ">"
        return ret_str

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
        # pylint: disable=unused-argument, R0201
        #
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
        # pylint: disable= R0201
        # This is expected by BLACS to indicate success:
        return True

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

    def program_manual(self, front_panel_values):
        """Performans manual updates from BLACS front panel.

        Attributes:
            front_panel_values: Not where they come from.

        Returns:
            dict: Which are the values the Arduino gives us back after we programmed it.
        """
        # Update values from front panel

        return {}
