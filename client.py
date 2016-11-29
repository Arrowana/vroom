import socket
import time
import re
import struct
import sys

FORMAT = '>h3f'

class NetworkHandler:
	def __init__(self, address, port):
		self._init_attributes()
	
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
			userid = matched.groups(1)
		else:
			raise ValueError('{} is not a id response'.format(data))

	def process(userid, state):
		if userid in self.users:
			self.users[userid]['state'] = {'x': state[0], 'y': state[1], 'heading': state[2]}
		else:
			self.users[userid] = {'state': {'x': state[0], 'y': state[1], 'heading': state[2]}}

	def update(self):
		data = self.s.recv(1024)
		print data
		if re.match(r'state:.*', data):
			data = data[6:]
			size = struct.calcsize(FORMAT)

			while len(data) >= size:
				state_bytes = data[:size]
				data = data[size:]
				userid, state = struct.unpack(FORMAT, state_bytes)
				if userid != self.userid:
					self.process(userid, state)
		else:
			print 'Received wrong data'
		print data
		x, y, h = 0.1, 0.2, 0.3
		message = struct.pack('>3f', x, y, h)
		self.s.send(message)

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
