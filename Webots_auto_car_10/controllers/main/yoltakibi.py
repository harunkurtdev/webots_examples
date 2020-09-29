import cv2
import numpy as np
import matplotlib.pyplot as plt

img=cv2.imread("camera.png")
cv2.imshow("Camera",img)

cv2.waitKey(0)
cv2.destroyAllWindows()
