import socket
import pickle


class Network:
    def __init__(self, ip, datamultiplex=2):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.multiplexer = datamultiplex
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            print("ERROR: CONNECTION FAILED")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*self.multiplexer))
        except socket.error as e:
            print(e)

