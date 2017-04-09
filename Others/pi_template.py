from RPi import GPIO
from firebase import firebase

url = "https://kivy-aa39a.firebaseio.com/" # URL to Firebase database
token = "CEg81kbsyacNiXHTK1919veba3Ow4t258E5wekMm" # unique token used for authentication

firebase=firebase.FirebaseApplication(url,token)

GPIO.setmode(GPIO.BCM)
ledcolor={'yellow':23, 'red':24}

GPIO.setup(ledcolor.values(), GPIO.OUT)

def setLED(ledno, status):
    if status == 'on':
        GPIO.output(ledno, GPIO.HIGH) 
    else:
        GPIO.output(ledno, GPIO.LOW)
        
while True:
	# get firebase data and call setLED
    redstatus= firebase.get('/red')
    yellowstatus=firebase.get('/yellow')
    
    setLED(ledcolor['red'], redstatus)
    setLED(ledcolor['yellow'], yellowstatus)