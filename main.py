import cv2
import dlib
import numpy as np

from detector import Detector
from tracker import Tracker
from helpers import print_info

detect = Detector('yolo/y416/yolov3.cfg', 'yolo/y416/yolov3.weights')
track = Tracker(50)

print_info("Loading Video...")
cap = cv2.VideoCapture('mp4/005.mp4')
print_info("Video Loaded!")
WIDTH  = int(cap.get(3))
HEIGHT = int(cap.get(4))
print_info(f"Width: {WIDTH} | Height: {HEIGHT}")

count = 0
trackers = []

while True:

    ret, frame = cap.read()

    if frame is None:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if count % 50 == 0:
        detect_image, objects = detect.detect_person(frame.copy())

        if len(objects) > 0:
            track.reset_trackers()

        for box in objects:
            track.start_tracker(rgb_frame, box)

        cv2.imshow("Detected", detect_image)
    else:
        
        tracking_image = track.track_person(frame.copy(), rgb_frame)

        n_o_p = track.get_tracker_length()

        tracking_image = cv2.putText(tracking_image, f'Number of people detected: {n_o_p}', (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("Tracked", tracking_image)
    
    cv2.imshow("Original Footage", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    count += 1

cap.release()
cv2.destroyAllWindows()