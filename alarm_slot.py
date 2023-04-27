import datetime
import time

# This is a class that will keep the alarm time persistently (using a file)
class AlarmSlot:
	def __init__(self):
		try:
			alarm_file = open("alarm_value.txt", 'x') 	# try to exclusively open file to create it if doesn't exist
			alarm_file.close()
		except OSError: pass							# if file exists, FileExistsError is raised
		
		self.read_alarm_time() 							# read alarm time from file
		self.read_onoff()								# read onoff value from file
		
		self.write_file() 								# write time object to file, necessary in case default vals were returned
	
	
	# Get alarm time (internal and REST requests), returns string
	def read_alarm_time(self):
		alarm_file = open("alarm_value.txt", "r") # open file for read
		
		lines = alarm_file.readlines()		# read contents
		alarm_file.close() 				# close file again
		
		try:
			time_string = lines[0] 				# read the alarm time from the first string
		except IndexError:						# for empty file, IndexError is thrown, return default time
			time_string = "09:00:00"			# nine in the morning is default time
		
		self.alarm_time = self.parse_time_string(time_string)
		return time_string 						
	
	# Get onoff value (internal and REST requests), returns string
	def read_onoff(self):
		alarm_file = open("alarm_value.txt", "r") # open file for read
		
		lines = alarm_file.readlines()		# read contents
		alarm_file.close() 				# close file again
		
		try:
			onoff_string = lines[1] 			# read the second line
		except IndexError:						# for empty file, IndexError is thrown, return default
			onoff_string = "off" 				# return off by default
			
		self.onoff = self.parse_onoff_string(onoff_string)
		return onoff_string						
			
	# Set alarm time (from REST requests)
	def set_alarm_time(self, time_string):
		self.alarm_time = self.parse_time_string(time_string)
		self.write_file()
		
	# Set onoff value (from REST requests)
	def set_onoff(self, onoff_string):
		self.onoff = self.parse_onoff_string(onoff_string)
		self.write_file()
			
	# Write alarm time and onoff to file
	def write_file(self):		
		alarm_file = open("alarm_value.txt", "w") 	# open file for write (automatically clears file)
		
		time_string = self.alarm_time.strftime("%H:%M:%S")
		alarm_file.write(time_string + "\n")
		
		onoff_string = "on" if self.onoff else "off"
		alarm_file.write(onoff_string + "\n")
		
		alarm_file.close() 					# close file again
				
				
	def parse_time_string(self, time_string):
		if len(time_string) >= 8: 								# parse given time
			hours = int(time_string[0:2])
			mins = int(time_string[3:5])
			secs = int(time_string[6:8])
			return datetime.time(hours, mins, secs) 	# update alarm time object, throws ValueError if values are in wrong range	
		else: raise ValueError
		
	def parse_onoff_string(self, onoff_string):
		return "on" in onoff_string
		
	# Check the current time (now), falls within the same minute as alarm_time
	def check_alarm(self):
		now = datetime.datetime.now()
		equal_minute = now.minute == self.alarm_time.minute
		equal_hour = now.hour == self.alarm_time.hour
		return equal_minute and equal_hour
		
			
