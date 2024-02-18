#
# MDEF Measuring the World
# Team realG
#
# 18 Feb 2023
# Added comments for documentation and removed sensitive information
#
# Run this code to receive MQTT messages and save them to local files
#

import paho.mqtt.client as mqtt
import time
import calendar
from datetime import datetime

current_GMT = time.gmtime()

mqtt_broker = "" # put MQTT url
mqtt_user = "" # put user
mqtt_pass = "" # put password
broker_port = 1883 # replace port number

def on_connect(client, userdata, flags, rc):
   print(f"Connected With Result Code: {rc}")

def on_message(client, userdata, message): 
   print(f"Message Recieved: {message.payload.decode()}")
   time_stamp = calendar.timegm(current_GMT)
   now = datetime.now() # current date and time
   date_time = now.strftime("%m/%d/%Y, %H:%M:%S") # format the date time
   print("Current timestamp:", now)

   if(message.payload.decode() != "futurehacker"): # disregard "futurehacker" messages 
      # Opening files. We are writing to two files for redundancy.
      file1 = open('myfile.csv', 'a')
      file2 = open('myfile.txt', 'a')
      newdata = message.payload.decode() + "," + date_time + "\n"
 
      # Writing a string to file
      file1.write(newdata)
      file2.write(newdata)

      # Closing file
      file1.close()
      file2.close()


def on_log(client, obj, level, string):
    print (string)

def read_sensor():
	sensor_reading = "Hola hola caracola"
	return sensor_reading

client = mqtt.Client(clean_session = True)
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.username_pw_set(username = mqtt_user, password = mqtt_pass)
client.connect(mqtt_broker, broker_port)


# Subscribe to your topic here
client.subscribe("lab/mdef/realg", qos=1)


# Start looping (non-blocking)
client.loop_start()

while True:
	time.sleep(5)