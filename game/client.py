import pygame
# from constants import *
from Player import *
from network import *

# Initialize socket
PORT = 8080
SERVER = '192.168.0.190'
client = ClientSocket(SERVER, PORT)

# Initialize pygame
pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
clock = pygame.time.Clock()
TUTORIALS_BG = pygame.image.load("assets/grass.png")
SCREEN = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

def main():
    running = True
    player1 = Engineer((80, 80), (2.5, 2.5), 1, PLAYER_ENGINEER, "Bruce", PLAYER_WALKING, 10)
    inputs = {}

    while running:
        SCREEN.blit(TUTORIALS_BG, (0, 0))

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
                if pygame.joystick.Joystick(0).get_button(0):
                    ...
                if pygame.joystick.Joystick(0).get_button(1):
                    ...
                if pygame.joystick.Joystick(0).get_button(3):
                    ...

        x = round(pygame.joystick.Joystick(0).get_axis(0))
        y = round(pygame.joystick.Joystick(0).get_axis(1))
        inputs["js"] = (x, y)

        client.send(inputs)
        state = client.receive()

        player1.pos = state["players"][str(client.id)]["pos"]
        player1.update([0, 0], 0, SCREEN)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
  main()
