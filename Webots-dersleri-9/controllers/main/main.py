"""main controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from vehicle import Driver
from controller import Camera,Lidar
import matplotlib.pyplot as plt
import cv2
import numpy as np
import math

# create the Robot instance.
driver = Driver()

# get the time step of the current world.
timestep = int(driver.getBasicTimeStep())

Max_hizi=80

ileri_hizi=20
fren=0
sayici=0
plot=10

camera=driver.getCamera("camera")
Camera.enable(camera,timestep)

lms291=driver.getLidar("Sick LMS 291")
Lidar.enable(lms291,timestep)

lms291_yatay=Lidar.getHorizontalResolution(lms291)

fig=plt.figure(figsize=(3,3))


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while driver.step() != -1:
    if sayici<1000:
        driver.setCruisingSpeed(ileri_hizi)# aracın ileri doğru hızını
        #belirler
        driver.setSteeringAngle(0.6)#aracın + veya - durumuna
        #göre sağa veya sola döndürür
        driver.setDippedBeams(True)#ışığı yakma true false
        driver.setIndicator(2) # aracın sinyal lambalarının sağa döndüğü 1 ile
        #sola döndüğünü 2 ile kapalı tutmak için 0
    elif sayici>1000 and sayici<1100:
        driver.setCruisingSpeed(fren)#frenlerken
        driver.setBrakeIntensity(1.0) # % de kaç
        # frene basılsın ?
        driver.setDippedBeams(False)#ışığı kapatıyoruz
    elif sayici>1100 and sayici<1500:
        driver.setCruisingSpeed(-ileri_hizi)
        driver.setSteeringAngle(-0.6)
    elif sayici>1500 and sayici<1900:
        driver.setCruisingSpeed(fren)#frenlerken
        driver.setBrakeIntensity(1.0) # % de kaç
        # frene basılsın ?
        driver.setDippedBeams(False)#ışığı kapatıyoruz
    elif sayici>1900:
        sayici=0
    sayici+=1
    
    Camera.getImage(camera)
    Camera.saveImage(camera,"camera.png",1)
    frame=cv2.imread("camera.png")
    #cv2.imshow("Camera",frame)
    #cv2.waitKey(1)
    
    lms291_deger=[]
    lms291_deger=Lidar.getRangeImage(lms291)
    
    if plot==10:
        y=lms291_deger
        x=np.linspace(math.pi,0,np.size(y))
        plt.polar(x,y)
        plt.pause(0.00001)
        plt.clf()
        plot=0
    
    plot+=1

plt.show()
            
        
# Enter here exit cleanup code.
