# ar_tag_detector.py
import cv2
import cv2.aruco as aruco
import numpy as np
import time
from tkinter import *
from PIL import Image, ImageTk

def detect_ar_tag(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters()
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    return ids

def overlay_text(frame, text, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (10, 50), font, 2, color, 3, cv2.LINE_AA)

def ar_tag_detection():
    cap = cv2.VideoCapture(2)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ids = detect_ar_tag(frame)
        if ids is not None:
            for tag_id in ids:
                number = int(tag_id[0])
                current_time = time.localtime().tm_sec
                if abs(current_time - number) <= 5:
                    overlay_text(frame, "Authentic", (0, 255, 0))
                else:
                    overlay_text(frame, "Inauthentic", (0, 0, 255))
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

class VideoStreamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        self.canvas = Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        self.delay = 15
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            ids = detect_ar_tag(frame)
            if ids is not None:
                for tag_id in ids:
                    number = int(tag_id[0])
                    current_time = time.localtime().tm_sec
                    if abs(current_time - number) <= 5:
                        overlay_text(frame, "Authentic", (0, 255, 0))
                    else:
                        overlay_text(frame, "Inauthentic", (0, 0, 255))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.window.after(self.delay, self.update)

def main():
    ar_tag_detection()

if __name__ == "__main__":
    main()
