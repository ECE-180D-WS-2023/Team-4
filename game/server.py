import threading
import pygame
from constants import *
from Player import *
from network import *

# Initialize socket
PORT = 8080
SERVER = '192.168.0.190'
server = ServerSocket(SERVER, PORT)

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

game_state = {"players": {}}

def client_thread(conn, id):
    # Send client id
    conn.send(id)

    # Initialize player
    game_state["players"][str(id)] = {"pos": (80, 80)}

    while True:
        client_inputs = conn.receive()

        # Movement
        js_input = client_inputs.get("js", (0, 0))
        x = game_state["players"][str(id)]["pos"][0] + js_input[0]*5
        y = game_state["players"][str(id)]["pos"][1] + js_input[1]*5
        game_state["players"][str(id)]["pos"] = (x, y)

        conn.send(game_state)

        clock.tick(60)

    conn.close()

def main():
    id = 0
    running = True
    while running:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_thread, args=(conn, id))
        thread.start()
        id += 1
        print(f"[NEW CONNECTION #{threading.active_count() - 1}] {addr} connected")

if __name__ == "__main__":
    main()
