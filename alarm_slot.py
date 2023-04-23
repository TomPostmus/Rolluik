import datetime
import time

# This is a class that will keep the alarm time persistently (using a file)
class AlarmSlot:
	def __init__(self):
		try:
			self.alarm_file = open("alarm_value.txt", 'x') 	# try to exclusively open file to create it if doesn't exist
			self.alarm_file.close()
		except OSError: pass										# if file exists, FileExistsError is raised
		
		self.alarm_time = self.read_alarm_file() 	# get time object of alarm from file
		self.write_alarm_file(self.alarm_time) 		# write time object to file
	
	
	# Read the alarm file and return datetime object
	def read_alarm_file(self):
		self.alarm_file = open("alarm_value.txt", "r") # open file for read
		
		lines = self.alarm_file.readlines()
		try:
			time_string = lines[0] 		# read the alarm time from the first string
		except:
			time_string = ""			# if the file is empty, IndexError will be thrown
		
		self.alarm_file.close() 		# close file again
		
		if len(time_string) == 8: 		# if it is a valid time, parse it
			hours = int(time_string[0:2])
			mins = int(time_string[3:5])
			secs = int(time_string[6:8])
			return datetime.time(hours, mins, secs)
		else: 							# otherwise, create new time obj
			return datetime.time(9, 0, 0) # default time is 9 morning
			
			
	# Update alarm time object and write to alarm file
	def write_alarm_file(self, alarm_time):
		self.alarm_time = alarm_time # update alarm_time object
		
		self.alarm_file = open("alarm_value.txt", "w") 	# open file for write (automatically clears file)
		
		# Write in format HH:MM:SS
		hours = alarm_time.strftime("%H")
		mins = alarm_time.strftime("%M")
		secs = alarm_time.strftime("%S")
		time_string = hours + ":" + mins + ":" + secs
		self.alarm_file.write(time_string)
		
		self.alarm_file.close() # close file again
				
		
	# Check the current time (now), falls within the same minute as alarm_time
	def check_alarm(self):
		return datetime.datetime.now().minute == self.alarm_time.minute
		
			
