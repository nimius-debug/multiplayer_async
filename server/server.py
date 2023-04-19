import asyncio
import pickle
import random
import socket
import pygame
import sys
import os
from connectionManager import ConnectionManager
# Add the path of the folder containing the file you want to import
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../util'))
sys.path.insert(0, folder_path)
from player import Player

class Server:
    def __init__(self, ip, port):
        pygame.init()
        pygame.display.init()
        self.ip = ip
        self.port = port
        self.conn_mgr = ConnectionManager()

    def random_position(self):
        return random.randint(0, 450), random.randint(0, 450)

    def random_color(self):
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    def new_player(self, user_tag):
        pos = self.random_position()
        # color = self.random_color()
        player = Player(pos, self.conn_mgr.players, user_tag)
        # player.user_tag = user_tag
        return player

    async def handle_client(self, reader, writer):
        user_tag = await reader.read(2048)
        user_tag = pickle.loads(user_tag)

        player = self.new_player(user_tag)
        # print("Player: ", player)
        self.conn_mgr.add_player(player)

        player_data = player.serialize()
        print(f"Sending player object: {player_data}")
        writer.write(pickle.dumps(player_data))
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
                player = self.conn_mgr.get_player(data['user_tag'])
                # print("Player: ", player)
                player.pos = pygame.math.Vector2(data['pos'])
                # print("Player pos: ", player.pos)
                player.direction = pygame.math.Vector2(data['dir'])
                # print("Player dir: ", player.direction)
                other_players = self.conn_mgr.get_all_players_except(player)
                # print("Other players: ", other_players)
                other_players = [p.serialize() for p in other_players]
                # print("Sending other players data:", other_players)
                writer.write(pickle.dumps(other_players))
                print("Received: ", data) 
                await writer.drain()

        except Exception as e:
            print(f"Exception occurred: {e}")

        writer.close()
        await writer.wait_closed()

        print("Lost connection")
        self.conn_mgr.remove_player(player)

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.ip, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    server_ip = socket.gethostbyname(socket.gethostname())
    port = 5555
    server = Server(server_ip, port)
    asyncio.run(server.start_server())
