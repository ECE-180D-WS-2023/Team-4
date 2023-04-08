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

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = radians*180.0//np.pi

    # if angle > 180.0: # for pressing button situation the angle is between -90 to 90? or do we do 0 to 180 and have 90 has the starting
    #     angle = 360-angle
    
    return angle

def read_frames_from_camera(running_event, frame_available, frame_queue):
    """Read frames from camera

    Args:
        running_event (threading.Event): Threading event that, when set, releases the camera
        frame_available (threading.Condition): Threading condition that is used to notify other threads when a new frame is available
        frame_queue (queue.Queue): Queue to place new frames in
    """
    camera = cv.VideoCapture(0)
    assert camera.isOpened()

    while not running_event.is_set():
        (ret, frame) = camera.read()
        if not ret:
            break

        with frame_available:
            try:
                frame_queue.put(frame, block=False)
                frame_available.notify_all()
            except:
                frame_available.notify_all()
                # print("Queue is full")

    camera.release()

def calculate_angle_using_mediapipe(running_event, frame_available, frame_queue, angle_queue):
    """Read frames from camera

    Args:
        running_event (threading.Event): Threading event that, when set, stops processing
        frame_available (threading.Condition): Threading condition that indicates when a new frame is available
        frame_queue (queue.Queue): Queue to to grab new frames from
    """
    # globals for values you need in the game
    angle = 0
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    while not running_event.is_set():
        with frame_available:
            if frame_available.wait(timeout=1.0):
                print("Getting")
                frame = frame_queue.get()
            else: # False means timeout
                continue # -> recheck `running`

        if frame is None:
            break # fallback value to shut down

        # Process the frame
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image = cv.flip(image, 1)
        image.flags.writeable = False
        results = pose.process(image)

        try:
            landmarks = results.pose_landmarks.landmark
            mid = [960/1920.0, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y + 100/1080.0]
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            mid = [nose[0], right_wrist[1] + 300/1080.0]
            new_angle = calculate_angle(nose, mid, right_wrist)
            angle = new_angle if abs(new_angle - angle) > 1 else angle
        except:
            pass

        angle_queue.put(angle)
