#Import the necessary libraries
import RPi.GPIO as GPIO

import threading
import telepot
import time

import sys
import subprocess
import os
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
        
def motorOn():
        print("Switch on the motor")
        os.system("python tplink_smartplug.py -t 192.168.31.60 -c 'on'")

def motorOff():
        print("Switch off the motor")
        os.system("python tplink_smartplug.py -t 192.168.31.60 -c 'off'")

def takeVideo(videoFile):
        print("Save the video",videoFile);
        #cmd = "raspivid -o WateringProof.h264 -t 10000"
        cmd = "raspivid -o " + videoFile + " -t 10000"
	subprocess.call(cmd, shell=True)

def sendVideo(videoFile):
        chatId='********'
        document = open(videoFile, 'rb')
        bot.sendDocument(chatId, document)
        document.close()
        #delete the video file
        os.remove(videoFile);


def waterPlants(  ):
    with lock:  
        print "Acquired lock:start watering at:" + datetime.now().strftime('%H:%M:%S') 
        #valveOn(18);
        motorOn();
        time.sleep(5);

        #start camera and take video
        fileTimestamp = datetime.now().strftime('%Y-%m-%d%H:%M:%S') 
        videoFile     = fileTimestamp + '.h264'
        takeVideo(videoFile)
	
        time.sleep(10)
        motorOff(); #Switch off after 25 seconds

        #send video to phone
        sendVideo(videoFile)

        print "Video sent at " + datetime.now().strftime('%H:%M:%S')  


class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      print "Starting " + self.name
      waterDaily(self.name)
      print "Exiting " + self.name

lock = threading.Lock()

def waterDaily(threadName):
   #Switch on the valve 20 seconds and then switch off
   #Get time of day, if evening 5, water the plants
   wateringTime= '10:00'   

   while True:
      currentTime = datetime.now().strftime('%H:%M')
      print("Current time:",currentTime)
      print("Water time:",wateringTime)
      if (currentTime == wateringTime):         
        waterPlants();
        time.sleep(86280);  #23 hrs 58 mins in seconds
                 			
      else:
   	  print("Its not yet time to water")
          time.sleep(10);

      


def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        words = command.split()
        str = ' '.join(words[1:999])

        if words[0] == 'Waterplants':
                print "Call function to water plants" 
                bot.sendMessage(chat_id, "Ack")
                waterPlants();
                
                # os.system("/home/pi/pi/dev/youtube-music/play-from-youtube.sh %s &" % str)
        else:
                bot.sendMessage(chat_id, "Invalid Message")


def periodicImageCapture():
     imageTimestamp = datetime.now().strftime('%Y-%m-%d%H:%M:%S') 
     imageFile      = 'images/'+ imageTimestamp + '.jpg'
     with lock:
         cmd = "raspistill -o " + imageFile 
         subprocess.call(cmd, shell=True)


# Create new threads
thread1 = myThread(1, "DailyThread")

# Start new Threads
thread1.start()


bot = telepot.Bot('*****')
bot.message_loop(handle)

while 1:
        periodicImageCapture()
        time.sleep(7200)  #every 2 hours


thread1.join()
print "Exiting Main Thread"
