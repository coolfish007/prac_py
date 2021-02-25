import cv2
import numpy as np


def remove_watermark(image):
    hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low = np.array([0, 0, 237])
    high = np.array([180, 43, 250])
    mask = cv2.inRange(hue_image, low, high)

    kernel = np.ones((3, 3), np.uint8)
    dilate_img = cv2.dilate(mask, kernel, iterations=1)
    res = cv2.inpaint(image, dilate_img, 5, flags=cv2.INPAINT_TELEA)

    cv2.imshow("mask_img", mask)
    cv2.imshow("res", res)
    cv2.waitKey(0)


image = cv2.imread("images/201904261057095210.jpg")
remove_watermark(image)
