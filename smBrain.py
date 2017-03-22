import math
import libdw.util as util
import libdw.sm as sm
import libdw.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    startState=[0,0,0]
    def getNextValues(self, state, inp):
        print inp.sonars[2],inp.sonars[4]
        
        #print inp.odometry.theta
        if state[0]==0:
            if inp.sonars[2]>0.5:
                state[0] = 0
                return (state, io.Action(fvel =  0.2 , rvel = 0))
            else:
                #print 'need to turn'
                state[0] = 1
                #turning = True
                return (state, io.Action(fvel =  0 , rvel =0.2))
        elif state[0]==1:
            print 'going to 1'
            #print theta0
            anglediff = inp.odometry.theta-state[1]
            if anglediff >= math.pi/2:
                print anglediff
                if inp.sonars[2]>=0.5:
                    print 'turning finish'
                    state[0] = 2
                    return (state, io.Action(fvel = 0.2, rvel = 0))
                else:
                    print 'inp2<0.5'
                    state[1] = inp.odometry.theta
                    return (state, io.Action(fvel = 0, rvel = 0.2))
            else:
                print 'right way'
                state[0] = 1
                return (state, io.Action(fvel =  0 , rvel =0.2))
        elif state[0]==2:
            state[2] = inp.sonars[5]
            print 'enter state 2'
            if inp.sonars[4]>0.5 and (inp.sonars[5] - state[2]) == 0.5:
                state[0] = 1
                state[1] = inp.odometry.theta
                return (state, io.Action(fvel = 0,rvel = 0.2))
            else:
                state[0] = 1
                return (state, io.Action(fvel = 0.2, rvel = 0))
                
                
             
            
            
mySM = MySMClass()            
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    # print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass



#import math
#import libdw.util as util
#import libdw.sm as sm
#import libdw.gfx as gfx
#from soar.io import io
#
#class MySMClass(sm.SM):
#    startState=0
#    def getNextValues(self, state, inp):
#        #print inp.sonars# list
#        print inp.odometry.theta
#        if inp.sonars[2]>0.5:
#            return (state, io.Action(fvel = 0.1, rvel = 0.05))
#        elif inp.sonars[2]<0.5:
#            return (state, io.Action(fvel = -0.1, rvel = 0.05))
#        else:
#            return (state,io.Action(fvel = 0,rvel = 0))
#
#mySM = MySMClass()
#mySM.name = 'brainSM'
#
#######################################################################
####
####          Brain methods
####
#######################################################################
#
#def plotSonar(sonarNum):
#    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
#                                        lambda: 
#                                        io.SensorInput().sonars[sonarNum]))
#
## this function is called when the brain is (re)loaded
#def setup():
#    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
#                                  sonarMonitor=False) # sonar monitor widget
#    
#    # set robot's behavior
#    robot.behavior = mySM
#
## this function is called when the start button is pushed
#def brainStart():
#    robot.behavior.start(traceTasks = robot.gfx.tasks())
#
## this function is called 10 times per second
#def step():
#    inp = io.SensorInput()
#    print inp.sonars[2]
#    robot.behavior.step(inp).execute()
#    io.done(robot.behavior.isDone())
#
## called when the stop button is pushed
#def brainStop():
#    pass
#
## called when brain or world is reloaded (before setup)
#def shutdown():
#    pass
