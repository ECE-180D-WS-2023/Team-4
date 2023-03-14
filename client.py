import paho.mqtt.client as mqtt
import numpy as np
import json
import pygame
from game import *

# TODO: Refactor to work with more players
# TODO: Check if player of the same number already exists
# Get player metadata from user
while True:
    player_number = input("Enter player number (1|2): ")
    if player_number in ["1", "2"]:
        print("")
        break

subscribe_topic = f"/rps/srv/player{player_number}"
publish_topic = f"/rps/player{player_number}/srv"

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

    client.subscribe(subscribe_topic, qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    # TODO: Refactor to work with list of sprites
    # remote_sprite = json.loads(message.payload)
    # remote_sprites.add(remote_sprite)
    # all_sprites.add(remote_sprite)
    # print(json.loads(message.payload))
    pos = json.loads(message.payload)["pos"]
    other_player.set_position(pos[0], pos[1])

def create_client():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


    client.connect_async('mqtt.eclipseprojects.io')
    # client.connect_async("192.168.8.20")
    # client.connect_async("localhost")
    client.loop_start()

    return client

client = create_client()



pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
other_player = Player()
# slingshot = Slingshot()

local_sprites = pygame.sprite.Group()
remote_sprites = pygame.sprite.Group()
local_sprites.add(player)
remote_sprites.add(other_player)
all_sprites.add(player)
all_sprites.add(other_player)
# all_sprites.add([player, slingshot])
# shots = pygame.sprite.Group()

running = True
while running:
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_q] or pressed_keys[K_ESCAPE]:
        running = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # elif event.type == KEYDOWN:
        #     if event.key == K_RETURN:
        #         if player.mounted:
        #             player.mounted = False
        #         elif pygame.sprite.collide_rect(player, slingshot):
        #             player.mounted = True
        #             player.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50)
        #     elif event.key == K_SPACE:
        #         if player.mounted:
        #             fire_shot()

    player.move(pressed_keys)
    other_player.update()
    # shots.update()

    redraw_screen(screen)
    client.publish(publish_topic, json.dumps({"pos": player.get_position()}))
    # Add collision logic
    # if pygame.sprite.spritecollideany(player, shots):
    #     player.kill()
    #     running = False

    # Show screen
    pygame.display.flip()
    clock.tick(60)
