# include library
from serial import *
import struct
from copy import copy


toHex = lambda x: "".join("{:02X}".format(ord(c)) for c in x)
MOVE_XYZ = 0
ROTATE_XYZ = 1

class CommunicationNode:
	def __init__(self, portname, baudrate):
		# configure and open the port
		self.port = Serial(port = portname, baudrate = baudrate,
			parity = PARITY_NONE,
			stopbits = STOPBITS_ONE,
			bytesize = 	EIGHTBITS)
		# Didn't set the 'timeout' field, which means the port.read
		# will be blocked if the number of bytes read is not reached.
		if not (self.is_open()):
			self.port.open()

	def on_shutdown(self):
		self.port.close()

	def is_open(self):
		# using the port field to check if the prot is still open
		return self.port.port != None

	def __del__(self):
		self.on_shutdown()
#The protocol:
# Header          | command_id    | len       | data
# 1 byte(255)    | 1 byte        | 1 byte   | data

	def send_move(self,x,y,z):
		msg = struct.pack("<3B3f",0xff,MOVE_XYZ,12,x,y,z);
		self.port.write(msg)

	def send_rotate(self,x,y,z)	:
		msg = struct.pack("<3B3i",0xff,ROTATE_XYZ,12,x,y,z);
		self.port.write(msg)

	def test(self):
		#self.send_move(1,2,3);
		self.send_rotate(1,2,3);
		line = self.port.readline()
		#line = self.read_in_all()
		if line:
			line = line.decode('ascii')
			#print ("msg received: %s"%(line,))
			print(line,end='')

	def read_in_all(self):
		# read in all the lines available in the port
		line = None
		while(self.port.in_waiting):
			line += self.port.readline()
		return line
