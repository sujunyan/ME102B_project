# include library
from serial import *
import struct
from copy import copy
import time


toHex = lambda x: "".join("{:02X}".format(ord(c)) for c in x)
MOVE_XYZ = 0
ROTATE_XYZ = 1
PUSH_AND_GRIBPPER_ACTION = 2

# 3 * 3 matrix for lego pos
Lego_pos_list = [ [ (182,105,0), (268,105,0), (354,105,0)   ] ,
                    [(182,191,0), (268,191,0), (354,191,0) ],
                    [(182,270,0), (268,270,0), (354,270,0) ] ]

line_x1 = 230
line_x2 = 300


class CommunicationNode:
	def __init__(self, portname, baudrate):
		# configure and open the port
		self.portname = portname
		self.baudrate = baudrate
		self.origin = (160,87,0)
		self.dispensor_pos = (460,60,0)
			# Didn't set the 'timeout' field, which means the port.read
		# will be blocked if the number of bytes read is not reached.
	def start(self):

		self.port = Serial(port = self.portname, baudrate = self.baudrate,
			parity = PARITY_NONE,
			stopbits = STOPBITS_ONE,
			bytesize = 	EIGHTBITS)
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

	def send_gripper_action(self,val):
		#case 1: {pushGripper();break;}
        #case 2: {pullGripper();break;}
        #case 3: {tightenGripper();break;}
        #case 4: {releaseGripper();break;}
        #case 5: {pickLego();break;}
        #case 6: {placeLego();break;}
		msg = struct.pack("<4B",0xff,PUSH_AND_GRIBPPER_ACTION,1,val);
		self.port.write(msg)

	def test(self):
		while(True):
			nums = input("Enter 3 nunmbers to move\n")
			li = [float(i) for i in nums.split()]
			print(li)
			if (len(li) != 3):
				print("Please enter 3 numbers")
				continue
			self.send_move(*li);
			#line = self.port.readline()
			line = self.read_in_all()
			if line:
				line = line.decode('ascii')
				#print ("msg received: %s"%(line,))
				print(line,end='')
			print(li)
	def setPortName(self,port_name):
		self.portname = portname

	def read_in_all(self):
		# read in all the lines available in the port
		if(self.port.in_waiting):
			line = self.port.readline()
		else:
			return None
		while(self.port.in_waiting):
			in_line = self.port.readline()
			line += in_line
			print(in_line,end='')
		return line

	def goToOrigin(self):
		self.send_move(*self.origin)

	def goToDispensor(self):
		self.send_move(*self.dispensor_pos)



	def pickAndPlace(self,start_pos,end_pos):
		self.send_move(*start_pos)
		self.send_gripper_action(5) # pick a lego
		time.sleep(5)
		(start_x,start_y,z)  = start_pos
		start_offset = 60 # path planning to avoid
		next_x = start_x
		if(start_x < 300):
			next_x = start_x + start_offset
		if(start_x > 300):
			next_x = start_x - start_offset
		self.send_move(next_x, start_y, 0)
		next_y = 20 # might need delay
		self.send_move(next_x, next_y, 0) # go all the way to the right side

		(end_x,end_y,z) = end_pos
		if (end_x < line_x1):
			next_x = line_x1
		else:
			next_x = line_x2
		self.send_move(next_x,next_y,0)
		next_y = end_y
		self.send_move(next_x,next_y,0)
		next_x = end_x
		self.send_move(next_x,next_y,0)
		self.send_gripper_action(6) # place a lego


if __name__ == '__main__':
	port_name = "COM3"
	baudrate = 115200
	node = CommunicationNode(port_name,baudrate)
	node.start()
	node.test()

#150 -70 0
