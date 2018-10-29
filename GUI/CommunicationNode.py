# include library
from serial import *
import struct
from copy import copy

# link local files
from judgement_info import *
from board_info import *
from protocol import *

toHex = lambda x: "".join("{:02X}".format(ord(c)) for c in x)

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
		self.data = unpack_data_t(p_header = frame_header_t())
		self.judge_rece_mesg = receive_judge_t()
		self.board_rece_mesg = receive_board_t()

	def on_shutdown():
		self.port.close()

	def is_open(self):
		# using the port field to check if the prot is still open
		return self.port.port != None

	def send_move(self,x,y,z):
		
