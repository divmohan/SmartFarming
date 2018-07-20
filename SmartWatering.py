#Import the necessary libraries
import RPi.GPIO as GPIO
import sys

import time
import subprocess
from datetime import datetime

GPIO.setmode(GPIO.BCM)
#Setup pin 18 as an output
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
#This function turns the valve on and off in 10 sec. intervals. 

def valveOff(Pin):
        GPIO.output(18, GPIO.HIGH)
        print("GPIO HIGH (on), valve should be off") 
    
def valveOn(Pin):    
        GPIO.output(18, GPIO.LOW)
        print("GPIO LOW (off), valve should be on")
        
def takeVideo():
        print("In takeVideo()")
	cmd = "raspivid -o WateringProof.h264 -t 10000"
	subprocess.call(cmd, shell=True)

def waterPlants():
        valveOn(18);
        time.sleep(5);
        #start camera and take video
        takeVideo()
        #time.sleep(10)
        valveOff(18);


#Check function to see if solenoid is off or on and alert if its not working well
#def checkAndNotify():


print("Arguments:",sys.argv[1]);

#Switch on the valve 20 seconds and then switch off
#Get time of day, if evening 5, water the plants
wateringTime= '22'

currentTime = datetime.now().strftime('%H')
print("Current time:",currentTime)

print("Water time:",wateringTime)

if (currentTime == wateringTime):
        if( 'BOC' == str(sys.argv[1]) ):
            print("Based on climate")

        elif('BOCS' == str(sys.argv[1])):
            print("Based on climate and sensor readings");

        else:
            print("Water the plants");
            waterPlants();
          
else:
   print("Its not yet time to water")
#GPIO.cleanup()
