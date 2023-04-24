import datetime
import time

from flask import Flask
from flask import request

from alarm_slot import AlarmSlot
from alarm_listener import AlarmListener
import actuation

app = Flask(__name__) 						# initialize FLask
alarm_slot = AlarmSlot() 					# initialize our AlarmSlot object
alarm_listener = AlarmListener(alarm_slot) 	# initialize alarm listener


### Server REST routes ###

# Main path
@app.route("/") 
def index():
	alarm_time = alarm_slot.read_alarm_file() 				# get date time object from AlarmSlot
	return alarm_time.strftime("%H:%M:%S")

# Get or set alarm
@app.route("/alarm/<time>", methods=['POST']) 
def alarm(time):
	# Post request only
	if request.method == 'POST':
		if len(time) == 8: # parse given time
			hours = int(time[0:2])
			mins = int(time[3:5])
			secs = int(time[6:8])
			
			try:
				alarm_time = datetime.time(hours, mins, secs) 	# in datetime format
				alarm_slot.write_alarm_file(alarm_time) 		# update alarm slot
				return alarm_time.strftime("%H:%M:%S")
			except: pass
		
		return "Bad request\n", 400 							# if it does not succeed, return bad request

# Move blinds endpoint
@app.route("/move/<action>", methods=['POST'])
def move(action):
	# Post request only
	if request.method == 'POST':
		if action == "up":
			actuation.go_up()
			
		elif action == "down":
			actuation.go_down()
			
		else: # TODO: parse number for how many cm we want to move
			pass

app.run(host="192.168.2.165", port=5000) # run server 
