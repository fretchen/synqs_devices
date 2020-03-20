#####################################################################
#                                                                   #
# /user_devices/YunTemp/labscript_devices.py               #
#                                                                   #
# Copyright 2019, Monash University and contributors                #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################

from labscript import Device, set_passed_properties


class YunTemp(Device):
    description = "Yun Temperature Control"

    # This decorator declares that some keyword arguments should be saved to the
    # connection table, so that BLACS can read them:
    @set_passed_properties({"connection_table_properties": ["com_port", "baud_rate"]})
    def __init__(self, name, com_port="COM1", baud_rate=115200, **kwargs):
        Device.__init__(self, name=name, parent_device=None, connection=None, **kwargs)
        self.start_commands = []
        self.stop_commands = []
        # The existence of this attribute is how BLACS knows it needs to make a tab for
        # this device:
        self.BLACS_connection = com_port
