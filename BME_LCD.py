#!/usr/bin/python2
from Tkinter import *
import tkFont
import RPi.GPIO as GPIO
import os.path
import sys
import time
import numbers
import signal
from BME280 import *

LogDir = '/pub/tmp/'
LogFile = LogDir + 'BME280_Log.csv'
GPIO.setwarnings(False)

# Sensors 
try:
    sensorA = BME280(address=0x76)
    BME_A_Present = True
except IOError as e:
    print "I/O error({0}): {1} when initializing BME280 Sensor 0".format(e.errno, e.strerror)
    BME_A_Present = False
# Reads sensor data
BME_A_Temperature = sensorA.read_temperature()
BME_A_Pressure = sensorA.read_pressure()
BME_A_Humidity = sensorA.read_humidity()

# Check file presence, write header
if (os.path.isfile(LogFile) == False):
  with open(LogFile, 'a') as EnvLog:
    EnvLog.write("TimeStamp,Temperature,Pressure,Humidity\r\n")
    print ("File %s does not exist\r\n" % LogFile)
    EnvLog.close()
    

GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)

win = Tk()
myFont = tkFont.Font(family = 'Helvetica', size = 16, weight = 'bold')


# Main Tkinter application
class Application(Frame):

# Measure data from the sensor
    def measure(self):
        # Reads sensor data
        BME_A_Temperature = sensorA.read_temperature()
        BME_A_Pressure = sensorA.read_pressure()
        BME_A_Humidity = sensorA.read_humidity()
        
        print time.strftime("%d/%m/%Y\t%H:%M:%S") + ("\tTemp: %2.2f C\tPress: %6.0f Pa\tRh: %3.1f" % (float(BME_A_Temperature),float(BME_A_Pressure),float(BME_A_Humidity),) )
        with open(LogFile, 'a') as EnvLog:
                EnvLog.write (time.strftime("%d/%m/%Y-%H:%M:%S,") + ("%4.2f,%6.0f,%4.1f\r\n" % (float(BME_A_Temperature),float(BME_A_Pressure),float(BME_A_Humidity)) ))
                EnvLog.close()
        #Entry(main,  text = "%s" %(ans) ).grid(row=2, column=1)
        #time.sleep(10)

        self.temp_data.set("Temperature: %.3f" %(float(BME_A_Temperature)))
        self.temperature.pack()
        self.press_data.set("Pressure: %.0f" %(float(BME_A_Pressure)))
        self.pressure.pack()
        self.hum_data.set("Humidity: %.2f" %(float(BME_A_Humidity)))
        self.humidity.pack()

        # Wait 1 second between each measurement
        self.after(1000,self.measure)

# Create display elements

    def createWidgets(self):

                self.temperature = Label(self, textvariable=self.temp_data, font=('Verdana', 28,'bold'))
                self.temp_data.set("Temperature")
                self.temperature.pack()

                self.pressure = Label(self, textvariable=self.press_data, font=('Verdana', 28,'bold'))
                self.press_data.set("Pressure")
                self.pressure.pack()
                
                self.humidity = Label(self, textvariable=self.hum_data, font=('Verdana', 28, 'bold'))
                self.hum_data.set("Humidity")
                self.humidity.pack()

# Init the variables & start measurements
    def __init__(self, master=None):
                Frame.__init__(self, master)
                self.temp_data = StringVar()
                self.press_data = StringVar()
                self.hum_data = StringVar()
                self.createWidgets()
                self.pack()
                self.measure()

def ledON():
        print("Button pressed")
        if GPIO.input(40) :
                GPIO.output(40,GPIO.LOW)
                ledButton["text"] = "ON"
        else:
                GPIO.output(40,GPIO.HIGH)
                ledButton["text"] = "OFF"

def exitProgram():
        print("Exit Button pressed")
        GPIO.cleanup()
        win.quit()
        win.destroy() 


win.title("GUI Interface")
win.geometry('480x320')
win.attributes('-fullscreen', True)

exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height = 2 , width = 6) 
exitButton.pack(side = BOTTOM)

ledButton = Button(win, text = "OFF", font = myFont, command = ledON, height = 2, width = 6)
ledButton.pack()



# Create and run the GUI


app = Application(master=win)
app.mainloop()
