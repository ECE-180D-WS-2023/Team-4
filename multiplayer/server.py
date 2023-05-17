import pygame
import random
import threading
import time
from constants import *
from network import *
from player import *
from veggie import *
from slingshot import *
from weapon import *

# Initialize socket
PORT = 8080
SERVER = '192.168.0.190'
server = ServerSocket(SERVER, PORT)

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

game_state = {
    "players": {},
    "veggies": {
        0: [],  # team 0
        1: [],  # team 1
    },
    "shots": [],
    "slingshots": [
        Slingshot((SCREEN_WIDTH/2, SCREEN_HEIGHT*(1/4))),
        Slingshot((SCREEN_WIDTH/2, SCREEN_HEIGHT*(3/4))),
    ],
}

def run_game():
    team_boundaries = {
        0: {
            "top": 0,
            "bottom": SCREEN_HEIGHT / 2
        },
        1: {
            "top": SCREEN_HEIGHT / 2,
            "bottom": SCREEN_HEIGHT
        }
    }
    spawn_times = {
        0: [],
        1: []
    }
    veggies_list = Veggie.__subclasses__()
    while True:
        for team, veggies in game_state["veggies"].items():
            # Add new spawn time for veggies
            if len(spawn_times[team]) < MAX_VEGGIES - len(veggies):
                spawn_times[team].append(time.time() + random.uniform(1, 4))
            # Add new veggies if past their spawn time
            for spawn_time in list(spawn_times[team]):
                if time.time() > spawn_time:
                    v_x = random.randint(0, SCREEN_WIDTH - VEGGIE_WIDTH)
                    v_y = random.randint(team_boundaries[team]["top"], team_boundaries[team]["bottom"])
                    v_type = random.choice(veggies_list)
                    game_state["veggies"][team].append(v_type((v_x, v_y)))
                    spawn_times[team].remove(spawn_time)

        clock.tick(20)

def handle_client(conn, id):
    # Send client id
    conn.send(id)

    # Initialize player
    my_team_num = id % 2
    game_state["players"][str(id)] = Engineer(TEAM0_SPAWN if my_team_num == 0 else TEAM1_SPAWN, team_num=my_team_num)
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
                my_player.shoot(game_state["shots"])
            elif 1 in js_buttondown:
                my_player.harvest(game_state["veggies"][my_player.team_num])

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
        for veggies in game_state["veggies"].values():
            for veggie in veggies:
                veggie.update()
        for shot in game_state["shots"]:
            shot.update()

        conn.send(game_state)
        clock.tick(60)

    conn.close()

def main():
    game_logic_thread = threading.Thread(target=run_game)
    game_logic_thread.start()

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
