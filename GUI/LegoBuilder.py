
import sys
#from PyQt5.QtWidgets import QApplication, QWidget, QToolTip,QPushButton,QDesktopWidget,QInputDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LegoBuilder(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        startWindow()

    def setBackgroudColor(self):
        p = self.palette()
        background_color = QColor(0,0,0)
        background_color.setNamedColor('#ffffe6')
        p.setColor(self.backgroundRole(), background_color)
        self.setPalette(p)

    def startWindow(self):
        btn = QPushButton('Button', self)
        self.resize(1245,787)
        self.center()
        self.setBackgroudColor()
        self.setWindowTitle("center")
        self.show()



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDialog(self):
        (text,ok) = QInputDialog.getText(self,'Input Dialog','Enter your name')


if __name__ == '__main__':
    #创建应用程序和对象
    app = QApplication(sys.argv)
    ex = LegoBuilder()
    sys.exit(app.exec_())
