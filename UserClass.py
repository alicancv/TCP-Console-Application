import socket
import threading
import time

_port = 1234
_server = socket.gethostbyname(socket.gethostname())
_groups = ["family", "friend", "other"]


class User:
    def __init__(self, username, password, port):
        self.connections = {}
        self.groups = {}
        self.message_box = {}
        self.username = username
        self.password = password
        self.port = port

    def startListen(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((_server, self.port))
            self.server.listen()
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.start()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return False
        except:
            return True

    def receive(self):
        while True:
            client, address = self.server.accept()

            thread1 = threading.Thread(target=self.getMessage, args=(client,))
            thread1.start()

    def getMessage(self, client):
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if(message != ""):
                    print(message)
                    sender = ""
                    for i in message:
                        if i != ":":
                            sender += i
                        else:
                            break
                    if sender in self.message_box.keys():
                        self.message_box[sender].append(message)
                    else:
                        self.message_box[sender] = [message]
            except:
                client.close()
                break

    def sendMessage(self, msg):
        self.client.send(bytes(msg, "utf-8"))
        time.sleep(0.1)

    def clientConnect(self, server, port):
        self.client.connect((server, port))
        thread1 = threading.Thread(target=self.getMessage, args=(self.client,))
        thread1.start()

    def clientDisconnect(self):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


admin = User("admin", "admin123", _port)
user1 = User("user1", "user1123", _port+1)
user2 = User("user2", "user2123", _port+2)
user3 = User("user3", "user3123", _port+3)

admin.connections["user1"] = user1.port
admin.groups["user1"] = _groups[0]
admin.connections["user2"] = user2.port
admin.groups["user2"] = _groups[1]
admin.connections["user3"] = user3.port
admin.groups["user3"] = _groups[2]

user1.connections["admin"] = admin.port
user1.groups["admin"] = _groups[0]
user1.connections["user2"] = user2.port
user1.groups["user2"] = _groups[1]
user1.connections["user3"] = user3.port
user1.groups["user3"] = _groups[2]

user2.connections["admin"] = admin.port
user2.groups["admin"] = _groups[0]
user2.connections["user1"] = user1.port
user2.groups["user1"] = _groups[1]
user2.connections["user3"] = user3.port
user2.groups["user3"] = _groups[2]
