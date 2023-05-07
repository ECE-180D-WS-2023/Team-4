import pygame
import threading
from constants import *
from game import *
from network import *
from player import *
from veggie import *

# Initialize socket
PORT = 8080
SERVER = '192.168.0.190'
client = ClientSocket(SERVER, PORT)

# Initialize pygame
pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

game = Game(client.id)

def handle_server():
    while game.running:
        client.send(game.inputs)
        game.state = client.receive()

def main():
    thread = threading.Thread(target=handle_server)
    thread.start()
    while game.running:
        game.handle_inputs()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
  main()
