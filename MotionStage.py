#Python wrapper

import os
import time
import clr
import numpy as np
from System import Decimal

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.DCServoCLI.dll")
#from DeviceManagerCLI import *
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.DCServoCLI import *

def get_device_list() -> list:
    # Scan the usb ports for available devices connected but NOT open
    DeviceManagerCLI.BuildDeviceList()
    #queries the devices attached
    return(list(DeviceManagerCLI.GetDeviceList()))

class KDC101():

    def __init__(self, serial=None):
        if serial is None:
            try:
                serial = list(get_device_list())[0]
            except:
                raise NameError("No hardware devices found")
            
        DeviceManagerCLI.BuildDeviceList()

        try:
            self.device = KCubeDCServo.CreateKCubeDCServo(str(serial))
        except:
            raise NameError("Device not found.")
        
        print("Is device connected? " + str(self.isConnected()))

        self.device.Connect(str(serial))

        time.sleep(0.25)

        self.device.StartPolling(250)
        
        time.sleep(0.25)

        if self.isConnected():
            self.device.EnableDevice()

        # Surely must be able to replace this with it detecting the attached stage and loading the 
        #m_config = self.device.LoadMotorConfiguration(str(serial), DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        self.device.LoadMotorConfiguration(str(serial))

        self.AdvancedMotorLimits = self.device.get_AdvancedMotorLimits()
        #m_config.DeviceSettingsName = "MTS25-Z8"

        # m_config.UpdateCurrentConfiguration()

        # self.device.SetSettings(self.device.MotorDeviceSettings, True, False)

    def isConnected(self):
        return self.device.IsConnected
    
    def isEnabled(self):
        return self.device.IsEnabled
    
    def currentPosition(self):
        return Decimal.ToDouble(self.device.Position)
    
    def goTo(self, position, boundsCheck=True):
        limits = self.getLimits()
        if position >= np.min(limits) and position <= np.max(limits):
            self.device.MoveTo(Decimal(position), 0)
            time.sleep(0.25) # Takes a small amount of time for the device to register that it's moving
        else:
            raise ValueError("Position is outside stage hardware limits.")

    def isMotionDone(self):
        return not self.device.IsInMotion
    
    def waitForMotion(self, updateTime = 0.1):
        while self.device.Status.IsInMotion == True:
            time.sleep(updateTime) # check at 10Hz

    def getLimits(self):
        return (Decimal.ToDouble(self.AdvancedMotorLimits.LengthMinimum), Decimal.ToDouble(self.AdvancedMotorLimits.LengthMaximum))


    def home(self):
        self.device.Home(0) # 0 says return the function immediately (gives us the option to choose waiting via waitForMotionDone or read current position during homing motion)

    def close(self):
        if self.isConnected():
            self.device.Disconnect()
            print("Disconnected")

    def __del__(self):
        pass

    def real_to_device(value):
        return
