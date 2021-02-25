import cv2

img = cv2.imread("images/201904261057095210.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def mouse_click(event, x, y, flags, para):
    if event == cv2.EVENT_LBUTTONDOWN:  # 左边鼠标点击
        print("PIX:", x, y)
        print("BGR:", img[y, x])
        print("GRAY:", gray[y, x])
        print("HSV:", hsv[y, x])
        print("=" * 30)


if __name__ == "__main__":
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", mouse_click)
    while True:
        cv2.imshow("img", img)
        if cv2.waitKey() == ord("q"):
            break
    cv2.destroyAllWindows()
