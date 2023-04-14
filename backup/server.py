import asyncio
import pickle
import random
import socket
from player import Player
from connectionManager import ConnectionManager

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.conn_mgr = ConnectionManager()

    def random_position(self):
        return random.randint(0, 450), random.randint(0, 450)

    def random_color(self):
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    def new_player(self, user_tag):
        x, y = self.random_position()
        color = self.random_color()
        return Player(x, y, 50, 50, color, user_tag)

    async def handle_client(self, reader, writer):
        conn_id = self.conn_mgr.get_new_connection_id()

        user_tag = await reader.read(2048)
        user_tag = pickle.loads(user_tag)

        player = self.new_player(user_tag)
        print("Player: ", player)
        self.conn_mgr.add_player(conn_id, player)

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
                self.conn_mgr.players[conn_id] = data

                other_players = self.conn_mgr.get_all_players_except(conn_id)
                writer.write(pickle.dumps(other_players))
                print("Received: ", data) 
                await writer.drain()

        except:
            pass

        writer.close()
        await writer.wait_closed()

        print("Lost connection")
        self.conn_mgr.remove_player(conn_id)

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