
from CommunicationNode import CommunicationNode
from LegoBuilder import *

port_name = "COM3"
baudrate = 115200
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FrontPageWidget()
    sys.exit(app.exec_())
        #node.send_move(0,10,0)
