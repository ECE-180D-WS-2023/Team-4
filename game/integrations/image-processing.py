import pygame
import threading
import time
import mediapipe as mp
import cv2 as cv
import numpy as np
from aim_hand import *

mp_drawing = mp.solutions.drawing_utils # give drawing utilities
mp_pose = mp.solutions.pose # import pose estimation model

running = True
latest_frame = None
latest_frame_available = threading.Condition()

def camera_worker_function():
    global latest_frame

    camera = cv.VideoCapture(0)
    assert camera.isOpened()

    while running:
        (rv, frame) = camera.read()
        if not rv: break

        with latest_frame_available:
            latest_frame = frame
            latest_frame_available.notify_all()

    camera.release()

def mediapipe_worker_function():
    # globals for values you need in the game
    angle = 0

    while running:
        with latest_frame_available:
            if latest_frame_available.wait(timeout=1.0):
                frame = latest_frame
            else: # False means timeout
                continue # -> recheck `running`

        if frame is None: break # sentinel value to shut down

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image = cv.flip(image, 1)
        image.flags.writeable = False
        results = pose.process(image)
        # print(results)
        try:
            landmarks = results.pose_landmarks.landmark
            mid = [960/1920.0, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y + 100/1080.0]
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            mid = [nose[0], right_wrist[1] + 300/1080.0]
            angle = calculate_angle(nose, mid, right_wrist)
        except:
            pass
        print(angle)

camera_thread = threading.Thread(target=camera_worker_function)    
camera_thread.start()

mediapipe_thread = threading.Thread(target=mediapipe_worker_function)
mediapipe_thread.start()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

class Player(object):
    def __init__(self):
        self.player = pygame.rect.Rect((300, 400, 50, 50))
        self.color = "white"

    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed, y_speed))

    def change_color(self, color):
        self.color= color

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)

    pygame.init()

player1 = Player()
player2 = Player()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

cap = cv.VideoCapture(0)
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYBUTTONDOWN:
            # if pygame.joystick.Joystick(1).get_button(0):
            #     player1.change_color("blue")
            if pygame.joystick.Joystick(0).get_button(0):
                player2.change_color("red")
        #     elif pygame.joystick.Joystick(1).get_button(0):
        #         player.change_color("green")
        #     elif pygame.joystick.Joystick(1).get_button(1):
        #         player.change_color("purple")

    # if event.type == pygame.JOYAXISMOTION:
    #     print(event)
    # x1_speed = round(pygame.joystick.Joystick(1).get_axis(0))
    # y1_speed = round(pygame.joystick.Joystick(1).get_axis(1))
    x2_speed = round(pygame.joystick.Joystick(0).get_axis(0))*5
    y2_speed = round(pygame.joystick.Joystick(0).get_axis(1))*5

    # player1.move(x1_speed, y1_speed)
    player2.move(x2_speed, y2_speed)

    screen.fill((0,0,0))
    player1.draw(screen)
    player2.draw(screen)

    # t = time.time()
    # angle = get_angle(cap, pose)
    # # print(angle)
    # print(time.time() - t)

    pygame.display.update()
    clock.tick(100)

with latest_frame_available:
    latest_frame = None # sentinel value
    latest_frame_available.notify_all()
mediapipe_thread.join()
camera_thread.join()
