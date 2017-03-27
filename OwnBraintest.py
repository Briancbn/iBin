import math
import libdw.util as util
import libdw.sm as sm
import libdw.gfx as gfx
from soar.io import io
from time import sleep

class MySMClass(sm.SM):
    startState='Unbounded'
    #state 0,forward,1,reverse,3,stop
    def getNextValues(self, state, inp):
        print inp.sonars# list
        print inp.odometry.theta
#        return (state, io.Action(fvel = 0, rvel = 0.0))
        
        Bounded = self.state == 'Bounded'
        Unbounded = self.state == 'Unbounded'
        
        Iofoward=io.Action(fvel = 0.20, rvel = 0.00)
        IoVeerleft=io.Action(fvel = 0.10, rvel = 0.30)
        IoVeerright=io.Action(fvel = 0.10, rvel = -0.30)
        IoTurnleft=io.Action(fvel = 0.00, rvel = 0.5)
        
        distance=0.5
        inptoofar = inp.sonars[2] > distance
        inptoonear = inp.sonars[2] < distance
        
        distanceright=0.4
        tolerance=0.1
        inprighttoofar = inp.sonars[4] >= distanceright+tolerance
        inprighttopfar = inp.sonars[3] >= distanceright+tolerance
        inprighttoonear = inp.sonars[4] < distanceright-tolerance
        inprighttopnear =  inp.sonars[3] <= distanceright+tolerance


#        if state_moveforward  inptoofar and inprighttoofar:
#            nextState='forward'
#            output=Iofoward
#                                    
        if Unbounded:
            if inptoofar:
                nextState='Unbounded'
                output=Iofoward
            
            elif inptoonear:
                nextState='Bounded'
                output=IoVeerleft
        
        if Bounded:
            if inptoonear or inprighttopnear:
                nextState='Bounded'
                output=IoTurnleft
            
            elif inprighttoonear:
                nextState='Bounded'
                output=IoVeerleft
            
            elif inprighttoofar:
                nextState='Bounded'
                output=IoVeerright
            
            else:
                nextState='Bounded'
                output=Iofoward
        
        return nextState,output
        
        
            
        
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
#    print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
