import socket
import time
import re

import struct

import sys

address = '127.0.0.1'
port = 5755

name = sys.argv[1]
print name

# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect((address, port))

previous_time = time.time()

userid = None

def handshake():
	s.send('get_id'.format(name))
	time.sleep(0.05) #test sending state every 50 ms
	data = s.recv(1024)
	print data
	matched = re.match(r'id:(\d+)', data)
	if matched:
		userid = matched.groups(1)
	else:
		raise ValueError('{} is not a id response'.format(data))

try:
	handshake()

	while True:
		data = s.recv(1024)
		print data
		if time.time() - previous_time > 0.05:
			if userid:
				#send our state
				s.send('10')
				previous_time = time.time()
finally:
	s.close()
