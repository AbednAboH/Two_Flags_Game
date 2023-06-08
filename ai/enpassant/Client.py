import socket

class Client():

    def __init__(self,server):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clock = 30
        self.Setup = ""
        self.start = False
        self.white_is_ai = False
        self.quit = False
        self.setup = False
        self.move=None
        self.end = False
        self.server_address=server
    def get_server_address(self):
        pass

    def Connect(self):
        print('connecting to %s port %s' % self.server_address)
        try:
            self.sock.connect(self.server_address)
        except:
            print("connection failed ,please check server address")

    def send(self, message):
        try:
            # Send data
            message = bytes(message,"utf-8")
            print('"%s"' % message.decode("utf-8"))
            self.sock.send(message)
        finally:
            pass

    def recieve(self):
        while True:

            try:
                data = self.sock.recv(4000)
                data = data.decode("utf-8")
                print(data)
                if (data[:5]=="Setup"):
                    self.Setup=data[6:]
                    self.send(b"OK")
                if (data[:4] == "Time"):
                    self.clock = int(data[4:]) * 60
                    self.send(b"OK")
                elif (data=="Begin"):
                    self.start=True
                    self.white_is_ai=True
                    self.send(b"OK")
                elif data=="exit":
                    self.end=True
                elif (len(data)==4):
                    self.start=True
                    self.move=data
            except:
               pass
    def startprocess(self):
        self.Connect()
        self.recieve()




