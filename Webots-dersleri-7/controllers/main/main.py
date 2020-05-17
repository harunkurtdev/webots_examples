"""main controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,InertialUnit
from controller import Motor,Gyro
from controller import Compass,GPS,Camera

import math
import numpy as np
import cv2
# create the Robot instance.

def CLAMP(n,minn,maxn):
    if n<minn:
        return minn
    elif n>maxn:
        return maxn
    else :
        return n


robot = Robot()
M_PI=np.pi
k_pitch_p=30.0
k_roll_p=50.0
k_vertical_p=3.0

k_vertical_thrust=68.5
k_vertical_offset=0.6
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

camera=robot.getCamera("camera")
Camera.enable(camera,timestep)
imu=InertialUnit("inertial unit")
imu.enable(timestep)
pusula=Compass("compass")
gyro=Gyro("gyro")
pusula.enable(timestep)
gyro.enable(timestep)
gps=GPS("gps")
gps.enable(timestep)

# motorların tagını getirir 
#motorları getirir
solMotorİleri=robot.getMotor("front left propeller")
sağMotorİleri=robot.getMotor("front right propeller")
sağMotorGeri=robot.getMotor("rear right propeller")
solMotorGeri=robot.getMotor("rear left propeller")

#motorları hareket etirir
solMotorİleri.setPosition(float("inf"))
solMotorGeri.setPosition(float("inf"))
sağMotorİleri.setPosition(float("inf"))
sağMotorGeri.setPosition(float("inf"))

#camera motorlarını çağıralım
camera_roll_motor=robot.getMotor("camera roll")
camera_pitch_motor=robot.getMotor("camera pitch")


solMotorİleri.setVelocity(1.0)
solMotorGeri.setVelocity(1.0)
sağMotorİleri.setVelocity(1.0)
sağMotorGeri.setVelocity(1.0)



while robot.step(timestep) != -1:
    if(robot.getTime()>1.0):
        break



# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != 1:
    
    roll=imu.getRollPitchYaw()[0]+M_PI/2.0
    pitch=imu.getRollPitchYaw()[1]
    rakim=gps.getValues()[1]
    roll_hiz=gyro.getValues()[0]
    pitch_hiz=gyro.getValues()[1]
    
    print("x ekseni : {0} - y ekseni : {1} ".format(roll,pitch))
    
    camera_roll_motor.setPosition(0.1*roll_hiz)
    camera_pitch_motor.setPosition(0.1*pitch_hiz)
    
    roll_dagitim=0.0
    pitch_dagitim=0.0
    yaw_dagitim=0.0
    target_rakim=1.0
    
    roll_giris=k_roll_p*CLAMP(roll,-1.0,1.0)+roll_hiz+roll_dagitim
    pitch_giris=k_pitch_p*CLAMP(pitch,-1.0,1.0)-pitch_hiz+pitch_dagitim
    yaw_giris=yaw_dagitim
    clamped_yukseklik=CLAMP(target_rakim-rakim-k_vertical_offset,-1.0,1.0)
    vertical_input=k_vertical_p*math.pow(clamped_yukseklik,3.0)
    
    solMotorileri_giris=k_vertical_thrust+vertical_input-roll_giris-pitch_giris+yaw_giris
    sagMotorileri_giris=k_vertical_thrust+vertical_input+roll_giris-pitch_giris-yaw_giris
    solMotorGeri_giris=k_vertical_thrust+vertical_input-roll_giris+pitch_giris-yaw_giris
    sagMotorGeri_giris=k_vertical_thrust+vertical_input+roll_giris+pitch_giris+yaw_giris
    
    solMotorİleri.setVelocity(solMotorileri_giris)
    solMotorGeri.setVelocity(-solMotorGeri_giris)
    sağMotorİleri.setVelocity(-sagMotorileri_giris)
    sağMotorGeri.setVelocity(sagMotorGeri_giris)
    
    Camera.getImage(camera)
    Camera.saveImage(camera,"color.png",1)
    #frameColor=cv2.imread("color.png")
    #cv2.imshow("Camera Bilgisi",frameColor)
    
    #cv2.waitKey(10)


# Enter here exit cleanup code.
