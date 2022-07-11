import cv2
import numpy as np
import matplotlib.pyplot as plt

#create the cropped image based on downloaded image
img = cv2.imread(r"C:\Users\lowel\Downloads\connect 4.jpg")
cropped_board = img[110:550,0:520]
shape = cropped_board.shape



#find values that are necessary to access specific pixels
rows = 6
columns = 7

height = shape[0]//rows
width  = shape[1]//columns

y1 = (height // 2)
x1 = (width // 2)

#define an array that is the correct size with values that are all zeros
arr = np.zeros([6,7])

#upload values to the array
# **opencv Inteprets colors in BGR and Matplotlib is in RGB**
for i in range(rows):
    for j in range(columns):
        y = y1 + (height*i)
        x = x1 + (width*j)
        colors = cropped_board[y,x]

        if ((colors[2] < 255) & (colors[2] > 230)) & ((colors[1] < 230) & (colors[1] > 200)) & ((colors[0] < 20)) :
            arr[i][j] = 1

        elif ((colors[2] < 255) & (colors[2] > 230)) & ((colors[1] < 100) & (colors[1] > 40)) & ((colors[0] < 20)) :
            arr[i][j] = -1

        else:
            arr[i][j] = 0


print(arr)
#print(cropped_board[-10,-37])
#print(len(cropped_board))
#print(x1,y1,height,width)
cv2.imshow('cropped',cropped_board)
cv2.waitKey(0)
cv2.destroyAllWindows()

plt.imshow(cropped_board)
plt.show()
