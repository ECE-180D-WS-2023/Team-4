import pygame, sys
from button import Button
from Player import Player
from Veggie import Veggie
from Base import Base
from Slingshot import Slingshot
from constants import *
import time

pygame.init()          # Start game

# Joystick configuration
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)


# https://stackoverflow.com/questions/73758038/pygame-wrong-resolution-on-macos
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

pygame.display.set_caption("Veggie Wars")

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
harvestables = pygame.sprite.Group()
bases = pygame.sprite.Group()
shots = pygame.sprite.Group()

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def redraw_screen(screen):
    for sprite in players:
        screen.blit(sprite.surf, sprite.rect)
    for sprite in harvestables:
        screen.blit(sprite.surf, sprite.rect)
    for sprite in bases:
        screen.blit(sprite.surf, sprite.rect)

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
    player1 = Player((30, 40), (2, 2), 1, PLAYER_ENGINEER, "Bruce", PLAYER_WALKING, 10)
    veggie1 = Veggie((420, 270), (0, 0), 3, "carrot", 10)
    base1 = Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(3/4)), (3, 3), 1, 10, 10)
    base2 = Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(1/4)), (3, 3), 2, 20, 10)
    slingshot1 = Slingshot((500, 500), (0, 0), 1)


    all_sprites.add([veggie1, base1, base2, slingshot1])
    players.add([player1])                        # Add player1 to players group
    harvestables.add([veggie1])                   # Add veggie1 to harvestable group
    bases.add([base1, base2])                            # Add base1 to bases group

    running = True
    TUTORIALS_BG = pygame.image.load("assets/grass.png")
    while running:
        TUTORIALS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(TUTORIALS_BG, (0, 0))


        pressed_keys = pygame.key.get_pressed()   # Keyboard input
        

        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mount Slingshot
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    player1.toggle_mount(slingshot1)
            # Attack
            elif event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0):
                    if player1.attack("carrot"):
                        temp_veggie = Veggie(player1.position, (0, 0.5), 1, "carrot", 10)
                        all_sprites.add([temp_veggie])
                        shots.add([temp_veggie])
            
        # Joystick reading
        if player1.player_state == PLAYER_WALKING:
            x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
            y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
        elif player1.player_state == PLAYER_SHOOTING:
            x_speed += round(pygame.joystick.Joystick(0).get_axis(0))
            y_speed = 0

        # player.display_backpack(pressed_keys)    # display backpack
        player1.switch_state(pressed_keys)         # switch player states

        # Refresh screen and display objects
        redraw_screen(SCREEN)
        player1.update([x_speed, y_speed], SCREEN)         # moving players
        for sprite in all_sprites:
            sprite.update(SCREEN)
        

        if pygame.sprite.spritecollideany(player1, harvestables):
            # the harvestable glows and it takes time to harvest that veggie
            # veggie is destroyed after harvested
            if player1.player_state != PLAYER_HARVESTING:
                pass
            else:
                # has to be right on top of the veggie
                player1.harvest(veggie1.m_type)
                veggie1.kill()
                

        if pygame.sprite.collide_rect(player1, base2):
            # if the base has health
                # if the base is immune
                    # record time and pass
                # else
                    # take damage and reset immune time
            if base2.immune_time <= 0:
                base2.immune_time = pygame.time.get_ticks()
                pass
            elif base2.health > 0:
                hit_time = pygame.time.get_ticks()
                damage = 10
                base2.health = base2.health - damage
                print("current base health: ", base2.health)

            else:
                base2.kill()
                running = False
        
        pygame.display.flip()

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

