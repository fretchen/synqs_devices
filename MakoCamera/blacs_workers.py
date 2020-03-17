#####################################################################
#                                                                   #
# /labscript_devices/MakoCamera/blacs_workers.py                   #
#                                                                   #
# Copyright 2019, Monash University and contributors                #
#                                                                   #
# This file is part of labscript_devices, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################

# Original imaqdx_camera server by dt, with modifications by rpanderson and cbillington.

#import numpy as np
from labscript_utils import dedent
#from time import sleep
from labscript_devices.IMAQdxCamera.blacs_workers import IMAQdxCameraWorker

# Don't import API yet so as not to throw an error, allow worker to run as a dummy
# device, or for subclasses to import this module to inherit classes without requiring API
Vimba = None
VimbaException = None

class Mako_Camera(object):
    def __init__(self, serial_number):
        global Vimba
        global VimbaException
        from pymba import Vimba, VimbaException
        
        self.data=[]
        self.frames=[]
        self.itr=0
        vimba = Vimba()
        vimba.startup()
        sn=str(serial_number)
        Camera_ID='50-0'+ sn
        #print(serial_number)
        #serial_number='DEV_000F315C1307'+str(serial_number)'DEV_000F315C57F9''50-0536923001'
        #pos
        self.camera = vimba.camera(Camera_ID)#vimba.camera_ids()[serial_number])#Device id.
        self.camera.open(camera_access_mode = 1)
        
    def set_attributes(self, attributes_dict):
        for prop, vals in attributes_dict.items():
            self.set_attribute(prop, vals)
    
    def set_attribute(self, name, value):
        """Set the value of the attribute of the given name to the given value"""
        try:
            setattr(self.camera, name, value)
        except:
            print('failed to set {name} to {value}')
        #feature = self.camera.feature(name)
        #feature.value = value
    
    def get_attributes(self, visibility_level, writeable_only=True):
        """Return a dict of all attributes of readable attributes, for the given
        visibility level. Optionally return only writeable attributes.
        """
        props = {}
        features=self.camera.feature_names()
        for feature in features:
            props[feature]=self.get_attribute(feature)
        
        del props['AcquisitionAbort'], props['AcquisitionStart'], props['AcquisitionStop'], props['GVSPAdjustPacketSize'], props['GevTimestampControlLatch'], props['GevTimestampControlReset'], props['LUTLoadAll'], props['LUTSaveAll'], props['TriggerSoftware'], props['UserSetLoad'], props['UserSetSave']
        return props

    def get_attribute(self, name):
        """Return current value of attribute of the given name"""
        value = getattr(self.camera, name)
        return value

    def snap(self):
        self.itr=0
        mako_attributes={'AcquisitionMode':'Continuous', 'ExposureMode':'Timed', 'ExposureTimeAbs':3000, 'TriggerActivation':'RisingEdge', 'TriggerMode':'Off',  'TriggerSelector':'FrameStart', 'TriggerSource':'Freerun'}
        self.set_attributes(mako_attributes)
        #self.set_attribute('ExposureTimeAbs',5000)
        self.frames=[self.camera.new_frame()]
        for self.frame in self.frames:
            self.frame.announce()
            self.camera.start_capture()
            self.frame.queue_for_capture()
            self.camera.AcquisitionStart()
            img=self.grab()
            self.camera.AcquisitionStop()
            self.camera.disarm()
        return img
        
    def configure_acquisition(self, continuous=True, bufferCount=7):
        mako_attributes={'AcquisitionMode':'Continuous', 'ExposureMode':'Timed', 'ExposureTimeAbs':3000, 'TriggerActivation':'RisingEdge', 'TriggerMode':'Off',  'TriggerSelector':'FrameStart', 'TriggerSource':'Freerun'}
        self.set_attributes(mako_attributes)
        if continuous:
            self.camera.AcquisitionMode='Continuous'
            one=True
            self.frames=[self.camera.new_frame() for _ in range(bufferCount)]#Make a frame buffer.
        
            for self.frame in self.frames:
                self.frame.announce()
                if one:
                    self.camera.start_capture()
                    one=False
                self.frame.queue_for_capture()
            
            self.camera.AcquisitionStart()
        
        else:
            self.camera.TriggerMode = 'On'
            self.camera.TriggerSource = 'Line1'
            self.camera.AcquisitionMode='MultiFrame'
            self.camera.ExposureMode = 'TriggerWidth'
            
                        
    def grab(self):
        """Grab and return single image during pre-configured acquisition."""
        self.frames[self.itr].wait_for_capture(1000)
        self.data=self.frames[self.itr].buffer_data_numpy()
        self.frames[self.itr].queue_for_capture()
        self.itr+=1
        if self.itr==len(self.frames):
            self.itr=0
        
        return self.data
        
    def grab_multiple(self, n_images,images):
        """Grab n_images into images array during buffered acquistion. Length of exposure is controlled by the hardware TTL trigger duration"""
        self.frames=[self.camera.new_frame() for _ in range(n_images)]#Make a frame buffer.
        for self.frame in self.frames:
            self.frame.announce()                    
        self.camera.start_capture()        
        for i in range(n_images):
            self.frames[i].queue_for_capture()
            self.camera.AcquisitionStart()
            self.frames[i].wait_for_capture(21000)#in ms
            images.append(self.frames[i].buffer_data_numpy())
            self.camera.AcquisitionStop()
   
    def stop_acquisition(self):
        self.camera.AcquisitionStop()
        self.camera.disarm()

    def abort_acquisition(self):
        self.camera.AcquisitionAbort()
        
    def close(self):
        self.camera.disarm()
        self.camera.close()
        

class MakoCameraWorker(IMAQdxCameraWorker):
    """Mako API Camera Worker. 
    
    Inherits from IMAQdxCameraWorker. Overloads get_attributes_as_dict 
    to use Mako_Camera.get_attributes() method."""
    interface_class = Mako_Camera

    def get_attributes_as_dict(self, visibility_level):
        """Return a dict of the attributes of the camera for the given visibility
        level"""
        return self.camera.get_attributes(visibility_level)


