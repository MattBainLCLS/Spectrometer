import hardware

import numpy as np
import scipy.constants as const

import time

from PyQt6 import QtCore



class Dummy(QtCore.QObject):

    def __init__(self):
        self.connected = False

        time.sleep(0.5)

        self.motor_limits = (float(0), float(25))

        self.connected = True
        self.moving = False

        self.position = 0

    def isConnected(self):
        return self.connected
    
    def isEnabled(self):
        return self.device.IsEnabled
    
    def currentPosition(self):
        return self.position
    
    def goTo(self, position, boundsCheck=True):
        limits = self.getLimits()
        if position >= np.min(limits) and position <= np.max(limits):
            self.moving = True
            self.position = position
            time.sleep(0.25) # Takes a small amount of time for the device to register that it's moving
            self.moving = False
        else:
            raise ValueError("Position is outside stage hardware limits.")

    def isMotionDone(self):
        return not self.moving
    
    def waitForMotion(self, updateTime = 0.1):
        while self.moving == True:
            time.sleep(updateTime) # check at 10Hz

    def getLimits(self):
        return (self.motor_limits)


    def home(self):
        start_position = self.position
        limits = self.getLimits()
        self.position = np.min(limits)
        time.sleep(0.25)
        self.position = np.max(limits)
        time.sleep(0.25)

    def close(self):
        if self.isConnected():
            self.connected = False

    @staticmethod
    def find_devices():
        found_device_list = list()
        found_device_list.append(hardware.FoundDevice(manufacturer = "dummy", model = "motion stage", serial = "00001"))
        found_device_list.append(hardware.FoundDevice(manufacturer = "dummy", model = "motion stage", serial = "00002"))
        return found_device_list