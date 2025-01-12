from . import avaspec
import hardware

import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt

import time

from PyQt6 import QtCore

class Avantes():

    def __init__(self, serial = None):

        if serial is None: # Use the first spectrometer connected
            try:
                avaspec.AVS_Init(0)
                devices = avaspec.AVS_GetList()
                serial = devices[0].SerialNumber.decode("UTF-8")
            except:
                raise NameError("No hardware devices found.")
            else:
                self.device_handle = avaspec.AVS_Activate(devices[0])
        else: # try to match the serial number and connect to that. 
            avaspec.AVS_Init(0)
            found = False
            for device in avaspec.AVS_GetList():
                if serial == device.SerialNumber.decode("UTF-8"):
                    self.device_handle = avaspec.AVS_Activate(device)
                    found = True
            if not found:
                raise NameError("No hardware devices found.")

        device_config = avaspec.AVS_GetParameter(self.device_handle, 63484)
        self.number_of_pixels = device_config.m_Detector_m_NrPixels
        self.wavelengths = avaspec.AVS_GetLambda(self.device_handle)[0:self.number_of_pixels]

        self.measurement_config = avaspec.MeasConfigType()
        self.measurement_config.m_StopPixel = self.number_of_pixels - 1
        self.measurement_config.m_IntegrationTime = float(30)
        self.measurement_config.m_NrAverages = int(1)

    def grab(self):

        avaspec.AVS_PrepareMeasure(self.device_handle, self.measurement_config)

        self.waiting_for_measurement = True
        avs_callback = avaspec.AVS_MeasureCallbackFunc(self.__measure_complete_callback)
        avaspec.AVS_MeasureCallback(self.device_handle, avs_callback, 1)
        while self.waiting_for_measurement:
            time.sleep(0.001)

        data = avaspec.AVS_GetScopeData(self.device_handle)
        
        return np.asarray(data[1][0:self.number_of_pixels])
    
    def __measure_complete_callback(self, pparam1, pparam2):
        param1 = pparam1[0] # dereference the pointers
        param2 = pparam2[0]
        self.waiting_for_measurement=False

    def __del__(self):
        avaspec.AVS_Deactivate(self.device_handle)
        avaspec.AVS_Done()

    @staticmethod
    def find_devices():
        avaspec.AVS_Init(0)
        found_device_list = list()
        for device in avaspec.AVS_GetList():
            found_device_list.append(hardware.FoundDevice(manufacturer = "Avantes", model = device.UserFriendlyName.decode("UTF-8"), serial = device.SerialNumber.decode("UTF-8")))
        
        return found_device_list
        
        