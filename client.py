import socket
import time
import re
import struct
import sys
import select

import game_object

FORMAT = '>h3f'

class NetworkHandler:
	def __init__(self, address, port, network_entities):
		self._init_attributes()

		self.network_entities = network_entities
	
		self._connect(address, port)
		self._handshake()

	def _init_attributes(self):
		self.userid = None
		self.users = {}

	def _connect(self, address, port):
		# create an INET, STREAMing socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# now connect to the web server on port 80 - the normal http port
		self.s.connect((address, port))

	def _handshake(self):
		self.s.send('get_id') #Send request for id
		data = self.s.recv(1024)
		print data

		matched = re.match(r'id:(\d+)', data)
		if matched:
			self.userid = int(matched.groups(1)[0])
		else:
			raise ValueError('{} is not a id response'.format(data))

	def process(self, userid, state):
		x, y, heading = state
		if userid in self.users:
			player = self.users[userid]['network_object']
		else:
			player = game_object.Player()
			self.users[userid] = {'network_object': player} 
			player.userid = userid
			self.network_entities.append(player)

		player.pose.x = x
		player.pose.y = y
		player.heading = heading
		player.update_resources()

	def _receive(self, r):
		data = r.recv(1024)
		print repr(data)
		if re.match(r'state:.*', data):
			data = data[6:]
			size = struct.calcsize(FORMAT)

			while len(data) >= size:
				state_bytes = data[:size]
				data = data[size:]
				userid, x, y, heading = struct.unpack(FORMAT, state_bytes)
				if userid != self.userid:
					self.process(userid, (x, y, heading))
		else:
			print 'Received wrong data'

	def update(self, player):
		readable, writable, exception = select.select([self.s], [self.s], [])
		for r in readable:
			self._receive(r)
		
		for w in writable:
			message = struct.pack('>3f', player.pose.x, player.pose.y, player.heading)
			w.send(message)

	def close(self):
		self.s.close()

def main():
	address = '127.0.0.1'
	port = 5755

	network_handler = NetworkHandler(address, port)

	try:
		while True:
			network_handler.update()
			print 'Sent state'
			time.sleep(0.05)
	finally:
		network_handler.close()

if __name__ == '__main__':
	main()
