import pygame
from collections import defaultdict
from .scene import *
from ..constants import *
from ..spritesheet import *
from ..integrations.speech_recognition import *
from ..integrations.image_processing import *
from ..network import *

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("assets/grass.png").convert_alpha()
        self.state = {}
        self.inputs = {}
        self.speech_recognizer = SpeechRecognizer()
        self.image_processor = ImageProcessor()
        self.spritesheets = {
            # Players
            "Engineer": SpriteSheet("assets/players/engineer.png").get_animation_list((PLAYER_WIDTH, PLAYER_HEIGHT), PLAYER_SCALE, [3,3,3,3]),
            "Soldier": SpriteSheet("assets/players/soldier.png").get_animation_list((PLAYER_WIDTH, PLAYER_HEIGHT), PLAYER_SCALE, [3,3,3,3]),
            # Weapons
            "Cannon": SpriteSheet("assets/weapons/cannon.png").get_animation_list((67, 150), 1),
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

    def startup(self, globals):
        super().startup(globals)
        self.speech_recognizer.start()
        # self.server_process = multiprocessing.Process(target=server.run, args=(globals["address"],))
        # self.server_process.start()
        while True:
            try:
                self.client = ClientSocket(globals["address"])
                break
            except:
                ...

    def cleanup(self):
        self.speech_recognizer.stop()
        self.image_processor.stop()

    def handle_event(self, event):
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

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for group in self.state.values():
            for team in group:
                if isinstance(team, dict):
                    team = list(team.values())
                for object in team:
                    object.draw(self.spritesheets, screen)

    def update(self):
        try:
            # NOTE: this finds the team number manually (not extensible)
            if self.state["players"][self.client.id % 2][self.client.id].state == PLAYER_SHOOTING:
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
        self.client.send(self.inputs)
        self.state = self.client.receive()
        self.inputs = defaultdict(list)
