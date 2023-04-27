import time
import RPi.GPIO as GPIO

# Pin definitions (GPIO)
onoff_pin = 23
direction_pin = 24

# Use GPIO pin numbering
GPIO.setmode(GPIO.BCM)

# Set as output pins
GPIO.setup(onoff_pin, GPIO.OUT)
GPIO.setup(direction_pin, GPIO.OUT)

# Put onoff pin off by default (otherwise motor will run)
GPIO.output(onoff_pin, GPIO.LOW)

def go_up():
	GPIO.output(onoff_pin, GPIO.HIGH) # turn motor on
	GPIO.output(direction_pin, GPIO.HIGH) # direction up
	
	time.sleep(10) # wait 10 seconds for blinds to go up

	GPIO.output(onoff_pin, GPIO.LOW) # turn motor off

def go_down():
	GPIO.output(onoff_pin, GPIO.HIGH) # turn motor on
	GPIO.output(direction_pin, GPIO.LOW) # direction down

	time.sleep(10) # wait 10 seconds for blinds to go down

	GPIO.output(onoff_pin, GPIO.LOW)

def move_distance(distance):
	GPIO.output(onoff_pin, GPIO.HIGH) 				# turn motor on
	GPIO_direction_val = GPIO.LOW if distance < 0 else GPIO.HIGH
	GPIO.output(direction_pin, GPIO_direction_val) 	# set direction pin
	
	cm_to_seconds = 0.5								# factor for conversion from cm to seconds (constant motor speed is asssumed)
	
	time.sleep(abs(distance * cm_to_seconds))		# wait x seconds to turn motor off
	
	GPIO.output(onoff_pin, GPIO.LOW) # turn motor off
	
