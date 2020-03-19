from blacs.device_base_class import DeviceTab

class YunTempTab(DeviceTab):
    def initialise_workers(self):

        # Look up the COM port and baud rate in the connection table:
        connection_table = self.settings['connection_table']
        device = connection_table.find_by_name(self.device_name)

        com_port = device.properties['com_port']
        baud_rate = device.properties['baud_rate']

        # Start a worker process with our worker class, and pass it the com port and
        # baud rate, which it will need:
        self.create_worker(
            'main_worker',
            'user_devices.YunTemp.blacs_workers.YunTempWorker',
            {'com_port': com_port, 'baud_rate': baud_rate},
        )
        self.primary_worker = 'main_worker'
