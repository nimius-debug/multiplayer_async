import socket
import asyncio
from player import Player
from connectionManager import ConnectionManager
import pickle
import random

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
    print("Player: ", player)
    conn_mgr.add_player(conn_id, player)

    print(f"Sending player object: {player}")
    writer.write(pickle.dumps(player))
    await writer.drain()
    
    # Get the client's address
    client_address = writer.get_extra_info('peername')
    print(f"Connected to: {client_address}")

    try:
        while True:
            data = await reader.read(2048)
            print("Data: ", data)
            if not data:
                break

            data = pickle.loads(data)
            print("Data2: ", data)
            conn_mgr.players[conn_id] = data
            
            other_players = conn_mgr.get_all_players_except(conn_id)
            writer.write(pickle.dumps(other_players))
            print("Received: ", data) 
            # print("Sending : ", other_players)
            await writer.drain()

    except :
        pass

    writer.close()
    await writer.wait_closed()

    print("Lost connection")
    conn_mgr.remove_player(conn_id)
  
async def main():
    server_ip = socket.gethostbyname(socket.gethostname())
    port = 5555
    server = await asyncio.start_server(handle_client, server_ip, port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
