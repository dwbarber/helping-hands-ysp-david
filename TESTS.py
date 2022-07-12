import cv2

cam = cv2.VideoCapture(1)

cv2.namedWindow("test")

while True:
    ret, frame = cam.read()
    k = cv2.waitKey(1)
    if k%256 == 32:
        # SPACE pressed
        img_name = "Current.png".format
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))


cam.release()
cv2.destroyAllWindows()
