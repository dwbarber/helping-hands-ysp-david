import cv2
import pickle


cap = cv2.VideoCapture(1)

calib_result_pickle = pickle.load(open("camera_calib_pickle.p", "rb"))
mtx = calib_result_pickle["mtx"]
optimal_camera_matrix = calib_result_pickle["optimal_camera_matrix"]
dist = calib_result_pickle["dist"]

# create the cropped image based on camera image r'C:\Users\lowel\OneDrive\Pictures\cameraCal\img0.jpg'
src = cv2.imread(r"C:\Users\lowel\PycharmProjects\helping-hands-ysp-david\frame.jpg")
# distorted_image = cv2.rotate(src, cv2.ROTATE_180)
undistorted_image = cv2.undistort(src, mtx, dist, None, optimal_camera_matrix)

cropped_board = undistorted_image[235:322, 420:575]

cv2.imshow('frame', undistorted_image)
cv2.imwrite('image.jpg', undistorted_image)
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()