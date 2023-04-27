import datetime
import time
import os

from flask import Flask
from flask import request

from alarm_slot import AlarmSlot
from alarm_listener import AlarmListener
import actuation

# First check that we have internet connection
while (os.system("ping -c 1 google.com") != 0): # ping google until connection is found
	time.sleep(1)

app = Flask(__name__) 						# initialize FLask
alarm_slot = AlarmSlot() 					# initialize our AlarmSlot object
alarm_listener = AlarmListener(alarm_slot) 	# initialize alarm listener


### Server REST routes ###

# Main path
@app.route("/") 
def index():
	alarm_time = alarm_slot.read_alarm_time() 				# get date time object from AlarmSlot
	onoff = alarm_slot.read_onoff()
	return alarm_time + onoff

# Set alarm time
@app.route("/alarm/<time>", methods=['POST']) 
def alarm(time):
	try:
		alarm_slot.set_alarm_time(time) 					# update alarm slot
		return alarm_slot.read_alarm_time()
	except: pass											# on invalid values (out of range), pass
	
	return "Bad request\n", 400 							# if it does not succeed, return bad request

# Set onoff value
@app.route("/onoff/<value>", methods=['POST']) 
def onoff(value):
	try:
		alarm_slot.set_onoff(value) 						# update alarm slot
		if value:
			alarm_listener.start()							# activate timer listener
		return alarm_slot.read_onoff()
	except: pass											# on invalid values, pass
	
	return "Bad request\n", 400 							# if it does not succeed, return bad request


# Move blinds endpoint
@app.route("/move/<action>", methods=['POST'])
def move(action):
	if action == "up":
		actuation.go_up()
		return "Done"
		
	elif action == "down":
		actuation.go_down()
		return "Done"
		
	else:
		#try:
			distance = int(action)
			actuation.move_distance(distance)
			return "Done"
		#except ValueError: print("Value error")
		
	return "Bad request\n", 400 

app.run(host="0.0.0.0", port=5000) # run server 
