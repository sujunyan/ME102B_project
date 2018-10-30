
from CommunicationNode import CommunicationNode

port_name = "COM5"
baudrate = 115200
if __name__ == '__main__':
    node = CommunicationNode(port_name,baudrate);
    while(True):
        node.test()
