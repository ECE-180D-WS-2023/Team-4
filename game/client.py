import socket
import json
import pygame
from constants import *
from Player import *

HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
TUTORIALS_BG = pygame.image.load("assets/grass.png")

# Initialize client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# Initialize pygame
pygame.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)


players = pygame.sprite.Group()

def send(msg):
    json_message = json.dumps(msg)
    message = json_message.encode(FORMAT)
    # msg_length = len(message)
    # send_length = str(msg_length).encode(FORMAT)
    # send_length += b' ' * (HEADER - len(send_length))
    # client.send(send_length)
    client.send(message)

def receive():
    # Receive data from the server
    # response_length = client.recv(HEADER).decode(FORMAT)
    # if response_length:
    #     response_length = int(response_length)
    response = client.recv(HEADER).decode(FORMAT)
    return json.loads(response)

def main():
    running = True
    player1 = Engineer((80, 80), (2.5, 2.5), 1, PLAYER_ENGINEER, "Bruce", PLAYER_WALKING, 10)
    data_package = {"DISCONNECT":0, "player1_pos": player1.pos, "player1_vel": player1.vel}

    send(data_package)
    players.add([player1])

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

        if y == -1:     # Up
            data_package["js"] = "up"
        elif y == 1:      # Down
            data_package["js"] = "down"
        elif x == -1:     # Left
            data_package["js"] = "left"
        elif x == 1:      # Right
            data_package["js"] = "right"
        else:
            data_package["js"] = None


        send(data_package)
        data_package = receive()

        # print(data_package["player1_pos"])
        

        # for player in players:
        #     player.update([0, 0], 0, SCREEN)
        player1.pos = data_package["player1_pos"]
        player1.update([0, 0], 0, SCREEN)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
  main()