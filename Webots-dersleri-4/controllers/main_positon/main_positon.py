"""main controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor,DistanceSensor,Lidar,Gyro,Compass,LidarPoint
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import time

file=open("Position.txt","w")
hizi=6.28
maxMesafe=1024

#sensörün mesafede nasıl algı m
min_uzaklık=1.0

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

lms291=robot.getLidar("Sick LMS 291")
print(lms291)
Lidar.enable(lms291,timestep)
Lidar.enablePointCloud(lms291)

lms291_yatayda=Lidar.getHorizontalResolution(lms291)
#print(lms291_yatayda)

#yatay=lms291_yatayda/2
#max_range=Lidar.getMaxRange(lms291)
#num_points=Lidar.getNumberOfPoints(lms291)

print("Lidar Başladı")

#araç üzeirnden gyro çekme
gyro=robot.getGyro("gyro")
Gyro.enable(gyro,timestep)

#araç üzerinden pususla çağırma
pusula=robot.getCompass("compass")
Compass.enable(pusula,timestep)

# motorların tagını getirir 
#motorları getirir
solMotorİleri=robot.getMotor("front left wheel")
sağMotorİleri=robot.getMotor("front right wheel")
sağMotorGeri=robot.getMotor("back right wheel")
solMotorGeri=robot.getMotor("back left wheel")

#motorları hareket etirir
solMotorİleri.setPosition(float("inf"))
solMotorGeri.setPosition(float("inf"))
sağMotorİleri.setPosition(float("inf"))
sağMotorGeri.setPosition(float("inf"))

sayici=0
eskiYacisi=0
aciStart=0
tetaDerece=0
teta=0
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
 
    sol_hiz=-0.5*hizi
    sag_hiz=0.5*hizi
     
     # motoların hızını belirler
    # - koyarsak araç geri geri gelir
    solMotorİleri.setVelocity(sol_hiz)
    solMotorGeri.setVelocity(sol_hiz)
    sağMotorİleri.setVelocity(sag_hiz)
    sağMotorGeri.setVelocity(sag_hiz)
    
    # X Y Z eksenşnde Lidar dan atışları getirir
    bulut=Lidar.getPointCloud(lms291)
    
    
    # Pusuladan gelen verilerimizi getirir
    dunya=Compass.getValues(pusula)
    
    angle=math.atan2(dunya[0],dunya[2])*180/math.pi
    
    #print(angle)
    
    if angle<0:
        angle=angle+360
    
    phi=(angle*math.pi)/180
    print(angle)
    
    a=[]
    b=[]
    c=[]
    
    for i in range(0,719):
        z=bulut[i].x
        x=bulut[i].y
        y=bulut[i].z
        
        x2=x**2
        y2=y**2
        z2=z**2
        
        r=math.sqrt(x2+y2+z2)
        
        x=r*math.cos(phi)
        y=r*math.sin(phi)
        #z=r*math.cos(teta)
        
        
        # x ekseninde dönüşler 
        #y=(y*math.cos(angle)) - (z*math.sin(angle))
        #z=(y*math.sin(angle)) - (z*math.sin(angle))
        
        a=np.append(a,x)
        b=np.append(b,y)
        c=np.append(c,z)
        
        #verileirmizi kayıt ettik
        file.write(" X :{0} Y :{1} Z:{2} \n".format(x,y,z))
        tetaDerece=tetaDerece+0.5
        teta=(tetaDerece*math.pi)/180
        
        if sayici==0:
            aciStart=int(angle)+1
            sayici+=1
        elif aciStart==int(angle):
            Lidar.disable(lms291)
            print("Lidar Durduruldu")
            
file.close()    
# Enter here exit cleanup code.
