### Need to convert to a function called 'ussensor' hi everyone
def is_full():
    
    import RPi.GPIO as GPIO                    #Import GPIO library
    import time                                #Import time library
    GPIO.setmode(GPIO.BOARD)                     #Set GPIO pin numbering 
    
    TRIG = 16                                  #Associate pin 23 to TRIG
    ECHO = 18                                  #Associate pin 24 to ECHO
    
    print "Distance measurement in progress"
    
    GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
    GPIO.setup(ECHO,GPIO.IN,GPIO.PUD_DOWN)     #Set pin as GPIO in
    
    binlength= 15                              #set bin length
    
    while True:
    
      GPIO.output(TRIG, False)                 #Set TRIG as LOW
      print "Waitng For Sensor To Settle"
      time.sleep(0.1)                            #Delay of 2 seconds
    
      GPIO.output(TRIG, True)                  #Set TRIG as HIGH
      time.sleep(0.00001)                      #Delay of 0.00001 seconds
      GPIO.output(TRIG, False)                 #Set TRIG as LOW
    
      while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
        pulse_start = time.time()              #Saves the last known time of LOW pulse
    
      while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
        pulse_end = time.time()                #Saves the last known time of HIGH pulse 
    
      pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable
    
      distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
      distance = round(distance, 2)            #Round to two decimal points
    
      if distance > 2 and distance < 400:      #Check whether the distance is within range
        print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
      else:
        print "Out Of Range"                   #display out of range

      if distance < binlength:
          return True
      else:
          return False
      
