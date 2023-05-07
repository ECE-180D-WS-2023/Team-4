import mediapipe as mp
import threading
import queue
import cv2 as cv
import numpy as np

mp_drawing = mp.solutions.drawing_utils # give drawing utilities
mp_pose = mp.solutions.pose # import pose estimation model

def calculate_angle(a,b,c):
    a = np.array(a) # first
    b = np.array(b) # mid
    c = np.array(c) # end

    radians = np.arctan2(b[1]-c[1], c[0]-b[0]) - np.arctan2(b[1]-a[1], a[0]-b[0])
    angle = radians*180.0//np.pi

    # if angle > 180.0: # for pressing button situation the angle is between -90 to 90? or do we do 0 to 180 and have 90 has the starting
    #     angle = 360-angle
    
    return angle

class ImageProcessor:
    def __init__(self):
        self._angle = 0
        self.angle_queue = queue.Queue(maxsize=5)
        self._thread = threading.Thread(target=self._image_processing_thread_func, args=[self.angle_queue])
        self.running = threading.Event()

    @property
    def angle(self):
        try:
            self._angle = self.angle_queue.get(block=False)
        except:
            pass
        return self._angle

    def _image_processing_thread_func(self, angle_queue):
        angle = 0
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        camera = cv.VideoCapture(0)
        assert camera.isOpened()

        while self.running.is_set():
            (ret, frame) = camera.read()
            if not ret:
                break

            image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            try:
                landmarks = results.pose_landmarks.landmark
                nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
                right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                anchor = [nose.x, right_wrist.y + 250/1080.0]
                new_angle = calculate_angle((nose.x, nose.y), anchor, (right_wrist.x, right_wrist.y))
                angle = new_angle if abs(new_angle - angle) > 1 else angle
            except Exception as e:
                print(f"[POSE]: {e}")
            
            try:
                angle_queue.put(angle, block=False)
            except queue.Full:
                # print("Angle queue full!")
                oldest_item = angle_queue.get()
                angle_queue.put_nowait(angle)

    def start(self):
        if not self._thread.is_alive():
            self.running.set()
            self._thread = threading.Thread(
                target=self._image_processing_thread_func,
                args=[self.angle_queue]
            )
            self._thread.start()
            print("meow")

    def stop(self):
        if self._thread.is_alive():
            self.running.clear()
            self._thread.join()
