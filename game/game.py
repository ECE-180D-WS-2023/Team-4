import pygame, sys, threading, queue
from button import Button
import random
from Player import Player
from Veggie import Veggie
from Base import Base
from Slingshot import Slingshot
from constants import *
from integrations.image_processing import *
import time, math
from integrations.speech_recognition import speech_rec

pygame.init()          # Start game

# Joystick configuration
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)


# https://stackoverflow.com/questions/73758038/pygame-wrong-resolution-on-macos
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
# SCREEN = pygame.display.set_mode((600, 800))

pygame.display.set_caption("Veggie Wars")

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
veggies = pygame.sprite.Group()
bases = pygame.sprite.Group()
slingshots = pygame.sprite.Group()
shots = pygame.sprite.Group()

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def tutorials():
    """
    MODE: TUTORIALS

    Only one player can move around.
    """
    clock = pygame.time.Clock()
    player1 = Player((80, 80), (2, 2), 1, PLAYER_ENGINEER, "Bruce", PLAYER_WALKING, 10)
    base1 = Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(3/4)), (3, 3), 1, 20, 0)
    base2 = Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(1/4)), (3, 3), 2, 20, 0)
    slingshot1 = Slingshot((900, 1000), (0, 0), 1)


    all_sprites.add([base1, base2, slingshot1])
    players.add([player1])                        # Add player1 to players group
    bases.add([base1, base2])                     # Add base1 to bases group
    slingshots.add([slingshot1])

    running_threads = threading.Event()
    running = True
    latest_frame = queue.Queue(maxsize=3)
    latest_frame_available = threading.Condition()
    angle_queue = queue.Queue(maxsize=10)

    camera_thread = threading.Thread(target=read_frames_from_camera, args=[running_threads, latest_frame_available, latest_frame])
    mediapipe_thread = threading.Thread(target=calculate_angle_using_mediapipe, args=[running_threads, latest_frame_available, latest_frame, angle_queue])

    TUTORIALS_BG = pygame.image.load("assets/grass.png")

    audio_list = ["Eddie"]
    stop_listening = speech_rec(audio_list)
    angle = 0


    for _ in range(MAX_VEGGIES):
        v_x = random.randint(0, SCREEN_WIDTH - VEGGIE_WIDTH)
        v_y = random.randint(0, SCREEN_HEIGHT - VEGGIE_HEIGHT)
        veggie = Veggie((v_x, v_y), (0, 0), 1, 10)
        veggies.add(veggie)

    while running:
        TUTORIALS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(TUTORIALS_BG, (0, 0))


        pressed_keys = pygame.key.get_pressed()   # Keyboard input

        # Audio Input
        if audio_list[0] == "switch":
            print(".....................")
            audio_list[0] = "Eddie"
            player1.toggle_mount(slingshot1)

        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                stop_listening(wait_for_stop=False)
                pygame.quit()
                sys.exit()
            # Mount Slingshot
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    audio_list[0] = "Eddie"
                    player1.toggle_mount(slingshot1)
                if event.key == K_SPACE:
                    player1.harvest(veggies)
            # Attack
            elif event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0):
                    player1.attack(Veggie, angle, (shots, all_sprites))

        if len(veggies) < MAX_VEGGIES:
            v_x = random.randint(0, SCREEN_WIDTH - VEGGIE_WIDTH)
            v_y = random.randint(0, SCREEN_HEIGHT - VEGGIE_HEIGHT)
            veggie = Veggie((v_x, v_y), (0, 0), 1, 10)
            veggies.add(veggie)

        if player1.state == PLAYER_SHOOTING:
            if not camera_thread.is_alive():
                running_threads.clear()
                camera_thread = threading.Thread(target=read_frames_from_camera, args=[running_threads, latest_frame_available, latest_frame])
                mediapipe_thread = threading.Thread(target=calculate_angle_using_mediapipe, args=[running_threads, latest_frame_available, latest_frame, angle_queue])
                camera_thread.start()
                mediapipe_thread.start()
            try:
                angle = angle_queue.get(block=False)
            except:
                pass

        if player1.state != PLAYER_SHOOTING:
            if camera_thread.is_alive():
                running_threads.set()
                camera_thread.join()
                mediapipe_thread.join()

        x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
        y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
        


        # Refresh screen and display objects
        for player in players:
            player.update([x_speed, y_speed], angle, SCREEN)
        for veggie in veggies:
            veggie.update(SCREEN)
        for base in bases:
            base.update(shots, SCREEN)
        for slingshot in slingshots:
            slingshot.update(SCREEN)
        for shot in shots:
            shot.update(SCREEN)

        # show mask
        # for sprite in all_sprites:
        #     pygame.draw.rect(SCREEN, (255,255,255), sprite, 2)
        #     SCREEN.blit(sprite.mask.to_surface(sprite.surf, setcolor = (255,255,255)), sprite.rect)

        if base2.health == 0:
            for sprite in all_sprites:
                sprite.kill()
            running = False
            running_threads.set()
            stop_listening(wait_for_stop=False)
            pygame.quit()
            break

        pygame.display.flip()
        clock.tick(100)

    with latest_frame_available:
        latest_frame = None # sentinel value
        latest_frame_available.notify_all()
    mediapipe_thread.join()
    camera_thread.join()



def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Initialize main text box
        MENU_TEXT = get_font(100).render("Veggie Wars", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 80))

        # Initialize buttons
        PLAY_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png"), pos=(640, 230),
                            text_input="PLAY", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png"), pos=(640, 380),
                            text_input="OPTIONS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        TUTORIALS_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png"), pos=(640, 530),
                            text_input="TUTORIALS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/menu/Quit Rect.png"), pos=(640, 650),
                            text_input="QUIT", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # change color when hovering
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, TUTORIALS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # event after clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if TUTORIALS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    tutorials()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

