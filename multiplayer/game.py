import pygame
from constants import *
from spritesheet import *

class Game:
    def __init__(self):
        self.state = {}
        self.inputs = {}
        self.running = True
        self.show_backpack = False
        self.background = pygame.image.load("assets/grass.png")
        self.spritesheets = {
            "Player": SpriteSheet("assets/players/engineer.png"),
            "Engineer": SpriteSheet("assets/players/engineer.png"),
            "Soldier": SpriteSheet("assets/players/soldier.png"),
            "Veggie": SpriteSheet("assets/veggies/carrot-big.png"),
            "Slingshot": SpriteSheet("assets/veggies/cabbage.png"),
        }

    def handle_inputs(self):
        self.inputs = {}
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                pygame.quit()
            # Mount Slingshot and Harvesting
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ...
                if event.key == pygame.K_SPACE:
                    ...
                # Attack
            elif event.type == pygame.JOYBUTTONDOWN:
                self.inputs["js_buttondown"] = []
                if pygame.joystick.Joystick(0).get_button(0):
                    self.inputs["js_buttondown"].append(0)
                if pygame.joystick.Joystick(0).get_button(1):
                    self.inputs["js_buttondown"].append(1)
                if pygame.joystick.Joystick(0).get_button(3):
                    self.inputs["js_buttondown"].append(3)

        x = round(pygame.joystick.Joystick(0).get_axis(0))
        y = round(pygame.joystick.Joystick(0).get_axis(1))
        self.inputs["js_axis"] = (x, y)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        try:
            for player in self.state["players"].values():
                screen.blit(self.spritesheets[player.__class__.__name__].get_image(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 2), player.rect)
            for veggie in self.state["veggies"]:
                screen.blit(self.spritesheets[veggie.__class__.__name__].get_image(0, 0, VEGGIE_WIDTH, VEGGIE_HEIGHT, 1), veggie.rect)
            for shot in self.state["shots"]:
                screen.blit(self.spritesheets[shot.__class__.__name__].get_image(0, 0, 32, 32, 2), shot.rect)
            for slingshot in self.state["slingshots"]:
                screen.blit(self.spritesheets[slingshot.__class__.__name__].get_image(0, 0, VEGGIE_WIDTH, VEGGIE_HEIGHT, 1), slingshot.rect)
        except Exception as e:
            print(e)
