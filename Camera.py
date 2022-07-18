import cv2

cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    print("Could not open video device")
for i in range(1):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    # cv2.imshow('preview',frame)

    # Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

name = 'frame.jpg'
print('Creating...' + name)
cv2.imwrite(name, frame)


# create the cropped image based on camera image
src = cv2.imread(r"frame.jpg")
window_name = 'Image'
img = cv2.rotate(src, cv2.ROTATE_180)
hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
# cropped_board = hsv_img[110:550, 0:520]
cropped_board = hsv_img[80:320, 80:400]

cv2.imshow('frame', img)
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()