import cv2
import numpy as np

img = cv2.imread("images/201904261057095210.jpg")
img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
low = np.array([0, 0, 230])
high = np.array([170, 10, 238])

mask = cv2.inRange(img, low, high)
cv2.imshow("show", mask)
cv2.waitKey()
cv2.imwrite("images/test.jpg", mask)
