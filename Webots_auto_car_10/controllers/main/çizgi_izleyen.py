import cv2
import numpy as np
import matplotlib.pyplot as plt


img= cv2.VideoCapture(0)
while True:
    ret, image = img.read()
    # BGR ' yi HSV ye çevirdik
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # HSV nin içindeki renk aralıgını belirledik
    #lower_blue = np.array([160,0,0])
    #upper_blue = np.array([180,255,255])
    boundaries=[([20,0,0],[30,255,255])]
    # Yukarıda belırledıgımız eşik değerlerini gray goruntunun içinde eşleştirdik.
    for (lower,upper) in boundaries:
        lower=np.array(lower,dtype="uint8")
        upper=np.array(upper,dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        # bitwise and operatörü ile de ana goruntude yukarıda buldugumuz mask'i aldık.
        res = cv2.bitwise_and(image,image, mask= mask)
        #ayarladıgımız 3 görüntüyü gösterdik
    res=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY) #maskelenen görüntüyü gray uzayına çeviriyoruz.
    blurred=cv2.GaussianBlur(res,(7,7),0) #Gürültüyü azaltmak için görüntüyü blurluyoruz
    ret,th1=cv2.threshold(res,40,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) #Gri tonlamalı görüntüden ikili görüntü oluşturduk.
    ret1,th2=cv2.threshold(th1,127,255,cv2.THRESH_TOZERO) 
    contours,hierarchy=cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Görüntüde kontuar oluşturduk

    
    if len(contours)>0:
        centroid=max(contours,key=cv2.contourArea) #Kontuar alanı belirleniyor.
        M=cv2.moments(centroid) 
        area=cv2.contourArea(centroid)
        if area>3000:
            cx=int(M['m10']/M['m00']) #x koordinatını ve y koordinatını buluyoruz.
            cy=int(M['m01']/M['m00'])

            cv2.line(image,(cx,0),(cx,720),(255,0,0),1) #bulunan bu koordinatlara göre görüntüde line çiziliyor.
            cv2.line(image,(0,cy),(1280,cy),(255,0,0),1)
            cv2.line(image,(320,0),(320,640),(255,0,0),1)
            cv2.circle(image,(cx,cy),3,(0,0,255),-1)
            cv2.drawContours(image,contours,-1,(0,255,0),2) #Kontuar alanı çiziliyor
            if cx<500:
                print("sag yap") #Referans değeri(x koordinatı) 500 den küçük ise sağa dön
            if cx>520:
                print("SOL YAP") #Referans değeri(y koordinatı) 520 den büyük ise sola dön
            if 500<cx<520:
                print("Duz gıt") #Referans değeri(x-y koordinatı) 500 ile 520 arasında ise düz git
    cv2.imshow('İşlenmiş Görüntü',image) #işleme yaptığımız görüntülerin framelerini yansıtıyoruz
    cv2.imshow('th1',th1)
    cv2.imshow('th2',th2)
    cv2.imshow("input", res)
    key = cv2.waitKey(10) #'ESC' ye basıldıysa bütün frameleri kapat
    if key == 27:
        break
cv2.destroyAllWindows() #Bütün ekranları öldür.
cv2.VideoCapture(0).release() # video yakalamyı kapat
