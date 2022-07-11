import cv2
import  matplotlib.pyplot as plt

img = cv2.imread(r"C:\Users\lowel\Downloads\connect 4.jpg")
cropped = img[110:550,0:520]
plt.imshow(cropped)
plt.show()

