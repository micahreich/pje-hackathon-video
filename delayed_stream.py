import cv2
import collections
import time

# Initialize video capture from the webcam
cap = cv2.VideoCapture(0)

# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_delay = int(fps * 2)  # Number of frames to delay by 10 seconds

# Create a deque to store frames
frame_buffer = collections.deque(maxlen=frame_delay)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Add the current frame to the buffer
    frame_buffer.append(frame)
    
    # If the buffer is full, get the oldest frame (which is 10 seconds old)
    if len(frame_buffer) == frame_delay:
        delayed_frame = frame_buffer.popleft()
        
        # Process the delayed frame (you can add your processing code here)
        
        # Display the delayed frame
        cv2.imshow('Delayed Frame', delayed_frame)
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
