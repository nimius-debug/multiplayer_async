import socket
import sys
import os
import pickle
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../util'))
sys.path.insert(0, folder_path)
from player import Player


class Network:
    def __init__(self, user_tag):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.plr = None
        self.connect(user_tag)

    def getP(self):
        return self.plr

    def connect(self, user_tag):
        try:
            self.client.connect(self.addr)
            self.client.send(pickle.dumps(user_tag))
            
            player_data = self.client.recv(2048)
            print("Player data: ", player_data)
            self.plr = Player.deserialize(pickle.loads(player_data))
            print("Player: ", self.plr)
            return self.plr
        except Exception as e:
            print("Error connecting to server", e)
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data.serialize()))
            received_data = self.client.recv(2048)
            if not received_data:
                print("No data received from the server")
                return []
            return [Player.deserialize(p_data) for p_data in pickle.loads(received_data)]
        except socket.error as e:
            print(e)
        except EOFError:
            print("EOFError: Ran out of input")
            return []


