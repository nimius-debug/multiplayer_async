import socket
import asyncio
from _thread import *
from server.player import Player
from server.connectionManager import ConnectionManager
import pickle
import random



# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     s.bind((server, port))
# except socket.error as e:
#     str(e)

# s.listen()
# print("Waiting for a connection, Server Started")

def random_position():
    return random.randint(0, 450), random.randint(0, 450)

def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def new_player(user_tag):
    x, y = random_position()
    color = random_color()
    return Player(x, y, 50, 50, color, user_tag)

# Initialize the connection manager
conn_mgr = ConnectionManager()

async def handle_client(reader, writer):
    conn_id = conn_mgr.get_new_connection_id()

    user_tag = await reader.read(2048)
    user_tag = pickle.loads(user_tag)

    player = new_player(user_tag)
    conn_mgr.add_player(conn_id, player)

    writer.write(pickle.dumps(player))
    await writer.drain()
    
    # Get the client's address
    client_address = writer.get_extra_info('peername')
    print(f"Connected to: {client_address}")

    try:
        while True:
            data = await reader.read(2048)
            if not data:
                break

            data = pickle.loads(data)
            conn_mgr.players[conn_id] = data
            
            other_players = conn_mgr.get_all_players_except(conn_id)
            writer.write(pickle.dumps(other_players))
            # print("Received: ", data) 
            # print("Sending : ", other_players)
            await writer.drain()

    except :
        pass

    writer.close()
    await writer.wait_closed()

    print("Lost connection")
    conn_mgr.remove_player(conn_id)
    
# def threaded_client(conn, conn_id):
#     user_tag = pickle.loads(conn.recv(2048))
#     player = new_player(user_tag)
#     conn_mgr.add_player(conn_id,player)
#     conn.send(pickle.dumps(player))
    
#     while True:
#         try:
#             data = pickle.loads(conn.recv(2048))
#             conn_mgr.players[conn_id] = data
            
#             print("Players: ", conn_mgr.get_all_players())
#             if not data:
#                 print("Disconnected")
#                 break
#             else:
#                 print("Received: ", data) 
#                 other_players = conn_mgr.get_all_players_except(conn_id)
#                 print("Sending : ", other_players)
#                 conn.sendall(pickle.dumps(other_players))
#         except:
#             break

#     print("Lost connection")
#     conn_mgr.remove_player(conn_id)
#     conn.close()

# conn_id = 0
async def main():
    server_ip = socket.gethostbyname(socket.gethostname())
    port = 5555
    server = await asyncio.start_server(handle_client, server_ip, port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
# while True:
#     conn, addr = s.accept()
#     print("Connected to:", addr)

#     start_new_thread(threaded_client, (conn, conn_id))
#     conn_id += 1
