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
    angle = radians*180.0/np.pi

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
        image.flags.writeable = False

        # make detection
        results = pose.process(image)

        # recolor image back to BGR
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            if cv.waitKey(1) & 0xFF == ord('r'):
                left_elbow_zero = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]
                left_shoulder_zero = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
                print('hello')
            
            # get coordinates
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]

            # calculate angles
            angle = calculate_angle(right_shoulder, left_shoulder, left_elbow)
            angle2 = calculate_angle(left_elbow_zero, left_shoulder_zero, left_elbow)

            # visualize angle
            cv.putText(image, str(angle), tuple(np.multiply(left_shoulder, [960, 540]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,0), 2, cv.LINE_AA)
            # cv.putText(image, str(angle2), tuple(np.multiply(left_shoulder - 200, [960, 540]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 2, (255,255,0), 2, cv.LINE_AA)
        except:
            pass

        # render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(240,236,120), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(172,14,240), thickness=3, circle_radius=2))

        cv.imshow('Mediapipe Feed', image)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()





