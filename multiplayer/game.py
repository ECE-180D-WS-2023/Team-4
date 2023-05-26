import pygame
from collections import defaultdict
from utils import *
from constants import *
from spritesheet import *
from integrations.speech_recognition import *
from integrations.image_processing import *

class Game:
    def __init__(self, client_id):
        self.client_id = client_id
        self.state = {}
        self.inputs = {}
        self.running = True
        self.show_backpack = False
        self.background = pygame.image.load("assets/grass.png")
        self.spritesheets = {
            # Players
            "Engineer": SpriteSheet("assets/players/engineer.png").get_animation_list((PLAYER_WIDTH, PLAYER_HEIGHT), PLAYER_SCALE, [3,3,3,3]),
            "Soldier": SpriteSheet("assets/players/soldier.png").get_animation_list((PLAYER_WIDTH, PLAYER_HEIGHT), PLAYER_SCALE, [3,3,3,3]),
            # Weapons
            "Cannon": SpriteSheet("assets/players/cannon.png").get_animation_list((67, 150), 1),
            # Veggies
            "Carrot": SpriteSheet("assets/veggies/carrot-big.png").get_animation_list((VEGGIE_WIDTH, VEGGIE_HEIGHT), VEGGIE_SCALE),
            "Mushroom": SpriteSheet("assets/veggies/mushroom.png").get_animation_list((VEGGIE_WIDTH, VEGGIE_HEIGHT), VEGGIE_SCALE),
            "Cabbage": SpriteSheet("assets/veggies/cabbage.png").get_animation_list((VEGGIE_WIDTH, VEGGIE_HEIGHT), VEGGIE_SCALE),
            "Potato": SpriteSheet("assets/veggies/potato.png").get_animation_list((VEGGIE_WIDTH, VEGGIE_HEIGHT), VEGGIE_SCALE),
            "YellowBellPepper": SpriteSheet("assets/veggies/yellow-bell-pepper.png").get_animation_list((VEGGIE_WIDTH, VEGGIE_HEIGHT), VEGGIE_SCALE),
            # Slingshots
            "Slingshot": SpriteSheet("assets/slingshot_station.png").get_animation_list((SLINGSHOT_WIDTH, SLINGSHOT_HEIGHT), SLINGSHOT_SCALE),
            # Bases
            "Base": SpriteSheet("assets/base2.png").get_animation_list((BASE_HEIGHT, BASE_HEIGHT), BASE_SCALE),
        }
        self.speech_recognizer = SpeechRecognizer()
        self.speech_recognizer.start()
        self.image_processor = ImageProcessor()

    def handle_inputs(self):
        self.inputs = defaultdict(list)
        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.inputs["keyboard"].append(event.key)
            elif event.type == pygame.JOYBUTTONDOWN:
                if pygame.joystick.Joystick(0).get_button(0):
                    self.inputs["js_buttondown"].append(0)
                if pygame.joystick.Joystick(0).get_button(1):
                    self.inputs["js_buttondown"].append(1)
                if pygame.joystick.Joystick(0).get_button(3):
                    self.speech_recognizer.unmute()
                    print("unmute")
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 3:
                    self.speech_recognizer.mute()
                    print("mute")

        try:
            # NOTE: this finds the team number manually (not extensible)
            if self.state["players"][self.client_id % 2][self.client_id].state == PLAYER_SHOOTING:
                self.image_processor.start()
                self.inputs["angle"] = self.image_processor.angle
            else:
                self.image_processor.stop()
        except Exception as e:
            print("[IMAGE INPUT]:", e)

        speech_prediction = self.speech_recognizer.prediction
        if speech_prediction != None:
            print("[SPEECH]:", speech_prediction)
            self.inputs["speech"] = speech_prediction

        x = round(pygame.joystick.Joystick(0).get_axis(0))
        y = round(pygame.joystick.Joystick(0).get_axis(1))
        self.inputs["js_axis"] = (x, y)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for group in self.state.values():
            for team in group:
                if isinstance(team, dict):
                    team = list(team.values())
                for object in team:
                    object.draw(self.spritesheets, screen)

        # try:
        #     for player in self.state["players"].values():
        #         screen.blit(self.spritesheets[player.__class__.__name__].get_image(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SCALE), player.rect)
        #         if player.weapon:
        #             blitRotate(screen, self.spritesheets[player.weapon.__class__.__name__].get_image(0, 0, 67, 150), player.weapon.rect.center, (34,170), player.weapon.angle)
        #     for veggies in self.state["veggies"].values():
        #         for veggie in veggies:
        #             screen.blit(self.spritesheets[veggie.__class__.__name__].get_image(0, 0, VEGGIE_WIDTH, VEGGIE_HEIGHT, VEGGIE_SCALE), veggie.rect)
        #     for shot in self.state["shots"]:
        #         screen.blit(self.spritesheets[shot.__class__.__name__].get_image(0, 0, SHOT_WIDTH, SHOT_HEIGHT, SHOT_SCALE), shot.rect)
        #     for slingshot in self.state["slingshots"]:
        #         screen.blit(self.spritesheets[slingshot.__class__.__name__].get_image(0, 0, VEGGIE_WIDTH, VEGGIE_HEIGHT, 1), slingshot.rect)
        # except Exception as e:
        #     print("[DRAW]:", e)
