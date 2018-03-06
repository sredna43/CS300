''' ChatBot Homework 1 Anders Olson '''

#import necessary files for chat server
import socket
import threading
import sys
import random
from datetime import datetime
import sqlite3
import os.path

#server class, to be used on AWS machine
class Server:
    '''server set up'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    #what question did we ask the user? 0=none, 1=name, 2=well being
    question_asked = 0
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
        ### BASIC RESPNOSES ### (I know it says "resp - noses" but I'm going to leave it)
        dontknow = ("I don't understand",)
        greetings = ("hello", "hi", "greetings", "sup", "what's up", "hey", "hola")
        farewells = ("goodbye", "bye", "see ya", "adios")
        greeting_responses = ["hello!", "hi", "greetings", "good day"]
        farewell_responses = ["goodbye!", "see you soon!", "have a nice day!", "adios", "bye now"]
        date_time = ["time", "time?", "date", "date?", "day", "today?"]
        q_state = ["how are you", "how are you?", "how are ya", "how are ya?", "hello, how are you?", "hello, how are you", "hello how are you?"]
        cpu_state = ["fine, thanks", "not well, I just became sentient", "I'm a computer, I feel nothing", "I'm good, how are you?"]
        good_feelings = ["good", "great", "fantastic", "stellar", "ok", "alright", "good,"]
        bad_feelings = ["tired", "sick", "bad", "annoyed", "frustrated", "pissed", "mad"]
        good_news = ["I'm glad to hear that", "Great!", "I hope it stays that way", "Wonderful"]
        bad_news = ["Oh no, I'm so sorry to hear that", "Oh... sorry", "It can only get better! :)"]

        #Here come the if statements
        if m.lower() in q_state:
            retstring = random.choice(cpu_state)
            if retstring == "I'm good, how are you?":
                self.question_asked = 1
            return retstring
        for word in m.split():
            #print(word)
            #print(m.split())
            if word.lower() in greetings:
                return random.choice(greeting_responses)
            elif word.lower() in farewells:
                return random.choice(farewell_responses)
            elif word.lower() in date_time:
                retstring = "The time is " + datetime.now().strftime('%H:%M:%S') + " and today is " + datetime.now().strftime('%m/%d/%Y')
                return retstring
            elif self.question_asked == 1 and word.lower() in good_feelings:
                question_asked = 0
                return random.choice(good_news)
            elif self.question_asked == 1 and word.lower() in bad_feelings:
                question_asked = 0
                return random.choice(bad_news)
            
        #Create a database if needed, or query it"
        if not os.path.isfile("answers.db"):
            print("new database created: answers.db")
            conn = sqlite3.connect("answers.db")
            c = conn.cursor()
            c.execute('''CREATE TABLE unknowns (has_answer, question, admin_answer)''')
            c.execute("INSERT INTO unknowns VALUES (1,'test question','test answer')")
        else:
            conn = sqlite3.connect("answers.db")
            c = conn.cursor()

        #Use the database
        c.execute("SELECT * FROM unknowns WHERE has_answer=1")
        answers = c.fetchall()

        for a in answers:
            if a[1] == m.lower():
                conn.commit()
                conn.close()
                return a[2]

        c.execute("INSERT INTO unknowns VALUES (?,?,?)", (0,m,dontknow[0]))
        
        conn.commit()
        conn.close()
        return random.choice(dontknow)
            
    
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
