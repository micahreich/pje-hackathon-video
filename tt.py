import numpy as np
import cv2

#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

frame = cv2.imread('patterns_1/spacing_0.2_markersize_50.png')

# Our operations on the frame come here
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# alpha = 1.5  # Increase contrast
# beta = 0     # Keep the same brightness
# enhanced_gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

# edges = cv2.Canny(gray, 20, 50)  # Adjust these thresholds as needed


# ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

# cv2.imshow('Thresholded Image', enhanced_gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

res = cv2.aruco.detectMarkers(gray, dictionary)
print(res[0],res[1],len(res[2]))

if len(res[0]) > 0:
    cv2.aruco.drawDetectedMarkers(gray,res[0],res[1])
    print("-----", res[0], "????", res[1].flatten())
    most_occuring_element = np.argmax(np.bincount(res[1].flatten()))
    print("most_occuring_element: ", most_occuring_element)
else:
    print("No markers found")

# while True:
#     # Display the resulting frame
#     cv2.imshow('frame',gray)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break