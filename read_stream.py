import cv2
import collections
import time
import numpy as np
import datetime

class InterpretStream:
    def __init__(self, time_threshold_s=2, delay_s=2):
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.time_threshold_s = time_threshold_s
        self.delay_s = delay_s

    def get_current_seconds(self):
        current_utc_time = datetime.datetime.utcnow()
        seconds = int(current_utc_time.second)
        return seconds
    
    def is_valid(self, aruco_id, curr_seconds):
        return abs(curr_seconds - aruco_id) <= self.time_threshold_s
    
    def run(self):
        # Initialize video capture from the webcam
        cap = cv2.VideoCapture(0)

        # Get the frame rate of the video
        fps = 20
        frame_delay = max(1, int(fps * self.delay_s))

        # Create a deque to store frames
        frame_buffer = collections.deque(maxlen=frame_delay)

        while True:
            ret, frame = cap.read()
            curr_seconds = self.get_current_seconds()
            
            if not ret:
                break
            
            # Add the current frame to the buffer
            frame_buffer.append(frame)
            
            # If the buffer is full, get the oldest frame
            if len(frame_buffer) == frame_delay:
                delayed_frame = frame_buffer.popleft()
                
                # Display the delayed frame
                
                # Process the delayed frame
                gray = cv2.cvtColor(delayed_frame, cv2.COLOR_BGR2GRAY)
                res = cv2.aruco.detectMarkers(gray, self.dictionary)
                if len(res[0]) > 0:
                    most_occuring_element = np.argmax(np.bincount(res[1].flatten()))
                    print("curr", curr_seconds, "most", most_occuring_element)
                    
                    if self.is_valid(most_occuring_element, curr_seconds):
                        result_string = "Valid"
                        color = (0, 255, 0)
                    else:
                        result_string = "Invalid"
                        color = (0, 0, 255)
                    
                    cv2.putText(
                        delayed_frame,
                        result_string,
                        (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        5,
                        color,
                        3,
                        cv2.LINE_AA
                    )
                    
                    cv2.imshow(f'Current Frame (delay={self.delay_s}s)', delayed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    stream = InterpretStream(
        time_threshold_s=2,
        delay_s=0
    )
    stream.run()