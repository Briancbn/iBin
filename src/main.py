# The implementation of functions
# ussensor should return true when the reading < distance of bin, return false when distance>certain distance
# card_input and user_input should return an Id
# ValidId should check the database and return true or false if it exist,
# and if true get the value

from time import sleep
from Ultrasonic_Sensor import is_full as is_full
from ValidId import check_id as check_id
from ValidId import current_points as current_points
from loadCell import getGram

# program always runs
while True:

    identity = ''

    if is_full():
        pass
    # send message to operator

    else:
        if card_input() != None:
            identity = card_id()

        elif user_input() != None:
            identity = user_input()

        # check for userinput and set to identity

    if check_id(identity):

        # use dictionary and class for ValidId store and read from firebase
        tolerance = 1
    # set tolerance for checking
        wait_time = 5

        cp = current_points(identity)
        # get points from database
        gained_points = getGram()
        sleep(wait_time)

        while gained_points - tolerance < getGram() < gained_points + tolerance:
            gained_points = getGram()
            sleep(wait_time)

        newpoints = cp + gained_points

        # printout on kivy
        # send to firebase
        ?????
    
    identity=''
    #set identity back to None