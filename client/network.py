import socket
import pickle


class Network:
    def __init__(self, user_tag):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.plr = self.connect(user_tag)

    def getP(self):
        return self.plr

    def connect(self, user_tag):
        try:
            self.client.connect(self.addr)
            self.client.send(pickle.dumps(user_tag))
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
