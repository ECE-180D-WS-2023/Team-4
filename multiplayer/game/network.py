import pickle
import json
import socket
import time

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # dummy socket
    try:
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class Socket:
    def __init__(self, host, port, sock):
        self.socket = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.address = (self.host, self.port)

    def send(self, msg):
        # msg = json.dumps(msg)
        # self.socket.send(("%04d" % len(msg)).encode())  # send message length
        # self.socket.send(msg.encode()) # send message
        msg = pickle.dumps(msg)
        self.socket.send(("%06d" % len(msg)).encode())  # send message length
        # print(("%06d" % len(msg)).encode())
        self.socket.send(msg) # send message

    def receive(self):
        # try:
        #     msg_length = int(self.socket.recv(4).decode())
        # except Exception as e:
        #     print(e)
        #     return False
        # message = self.socket.recv(msg_length).decode()
        # return json.loads(message)
        try:
            msg_length = int(self.socket.recv(6).decode())
        except Exception as e:
            print(e)
            return False
        message = bytearray()
        while len(message) < msg_length:
            chunk = self.socket.recv(msg_length)
            message.extend(chunk)
        return pickle.loads(message)

class ClientSocket(Socket):
    def __init__(self, host="127.0.0.1", port=8080, sock=None):
        super().__init__(host, port, sock)
        print("CLIENT:", self.address)
        self.socket.connect(self.address)
        self.id = self.receive()

class ServerSocket(Socket):
    def __init__(self, host="127.0.0.1", port=8080, sock=None):
        super().__init__(host, port, sock)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("SERVER:", self.address)
        while True:
            try:
                self.socket.bind(self.address)
                break
            except Exception as e:
                print(e)
                time.sleep(2)

        self.socket.listen()
        print(f"[LISTENING] Server is listening on {self.host}")

    def accept(self):
        conn, addr = self.socket.accept()
        return Socket(addr[0], addr[1], conn), addr
