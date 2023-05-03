import pygame
import threading
from constants import *
from network import *
from player import *
from veggie import *

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
}

def handle_client(conn, id):
    # Send client id
    conn.send(id)

    # Initialize player
    game_state["players"][str(id)] = Player((80, 80))
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
                game_state["shots"].append(Veggie(my_player.pos, 10, (1, 1)))

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
