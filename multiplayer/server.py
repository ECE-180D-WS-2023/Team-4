import pygame
import threading
from constants import *
from network import *
from player import *
from veggie import *
from slingshot import *
from weapon import *

# Initialize socket
PORT = 8080
SERVER = '172.20.10.2'
server = ServerSocket(SERVER, PORT)

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

game_state = {
    "players": {},
    "veggies": [],
    "shots": [],
    "slingshots": [
        Slingshot((SCREEN_WIDTH/2, SCREEN_HEIGHT*(1/4))),
        Slingshot((SCREEN_WIDTH/2, SCREEN_HEIGHT*(3/4))),
    ],
}

def handle_client(conn, id):
    # Send client id
    conn.send(id)

    # Initialize player
    game_state["players"][str(id)] = Player((80, 80), team_num=(id % 2))
    my_player = game_state["players"][str(id)]

    while True:
        client_inputs = conn.receive()

        # Joystick dpad
        js_axis = client_inputs.get("js_axis", (0, 0))
        my_player.direction.x = js_axis[0]
        my_player.direction.y = js_axis[1]

        # Joystick buttons
        js_buttondown = client_inputs.get("js_buttondown", False)
        if js_buttondown:
            if 0 in js_buttondown:
                if my_player.state == PLAYER_SHOOTING:
                    game_state["shots"].append(my_player.shoot())

        # Keyboard
        keyboard = client_inputs.get("keyboard", [])
        if K_RETURN in keyboard:
            ...

        # Speech recognition
        speech = client_inputs.get("speech", None)
        if speech == "switch":
            print("switch")
            my_player.toggle_mount(game_state["slingshots"][my_player.team_num])

        # Image Processing
        angle = client_inputs.get("angle", None)
        if my_player.state == PLAYER_SHOOTING:
            # my_player.weapon.angle = angle
            if angle != None:
                if my_player.team_num == 0:
                    my_player.weapon.angle = -angle + 180
                else:
                    my_player.weapon.angle = angle

        for player in game_state["players"].values():
            player.update()
        for veggie in game_state["veggies"]:
            veggie.update()
        for shot in game_state["shots"]:
            shot.update()

        conn.send(game_state)
        clock.tick(60)

    conn.close()

def main():
    id = 0
    running = True
    while running:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, id))
        thread.start()
        id += 1
        print(f"[NEW CONNECTION #{threading.active_count() - 1}] {addr} connected")

if __name__ == "__main__":
    main()
