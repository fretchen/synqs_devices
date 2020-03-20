Create a new device
===================

I will simply comment here on what I had to do to write an Arduino device for labscript

- Get blacs  and runmanager  installed. Not quite as trivial as it might sound…
- For running [blacs](https://github.com/labscript-suite/blacs) the first time there is a description called docs/UsingBlacs.pdf
- I will now follow the guide “How to add a new device” in the blacs folder
- However, it seems slightly out of date/incomplete. So will try to follow the recommendations of Philipp Starkeys thesis.
https://www.dropbox.com/s/mxoumrc2djibs3l/PhD_Starkey.pdf?dl=0


Devices can be found in labscript_devices. To make things work, we need to add four classes:

1. labscript API - it must be name the same way as the file it lives in. It is marked through the python decorator @labscript_device
2. BLACS GUI - can be named as one wishes and has the decorator  @BLACS_tab
3. BLACS worker process - can be named as one wishes and has the decorator  @BLACS_worker
4. runviewer - can be named as one wishes and has the decorator  @runviewer_parser
Creating a compilable boilerplate
- So let me start out with creating ArduinoUno.py in the folder labscript_devices.

- I then added the following header:

``` python
    from labscript import IntermediateDevice

    from blacs.device_base_class import DeviceTab
    from blacs.tab_base_classes import Worker

    from labscript_devices import BLACS_tab, BLACS_worker
```

- The first step is to actually define some dummy device now. We then will most likely not create a pseudoclock, which means that we will make the device an IntermediateDevice.

``` python
    class ArduinoUno(IntermediateDevice):
        # A human readable name for device model used in error messages
        description = 'Arduino Uno'

        # The maximum update rate of this device (in Hz)
        clock_limit = 100

        def __init__(self, name, parent_device, com_port = "", baud_rate= 115200):
            IntermediateDevice.__init__(self, name, parent_device)
            self.BLACS_connection = '%s,%s'%(com_port , str(baud_rate))

        def generate_code(self, hdf5_file):
            # Run the labscript suite base class method
            # (we assume inheritance from PseudoclockDevice here)
            # This generates instruction data for every child and
            # subsequent generation of children that is attached
            # to this device
            IntermediateDevice.generate_code(self, hdf5_file)

            # Create the HDF5 group for storage of
            # device attributes and instructions
            group = self.init_device_group(hdf5_file)

            # device specific code here ...
```
We then have to work on the specific control of the device, but this would seem like a minimal code.
The next step is to set up the GUI in BLACS through the DeviceTab class.

```python
    @BLACS_tab
    class ArduinoUnoTab(DeviceTab):
        def initialise_GUI(self):

            #  create the layout of the widgets
            dds_widgets,ao_widgets,do_widgets = self.auto_create_widgets()
            self.auto_place_widgets(dds_widgets,do_widgets)

            # Create and set the primary worker
            # the last ingredient are the parameters for the worker
            self.create_worker("main_worker",ArduinoUnoWorker,{})
            self.primary_worker = "main_worker"

            # Set the capabilities of this device
            self.supports_remote_value_check(False)
            self.supports_smart_programming(False)
```

Finally, we have to create a worker that will make the contact between the GUI and the Hardware itself.
```python
    class ArduinoUnoWorker(Worker):
        def init(self):
            # Once off device initialisation code called when the
            # worker process is first started.
            # Usually this is used to create the connection to the
            # device and/or instantiate the API from the device
            # manufacturer
            pass

        def shutdown(self):
            # Once off device shutdown code called when the
            # BLACS exits
            pass

        def program_manual(self, front_panel_values):
            # Update the output state of each channel using the values
            # in front_panel_values (which takes the form of a
            # dictionary keyed by the channel names specified
            # BLACS GUI configuration
            # return a dictionary of coerced/quantised values
            # channel, keyed by the channel name (or an empty dictionary)
            return {}
```
We have now setup the full the ArduinoUno.py file.

## Create the GUI

The next step is to bind it into the GUI. So we  create file, which we call connectiontable.py.
And we save it in the folder userlib/labscriptlib/my_pc/
It then contains:
```python
    from labscript import *

    from labscript_devices.ArduinoUno import ArduinoUno
    from labscript_devices.DummyPseudoclock.labscript_device import DummyPseudoclock

    DummyPseudoclock(name='clock_0')
    ArduinoUno(name='arduino_0', parent_device=clock_0.clockline)

    if __name__ == '__main__':
        start()
        stop(1)
```


- The next step is to run this script in [runmanager](https://github.com/labscript-suite/runmanager) as this creates the necessary h5 file for #blacs.
- So once we have run it in #runmanager it should have compiled without error you should find the file DATE_connectiontable_arduino_0.h5 .
-  This file has to be renamed connectiontable.h5 and moved into the position, which was specied in the the labconfig.
- You should now be able to start blacs through
    python -m blacs

without any errors. Only an empty useless widget should be present for the moment.

## Establishing a serial communication

In a next step we have to give the whole thing some live. Which means that we already have to establish a serial connection with the arduino

## Simulating a serial port

If you have an arduino around and know on which port it lives you can skip this step. Otherwise, we will explain here how you can simulate such a serial port. For that we simply create a file simSerialPort.py in the folder /userlib/pythonlib/ of your #labscript installation. The file reads then:

    import os, pty
    import time
    import numpy as np

    def test_serial():
        setpoint  = 750;
        master, slave = pty.openpty()
        s_name = os.ttyname(slave)
        print(s_name)
        while True:
            meas = np.random.randint(700, 800)
            err = setpoint - meas;
            control = np.random.randint(10)
            gain =1
            tauI = 100
            tauD = 1
            mode = os.read(master, 1);
            if mode:
                print('mode {}'.format(mode))
                if mode == b'w':
                    ard_str = str(setpoint) + ',' + str(meas) + ',' + str(err) + ',' + str(control)
                    ard_str = ard_str + ',' + str(gain) + ',' + str(tauI) +',' + str(tauD) + '\r\n'
                    out = ard_str.encode('windows-1252')
                    os.write(master, out)
                if mode == b's':
                    set = os.read(master, 20);
                    setpoint = int(set.decode('windows-1252'));
                    print('s{}'.format(setpoint));
            time.sleep(0.1)
    if __name__=='__main__':
        test_serial()

This program basically emulates the behavior of an arduino used for temperature control. We can start it in the shell through (being in the right directory):

    python simSerialPort.py

It will answer at the beginning with a single output, which will read something like this:

    /dev/ttys004

This is now the serial port on which #blacs can look for the Arduino.

## Setting up a basic user interface

We now have some serial device
