# The implementation of functions
# ussensor should return true when the reading < distance of bin, return false when distance>certain distance
# card_input and user_input should return an Id
# ValidId should check the database and return true or false if it exist,
# and if true get the value
from time import sleep
from Ultrasonic_Sensor import is_full
from ValidId import return_points, add_points
from loadCell import getGram

import sys
sys.path.append('../MFRC522-python')
from Read import ReturnID


while True:

    while is_full():
        print "             Please clean the bin"
        sleep(2)
    # send message to operator

    
    identity = ReturnID()
    name = return_points(identity, 'name')
    points = return_points(identity, 'points')
    
    time = 0
    # use dictionary and class for ValidId store and read from firebase
    tolerance = 3
    # set tolerance for checking
    wait_time = 1
    
    startpoints = getGram()
    dpoints = 0
    print "Start throwing garbage"
    while(True):
        while startpoints - tolerance < getGram() < startpoints + tolerance:
            sleep(wait_time)
            time += 1
            print "timeleft: ", time
            if time >= 5:
                break
        newpoints = getGram()
        dpoints += newpoints - startpoints
        startpoints = newpoints
        print "      Addpoints: ", dpoints
        if time >= 5:
            break
        time = 0
        
    add_points(identity, dpoints)
    