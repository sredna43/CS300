import socket
import threading
import sys

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    try:
        ip_addr = str(sys.argv[1])
        Port = str(sys.argv[2])
    except:
        ip_addr = '0.0.0.0'
        Port = 9009
    def __init__(self):
        self.sock.bind((self.ip_addr, self.Port))
        self.sock.listen(10)
        
    def handler(self, c, a):
        c.send(bytes("Welcome to CloudBot", 'utf-8'))
        while True:
            try:    
                data = c.recv(2048)
                if data:
                    print("<" + a[0] + ">" + str(data,'utf-8'))
                    
                    message_to_send = "<" + a[0] + ">" + data
                    broadcast(message_to_send, c)
            
            except:
                continue
    
    def broadcast(message, conn):
        for clients in connections:
            if clients != conn:
                try:
                    clients.send(bytes(message, 'utf-8'))
                except:
                    clients.close()
                    
                    remove(clients)
                    
    def remove(conn):
        if conn in connections:
            connections.remove(conn)
            
    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]), "connected")
            
class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, address):
        self.sock.connect((address, 9009))
        
        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()
        
        while True:
            data = self.sock.recv(2048)
            if not data:
                break
            print(str(data, 'utf-8'))
        
    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
        server = Server()
        server.run()
