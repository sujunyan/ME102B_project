import sys
#from PyQt5.QtWidgets import QApplication, QWidget, QToolTip,QPushButton,QDesktopWidget,QInputDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import CommunicationNode


port_name = "COM3"
baudrate = 115200
node = CommunicationNode.CommunicationNode(port_name,baudrate)

class FrontPageWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setLayout()
        self.setButton()
        self.show()

    def setBackgroud(self):
        p = self.palette()
        p.setBrush(self.backgroundRole(), QBrush(QPixmap("GUI-fig/Frontpage/Background.jpg")))
        self.setPalette(p)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def moveLego(self):
        tmp = (self.xEdit.text(),self.yEdit.text(),self.zEdit.text())
        (x,y,z) = (float(i) for i in tmp)

        node.send_move(x,y,z)
        #print (x,y,z)

    def gripperAction(self,val):
        node.send_gripper_action(val)
        print (val)



    def setButton(self):
        move_btn = QPushButton('move', self)
        move_btn.move(500,0)
        move_btn.clicked.connect(self.moveLego)

        #case 1: {pushGripper();break;}
        #case 2: {pullGripper();break;}
        #case 3: {tightenGripper();break;}
        #case 4: {releaseGripper();break;}

        #case 7: {calibrate();break;}

        push_btn = QPushButton('push down', self)
        push_btn.move(0,100)
        push_btn.clicked.connect(lambda: self.gripperAction(1))

        pull_btn = QPushButton('pull up gripper', self)
        pull_btn.move(100,100)
        pull_btn.clicked.connect(lambda: self.gripperAction(2))

        push_btn = QPushButton('tighten gribpper', self)
        push_btn.move(200,100)
        push_btn.clicked.connect(lambda: self.gripperAction(3))

        push_btn = QPushButton('release gribpper', self)
        push_btn.move(300,100)
        push_btn.clicked.connect(lambda: self.gripperAction(4))

        push_btn = QPushButton('pick lego', self)
        push_btn.move(0,200)
        push_btn.clicked.connect(lambda: self.gripperAction(5))

        push_btn = QPushButton('place lego', self)
        push_btn.move(100,200)
        push_btn.clicked.connect(lambda: self.gripperAction(6))


        push_btn = QPushButton('calibrate', self)
        push_btn.move(0,300)
        push_btn.clicked.connect(lambda: self.gripperAction(7))


    def legoStart(self):
        pass

    def setEdit(self):
        self.xEdit = QLineEdit(self)
        self.yEdit = QLineEdit(self)
        self.zEdit = QLineEdit(self)
        self.xEdit.setText('460')
        self.yEdit.setText('40')
        self.zEdit.setText('0')

        self.yEdit.move(170,0)
        self.zEdit.move(340,0)

    def setLayout(self):
        self.resize(1245,787)
        self.center()
        self.setEdit()
        #self.setBackgroud()
        self.setWindowTitle("LegoBuilder debug mode")
        ## set up the images



if __name__ == '__main__':
    node.start()
    app = QApplication(sys.argv)
    ex = FrontPageWidget()
    sys.exit(app.exec_())

#35
#170 65 0
#455  40 0
