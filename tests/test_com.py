"""
	Test communication between server and client
"""
import struct
import client

#header is composed of the state only
CMD_FMT = 'h'
CMD_UPDATE_STATE = 0 #Client sending its state >h3f
CMD_BROADCAST_STATES = 1 #Server sending states >2h + num_states*h3f
CMD_SIZE = struct.calcsize('h')

def pack_states(states):
	payload = struct.pack('>2h', CMD_BROADCAST_STATES, len(states))
	for state in states:
		payload += struct.pack('>h3f', *state)

	return payload

def unpack_state(data):
	cmd = struct.unpack('>h', data[:CMD_SIZE])
	if cmd == 0:
		#Valid state command
		if len(data) == struct.calcsize('>h3f'):
			cmd, x, y, heading = struct.unpack('>h3f', data)
		else:
			return None
	else:
		return None

def process_received(data):
	cmd, = struct.unpack('>h', data[:CMD_SIZE])
	if cmd == CMD_BROADCAST_STATES:
		return unpack_states(data[CMD_SIZE:])
	else:
		return None

def unpack_states(data):
	num_states, = struct.unpack('>h', data[:struct.calcsize('>h')])
	data = data[struct.calcsize('h'):]
	if len(data) == num_states*struct.calcsize('>h3f'):
		states = []
		for _ in range(num_states):
			state_bytes = data[:struct.calcsize('>h3f')]
			data = data[struct.calcsize('>h3f'):]
			state = struct.unpack('>h3f', state_bytes)
			states.append(state)

		return states
	else:
		return None

def test_pack_states():
	state = (0, 1, 2, 3) #Userid, x, y, heading

	packed_states = pack_states([state])
	assert packed_states is not None

def test_broadcast_and_unpack():
	states = [(0, 10, 10, 100), (1, 20, 20, 0), (3, 1, 2, 3)]
	packed_states = pack_states(states)
	print repr(packed_states)
	unpacked_states = process_received(packed_states)

	assert states == unpacked_states

def test_unpack_states_corrupted():
	corrupted = '\x00\x01\x00\x00'
	assert unpack_states(corrupted) is None

def test_process_received_corrupted():
	corrupted = '\x00\x00\x00\x00'

	assert unpack_state(corrupted) is None
	
