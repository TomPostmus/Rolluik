from flask import Flask
from flask import request
from alarm_slot import AlarmSlot
from alarm_listener import AlarmListener
import datetime
import time

app = Flask(__name__) 						# initialize FLask
alarm_slot = AlarmSlot() 					# initialize our AlarmSlot object
alarm_listener = AlarmListener(alarm_slot) 	# initialize alarm listener


### Server REST routes ###

# Main path
@app.route("/") 
def index():
	return "Halloooo"

# Get or set alarm
@app.route("/alarm/<time>", methods=['GET', 'POST']) 
def alarm(time): 
	# Get request
	if request.method == 'GET': 
		alarm_time = alarm_slot.read_alarm_file() 				# get date time object from AlarmSlot
		return alarm_time.strftime("%H:%M:%S") + "\n"
	
	# Post request
	elif request.method == 'POST':
		if len(time) == 8: # parse given time
			hours = int(time[0:2])
			mins = int(time[3:5])
			secs = int(time[6:8])
			
			try:
				alarm_time = datetime.time(hours, mins, secs) 	# in datetime format
				alarm_slot.write_alarm_file(alarm_time) 		# update alarm slot
				return "Updated time\n"
			except: pass
		
		return "Bad request\n", 400 							# if it does not succeed, return bad request


app.run(host="0.0.0.0") # run server
