#Python wrapper

import os
import time
import clr
import numpy as np
from System import Decimal

import hardware

clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.DCServoCLI.dll")

from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.DCServoCLI import *
    
# def MotionStage(FoundDevice):
#     match FoundDevice.manufacturer:
#         case "Thorlabs":
#             return ThorlabsMotionStage(hardware.FoundDevice.serial)


# def find_Thorlabs_devices(found_device_list) -> list:
#     # Scan the usb ports for available devices connected but NOT open
#     DeviceManagerCLI.BuildDeviceList()
#     #queries the devices attached

#     number_of_devices = DeviceManagerCLI.GetDeviceListSize()
#     serial_numbers = list(DeviceManagerCLI.GetDeviceList())
#     type_numbers = list(DeviceManagerCLI.GetDeviceTypesList()) # Should be an enum to conver this to a model number but I can't figure it out right now

#     for i in range(0, number_of_devices):
#         found_device_list.append(hardware.FoundDevice(manufacturer = "Thorlabs", model = type_numbers[i], serial = serial_numbers[i]))
#     return found_device_list

class ThorlabsMotionStage():

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


        self.device.Connect(str(serial))

        time.sleep(0.25)

        self.device.StartPolling(250)
        
        time.sleep(0.25)

        if self.isConnected():
            self.device.EnableDevice()

        self.device.LoadMotorConfiguration(str(serial))

        AdvancedMotorLimits = self.device.get_AdvancedMotorLimits()

        self.motor_limits = (Decimal.ToDouble(AdvancedMotorLimits.LengthMinimum), Decimal.ToDouble(AdvancedMotorLimits.LengthMaximum))

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
        return not self.device.Status.IsInMotion
    
    def waitForMotion(self, updateTime = 0.1):
        while self.device.Status.IsInMotion == True:
            time.sleep(updateTime) # check at 10Hz

    def getLimits(self):
        return self.motor_limits


    def home(self):
        self.device.Home(0) # 0 says return the function immediately (gives us the option to choose waiting via waitForMotionDone or read current position during homing motion)
        time.sleep(0.25)

    def close(self):
        if self.isConnected():
            self.device.Disconnect()

    def __del__(self):
        pass

    def real_to_device(value):
        return

    @staticmethod
    def find_devices():

        found_device_list = list()
        # Scan the usb ports for available devices connected but NOT open
        DeviceManagerCLI.BuildDeviceList()
        #queries the devices attached

        number_of_devices = DeviceManagerCLI.GetDeviceListSize()
        serial_numbers = list(DeviceManagerCLI.GetDeviceList())
        type_numbers = list(DeviceManagerCLI.GetDeviceTypesList()) # Should be an enum to conver this to a model number but I can't figure it out right now

        for i in range(0, number_of_devices):
            found_device_list.append(hardware.FoundDevice(manufacturer = "Thorlabs", model = type_numbers[i], serial = serial_numbers[i]))
        return found_device_list
