"""main controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from vehicle import Driver

Max_hizi=80.0
ileri_hizi=10.0
durma_hizi=0.0

sayici=0

# create the Robot instance.
#robot = Robot()
driver=Driver()

# get the time step of the current world.
#timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while driver.step() != -1:
    if sayici<1000:
        #driver.setCruisingSpeed(ileri_hizi)#aracın hızı
        #driver.setSteeringAngle(-0.7) #aracın direksiyon dönüşü
        #driver.setDippedBeams(True)
        
        
    
    sayici+=1
# Enter here exit cleanup code.
