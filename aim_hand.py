import mediapipe as mp
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

# Video Feed
cap = cv.VideoCapture(0)
# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # recolor image to RGB
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # flip image horizontally
        image = cv.flip(image, 1)

        # set flag
        image.flags.writeable = False

        # make detection
        results = pose.process(image)

        # recolor image back to BGR
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # if cv.waitKey(1) & 0xFF == ord('r'):
            # first = [960/1920.0,10/1080.0]
            # mid = [960/1920.0, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y + 100/1080.0]
            # print(mid)
            
            # get coordinates
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            # first = [960/1920.0,10/1080.0]
            mid = [nose[0], right_wrist[1] + 300/1080.0]
            mid_frame = [960, mid[1] * 1080]
            print(mid_frame)

            # calculate angles
            angle = calculate_angle(nose, mid, right_wrist)
            print(angle)

            # visualize angle
            cv.putText(image, "x", tuple(np.multiply(mid, [1920, 1080]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 3, (255,255,0), 3, cv.LINE_AA)
            cv.putText(image, "o", tuple(np.multiply(nose, [1920, 1080]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 3, (255,255,0), 3, cv.LINE_AA)
            cv.line(image, tuple(np.multiply(nose, [1920, 1080]).astype(int)), tuple(np.multiply(mid, [1920, 1080]).astype(int)), (255,255,0), 3)
            cv.line(image, tuple(np.multiply(right_wrist, [1920, 1080]).astype(int)), tuple(np.multiply(mid, [1920, 1080]).astype(int)), (255,255,0), 3)
            cv.putText(image, str(angle), (960,540), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,0), 2, cv.LINE_AA)
            
        except:
            pass

        # render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(240,236,120), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(172,14,240), thickness=3, circle_radius=2))

        cv.imshow('Mediapipe Feed', image) #(1920x1080)
        # print(cv.getWindowImageRect("Mediapipe Feed")) # to get the dimension of webcam

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()





