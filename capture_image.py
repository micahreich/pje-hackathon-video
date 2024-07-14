import cv2

# Step 1: Create a VideoCapture object to capture video from the webcam
cap = cv2.VideoCapture(0)  # 0 is usually the default camera

# Step 2: Capture a single frame
ret, frame = cap.read()

# Check if the frame was captured successfully
if ret:
    # Step 3: Save the captured frame as an image file
    cv2.imwrite('captured_image.jpg', frame)
else:
    print("Failed to capture image")

# Step 4: Release the VideoCapture object and close any open windows
cap.release()
cv2.destroyAllWindows()