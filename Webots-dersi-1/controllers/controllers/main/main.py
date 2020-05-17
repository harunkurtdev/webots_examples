"""main controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

hizi=6.28

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# motorların tagını getirir 
#motorları getirir
solMotorİleri=robot.getMotor("front left wheel")
sağMotorİleri=robot.getMotor("front right wheel")
sağMotorGeri=robot.getMotor("back right wheel")
solMotorGeri=robot.getMotor("back left wheel")

#motorları hareket etirir
solMotorİleri.setPosition(-float("inf"))
solMotorGeri.setPosition(-float("inf"))
sağMotorİleri.setPosition(-float("inf"))
sağMotorGeri.setPosition(-float("inf"))

# motoların hızını belirler
# - koyarsak araç geri geri gelir
solMotorİleri.setVelocity(-0.1*hizi)
solMotorGeri.setVelocity(-0.1*hizi)
sağMotorİleri.setVelocity(-0.1*hizi)
sağMotorGeri.setVelocity(-0.1*hizi)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
   
    pass
