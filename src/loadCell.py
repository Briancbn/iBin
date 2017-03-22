import RPi.GPIO as GPIO
from time import sleep


# Use the BCM GPIO numbers as the numbering scheme
GPIO.setmode(GPIO.BCM)


# Set pin 12 as the input pin for DOUT and pin 23 as the output pin for SCK
DOUT = 12
SCK = 23
GPIO.setup(DOUT, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(SCK, GPIO.OUT)


# Get Value from the digital input
def getValue():
    
    # Start recieve input when DOUT gives out a low signal
    while (GPIO.input(DOUT) == GPIO.HIGH):
        pass
    data = []

    # Get three sets of 8 bit data from Dout
    for i in range(3):
        value = '0b'
        for j in range(8):
            GPIO.output(SCK,GPIO.HIGH)
            value += str(int(GPIO.input(DOUT)))
            GPIO.output(SCK,GPIO.LOW)
        data.append(int(value,2))
        
    GPIO.output(SCK,GPIO.HIGH)
    GPIO.output(SCK,GPIO.LOW)

    # Modify data to human readable    
    data[0] ^= 0x80
    return (data[0] << 16 | data[1] << 8) | data[2]


# Get average value to avoid errors of the measurements
def averageValue():
    result = 0
    for i in range(32):
        result += getValue()
    return result * 1.0 / 32.0

GPIO.output(SCK,GPIO.HIGH)
sleep(0.0001)
GPIO.output(SCK,GPIO.LOW)


# Set scale to convert the unit to gram
scale = 338.0


# Zero the weight of the plate
offset = averageValue()


# Convert the average value that we get to output in the unit of gram 
def getGram():
    reading = int((offset - averageValue()) * 1.0 / scale)
    
    # In case negative 0 appears that will make the initial values look ugly
    if reading > 0:
       return reading
    else:
       return 0
