import socket

class wmm:
    def __init__(self, modemid, bufsize=256, port=52001):
        self.ipaddr = "192.168.2.%d" % (modemid)
        self.port = port
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.bind(("", self.port))

    def send(self, data):
        self.sock.sendto(bytes(data), (self.ipaddr, self.port))

    def recv(self):
        data, addr = self.sock.recvfrom(self.bufsize)
        return data