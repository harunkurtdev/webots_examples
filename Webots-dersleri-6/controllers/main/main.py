"""main controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Motor,DistanceSensor,Camera,RangeFinder
import cv2


hizi=6.28
maxMesafe=1024

#sensörün mesafede nasıl algı m
min_uzaklık=1.0

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

#Camera ve RangeFinder getirir
kinectColor=robot.getCamera("kinect color")
kinectRange=robot.getRangeFinder("kinect range")

#camera ve rangefinder başlatıldı
Camera.enable(kinectColor,timestep)
RangeFinder.enable(kinectRange,timestep)

# motorların tagını getirir 
#motorları getirir
solMotor=robot.getMotor("left wheel")
sağMotor=robot.getMotor("right wheel")

#motorları hareket etirir
solMotor.setPosition(float("inf"))
sağMotor.setPosition(float("inf"))

ps=[]
psNames=[
    "so0","so1","so2","so3",
    "so4","so5","so6","so7"
    ]

for i in range(8):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(timestep)

ball=0
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # mesafe sensörü çıkışları
    psDegerleri=[]
    for i in range(8):
        psDegerleri.append(ps[i].getValue())
        print(" mesafe değerlerimiz",ps[i].getValue())
    
    sag_engeller=psDegerleri[0]>70.0 or psDegerleri[1]>70.0 or psDegerleri[2]>70.0
    sol_engeller=psDegerleri[5]>70.0 or psDegerleri[6]>70.0 or psDegerleri[7]>70.0
    ileri_engeller=psDegerleri[3]>70.0 or psDegerleri[4]>50.0    
    #print("sağ engeller mesafe :", sag_engeller)
    #print("sol engeller mesafe :", sol_engeller)
    
    sol_hiz=0.5*hizi
    sag_hiz=0.5*hizi
    
    if ileri_engeller:
        sol_hiz-=0.5*hizi
        sag_hiz+=0.5*hizi
        #print("önümüzde bir engel var")
    elif sol_engeller:
        sol_hiz-=0.5*hizi
        sag_hiz+=0.5*hizi
        #print("sol bir engel var")
    elif sag_engeller:
        sol_hiz+=0.5*hizi
        sag_hiz-=0.5*hizi
        #print("sag bir engel var")
     
     # motoların hızını belirler
    # - koyarsak araç geri geri gelir
   
    solMotor.setVelocity(sol_hiz)
    sağMotor.setVelocity(sag_hiz)
    
    Camera.getImage(kinectColor)
    Camera.saveImage(kinectColor,"color.png",1)
    
    RangeFinder.getRangeImage(kinectRange)
    RangeFinder.saveImage(kinectRange,"range.png",1)
    
    frameColor=cv2.imread("color.png")
    
    cikti=frameColor.copy()
    gray=cv2.cvtColor(frameColor,cv2.COLOR_BGR2GRAY)
    
    gray_blur=cv2.blur(gray,(3,3))
    
    daireler=cv2.HoughCircles(gray_blur,cv2.HOUGH_GRADINET,1,20,param1=50,param2=30,minRadius=1,maxRadius=40)
    
    if daireler is not None:
        daireler=np.round(daireler[0,:]).astype("int")
     
         for (x,y,r) in daireler:
             cv2.circle(cikti,(x,y),r,(0,255,0),4)
             cv2.rectangle(cikti,(x-5,y-5),(x+5,y+5),(0,120,255),-1)
             
             ball=1
    
    if ball==1:
        print("Toplar bulundu")
        
    
    cv2.imshow("Color",frameColor)
    
    
    cv2.waitKey(10)    
# Enter here exit cleanup code.
