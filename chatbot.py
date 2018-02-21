''' ChatBot Homework 1 Anders Olson '''

#import necessary files for chat server
import socket
import threading
import sys
import random
from datetime import datetime

#server class, to be used on AWS machine
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
                    message = str(data, 'utf-8')
                    print(message)
                    self.broadcast(message, c)
            except:
                continue
    
    def broadcast(self, m, conn):
        message = self.respond(m)
        send_message = "Cloudbot: " + message
        for clients in self.connections:
            if clients == conn:
                try:
                    clients.send(bytes(send_message, 'utf-8'))
                except:
                    clients.close()
                    
                    remove(clients)
                    
    def remove(self, conn):
        if conn in self.connections:
            self.connections.remove(conn)
            
    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]), "connected")

    def respond(self, m):
        #questions: 0=none, 1=user state, 2=name
        question_asked = 0
        greetings = ("hello", "hi", "greetings", "sup", "what's up", "hey", "hola")
        farewells = ("goodbye", "bye", "see ya", "adios")
        greeting_responses = ["hello!", "hi", "greetings", "good day"]
        farewell_responses = ["goodbye!", "see you soon!", "have a nice day!", "adios", "bye now"]
        date_time = ["time", " time?", "date", "date?", "day", "today?"]
        q_state = ["how are you", "how are you?", "how are ya", "how are ya?", "hello, how are you?", "hello, how are you"]
        cpu_state = ["fine, thanks", "not well, I just became sentient", "I'm a computer, I feel nothing", "I'm good, how are you?"]

        #Here come the if statements
        if m.lower() in q_state:
            return random.choice(cpu_state)
        for word in m.split():
            if word.lower() in greetings:
                return random.choice(greeting_responses)
            elif word.lower() in farewells:
                return random.choice(farewell_responses)
            elif word.lower() in date_time:
                retstring = "The time is " + datetime.now().strftime('%H:%M:%S') + " and today is " + datetime.now().strftime('%m/%d/%Y')
                return retstring
        
            
        '''nothing has understood what was said'''
        return "I'm sorry, I don't know that one."

#client class, to be used on local machine
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
