import pygame
import random
import threading
import time
from game.constants import *
from game.network import *
from game.gameobjects.player import *
from game.gameobjects.veggie import *
from game.gameobjects.slingshot import *
from game.gameobjects.base import *
from game.gameobjects.weapon import *

def game_thread(game_state):
    clock = pygame.time.Clock()

    # team_boundaries = {
    #     0: {
    #         "top": 0,
    #         "bottom": SCREEN_HEIGHT / 2
    #     },
    #     1: {
    #         "top": SCREEN_HEIGHT / 2,
    #         "bottom": SCREEN_HEIGHT
    #     }
    # }
    spawn_times = {
        0: [],
        1: []
    }
    veggies_list = Veggie.__subclasses__()
    while True:
        for team, veggies in enumerate(game_state["veggies"]):
            # Add new spawn time for veggies
            if len(spawn_times[team]) < MAX_VEGGIES - len(veggies):
                spawn_times[team].append(time.time() + random.uniform(1, 4))
            # Add new veggies if past their spawn time
            for spawn_time in list(spawn_times[team]):
                if time.time() > spawn_time:
                    v_x = random.randint(0, SCREEN_WIDTH)
                    v_y = random.randint(TEAM_BOUNDARIES[team]["top"], TEAM_BOUNDARIES[team]["bottom"])
                    v_type = random.choice(veggies_list)
                    game_state["veggies"][team].append(v_type((v_x, v_y), animate=True))
                    spawn_times[team].remove(spawn_time)

        clock.tick(20)

def client_thread(conn, id, game_state):
    clock = pygame.time.Clock()

    # Send client id
    conn.send(id)

    # Receive initial message
    init = conn.receive()

    # Initialize player
    my_team_num = (id + 1) % 2
    game_state["players"][my_team_num][id] = init["player_class"](TEAM0_SPAWN if my_team_num == 0 else TEAM1_SPAWN, team_num = my_team_num, weapon_class=init["weapon_class"])
    my_player = game_state["players"][my_team_num][id]

    while True:
        client_inputs = conn.receive()

        # Handle disconnect
        if not client_inputs:
            print(f"Client {id} disconnected")
            game_state["players"][my_team_num].remove(my_player)
            break

        # Joystick dpad
        js_axis = client_inputs.get("js_axis", (0, 0))
        my_player.direction.x = js_axis[0]
        my_player.direction.y = js_axis[1]

        # Joystick buttons
        js_buttondown = client_inputs.get("js_buttondown", False)
        if js_buttondown:
            if 0 in js_buttondown:
                my_player.shoot(game_state["shots"][my_team_num])
            elif 1 in js_buttondown:
                my_player.harvest(game_state["veggies"][my_team_num])

        # Keyboard
        keyboard = client_inputs.get("keyboard", [])
        if K_RETURN in keyboard:
            ...

        # Speech recognition
        speech = client_inputs.get("speech", None)
        if speech == "switch":
            print("switch")
            my_player.toggle_mount(game_state["slingshots"][my_team_num][0])

        # Image Processing
        angle = client_inputs.get("angle", None)
        if my_player.state == PLAYER_SHOOTING:
            # my_player.weapon.angle = angle
            if angle != None:
                if my_player.team_num == 0:
                    my_player.weapon.angle = -angle + 180
                else:
                    my_player.weapon.angle = angle

        # Update positions
        for group in game_state.values():
            for team_num, team_objects in enumerate(group):
                # Update objects
                team_objects_list = team_objects
                if isinstance(team_objects, dict):
                    team_objects_list = list(team_objects.values())
                for object in team_objects_list:
                    object.update()
                # Remove any dead objects
                if isinstance(team_objects, dict):
                    group[team_num] = {key: obj for key, obj in group[team_num].items() if getattr(obj, "kill", False) == False}
                else:
                    group[team_num] = [obj for obj in group[team_num] if getattr(obj, "kill", False) == False]

        # Check for hits
        for shot in game_state["shots"][my_team_num]:
            shot.check_collision(game_state["bases"][(my_team_num + 1) % 2])

        if len(game_state["bases"][0]) == 0:
            print("Team 1 Won")
            game_state = "game_over"
            conn.send(game_state)
            break
        elif len(game_state["bases"][1]) == 0:
            print("Team 0 Won")
            game_state = "game_over"
            conn.send(game_state)
            break

        conn.send(game_state)

        # Reset actions to avoid client constantly playing sounds
        # TODO: do this somewhere else; alter logic to play sounds
        my_player.actions = []

        clock.tick(60)

    # conn.close()

def run(address="192.168.0.190", port=8080):
    pygame.init()

    # Initialize socket
    server = ServerSocket(address, port)

    # Initialize game state
    game_state = {
        "players": [
            # dictionaries allow clients to quickly identify which player is theirs
            {}, # team 0
            {}, # team 1
        ],
        "veggies": [
            [],  # team 0
            [],  # team 1
        ],
        "shots": [
            [], # team 0
            [], # team 1
        ],
        "slingshots": [
            [Trolley((1590, 492))],
            [Trolley((962, 1088))],
        ],
        "bases": [
            [Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(1/8)))],
            [Base((SCREEN_WIDTH/2, SCREEN_HEIGHT*(7/8)))],
        ],
    }

    # Start game
    game_logic_thread = threading.Thread(target=game_thread, args=(game_state,))
    game_logic_thread.start()

    # Handle client connections
    id = 0
    running = True
    while running:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_thread, args=(conn, id, game_state))
        thread.start()
        id += 1
        print(f"[CLIENT CONNECTED: ID=#{threading.active_count() - 1}], ADDR={addr}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run()
