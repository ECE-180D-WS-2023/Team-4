import pygame
import sys
import threading
import queue
from pygame import mixer
from button import Button
import random
from Player import *
from Veggie import *
from Base import Base
from Slingshot import Slingshot
from constants import *
from integrations.image_processing import *
import time
import math
from integrations.speech_recognition import speech_rec
from Dimmer import *

mixer.init()           # music
pygame.init()          # Start game

# Joystick configuration
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x)
             for x in range(pygame.joystick.get_count())]
print(joysticks)


# https://stackoverflow.com/questions/73758038/pygame-wrong-resolution-on-macos
SCREEN = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
# SCREEN = pygame.display.set_mode((600, 800))

pygame.display.set_caption("Veggie Wars")

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
veggies = pygame.sprite.Group()
bases = pygame.sprite.Group()
slingshots = pygame.sprite.Group()
shots = pygame.sprite.Group()
effects = pygame.sprite.Group()

BG = pygame.image.load("assets/new_background.png")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render(
            "This is the PLAY screen.", True, "White")
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


def choosePlayer():

    background = pygame.image.load("assets/grass.png")
    dimmer = Dimmer(keepalive=True)
    running = True

    ENGINEER_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png"), pos=(500, 350),
                             text_input="ENGINEER", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

    SOLDIER_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png"), pos=(SCREEN_WIDTH/2, 350),
                            text_input="SOLDIER", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

    DARTHVADER_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png"), pos=(SCREEN_WIDTH - 500, 350),
                               text_input="DARTH VADER", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

    while running:

        CHOOSEPLAYER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(background, (0, 0))
        dimmer.dim(darken_factor=200, color_filter=(0, 0, 0))

        for button in [ENGINEER_BUTTON, SOLDIER_BUTTON, DARTHVADER_BUTTON]:
            button.changeColor(CHOOSEPLAYER_MOUSE_POS)
            button.hoverNoise(CHOOSEPLAYER_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ENGINEER_BUTTON.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                    player = Engineer(
                        (80, 80), (2.5, 2.5), 1, PLAYER_ENGINEER, "Bruce", PLAYER_WALKING, 10)
                    return player
                if SOLDIER_BUTTON.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                    player = Soldier((80, 80), (2.5, 2.5), 1,
                                     PLAYER_ENGINEER, "Bruce", PLAYER_WALKING, 10)
                    return player
                if DARTHVADER_BUTTON.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                    player = DarthVader(
                        (80, 80), (2.5, 2.5), 1, PLAYER_ENGINEER, "Bruce", PLAYER_WALKING, 10)
                    return player
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player = Player((80, 80), (2.5, 2.5), 1,
                                    PLAYER_ENGINEER, "Bruce", PLAYER_WALKING, 10)
                    return player
                if event.key == K_q:
                    player = Player((80, 80), (2.5, 2.5), 1,
                                    PLAYER_FARMER, "Bruce", PLAYER_WALKING, 10)
                    return player

        pygame.display.update()


def tutorials():
    """
    MODE: TUTORIALS

    Only one player can move around.
    """

    # load music and sounds
    pygame.mixer.music.load('assets/music/on-a-clear-day.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1, 0.0)

    is_shooting_music = False
    # walking_sound = pygame.mixer.Sound('assets/music/walking.mp3')
    # shooting_sound = pygame.mixer.Sound('assets/music/shotgun-firing.mp3')

    # Timer and Clock
    clock = pygame.time.Clock()
    Timer_on = False

    # GameObjects
    player1 = choosePlayer()
    base1 = Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(3/4)), (3, 3), 1, 20, 0)
    base2 = Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(1/4)), (3, 3), 2, 20, 0)
    slingshot1 = Slingshot((900, 1000), (0, 0), 1)

    all_sprites.add([base1, base2, slingshot1])
    # Add player1 to players group
    players.add([player1])
    bases.add([base1, base2])                     # Add base1 to bases group
    slingshots.add([slingshot1])

    running_threads = threading.Event()
    running = True
    latest_frame = queue.Queue(maxsize=3)
    latest_frame_available = threading.Condition()
    angle_queue = queue.Queue(maxsize=10)

    camera_thread = threading.Thread(target=read_frames_from_camera, args=[
                                     running_threads, latest_frame_available, latest_frame])
    mediapipe_thread = threading.Thread(target=calculate_angle_using_mediapipe, args=[
                                        running_threads, latest_frame_available, latest_frame, angle_queue])

    TUTORIALS_BG = pygame.image.load("assets/grass.png")

    audio_list = ["Eddie"]
    stop_listening = speech_rec(audio_list)
    angle = 0

    veggies_list = Veggie.__subclasses__()
    for _ in range(MAX_VEGGIES):
        v_x = random.randint(0, SCREEN_WIDTH - VEGGIE_WIDTH)
        v_y = random.randint(0, SCREEN_HEIGHT - VEGGIE_HEIGHT)
        v_type = random.choice(veggies_list)
        veggie = v_type((v_x, v_y), (0, 0), 1)
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
            # Mount Slingshot and Harvesting
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    audio_list[0] = "Eddie"
                    player1.toggle_mount(slingshot1)
                if event.key == K_SPACE:
                    player1.harvest(veggies)
                if event.key == K_TAB:
                    if not Timer_on:
                        tempEffect = GameObject((PLAYER_WIDTH*3, PLAYER_HEIGHT*3), player1.pos, player1.vel,
                                                player1.team_num, img="assets/players/timeEffects.png", animation_steps=[5,5,5,5], scale=1)
                        effects.add([tempEffect])
                        Timer_on = True
                        effect_start_time = pygame.time.get_ticks()
                        player1.promote()
                    
            # Attack
            elif event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0):
                    player1.attack(angle, (shots, all_sprites))
                if pygame.joystick.Joystick(0).get_button(1):
                    player1.harvest(veggies)
                if pygame.joystick.Joystick(0).get_button(3):
                    player1.toggle_mount(slingshot1)

        if len(veggies) < MAX_VEGGIES:
            v_x = random.randint(0, SCREEN_WIDTH - VEGGIE_WIDTH)
            v_y = random.randint(0, SCREEN_HEIGHT - VEGGIE_HEIGHT)
            veggie = Mushroom((v_x, v_y), (0, 0), 1)
            veggies.add(veggie)

        if player1.state == PLAYER_SHOOTING:
            if not is_shooting_music and player1.promoted == False:
                pygame.mixer.music.load('assets/music/not-afraid.mp3')
                pygame.mixer.music.play(-1)
                is_shooting_music = True
            if not camera_thread.is_alive():
                running_threads.clear()
                camera_thread = threading.Thread(target=read_frames_from_camera, args=[
                                                 running_threads, latest_frame_available, latest_frame])
                mediapipe_thread = threading.Thread(target=calculate_angle_using_mediapipe, args=[
                                                    running_threads, latest_frame_available, latest_frame, angle_queue])
                camera_thread.start()
                mediapipe_thread.start()
            try:
                angle = angle_queue.get(block=False)
            except:
                pass

        if player1.state != PLAYER_SHOOTING:
            if is_shooting_music and player1.promoted == False:
                pygame.mixer.music.load('assets/music/on-a-clear-day.mp3')
                pygame.mixer.music.play(-1)
                is_shooting_music = False
            if camera_thread.is_alive():
                running_threads.set()
                camera_thread.join()
                mediapipe_thread.join()

        try:
            x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
            y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
        except:
            x_speed = 0
            y_speed = 0

        # Refresh screen and display objects
        for effect in effects:
            if effect_start_time != None:
                if pygame.time.get_ticks() - effect_start_time < 2500:
                    effect.update(SCREEN, 3)
                else:
                    Timer_on = False
                    player1.state = PLAYER_WALKING
                    effect.kill()
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
        latest_frame = None  # sentinel value
        latest_frame_available.notify_all()
    mediapipe_thread.join()
    camera_thread.join()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render(
            "This is the OPTIONS screen.", True, "Black")
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

    # Initialize buttons
    PLAY_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png"), pos=(700, 350),
                         text_input="PLAY", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png"), pos=(700, 500),
                            text_input="OPTIONS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
    TUTORIALS_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png"), pos=(700, 650),
                              text_input="TUTORIALS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/menu/Quit Rect.png"), pos=(700, 800),
                         text_input="QUIT", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

    # Button clicking sound effect
    clicking_sound = mixer.Sound('assets/music/button_clicked.mp3')
    clicking_sound.set_volume(1.5)

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Initialize main text box
        MENU_TEXT = get_font(150).render("Veggie Wars", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 120))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # change color and play noise when hovering
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, TUTORIALS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.hoverNoise(MENU_MOUSE_POS)
            button.update(SCREEN)

        # event after clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    options()
                if TUTORIALS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    tutorials()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
