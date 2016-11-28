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

clients = {}

FORMAT = '>h3f'

def package(userid, x, y, heading):
	return struct.pack(FORMAT, userid, x, y, heading)

def send():
	clientsocket.send(struct.pack('>2f', *[random.random() for i in range(2)]))

class Client:
	def __init__(self):
		self.username = None
		self.state = None
		self.userid = None
	
	def set_username(self, username):
		self.username = username

class GameState:
	def __init__(self):
		pass

previous_update = time.time()
current_userid = 0

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

				matched = re.match(r'get_id', data)
				if matched:
					print 'Received request for id from user:', s
					clients[s].userid = current_userid
					s.send('id:{}'.format(current_userid))
					current_userid += 1
				else:
					print 'Received state: {}, from: {}'.format(data, clients[s].username)
					clients[s].state = data
					
	if time.time() - previous_update > 0.05:
		#Update state
		previous_update = time.time()
		payload = ''
		for s, client in clients.items():
			payload += '{}:{},'.format(client.userid, client.state)
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
