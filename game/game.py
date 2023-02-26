import pygame, sys
from button import Button
from Player import Player
from Veggie import Veggie
from Base import Base
from Constants import *
import time

pygame.init()          # Start game

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Veggie Wars")

# Initialize sprite groups
players = pygame.sprite.Group()
harvestables = pygame.sprite.Group()
bases = pygame.sprite.Group()

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def redraw_screen(screen):
    screen.fill((0, 0, 0))
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
    # Initialize player
    player1_dict = {"pos_x": 30, "pos_y": 40, "vel_x":2, "vel_y":2, "health":10,
                    "team_num":1, "name":"Bruce", "role": PLAYER_ENGINEER, "state":PLAYER_WALKING}
    player1 = Player(**player1_dict)

    # Initialize veggie
    veggie1_dict = {"pos_x": 420, "pos_y": 270, "vel_x":3, "vel_y":3, "health":10,
                    "team_num":3, "veggie_type": "cabbage"}
    veggie1 = Veggie(**veggie1_dict)              

    # Initialize base 1
    base1_dict = {"pos_x": 420, "pos_y": 680, "vel_x":3, "vel_y":3, "health":10,
                  "team_num":1, "shield":10}
    base1 = Base(**base1_dict)

    # Initialize base 2
    base2_dict = {"pos_x": 420, "pos_y": 50, "vel_x":3, "vel_y":3, "health":20,
                  "team_num":2, "shield":10}
    base2 = Base(**base2_dict)


    players.add([player1])                        # Add player1 to players group
    harvestables.add([veggie1])                   # Add veggie1 to harvestable group
    bases.add([base1, base2])                            # Add base1 to bases group

    running = True
    while running:
        TUTORIALS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")
        

        pressed_keys = pygame.key.get_pressed()   # Keyboard input
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player1.move(pressed_keys)                 # moving players
        # player.display_backpack(pressed_keys)    # display backpack
        player1.switch_state(pressed_keys)         # switch player states

        # Refresh screen
        redraw_screen(SCREEN)

        if pygame.sprite.collide_circle(player1, veggie1):
            # the harvestable glows and it takes time to harvest that veggie
            # veggie is destroyed after harvested
            if player1.player_state != PLAYER_HARVESTING:
                pass
            else:
                # has to be right on top of the veggie
                veggie1.kill()
                running = False
            
            # player.backpack + 1
        
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
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 230), 
                            text_input="PLAY", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 380), 
                            text_input="OPTIONS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        TUTORIALS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 530),
                            text_input="TUTORIALS", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 650), 
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

