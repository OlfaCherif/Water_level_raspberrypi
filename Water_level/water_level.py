import RPi.GPIO as GPIO
import time,os

import datetime
import urllib2

TRIG = 6
ECHO = 5
LEDALARM = 23

GPIO.setmode(GPIO.BCM) 
#these parameters are related to the HC-SR04
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
GPIO.setup(LEDALARM,GPIO.OUT)
GPIO.output(LEDALARM, True)


def get_distance():
	dist_add = 0
	k=0
	for x in range(20):
		try:
			GPIO.output(TRIG, True)
			time.sleep(0.00001)
			GPIO.output(TRIG, False)

			while GPIO.input(ECHO)==0: 
				pulse_start = time.time() 
                #to read the last time the GPIO doesn't received the ultrasounds yet

			while GPIO.input(ECHO)==1:
				pulse_end = time.time() 
                #read the time when the echo of the sensor received ultrasounds

			pulse_duration = pulse_end - pulse_start
            # The total duration between the  sending and receiving 
			
			distance = pulse_duration * 17150 
            #this value depends on the velocity of sounds 

			distance = round(distance, 3) 
            #take three digits 
			
			if(distance > 125):
                # ignore erroneous readings (max distance cannot be more than 125)
				k=k+1
				continue
		
			dist_add = dist_add + distance
			#print "dist_add: ", dist_add
			time.sleep(.1) # 100ms interval between readings
		
		except Exception as e: 
		
			pass
	
	
	print ("x: ", x+1)
	print ("k: ", k)

	avg_dist=dist_add/(x+1-k)
	dist=round(avg_dist,3)
	return dist

def sendData_to_remoteServer(url,dist):
	url_full=url+str(dist)
	urllib.urlopen(url_full)
	
def low_level_warning(dist):
	level=114-dist
	if(level<40):
		print("level low : ", level)
		GPIO.output(LEDALARM, False)
	else:
		GPIO.output(LEDALARM, True)
		print("level ok")
		


distance=get_distance()
print("distance =",distance)
low_level_warning(distance)
