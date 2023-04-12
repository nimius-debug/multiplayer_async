import socket
import pickle

class Network:
    def __init__(self, user_tag):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.client)
        self.server = socket.gethostbyname(socket.gethostname())
        print(self.server)
        self.port = 5555
        self.addr = (self.server, self.port)
        print(self.addr)
        self.plr = None  # set plr to None initially
        self.connect(user_tag)  # call connect method to set self.plr
        # self.plr = self.connect(user_tag)

    def getP(self):
        return self.plr

    def connect(self, user_tag):
        try:
            self.client.connect(self.addr)
            self.client.send(pickle.dumps(user_tag))
            player_data = self.client.recv(2048)
            print("Player data: ", player_data)
            self.plr = pickle.loads(player_data)
            print("PPPPPPPPPIIIIIIINNNNNAAAAAAAAAAAAAAA", self.plr)
            return self.plr
        except Exception as e:
            print("Error connecting to server", e)
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
