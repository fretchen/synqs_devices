"""The file that generates the GUI for the YunTemp.

"""

from blacs.device_base_class import DeviceTab


class YunTempTab(DeviceTab):
    """The class behind the GUI. It inherits from DeviceTab.


    Attributes:
        settings: Not sure here.
        worker: Not sure here.
    """

    def initialise_GUI(self):
        """Define the layout of the tab.

        Returns:
            Nothing really. Just sets things up.
        """
        # Capabilities
        self.base_units =    {'freq':'Hz',               'phase':'Degrees'}
        self.base_min =      {'freq':200e3,              'phase':0}
        self.base_max =      {'freq':402.653183*10.0**6, 'phase':360}
        self.base_step =     {'freq':10**6,              'phase':1}
        self.base_decimals = {'freq':0,                  'phase':3} # TODO: find out what the phase precision is!
        self.num_DDS = 1

        # # Create DDS Output objects
        # dds_prop = {'channel_1':
        #     { 'freq': {'base_unit':self.base_units['freq'],
        #             'min':self.base_min['freq'],
        #             'max':self.base_max['freq'],
        #             'step':self.base_step['freq'],
        #             'decimals':self.base_decimals['freq']
        #             },
        #     'phase': {'base_unit':self.base_units['phase'],
        #             'min':self.base_min['phase'],
        #             'max':self.base_max['phase'],
        #             'step':self.base_step['phase'],
        #             'decimals':self.base_decimals['phase']
        #             }
        #     }
        # };

        analog_props = { 'setpoint': {'base_unit': 'V',
                            'min':0.,
                            'max':500.,
                            'step':1.,
                            'decimals':1
                            },
                        'P': {'base_unit': 'V',
                                'min':0.,
                                'max':500.,
                                'step':1.,
                                'decimals':1
                            },
                        'I': {'base_unit': 'V',
                            'min':0.,
                            'max':500.,
                            'step':1.,
                            'decimals':1
                        },
                        };
        # for i in range(self.num_DDS): # only 1 DDS output
        #     dds_prop['channel %d' % i] = {}
        #     for subchnl in ['freq', 'phase']:
        #         dds_prop['channel %d' % i][subchnl] = {'base_unit':self.base_units[subchnl],
        #                                              'min':self.base_min[subchnl],
        #                                              'max':self.base_max[subchnl],
        #                                              'step':self.base_step[subchnl],
        #                                              'decimals':self.base_decimals[subchnl]
        #                                             }
        # Create the output objects
        #self.create_dds_outputs(dds_prop)
        self.create_analog_outputs(analog_props)
        # Create widgets for output objects
        dds_widgets,ao_widgets,do_widgets = self.auto_create_widgets()
        # and auto place the widgets in the UI
        self.auto_place_widgets(ao_widgets)

    def initialise_workers(self):
        """Connects the Tab to the worker.

        Not sure about the details to be honest.

        Args:
            self: Anything else?

        Returns:
            Nothing really. Just does the binding.
        """
        connection_object = self.settings['connection_table'].find_by_name(self.device_name)
        conn_properties = connection_object.properties

        # Store the COM port to be used
        blacs_connection =  str(connection_object.BLACS_connection)
        if ',' in blacs_connection:
            self.com_port, baud_rate = blacs_connection.split(',')
            self.baud_rate = int(baud_rate)
        else:
            self.com_port = blacs_connection
            self.baud_rate = 19200

        # Create and set the primary worker
        self.create_worker("main_worker","user_devices.YunTemp.blacs_workers.YunTempWorker",
                                {'com_port':self.com_port,
                                'baud_rate': self.baud_rate
                                })
        self.primary_worker = "main_worker"

        # Set the capabilities of this device
        self.supports_remote_value_check(True)
        self.supports_smart_programming(True)
