"""This is where BLACS really connects to the hardware.

Everything elso is just sending it here.
"""

from blacs.tab_base_classes import Worker
import requests

class YunTempWorker(Worker):
    """The class behind the Output Worker. It inherits from Worker.


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

        Returns:
            ret_str: a string that is some key information about the worker.
        """
        ret_str = "<YunTempWorker {}".format(self.target) + ">"
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

        We are not using it here right now.
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
                self.temp_http_str(),
                auth=(self.usern, self.passw),
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
        if len(vals) == 7:
            setpoint = vals[0]
            value = vals[1]
            error = vals[2]
            output = vals[3]
            gain = vals[4]
            integral = vals[5]
            sp_vals = vals[6].split("\r")
            diff = sp_vals[0]

        current_output_values = {
            "setpoint": float(setpoint),
            "P": float(gain),
            "I": float(integral),
        }
        return current_output_values

    def temp_http_str(self):
        """ Return the string representation for getting all vals.
        """
        return self.target + "arduino/read/all/"

    def set_setpoint(self):
        """Set the setpoint.

        Returns:
            success of the communication.
        """
        try:
            set_str = "/arduino/write/setpoint/" + str(self.setpoint) + "/"
            addr = self.target + set_str
            proxies = {
                "http": None,
                "https": None,
            }
            r = requests.get(addr, timeout=self.timeout, proxies=proxies)
            return r.ok
        except ConnectionError:
            return False

    def set_gain(self):
        """Set the proportional.

        Returns:
            success of the communication.
        """
        try:
            proxies = {
                "http": None,
                "https": None,
            }

            set_str = "/arduino/write/gain/" + str(self.gain) + "/"
            addr = self.target + set_str
            r = requests.get(addr, timeout=self.timeout, proxies=proxies)
            return r.ok
        except ConnectionError:
            return False

    def set_integral(self):
        """Set the integral.

        Returns:
            success of the communication.
        """
        try:
            proxies = {
                "http": None,
                "https": None,
            }
            set_str = "/arduino/write/integral/" + str(self.integral) + "/"
            addr = self.target + set_str
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
            addr = self.target + set_str
            r = requests.get(addr, timeout=self.timeout, proxies=proxies)
            return r.ok
        except ConnectionError:
            return False

    def program_manual(self, front_panel_values):
        """Performans manual updates from BLACS front panel.

        Attributes:
            front_panel_values: Not where they come from.

        Returns:
            dict: Which are the values the Arduino gives us back after we programmed it.
        """
        try:
            proxies = {
                "http": None,
                "https": None,
            }
            r = requests.get(
                self.temp_http_str(),
                auth=(self.usern, self.passw),
                timeout=self.timeout,
                proxies=proxies,
            )

        except ConnectionError:
            print("No connection")
            return 0, 0

        # Update values from front panel
        print(front_panel_values)
        self.setpoint = front_panel_values["setpoint"]
        self.gain = front_panel_values["P"]
        self.integral = front_panel_values["I"]
        # front_panel_values['value'] = self.value
        # Program Device to front panel values
        self.set_setpoint()
        self.set_gain()
        self.set_integral()

        return self.check_remote_values()


# class YunTempAcquisitionWorker(Worker):
#     """The class behind the Input Values. It inherits from Worker.
#
#     It is trying to set up everything to pull in values from the Arduino. However,
#     the documentation is sketchy at best.
#
#
#     Attributes:
#     """
#
#     MAX_READ_INTERVAL = 0.2
#     MAX_READ_PTS = 10000
#
#     def init(self):
#         """Initialize the Worker.
#
#         Initializes the IP socket and resets everything properly. Do NOT
#         rename it to __init__ . There is something specific about Blacs that remains
#         a bit mystical to me.
#         """
#         # Each shot, we will remember the shot file for the duration of that shot
#         self.timeout = 1
#         self.shot_file = None
#
#
#     def check_remote_values(self):
#         """Somehow needed, but not sure what it should do.
#
#         """
#         # Dummy
#         try:
#             proxies = {
#                 "http": None,
#                 "https": None,
#             }
#             r = requests.get(
#                 self.temp_http_str(), timeout=self.timeout, proxies=proxies
#             )
#         except ConnectionError:
#             print("No connection")
#             return 0, 0
#         html_text = r.text
#         lines = html_text.split("<br />")
#         ard_str = lines[1]
#
#         vals = ard_str.split(",")
#         if len(vals) == 7:
#             setpoint =  vals[0]
#             value    =  vals[1]
#             error    =  vals[2]
#             output   =  vals[3]
#             gain     =  vals[4]
#             integral =  vals[5]
#             sp_vals  =  vals[6].split("\r")
#             diff     =  sp_vals[0]
#
#         current_output_values = {
#             "setpoint": float(setpoint),
#             "P": float(gain),
#             "I": float(integral)
#         }
#         return current_output_values
#
#     def abort_buffered(self):
#         print('let me transition to buffered');
#         return self.transition_to_manual(True)
#
#     def abort_transition_to_buffered(self):
#         print('let me transition to buffered');
#         return self.transition_to_manual(True)
#
#     def program_manual(self, values):
#         return {}
#
#     def temp_http_str(self):
#         return self.target + "arduino/read/all/"
