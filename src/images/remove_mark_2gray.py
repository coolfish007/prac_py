import cv2
import numpy as np

img = cv2.imread("images/201904261057095210.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_gray[img_gray >= 205] = 255
cv2.imwrite("images/ret.jpg", img_gray)

B = img[:, :, 0]
G = img[:, :, 1]
R = img[:, :, 2]
# 灰度g=p*R+q*G+t*B（其中p=0.2989,q=0.5870,t=0.1140），于是B=(g-p*R-q*G)/t。于是我们只要保留R和G两个颜色分量，再加上灰度图g，就可以回复原来的RGB图像。
g = img_gray[:]
p = 0.11
q = 0.59
t = 0.3
B_new = (g - p * R - q * G) / t
B_new = np.uint8(B_new)
src_new = np.zeros((img.shape)).astype("uint8")
src_new[:, :, 0] = B_new
src_new[:, :, 1] = G
src_new[:, :, 2] = R

cv2.imshow("original", img)
cv2.imshow("gray", img_gray)
cv2.imshow("recover", src_new)
cv2.waitKey()
cv2.destroyAllWindows()
