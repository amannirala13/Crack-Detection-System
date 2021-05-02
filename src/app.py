# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 01:39:31 2021
@author: amannirala13
"""
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


		tk.Label(self.root, text="COM Port: ").grid(row=0, pady = 10)
		tk.Label(self.root, text="Baud Rate: ").grid(row=0, column=2, pady = 10)
		tk.Label(self.root, text="Depth Sensitivity(cm): ").grid(row=1, pady = 10)
		tk.Label(self.root, text="Max Distance Allowed(cm): ").grid(row=2, pady = 10)
		tk.Label(self.root, text="Calibration Time(s): ").grid(row=4, pady = 10)
		self.comPortTextField = tk.Entry(self.root, bg='#CFD8DC')
		self.baudrateTextField = tk.Entry(self.root, bg='#CFD8DC')
		self.depthTextField = tk.Entry(self.root, bg='#CFD8DC')
		self.maxDistanceField = tk.Entry(self.root, bg='#CFD8DC')
		self.calibrationTimeTextField = tk.Entry(self.root, bg='#CFD8DC')
		self.calibrateBtn = tk.Button(self.root, text="Calibrate",width = 25, bg='#FFEE58', height=2)
		self.startBtn = tk.Button(self.root, text="Start detection", width = 25, bg='#66BB6A', height=2)
		self.showGraphBtn = tk.Button(self.root, text="Show Graph", width = 25, bg='#29B6F6', height=2)
		self.saveComConfigBtn = tk.Button(self.root, text="Save COM Config", width = 25,bg='#9575CD' ,height = 2)
		
		self.comPortTextField.grid(row=0,column=1, pady = 10)
		self.baudrateTextField.grid(row=0, column=3, pady = 10, padx=10)
		self.depthTextField.grid(row=1, column=1, pady = 10)
		self.maxDistanceField.grid(row=2, column=1, pady = 10)
		self.calibrationTimeTextField.grid(row=4, column=1, pady = 10)
		self.calibrateBtn.grid(row=5)
		self.startBtn.grid(row=5, column=1)
		self.showGraphBtn.grid(row = 5, column=2, columnspan=2,ipadx=10)
		self.saveComConfigBtn.grid(row=3, column=2, columnspan=2, rowspan=2,ipadx=10)
		
		try:
			comConfigFile = open('com.config', 'r')
			config = comConfigFile.read().split(':')
			if(len(config) == 2):
					self.com = config[0]
					self.baudrate = int(config[1])
					self.comPortTextField.insert(0,self.com)
					self.serialPort = serial.Serial(port = self.com, baudrate=self.baudrate)
					self.baudrateTextField.insert(0,self.baudrate)
			else:
				self.com = None
				self.baudrate = 9600
				self.baudrateTextField.insert(0,self.baudrate)
				self.serialPort = serial.Serial()
			comConfigFile.close()
		except IOError as e:
			print(e)
			self.com = None
			self.baudrate = 9600
			self.baudrateTextField.insert(0,self.baudrate)
			self.serialPort = serial.Serial()
		
		self.calibrateBtn.config(command=lambda:threading.Thread(target=self.startCalibration, daemon=True).start())
		self.startBtn.config(command=lambda:threading.Thread(target=self.startDetection, daemon=True).start())
		#self.startBtn.config(command= self.startDetection)
		self.showGraphBtn.config(command=lambda:threading.Thread(target= lambda: os.system('python graph.py log.data '+str(self.mainCalibration.surface_threshold), ),daemon=True).start())
		self.saveComConfigBtn.config(command=lambda:threading.Thread(target=self.saveCOMConfig).start())
	
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
		self.baudrate = int(self.baudrateTextField.get())
		if self.serialPort.port == None:
			self.com = self.comPortTextField.get()
			self.serialPort = serial.Serial(port=self.com, baudrate=self.baudrate)
		else:
			self.serialPort.open()
			
	def stopSerialPortCom(self):
		print("STATUS: Stopping communication with serial port...")
		try:
			self.serialPort.close()
		except Exception as e:
			print("ERROR: Unable to close serial port | ",e)
			
	def saveCOMConfig(self):
		try:
			comConfigFile = open('com.config','w')
			com = self.comPortTextField.get()
			baudRate = self.baudrateTextField.get()
			
			if com == '' or baudRate == '':
				print("ERROR: Please enter valid com and baudrate values")
				comConfigFile.close()
				return
			comConfigFile.write(com + ':' + baudRate)
			comConfigFile.close()
		except Exception as e:
			print("ERROR: Unable to open com.config file | ",e)

	def startCalibration(self):
		try:
			if not self.serialPort.isOpen():
				self.startSerialPortCom()
		except Exception as e:
			print("ERROR: Unable to open serial port | ", e)
			return
		#TODO: Put this whole block in try and catch and make changes in status text
		self.calibrateBtn.config(text= "Calibrating...")
		self.calibrateBtn.config(state = 'disable')
		self.startBtn.config(state = 'disable')
		try:
			self.mainCalibration.max_distance = float(self.maxDistanceField.get())
			calibrationTime = float(self.calibrationTimeTextField.get())
		except Exception as e:
			print("Please enter valid number arguments | ", e)
			
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
			except Exception as e:
				print("WARNING: Skipped corrupted bytes! | ",e)
						
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
			self.startBtn.config(bg='#66BB6A', text='Start Detection')
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
			except Exception as e:
				print("ERROR: Unable to open serial port | ",e)
				return
			self.IS_DETECTION_ON = True
			self.startBtn.config(bg='#e57373', text='Stop Detection')
			try:
				dataLogFile = open('log.data', 'w')
				dataLogFile.write('0,')
				dataLogFile.close()
			except Exception as e:
				print("ERROR: Unable to create data log file. Graph features will not work properly | ",e)
			while(self.IS_DETECTION_ON):
				try:
					if(self.serialPort.in_waiting > 0):
						try:
							dataLogFile = open('log.data', 'a')
						except Exception as e:
							print("ERROR: Unable to create data log file. Graph features will not work | ",e)
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
	try:
		window.iconbitmap('ic.ico')
	except:
		print("WARNING: ic.ico file missing or not supported")
	window.title("Crack Detection(1.1)- amannirala13")
	App(root = window)
	window.mainloop()