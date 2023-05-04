import json
import socket

class Socket:
    def __init__(self, host, port, sock):
        self.socket = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.address = (self.host, self.port)

    def send(self, msg):
        msg = json.dumps(msg)
        self.socket.send(("%04d" % len(msg)).encode())  # send message length
        self.socket.send(msg.encode()) # send message

    def receive(self):
        try:
            msg_length = int(self.socket.recv(4).decode())
        except Exception as e:
            print(e)
            return False
        message = self.socket.recv(msg_length).decode()
        return json.loads(message)

class ClientSocket(Socket):
    def __init__(self, host="127.0.0.1", port=8080, sock=None):
        super().__init__(host, port, sock)
        self.socket.connect(self.address)
        self.id = self.receive()

class ServerSocket(Socket):
    def __init__(self, host="127.0.0.1", port=8080, sock=None):
        super().__init__(host, port, sock)
        self.socket.bind(self.address)
        self.socket.listen()
        print(f"[LISTENING] Server is listening on {self.host}")

    def accept(self):
        conn, addr = self.socket.accept()
        return Socket(addr[0], addr[1], conn), addr
