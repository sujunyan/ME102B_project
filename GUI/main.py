
from CommunicationNode import CommunicationNode

port_name = "COM3"
baudrate = 115200
if __name__ == '__main__':
    node = CommunicationNode(port_name,baudrate)
        #node.send_move(0,10,0)
