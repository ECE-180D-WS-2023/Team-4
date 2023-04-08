import pygame
import threading
import multiprocessing
import queue
from image_processing import *

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

def main():
    running = multiprocessing.Event()
    latest_frame = multiprocessing.Queue()
    latest_frame_available = multiprocessing.Condition()
    angle_queue = multiprocessing.Queue(10)

    camera_thread = multiprocessing.Process(target=read_frames_from_camera, args=[running, latest_frame_available, latest_frame])
    mediapipe_thread = multiprocessing.Process(target=calculate_angle_using_mediapipe, args=[running, latest_frame_available, latest_frame, angle_queue])
    camera_thread.start()
    mediapipe_thread.start()

    player1 = Player()
    player2 = Player()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800,600))

    angle = 0
    while not running.is_set():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running.set()
            if event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0):
                    player2.change_color("red")

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
        try:
            angle = angle_queue.get(block=False)
            # angle = angle_queue.get_nowait()
        except:
            pass
        print(angle)


        pygame.display.update()
        clock.tick(100)

    with latest_frame_available:
        latest_frame = None # sentinel value
        latest_frame_available.notify_all()
    mediapipe_thread.join()
    camera_thread.join()

if __name__ == "__main__":
  main()
