import time
import threading
import actuation

class AlarmListener:
	
	def __init__(self, alarm_slot):
		self.alarm_slot = alarm_slot
		self.thread = threading.Thread(target=self.listen)
		self.thread.start()
		
	def listen(self):
		while True:
			time.sleep(0.1) 				# sleep 100 ms to achieve sample time
			if self.alarm_slot.check_alarm():
				print("Wake up time!")
				actuation.go_up() 			# pull up blinds!
				
				# Sleep until minute changes (in order to fire only once during alarm minute)
				while self.alarm_slot.check_alarm():
					time.sleep(1)
