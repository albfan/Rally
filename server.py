from ursinanetworking import *

print("\nHello from the Rally Server!")

print("\nPlease enter the ip (use 'localhost' for localhost)")

ip = input("\nIP: ")

server = UrsinaNetworkingServer(ip, 25565)
easy = EasyUrsinaNetworkingServer(server)

@server.event
def onClientConnected(client):
    easy.create_replicated_variable(
        f"player_{client.id}",
        { "type" : "player", "id" : client.id, "username": "Guest", "position": (0, 0, 0), "rotation" : (0, 0, 0), "texture" : "car-red.png", "highscore": 0.0}
    )
    print(f"{client} connected!")
    client.send_message("GetId", client.id)

@server.event
def onClientDisconnected(client):
    easy.remove_replicated_variable_by_name(f"player_{client.id}")
    
@server.event
def MyPosition(client, newpos):
    easy.update_replicated_variable_by_name(f"player_{client.id}", "position", newpos)

@server.event
def MyRotation(client, newrot):
    easy.update_replicated_variable_by_name(f"player_{client.id}", "rotation", newrot)

@server.event
def MyTexture(client, newtex):
    easy.update_replicated_variable_by_name(f"player_{client.id}", "texture", newtex)

@server.event
def MyUsername(client, newuser):
    easy.update_replicated_variable_by_name(f"player_{client.id}", "username", newuser)

@server.event
def MyHighscore(client, newscore):
    easy.update_replicated_variable_by_name(f"player_{client.id}", "highscore", newscore)

while True:
    easy.process_net_events()