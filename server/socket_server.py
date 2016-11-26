import socket
import random
import struct
import time

import select
import time
import re

address = '127.0.0.1'
port = 5755

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((address, port))
serversocket.listen(5)

read_list = [serversocket]
write_list = []

queue = ['10']*10 #FIFO queue for data
clients = {}

FORMAT = '>h2f'

def send():
    clientsocket.send(struct.pack('>2f', *[random.random() for i in range(2)]))

class Client:
    def __init__(self):
        self.username = None
        self.state = None
    
    def set_username(self, username):
        self.username = username

class GameState:
    def __init__(self):
        pass

previous_update = time.time()

while True:
    readable, writable, errored = select.select(read_list, write_list, [])
    for s in readable:
        if s is serversocket:
            clientsocket, address = serversocket.accept()
            print 'Connection from :', address

            write_list.append(clientsocket)
            read_list.append(clientsocket)
            clients[clientsocket] = Client()
        else:
            data = s.recv(1024)
            if data:
                print 'Received:', data

                matched = re.match(r'name:([\w\d]+)', data)
                if matched:
                    name = matched.group(1)
                    print 'Received username from user:', name
                    clients[s].set_username(name)
                else:
                    print 'Received state: {}, from: {}'.format(data, clients[s].username)
                    clients[s].state = data
                    
    if time.time() - previous_update > 0.05:
        #Update state
        previous_update = time.time()
        payload = ''
        for s, client in clients.items():
            payload += '{}:{},'.format(client.username, client.state)
        print 'Send payload'
    else:
        payload = None

    if payload:
        for w in writable:
            #Broadcast the state
            try:
                w.send(payload)
            except socket.error:
                read_list.remove(w)
                write_list.remove(w)

    time.sleep(0.005)
