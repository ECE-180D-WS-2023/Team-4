import pygame
import sys
import threading
import queue
from pygame import mixer
from button import *
from test_button import *
import random
from Player import *
from Veggie import *
from Base import Base
from Slingshot import Slingshot
from constants import *
from integrations.image_processing import *
import time
import socket
import math
from integrations.speech_recognition import *
from Dimmer import *
from Instructions import *
from input import *

mixer.init()           # music
pygame.init()          # Start game

# Joystick configuration
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x)
             for x in range(pygame.joystick.get_count())]
print(joysticks)

clock = pygame.time.Clock()

# https://stackoverflow.com/questions/73758038/pygame-wrong-resolution-on-macos
SCREEN = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
# SCREEN = pygame.display.set_mode((600, 800))

pygame.display.set_caption("Veggie Wars")


STATIC_BACKGROUND = pygame.image.load("assets/menu/static-background.png").convert_alpha()
BG_5 = pygame.image.load("assets/menu/5.png").convert_alpha()
BG_6 = pygame.image.load("assets/menu/6.png").convert_alpha()

def get_font(size, font="assets/fonts/font.ttf"):
    return pygame.font.Font(font, size)

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # dummy socket
    try:
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def host():
    # input_box_rect = pygame.Rect(1080,200,400,40)
    # input_text = get_private_ip()
    # input_active = False
    #
    # # Set up the cursor
    # cursor_active = False
    # cursor_timer = 0
    #
    # # Set up the label
    # label_text = "Enter IP Address:"
    # label_surface = get_font(30).render(label_text, True, (0,0,0))
    # label_rect = label_surface.get_rect()
    # label_rect.x = input_box_rect.x
    # label_rect.y = input_box_rect.y - label_rect.height - 5
    #
    background = pygame.image.load("assets/menu/static-background.png").convert_alpha()
    input = InputField((SCREEN_WIDTH/2, 100), 15, label_text="Enter IP:", border_padding=10)
    menu = ButtonMenu()
    menu.add_button(TestButton((SCREEN_WIDTH/2, 300), "FRONT"))
    menu.add_button(TestButton((SCREEN_WIDTH/2, 400), "BACK"))
    running = True
    while running:
        SCREEN.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.check_for_presses(event.pos):
                    running = False
                input.process_mousedown(event)
            elif event.type == KEYDOWN:
                input.process_keydown(event)

        menu.draw(SCREEN)
        input.draw(SCREEN)
        input.update()
        pygame.display.flip()
        clock.tick(60)

def join():
    ...

def play():
    background_5 = 0
    background_6 = 0

    # Initialize buttons
    HOST_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png").convert_alpha(), pos=(700, 350),
                         text_input="HOST", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
    JOIN_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png").convert_alpha(), pos=(700, 500),
                            text_input="JOIN", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
    BACK_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png").convert_alpha(), pos=(700, 650),
                            text_input="BACK", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

    # Button clicking sound effect
    clicking_sound = mixer.Sound('assets/music/button_clicked.mp3')
    clicking_sound.set_volume(1.5)

    running = True
    while running:
        SCREEN.blit(STATIC_BACKGROUND, (0, 0))
        SCREEN.blit(BG_5, (background_5, 0))
        SCREEN.blit(BG_6, (background_6, 0))
        background_5 -= 5
        background_6 -= 30
        if background_5 <= -BG_5.get_width():
            background_5 = 0
        if background_6 <= -BG_6.get_width():
            background_6 = 0

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Initialize main text box
        MENU_TEXT = get_font(150).render("Veggie Wars", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 120))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # change color and play noise when hovering
        for button in [HOST_BUTTON, JOIN_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.hoverNoise(MENU_MOUSE_POS)
            button.update(SCREEN)

        # event after clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HOST_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    host()
                if JOIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    # options()
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    running = False

        pygame.display.update()
        clock.tick(60)


def choosePlayer():

    # blit an universal background
    # background = pygame.image.load("assets/pause-phase/choose-playert.png")

    # Animations 
    book_animation = Animation((SCREEN_WIDTH/2,SCREEN_HEIGHT/2), pygame.image.load("assets/pause-phase/choose-player-old.png").convert_alpha(), 
                                [7], (2560, 1600), 1, pause_frame=[0,5], color=None)
    
    # text_appear_animation = Animation((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), pygame.image.load("assets/pause-phase/reveal-message.png").convert_alpha(),
                                 # [13], (SCREEN_WIDTH, SCREEN_HEIGHT), 1, pause_frame=[0, 12], animation_cooldown=90)

    phase2_text_appear = Animation((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), pygame.image.load("assets/pause-phase/phase2-text-appear.png").convert_alpha(),
                                  [13], (SCREEN_WIDTH, SCREEN_HEIGHT), 1, pause_frame=[0], animation_cooldown=90)
    # Phase 1
    STUDENT_PLAYERCARD = StudentCard(image=pygame.image.load("assets/players/student.png").convert_alpha(), pos=(1785, 677),
                             text_input="STUDENT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    SOLDIER_PLAYERCARD = SoldierCard(image=pygame.image.load("assets/players/soldier.png").convert_alpha(), pos=(1785, 677),
                            text_input="SOLDIER", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    ENCHANTRESS_PLAYERCARD = EnchantressCard(image=pygame.image.load("assets/players/enchantress.png").convert_alpha(), pos=(1785, 677),
                               text_input="ENCHANTRESS", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    IMREADY_BUTTON = Button(image=pygame.image.load("assets/pause-phase/pause-button-large.png").convert_alpha(), pos=(1800, 1225),
                               text_input="I'M READY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    RIGHT_ARROW = Button(image=pygame.image.load("assets/pause-phase/right-arrow.png").convert_alpha(), pos=(1985, 675),
                                text_input=None, font=None, base_color=None, hovering_color=None)

    LEFT_ARROW = Button(image=pygame.image.load("assets/pause-phase/left-arrow.png").convert_alpha(), pos=(1592, 675),
                                text_input=None, font=None, base_color=None, hovering_color=None)
    
    player_class = Student
    player_weapon = Newb_Crossbow
    map_selection = SPRING
    

    # Phase 2
    CONTINUE_BUTTON = Button(image=pygame.image.load("assets/pause-phase/pause-button-large.png").convert_alpha(), pos=(1800, 1225),
                               text_input="FIGHT!", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
    
    SKULL_CROSSBOW = Button(image=pygame.image.load("assets/pause-phase/skull-crossbow-button.png").convert_alpha(), pos=(556, 926),
                               text_input=None, font=None, base_color=None, hovering_color="White")
    
    DEMONIC_CROSSBOW = Button(image=pygame.image.load("assets/pause-phase/demonic-crossbow-button.png").convert_alpha(), pos=(697, 926),
                               text_input=None, font=None, base_color=None, hovering_color="White")
    
    FIRE_CROSSBOW = Button(image=pygame.image.load("assets/pause-phase/fire-crossbow-button.png").convert_alpha(), pos=(838, 926),
                               text_input=None, font=None, base_color=None, hovering_color="White")
    
    VENOM_CROSSBOW = Button(image=pygame.image.load("assets/pause-phase/venom-crossbow-button.png").convert_alpha(), pos=(976, 926),
                               text_input=None, font=None, base_color=None, hovering_color="White")
    
    DIVINE_CROSSBOW = Button(image=pygame.image.load("assets/pause-phase/divine-crossbow-button.png").convert_alpha(), pos=(1117, 926),
                               text_input=None, font=None, base_color=None, hovering_color="White")
    
    SPRING_MAP = Button(image=pygame.image.load("assets/pause-phase/map-button.png").convert_alpha(), pos=(1764, 630),
                               text_input=None, font=None, base_color=None, hovering_color="White")
    
    FALL_MAP = Button(image=pygame.image.load("assets/pause-phase/map-button.png").convert_alpha(), pos=(1764, 850),
                               text_input=None, font=None, base_color=None, hovering_color="White")
    
    WINTER_MAP = Button(image=pygame.image.load("assets/pause-phase/map-button.png").convert_alpha(), pos=(1764, 1079),
                               text_input=None, font=None, base_color=None, hovering_color="White")
    
    WEAPON_BOUNDING_BOX = pygame.image.load("assets/pause-phase/weapon-selection-outline.png")
    WBB_size = (80, 80)
    WBB_pos = None

    MAP_BOUNDING_BOX = pygame.image.load("assets/pause-phase/map-selection-outline.png")
    MBB_size = (630, 230)
    MBB_pos = None


    input_box_rect = pygame.Rect(1690,1114,200,50)
    input_text = ""
    input_active = False

    # Set up the cursor
    cursor_active = False
    cursor_timer = 0

    # Set up the label
    label_text = "Enter Your Name:"
    label_surface = get_font(30, "assets/fonts/inventory_font.ttf").render(label_text, True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.x = input_box_rect.x
    label_rect.y = input_box_rect.y - label_rect.height - 5

    # PlayerCard gallery
    playercard_id = 0
    playercards = [STUDENT_PLAYERCARD, SOLDIER_PLAYERCARD, ENCHANTRESS_PLAYERCARD]

    phase1 = True
    phase1_5 = False
    phase2 = False
    book_resume_signal = False
    phase2_resume_signal = False

    running = True

    while running:
        CHOOSEPLAYER_MOUSE_POS = pygame.mouse.get_pos()

        [stop_flag, pause_flag] = book_animation.update_norepeat(SCREEN, resume_signal=book_resume_signal)


        # reset resume flag
        if pause_flag == False:
            book_resume_signal = False
        
        if phase1:
            # Update playercard gallery
            playercards[playercard_id].is_active = True
            for playercard in playercards:
                if playercard.is_active:
                    playercard.changeColor(CHOOSEPLAYER_MOUSE_POS)
                    playercard.hoverNoise(CHOOSEPLAYER_MOUSE_POS)
                    playercard.update(SCREEN)

            for button in [IMREADY_BUTTON]:
                button.changeColor(CHOOSEPLAYER_MOUSE_POS)
                button.hoverNoise(CHOOSEPLAYER_MOUSE_POS)
                button.update(SCREEN)
                # button.hoverShow(CHOOSEPLAYER_MOUSE_POS, SCREEN)

            for arrow in [RIGHT_ARROW, LEFT_ARROW]:
                arrow.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if STUDENT_PLAYERCARD.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player_class = Student
                    elif SOLDIER_PLAYERCARD.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player_class = Soldier
                    elif ENCHANTRESS_PLAYERCARD.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player_class = Enchantress
                    elif RIGHT_ARROW.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        playercards[playercard_id].is_active = False
                        playercard_id += 1
                        if playercard_id == len(playercards):
                            playercard_id = 0
                    elif LEFT_ARROW.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        playercards[playercard_id].is_active = False
                        playercard_id -= 1
                        if playercard_id == -1:
                            playercard_id = len(playercards)-1
                    elif IMREADY_BUTTON.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        book_resume_signal = True
                        phase1 = False
                        phase1_5= True
                    elif input_box_rect.collidepoint(event.pos):
                        input_active = True
                        cursor_active = True
                        cursor_timer = pygame.time.get_ticks()
                    else:
                        msg_resume_signal = True
                        input_active = False
                        cursor_active = False

                elif event.type == KEYDOWN:
                    if input_active:
                        if event.unicode.isprintable():
                            input_text += event.unicode
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]

            # pygame.draw.rect(SCREEN, (0,0,0), input_box_rect, 2)
            input_surface = get_font(50, "assets/fonts/inventory_font.ttf").render(input_text, True, (255,255,255))
            SCREEN.blit(input_surface, (input_box_rect.x + 50, input_box_rect.y + 5))
            SCREEN.blit(label_surface, label_rect)

            if input_active:
                cursor_timer += pygame.time.get_ticks() % 1000
                if cursor_timer > 3000:
                    cursor_active = not cursor_active
                    cursor_timer = 0
                if cursor_active:
                    cursor_surface = get_font(50).render("|", True, (0,0,0))
                    cursor_rect = cursor_surface.get_rect()
                    cursor_rect.x = input_box_rect.x + 50 + input_surface.get_width()
                    cursor_rect.y = input_box_rect.y + 5
                    SCREEN.blit(cursor_surface, cursor_rect)
        # Phase 1.5
        elif phase1_5:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    book_resume_signal = True
                    phase2_resume_signal = True
                    phase1_5 = False
                    phase2 = True
        # Phase 2
        elif phase2:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CONTINUE_BUTTON.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player = player_class(
                            pos=(80, 80), vel=(2.5, 2.5), team_num=1, name=input_text, 
                            state=PLAYER_WALKING, health=10, weapon=player_weapon)
                        return player, map_selection
                    elif SKULL_CROSSBOW.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player_weapon = Skull_Crossbow
                        WBB_pos = (556, 926)
                    elif DEMONIC_CROSSBOW.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player_weapon = Demonic_Crossbow
                        WBB_pos = (697, 926)
                    elif FIRE_CROSSBOW.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player_weapon = Fire_Crossbow
                        WBB_pos = (838, 926)
                    elif VENOM_CROSSBOW.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player_weapon = Venom_Crossbow
                        WBB_pos = (976, 926)
                    elif DIVINE_CROSSBOW.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        player_weapon = Divine_Crossbow
                        WBB_pos = (1117, 926)
                    elif SPRING_MAP.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        map_selection = SPRING
                        MBB_pos = (1764, 630)
                    elif FALL_MAP.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        map_selection = FALL
                        MBB_pos = (1764, 850)
                    elif WINTER_MAP.checkForInput(CHOOSEPLAYER_MOUSE_POS):
                        map_selection = WINTER
                        MBB_pos = (1764, 1079)
                    
            # Buttons
            for button in [CONTINUE_BUTTON]:
                button.changeColor(CHOOSEPLAYER_MOUSE_POS)
                button.hoverNoise(CHOOSEPLAYER_MOUSE_POS)
                button.update(SCREEN)

            # Weapon bounding box
            if WBB_pos:
                SCREEN.blit(WEAPON_BOUNDING_BOX, (WBB_pos[0]-WBB_size[0]/2, WBB_pos[1]-WBB_size[1]/2))
            # Map bounding box
            if MBB_pos:
                SCREEN.blit(MAP_BOUNDING_BOX, (MBB_pos[0]-MBB_size[0]/2, MBB_pos[1]-MBB_size[1]/2))

            phase2_text_appear.update_norepeat(SCREEN, resume_signal=phase2_resume_signal)

        pygame.display.update()
        clock.tick(60)

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
    player1, map_selected = choosePlayer()
    base1 = Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(3.5/4)), (3, 3), 1, img = "assets/base/green-summer.png", health = 20, shield = 0)
    base2 = Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(0.5/4)), (3, 3), 2, img = "assets/base/maroon-summer.png", health = 20, shield = 0)
    slingshot1 = Slingshot((1400, 490), TROLLY_VELOCITY, 0)
    slingshot2 = Slingshot((750, 1090), TROLLY_VELOCITY, 1)


    # Initialize sprite groups
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    veggies = pygame.sprite.Group()
    bases = pygame.sprite.Group()
    slingshots = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    effects = pygame.sprite.Group()

    all_sprites.add([base1, base2, slingshot1, slingshot2])
    # Add player1 to players group
    players.add([player1])
    bases.add([base1, base2])                     # Add base1 to bases group
    slingshots.add([slingshot1, slingshot2])

    running_threads = threading.Event()
    running = True
    latest_frame = queue.Queue(maxsize=3)
    latest_frame_available = threading.Condition()
    angle_queue = queue.Queue(maxsize=10)

    camera_thread = threading.Thread(target=read_frames_from_camera, args=[
                                     running_threads, latest_frame_available, latest_frame])
    mediapipe_thread = threading.Thread(target=calculate_angle_using_mediapipe, args=[
                                        running_threads, latest_frame_available, latest_frame, angle_queue])
    image_processing_thread = threading.Thread(target=image_processing_thread_func, args=[
                                        running_threads, angle_queue])
    image_processor = ImageProcessor()

    if map_selected == SPRING:
        map_file = "assets/maps/summer_map.png"
    elif map_selected == FALL:
        map_file = "assets/maps/fall_map.png"
    elif map_selected == WINTER:
        map_file = "assets/maps/winter_map.png" 

    TUTORIALS_BG = pygame.image.load(map_file).convert_alpha()
    TUTORIALS_BG = pygame.transform.scale(TUTORIALS_BG, (2560, 1600))

    # audio_list = ["Eddie"]
    # recognizer, stop_listening = speech_rec(audio_list)
    #
    speech_recognizer = SpeechRecognizer()
    speech_recognizer.start()

    angle = 0

    veggies_list = Veggie.__subclasses__()
    for _ in range(MAX_VEGGIES):
        v_x = random.randint(0, SCREEN_WIDTH - VEGGIE_WIDTH)
        v_y = random.randint(VEGGIE_HEIGHT+team_boundaries[1]["top"], team_boundaries[1]["bottom"]-VEGGIE_HEIGHT)
        v_type = random.choice(veggies_list)
        veggie = v_type((v_x, v_y), (0, 0), 1)
        veggies.add(veggie)

    instruction_state = 3
    intro = True

    while running:
        try:
            TUTORIALS_MOUSE_POS = pygame.mouse.get_pos()
            SCREEN.blit(TUTORIALS_BG, (0, 0))
    
            objective_font = pygame.font.Font("assets/fonts/instruction.ttf", 50)
            objective = objective_font.render("MISSION POSSIBLE: Take down the opponent's base with Veggie Shots!", True, 'white')
            inventory_guide = objective_font.render("<- last column reveals your Next Veggie to launch and Total Veggies", True, 'white')
            pause_guide = objective_font.render("Press P on the keyboard to Pause", True, 'white')
            SCREEN.blit(objective, (500, 20))
            SCREEN.blit(inventory_guide, (400, 1500))
            SCREEN.blit(pause_guide, (800, 750))

            pressed_keys = pygame.key.get_pressed()   # Keyboard input
            if (player1.state != PLAYER_SHOOTING):
                if len(player1.inventory) < 1 and instruction_state != 0:
                    instructions = Instructions('Press A to Harvest a Veggie.\nInventory Limit: 5 Veggies\nVeggies in inventory: Weakest to Strongest')
                    instruction_state = 0
                elif len(player1.inventory) >= 1 and instruction_state != 1:
                    instructions = Instructions('Now Mount your Weapon!\nWalk to the Trolly on the rail, hold X, say Switch, release X')
                    instruction_state = 1

            # Audio Input
            # if audio_list[0] == "switch":
            #     print(".....................")
            #     audio_list[0] = "Eddie"
            #     player1.toggle_mount(slingshot1)
            if speech_recognizer.prediction == "switch":
                for slingshot in slingshots:
                    player1.toggle_mount(slingshot)

            for event in pygame.event.get():
                # Quit Game
                if event.type == pygame.QUIT:
                    raise ValueError
                # Mount Slingshot and Harvesting
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        paused = sub_menu()
                        if paused == "quit":
                            raise ValueError
                        elif paused == "main menu":
                            raise TypeError
                    if event.key == K_RETURN:
                        for slingshot in slingshots:
                            player1.toggle_mount(slingshot)
                    if event.key == K_SPACE:
                        player1.harvest(veggies)
                    if event.key == K_TAB:
                        if not Timer_on:
                            if isinstance(player1, Student):
                                tempEffect = GameObject((PLAYER_WIDTH*3, PLAYER_HEIGHT*3), player1.pos, player1.vel,
                                                        player1.team_num, img="assets/players/student-transform-effect.png", animation_steps=[5,5,5], scale=1)
                            elif isinstance(player1, Soldier):
                                tempEffect = GameObject((PLAYER_WIDTH*3, PLAYER_HEIGHT*3), player1.pos, player1.vel,
                                                        player1.team_num, img="assets/players/soldier-transform-effect.png", animation_steps=[5,5,5,5], scale=1)
                            elif isinstance(player1, Enchantress):
                                tempEffect = GameObject((PLAYER_WIDTH*3, PLAYER_HEIGHT*3), player1.pos, player1.vel,
                                                        player1.team_num, img="assets/players/enchantress-transform-effect.png", animation_steps=[5,5,5], scale=1)
                            elif isinstance(player1, Heroine):
                                tempEffect = GameObject((PLAYER_WIDTH*3, PLAYER_HEIGHT*3), player1.pos, player1.vel,
                                                        player1.team_num, img="assets/players/enchantress-transform-effect.png", animation_steps=[5,5,5], scale=1)
                            effects.add([tempEffect])
                            Timer_on = True
                            effect_start_time = pygame.time.get_ticks()
                            player1.promote()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(TUTORIALS_MOUSE_POS)
                # Attack
                elif event.type == pygame.JOYBUTTONDOWN:
                    if pygame.joystick.Joystick(0).get_button(0):
                        player1.attack(angle, (shots, all_sprites))
                    if pygame.joystick.Joystick(0).get_button(1):
                        harvested_veggie = pygame.sprite.spritecollideany(player1, veggies)
                        player1.harvest(veggies)
                        if harvested_veggie:
                            if harvested_veggie.__class__.__name__ == "Ruby":
                                base1.health += RUBY_POWER
                                print(base1.health)
                            elif harvested_veggie.__class__.__name__ == "Milk":
                                player1.vel_x += 1
                                player1.vel_y += 1
                            harvested_veggie.kill()

                    # if pygame.joystick.Joystick(0).get_button(3):
                    #     player1.toggle_mount(slingshot1)
                    if pygame.joystick.Joystick(0).get_button(3):
                        # recognizer.energy_threshold = 300
                        speech_recognizer.unmute()
                elif event.type == pygame.JOYBUTTONUP:
                    if not pygame.joystick.Joystick(0).get_button(3):
                        speech_recognizer.mute()


            if len(veggies) < MAX_VEGGIES:
                v_x = random.randint(VEGGIE_WIDTH, SCREEN_WIDTH - VEGGIE_WIDTH)
                v_y = random.randint(VEGGIE_HEIGHT+team_boundaries[1]["top"], team_boundaries[1]["bottom"]-VEGGIE_HEIGHT)
                v_type = random.choice(veggies_list)
                veggie = v_type((v_x, v_y), (0, 0), 1)
                veggies.add(veggie)

            if player1.state == PLAYER_SHOOTING:
                if instruction_state != 2 and len(player1.inventory) >= 1:
                    instructions = Instructions('Stay 3ft from the Camera.\nMake sure your nose and right wrist are visible.\nControl the shooting angle using your Right Hand(Wrist).\nPress B to fire.')
                    instruction_state = 2
                elif instruction_state != 3 and len(player1.inventory) < 1:
                    instructions = Instructions('Out of ammo.\nTo unmount the weapon:\nHold X.\nSay Switch.\nRelease X.')
                    instruction_state = 3
                if not is_shooting_music:
                    pygame.mixer.music.load('assets/music/not-afraid.mp3')
                    pygame.mixer.music.play(-1)
                    is_shooting_music = True
                image_processor.start()
                try:
                    # angle = angle_queue.get(block=False)
                    angle = image_processor.angle
                except:
                    pass

            if player1.state != PLAYER_SHOOTING:
                if is_shooting_music:
                    pygame.mixer.music.load('assets/music/on-a-clear-day.mp3')
                    pygame.mixer.music.play(-1)
                    is_shooting_music = False
                image_processor.stop()

            try:
                x_speed = -round(pygame.joystick.Joystick(0).get_axis(1))
                y_speed = round(pygame.joystick.Joystick(0).get_axis(0))
            except:
                x_speed = 0
                y_speed = 0

            for effect in effects:
                if effect_start_time != None:
                    if pygame.time.get_ticks() - effect_start_time < 2500:
                        effect.update(SCREEN, -1)
                    else:
                        Timer_on = False
                        player1.state = PLAYER_WALKING
                        effect.kill()
            # Refresh screen and display objects
            for veggie in veggies:
                veggie.update(SCREEN)
            for player in players:
                player.update([x_speed, y_speed], angle, SCREEN)
            for slingshot in slingshots:
                slingshot.update(SCREEN)
            for base in bases:
                base.update(shots, SCREEN)
            for shot in shots:
                shot.update(SCREEN)
            instructions.update(SCREEN)
            # objective.update(SCREEN)

            # show mask
            # for sprite in all_sprites:
            #     pygame.draw.rect(SCREEN, (255,255,255), sprite, 2)
            #     SCREEN.blit(sprite.mask.to_surface(sprite.surf, setcolor = (255,255,255)), sprite.rect)

            if base2.health == 0:
                if gameover() == "exit":
                    raise ValueError
                raise TypeError

            pygame.display.flip()
            clock.tick(100)

        except ValueError:
            for sprite in all_sprites:
                    sprite.kill()
            image_processor.stop()
            speech_recognizer.stop()
            pygame.quit()
        except TypeError:
            for sprite in all_sprites:
                    sprite.kill()
            image_processor.stop()
            speech_recognizer.stop()
            running = False

def gameover():
    background = pygame.image.load("assets/pause-phase/pause-background.png")
    dimmer = Dimmer(keepalive=True)
    running = True

    # Initialize buttons

    MAIN_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png").convert_alpha(), pos=(SCREEN_WIDTH/2, 650),
                              text_input="MAIN MENU", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

    EXIT_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png").convert_alpha(), pos=(SCREEN_WIDTH/2, 800),
                               text_input="EXIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

    # Button clicking sound effect
    clicking_sound = mixer.Sound('assets/music/button_clicked.mp3')
    clicking_sound.set_volume(1.5)

    while running:
        SCREEN.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        dimmer.dim(darken_factor=200, color_filter=(0, 0, 0))

        # Initialize main text box
        MENU_TEXT = get_font(150).render("You did It!", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 120))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # change color and play noise when hovering
        for button in [MAIN_BUTTON, EXIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.hoverNoise(MENU_MOUSE_POS)
            button.update(SCREEN)

        # event after clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    running = False
                if EXIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    running = False
                    return "exit"

        pygame.display.update()

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

def sub_menu():

    background = pygame.image.load("assets/pause-phase/pause-background.png")
    # dimmer = Dimmer(keepalive=True)
    running = True

    # Initialize buttons

    RESUME_BUTTON = Button(image=pygame.image.load("assets/pause-phase/pause-button-large.png").convert_alpha(), pos=(800, 600),
                             text_input="RESUME", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/pause-phase/pause-button-large.png").convert_alpha(), pos=(800, 800),
                            text_input="OPTIONS", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    MAIN_BUTTON = Button(image=pygame.image.load("assets/pause-phase/pause-button-large.png").convert_alpha(), pos=(800, 1000),
                              text_input="MAIN MENU", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    QUIT_BUTTON = Button(image=pygame.image.load("assets/pause-phase/pause-button-large.png").convert_alpha(), pos=(800, 1200),
                               text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

    # Button clicking sound effect
    clicking_sound = mixer.Sound('assets/music/button_clicked.mp3')
    clicking_sound.set_volume(1.5)

    while running:
        SCREEN.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        # dimmer.dim(darken_factor=200, color_filter=(0, 0, 0))

        # Initialize main text box
        MENU_TEXT = get_font(150).render("Paused", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, 120))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # change color and play noise when hovering
        for button in [RESUME_BUTTON, OPTIONS_BUTTON, MAIN_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.hoverNoise(MENU_MOUSE_POS)
            button.update(SCREEN)

        # event after clicking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    running = False
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    options()
                if MAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    running = False
                    return "main menu"
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    clicking_sound.play()
                    running = False
                    return "quit"
                    # pygame.quit()
                    # sys.exit()

        pygame.display.update()

def main_menu():

    background_5 = 0
    background_6 = 0

    # Initialize buttons
    PLAY_BUTTON = Button(image=pygame.image.load("assets/menu/Play Rect.png").convert_alpha(), pos=(700, 350),
                         text_input="PLAY", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
    OPTIONS_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png").convert_alpha(), pos=(700, 500),
                            text_input="OPTIONS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
    TUTORIALS_BUTTON = Button(image=pygame.image.load("assets/menu/Options Rect.png").convert_alpha(), pos=(700, 650),
                              text_input="TUTORIALS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
    QUIT_BUTTON = Button(image=pygame.image.load("assets/menu/Quit Rect.png").convert_alpha(), pos=(700, 800),
                         text_input="QUIT", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

    # Button clicking sound effect
    clicking_sound = mixer.Sound('assets/music/button_clicked.mp3')
    clicking_sound.set_volume(1.5)

    # Interactive character
    random_int = random.randint(1,3)
    sprite_scale = 5
    frame_col = 0
    animation_cooldown = 70
    character_surf = pygame.Surface((PLAYER_WIDTH*sprite_scale, PLAYER_HEIGHT*sprite_scale))
    character_rect = character_surf.get_rect()
    character_rect.center = (200, 1250) # initial position

    # Set up the jump
    jump_height = 3
    is_jumping = False
    jump_count = 0
    jump_speed = 40


    if random_int == 1:
        sprite_image = pygame.image.load("assets/players/student.png").convert_alpha()
    elif random_int == 2:
        sprite_image = pygame.image.load("assets/players/soldier.png").convert_alpha()
    elif random_int == 3:
        sprite_image = pygame.image.load("assets/players/enchantress.png").convert_alpha()

    animation_list = SpriteSheet(sprite_image).get_animation_list([3, 3, 3, 3], (PLAYER_WIDTH,PLAYER_HEIGHT), sprite_scale)
    mask = pygame.mask.from_surface(animation_list[2][frame_col])
    last_update = pygame.time.get_ticks()

    while True:
        SCREEN.blit(STATIC_BACKGROUND, (0, 0))
        SCREEN.blit(BG_5, (background_5, 0))
        SCREEN.blit(BG_6, (background_6, 0))
        background_5 -= 5
        background_6 -= 30
        if background_5 <= -BG_5.get_width():
            background_5 = 0
        if background_6 <= -BG_6.get_width():
            background_6 = 0

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
            elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if not is_jumping:
                            jump_start = pygame.time.get_ticks()
                            is_jumping = True
                            jump_count = 0

         # Update moving character

        if is_jumping:
            character_rect.centery -= jump_speed*2
            jump_count += 1
            if jump_count >= jump_height:
                is_jumping = False
        else:
            if jump_count > 0:
                character_rect.centery += jump_speed*2
                jump_count -= 1


        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame_col += 1
            last_update = current_time
            if frame_col >= len(animation_list[2]):
                frame_col = 0
        SCREEN.blit(animation_list[2][frame_col], character_rect)
        mask = pygame.mask.from_surface(animation_list[2][frame_col])



        pygame.display.update()

        clock.tick(120)

def introduction():

    logo = pygame.image.load("assets/menu/puzzle.png").convert_alpha()
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((0, 0, 0))

    logo_sound = mixer.Sound('assets/music/logo_sound.mp3')
    logo_sound.set_volume(1.5)

    fade_in_duration = 3000  # in milliseconds
    fade_out_duration = 3000  # in milliseconds

    logo_alpha_start = 0
    logo_alpha_end = 255
    label_alpha_start = 0
    label_alpha_end = 255

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()


    # progress bar
    loadingbar_animation = Animation((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), pygame.image.load("assets/menu/progress_bar.png")
                                     ,[8], (480, 320), 1, animation_cooldown=500)
    
    stop_flag = False
    logo_sound.play()

    while not stop_flag:

        SCREEN.fill((0,0,0))
        elapsed_time = pygame.time.get_ticks() - start_time

        if elapsed_time < fade_in_duration:
            logo_alpha = logo_alpha_start + int((logo_alpha_end - logo_alpha_start) * elapsed_time / fade_in_duration)
            label_alpha = label_alpha_start + int((label_alpha_end - label_alpha_start) * elapsed_time / fade_in_duration)
        elif elapsed_time < (fade_in_duration + fade_out_duration):
            logo_alpha = logo_alpha_end - int((logo_alpha_end - logo_alpha_start) * (elapsed_time - fade_in_duration) / fade_out_duration)
            label_alpha = label_alpha_end - int((label_alpha_end - label_alpha_start) * (elapsed_time - fade_in_duration) / fade_out_duration)
        else:
            [stop_flag, pause_flag] = loadingbar_animation.update_norepeat(SCREEN, 2000)

        logo_copy = logo.copy()
        logo_copy.set_alpha(logo_alpha)
        SCREEN.blit(logo_copy, (SCREEN_WIDTH // 2 - logo_copy.get_width() // 2, SCREEN_HEIGHT // 2 - logo_copy.get_height() // 2))

        label = pygame.font.Font("assets/fonts/introduction_font.ttf", 40).render("Veggie Wars Gaming", True, (255, 255, 255))
        label.set_alpha(label_alpha)
        label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + logo.get_height() // 2 + 20))
        SCREEN.blit(label, label_rect)

        # pygame.event.pump()
        pygame.display.update()

        clock.tick(120)
        
    main_menu()

introduction()
