import paho.mqtt.client as mqtt
import game

# Dictionary that contains each player's sprite information
# players = {
#   "player1": {
#     "sprite1": { "pos": (x, y), ... }
#     "sprite2": { "pos": (x, y), ... }
#     "sprite3": { "pos": (x, y), ... }
#   }
# }
players = {
        "player1": "",
        "player2": ""
}

subscribe_topics = {f"player{num+1}":f"/rps/player{num+1}/srv" for num in range(4)}
publish_topics = {f"player{num+1}":f"/rps/srv/player{num+1}" for num in range(4)}

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

    client.subscribe("/rps/player1/srv", qos=1)
    client.subscribe("/rps/player2/srv", qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    data = message.payload
    if message.topic.find("player1") > 0:
        players["player1"] = data
        if players["player2"]:
            client.publish("/rps/srv/player1", players["player2"])
    else: 
        players["player2"] = data
        if players["player1"]:
            client.publish("/rps/srv/player2", players["player1"])


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

while True:
    ...
