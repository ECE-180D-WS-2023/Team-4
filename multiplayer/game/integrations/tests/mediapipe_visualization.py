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

# Main
cap = cv.VideoCapture(0)
width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

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
            nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            anchor = [nose.x, right_wrist.y + 250/1080.0]
            angle = calculate_angle((nose.x, nose.y), anchor, (right_wrist.x, right_wrist.y))

            # visualize angle
            cv.putText(image, "x", tuple(np.multiply(anchor, [width, height]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 3, (0,255,0), 3, cv.LINE_AA)
            # cv.putText(image, "o", tuple(np.multiply([nose.x, nose.y], [width, height]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 3, cv.LINE_AA)
            cv.line(image, tuple(np.multiply([nose.x, nose.y], [width, height]).astype(int)), tuple(np.multiply(anchor, [width, height]).astype(int)), (255,255,0), 3)
            cv.line(image, tuple(np.multiply([right_wrist.x, right_wrist.y], [width, height]).astype(int)), tuple(np.multiply(anchor, [width, height]).astype(int)), (255,255,0), 3)
            cv.putText(image, str(angle), (960,540), cv.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv.LINE_AA)
        except Exception as e:
            print(e)

        # Render mediapipe landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=5),
                                mp_drawing.DrawingSpec(color=(233, 74, 247), thickness=3, circle_radius=2))

        cv.imshow('Mediapipe Feed', image) # (1920x1080)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
