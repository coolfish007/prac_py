import cv2

img = cv2.imread("images/201904261057095210.jpg", cv2.IMREAD_GRAYSCALE)
img[img >= 205] = 255
cv2.imshow("show", img)
cv2.waitKey()
cv2.imwrite("images/ret.jpg", img)
