# Library import block
import serial
import numpy as np
import os
try:
    import tkinter as tk
except:
    import Tkinter as tk
import time
import threading
from datetime import datetime, timedelta
#-------------------------------------------


class App(tk.Frame):
    
    def __init__(self,root, *args, **kwargs):
        tk.Frame.__init__(self,root, *args, **kwargs)
        self.root = root
        
        self.mainCalibration = self.Calibrate()
        self.IS_DETECTION_ON = False
        self.depthSensitivity = 0.0
        self.SMS_ONGOING = False
        self.smsEndTime = datetime.now()
        self.serialPort = serial.Serial(port="COM10", baudrate=9600)
        
        tk.Label(self.root, text="Depth Sensitivity(cm): ").grid(row=0)
        tk.Label(self.root, text="Max Distance Allowed(cm): ").grid(row=1)
        tk.Label(self.root, text="Calibration Time(s): ").grid(row=3)
        self.depthTextField = tk.Entry(self.root)
        self.maxDistanceField = tk.Entry(self.root)
        self.calibrationTimeTextField = tk.Entry(self.root)
        self.calibrateBtn = tk.Button(self.root, text="Calibrate",width = 25)
        self.startBtn = tk.Button(self.root, text="Start detection", width = 25)
        self.showGraphBtn = tk.Button(self.root, text="Show Graph", width = 25)
        
        self.depthTextField.grid(row=0, column=1)
        self.maxDistanceField.grid(row=1, column=1)
        self.calibrationTimeTextField.grid(row=3, column=1)
        self.calibrateBtn.grid(row=4)
        self.startBtn.grid(row=4, column=1)
        self.showGraphBtn.grid(row = 4, column=2)
        
        self.calibrateBtn.config(command=lambda:threading.Thread(target=self.startCalibration, daemon=True).start())
        self.startBtn.config(command=lambda:threading.Thread(target=self.startDetection, daemon=True).start())
        #self.startBtn.config(command= self.startDetection)
        self.showGraphBtn.config(command=lambda:threading.Thread(target= lambda: os.system('python graph.py '+str(self.mainCalibration.surface_threshold), ),daemon=True).start())
    
    class Calibrate():
        def __init__(self):
            self.surface_normal = 0.0
            self.max_error = 0.0
            self.min_error = 0.0
            self.mean_error = 0.0
            self.max_distance = 0.0
            self.surface_max_distance = 0.0
            self.surface_min_distance = 0.0
            self.surface_threshold = 0.0
            self.is_calibrated = False



    def startSerialPortCom(self):
        print("STATUS: Starting communication with serial port...")
        self.serialPort.open()
            
    def stopSerialPortCom(self):
        print("STATUS: Stopping communication with serial port...")
        try:
            self.serialPort.close()
        except Exception:
            print("ERROR: Unable to close serial port")
            
            

    def startCalibration(self):
        try:
            if not self.serialPort.isOpen():
                self.startSerialPortCom()
        except:
            print("ERROR: Unable to open serial port")
            return
        #TODO: Put this whole block in try and catch and make changes in status text
        self.calibrateBtn.config(text= "Calibrating...")
        self.calibrateBtn.config(state = 'disable')
        self.startBtn.config(state = 'disable')
        try:
            self.mainCalibration.max_distance = float(self.maxDistanceField.get())
            calibrationTime = float(self.calibrationTimeTextField.get())
        except:
            print("Please enter valid number arguments")
            
        endTime = datetime.now() + timedelta(seconds=calibrationTime)
        distanceList = []
        print("STATUS: Reading input....please wait...")
        self.serialPort.reset_input_buffer()
        while(datetime.now()<endTime):
            serialString = ''
            try:
                if(self.serialPort.in_waiting > 0):
                    serialString = self.serialPort.readline().strip()
                    distance = float(serialString.decode('Ascii'))
                    distanceList.append(distance)
            except:
                print("WARNING: Skipped corrupted bytes!")
                        
        data = np.array(distanceList)
        
        self.mainCalibration.surface_normal = np.mean(data)
        self.mainCalibration.surface_min_distance = np.min(data)
        self.mainCalibration.surface_max_distance = np.max(data)
        self.mainCalibration.max_error = self.mainCalibration.surface_max_distance - self.mainCalibration.surface_normal
        self.mainCalibration.min_error = self.mainCalibration.surface_min_distance - self.mainCalibration.surface_normal
        self.mainCalibration.mean_error = np.mean(data - self.mainCalibration.surface_normal)
        self.mainCalibration.is_calibrated = True
        
        print("Normal surface reading = ", self.mainCalibration.surface_normal)
        print("Minimum surface reading: ", self.mainCalibration.surface_min_distance)
        print("Maximum surface reading = ", self.mainCalibration.surface_max_distance)
        print("Maximum error = ", self.mainCalibration.max_error)
        print("Minimum error = ", self.mainCalibration.min_error)
        print("Mean error = ", self.mainCalibration.mean_error)
        
        if self.mainCalibration.max_distance < self.mainCalibration.surface_max_distance:
            self.mainCalibration.is_calibrated = False
            print("ERROR: Calibration failed due to noisy readings. Please calibrate again before using the application.")
            self.calibrateBtn.config(text = "Calibrate Now!")
            self.calibrateBtn.config(state = 'normal')
            self.startBtn.config(state = 'normal')
        else:
            self.calibrateBtn.config(text = "Calibrate")
            self.calibrateBtn.config(state = 'normal')
            self.startBtn.config(state = 'normal')
            self.mainCalibration.is_calibrated = True
            
        if self.serialPort.isOpen():
            self.stopSerialPortCom()               


        
    def startDetection(self):
        self.depthSensitivity = float(self.depthTextField.get())
        if self.IS_DETECTION_ON:
            self.IS_DETECTION_ON = False
        else:
            if not self.mainCalibration.is_calibrated:
                if self.serialPort.isOpen():
                    self.stopSerialPortCom()
                threading.Thread(target=self.startCalibration(), daemon=True).start()
            self.mainCalibration.surface_threshold = self.mainCalibration.surface_normal + self.mainCalibration.mean_error + self.depthSensitivity
            print("Surface threshold", self.mainCalibration.surface_threshold)
            print("Detecting surface...")
            try:
                if not self.serialPort.isOpen():
                    self.startSerialPortCom()
            except:
                print("ERROR: Unable to open serial port")
                return
            self.IS_DETECTION_ON = True
            try:
                dataLogFile = open('log.data', 'w')
                dataLogFile.write('0,')
                dataLogFile.close()
            except:
                print("ERROR: Unable to create data log file. Graph features will not work properly")
            while(self.IS_DETECTION_ON):
                try:
                    if(self.serialPort.in_waiting > 0):
                        try:
                            dataLogFile = open('log.data', 'a')
                        except:
                            print("ERROR: Unable to create data log file. Graph features will not work")
                        serialString = self.serialPort.readline()
                        distance = float(serialString.decode('Ascii').strip())
                        if distance<self.mainCalibration.max_distance:
                            dataLogFile.write(str(distance)+",")
                            if(distance > self.mainCalibration.surface_threshold):
                                print("Crack Detected: ", distance)
                                threading.Thread(target=self.sendSMS(distance)).start()
                        dataLogFile.close()
                except Exception:
                   print("WARNING: Skipped corrupted bytes!")
            self.IS_DETECTION_ON = False
        if self.serialPort.isOpen():
            self.stopSerialPortCom()  
    
    def sendSMS(self, distance):
        if not self.SMS_ONGOING:
            self.SMS_ONGOING = True
            print("INFO: Sending SMS")
            self.smsEndTime = datetime.now()+timedelta(seconds=30)
            os.system('python sms.py '+str(distance))
        elif datetime.now()>self.smsEndTime:    
            self.SMS_ONGOING = False
            self.sendSMS(distance)
        else:
            return
            
        
        
if __name__ == '__main__': 
    window = tk.Tk()
    window.title("Crack detection - v1.0")
    App(root = window)
    window.mainloop()