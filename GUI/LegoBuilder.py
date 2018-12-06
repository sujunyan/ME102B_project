
import sys
#from PyQt5.QtWidgets import QApplication, QWidget, QToolTip,QPushButton,QDesktopWidget,QInputDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import CommunicationNode



#port_name = "COM3"
#baudrate = 115200
#node = CommunicationNode.CommunicationNode(port_name,baudrate)

# the front page widget that is in charge of front page
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

    def setButton(self):

        build_mode_img = QPixmap("GUI-fig/Frontpage/BuildMode.png")
        build_mode_img = build_mode_img.scaled(434,100)
        build_mode_btn = PicButton(build_mode_img,self)
        build_mode_btn.move(406,423)
        build_mode_btn.clicked.connect(self.goBuildMode)

        game_mode_img = QPixmap("GUI-fig/Frontpage/GamesMode.png")
        game_mode_img = game_mode_img.scaled(434,100)
        game_mode_btn = PicButton(game_mode_img, self)
        game_mode_btn.move(406,530)
        game_mode_btn.clicked.connect(self.goGameMode)

    def goBuildMode(self):
        self.build_mode_widget = BuildModeWidget()
        self.build_mode_widget.show()
        self.close()

    def goGameMode(self):
        self.game_mode_widget = GameModeWidget()
        self.game_mode_widget.show()
        self.close()


    def setLayout(self):
        self.resize(1245,787)
        self.center()
        self.setBackgroud()
        self.setWindowTitle("LegoBuilder")
        ## set up the images

        pick_and_place_img = QPixmap("GUI-fig/Frontpage/PickAndPlace.png")
        pick_and_place_img = pick_and_place_img.scaled(586,156)
        pick_and_place_label = QLabel(self)
        pick_and_place_label.setPixmap(pick_and_place_img)
        pick_and_place_label.move(338,140)


        choose_mode_img = QPixmap("GUI-fig/Frontpage/ChooseMode.png")
        choose_mode_img = choose_mode_img.scaled(456,67)
        choose_mode_label = QLabel(self)
        choose_mode_label.setPixmap(choose_mode_img)
        choose_mode_label.move(403,339)


## parent class for the two modes
class ModeWidget(QWidget):
    def __init__(self):
        super().__init__()

    def setBackgroudColor(self):
        p = self.palette()
        background_color = QColor('#F9FFED')
        p.setBrush(self.backgroundRole(), background_color)
        self.setPalette(p)

    def goFrontPage(self):
        self.front_page = FrontPageWidget()
        self.show()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setGoFrontPageButton(self,path):
        ## set the button to go back
        # and corresponding header

        img = QPixmap(path)
        img = img.scaled(1245,152)
        label = QLabel(self)
        label.setPixmap(img)
        label.move(0,0)

        img = QPixmap("GUI-fig/BuildMode/BackButton.png")
        img = img.scaled(67.93,63.37)
        btn = PicButton(img,self)
        btn.move(23,45.3)
        btn.clicked.connect(self.goFrontPage)

    def setButton(self,img_path,size,pos,func):

        img = QPixmap(img_path)
        img = img.scaled(*size)
        btn = PicButton(img, self)
        btn.move(*pos)
        if (func):
            btn.clicked.connect(func)

    def setLebal(self,img_path,size,pos):
        img = QPixmap(img_path)
        img = img.scaled(*size)
        label = QLabel(self)
        label.setPixmap(img)
        label.move(*pos)


class BuildModeWidget(ModeWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.setLayout()
        self.grid = GridWidget(self)

    def setLayout(self):
        self.resize(1245,787)
        self.setBackgroudColor()
        self.center()
        self.setGoFrontPageButton("GUI-fig/BuildMode/BuildMode.png")
        self.setLebal("GUI-fig/BuildMode/ChooseBlock.png",(220,50),(50,190))
        self.setLebal("GUI-fig/BuildMode/SearchForPrebuild.png",(220,50),(916,190))
        self.setButton("GUI-fig/BuildMode/ComingSoon.png",(242,92),(53,258),None)
        self.setButton("GUI-fig/BuildMode/ComingSoon.png",(242,92),(53,388),None)
        self.setButton("GUI-fig/BuildMode/ComingSoon.png",(242,92),(53,518),None)
        self.setButton("GUI-fig/BuildMode/ComingSoon.png",(242,92),(53,648),None)


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


class LegoWidget(QWidget):
    def __init__(self,parent=None,position = (0,0) , size = (30,30),color = '#ff0000'):
        super(LegoWidget,self).__init__(parent)
        self.size = size
        self.color = color
        self.setGeometry(*position,*size )
        self.show()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawShape(qp)
        qp.end()

    def drawShape(self,qp):
        col = QColor(0, 0, 0)
        col.setNamedColor(self.color)
        qp.setPen(col)

        qp.setBrush(QColor(self.color))
        qp.drawRect(0, 0, * self.size)

    def setSetting(self,size,color):
        self.size = size
        self.color = color
        print("test")

class GridWidget(QWidget):
    def __init__(self, parent=None):
        super(GridWidget, self).__init__(parent)
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        # the mouse x and mouse y
        self.mouse_x = 0
        self.mouse_y = 0
        self.x = 367
        self.y = 234
        self.w = 480
        self.h = 480
        self.resolution = 32
        self.step = int(self.w / self.resolution)
        self.setGeometry(self.x, self.y, self.w , self.h )
        self.cur_lego_shape = LegoWidget(self)
        #self.setGeometry(0, 0, 1245,787)

        #self.label = QLabel(self)
        #self.label.resize(200, 40)
        self.show()

    def mouseMoveEvent(self, event):
        self.mouse_x = event.x()
        self.mouse_y = event.y()
        self.cur_lego_shape.move(*self.mouseToGrid())
        #print((event.x(),event.y()))

    def mousePressEvent(self,event):
        self.cur_lego_shape = LegoWidget(self,position =self.mouseToGrid())
        #self.cur_lego_shape.setSetting((60,60),'#00ff00')


    def mouseToGrid(self):
        # change from mouse coordinate to the grid coordinate
        (x,y) = (self.mouse_x,self.mouse_y)
        x = int(x/self.step) * self.step
        y = int(y/self.step) * self.step
        return (x,y)

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawGrid(qp)
        qp.end()

    def drawGrid(self,qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        # draw columns
        for x in range(0,self.h + self.step,self.step):
            qp.drawLine(x,0,x,self.w)
            #print(x)
        for y in range(0,self.w + self.step,self.step):
            qp.drawLine(0,y,self.h,y)
            #print(x)

class GameModeWidget(ModeWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.setLayout()

    def setLayout(self):
        self.resize(1245,787)
        self.setBackgroudColor()
        self.center()
        self.setGoFrontPageButton("GUI-fig/GamesModePage/GameMode.png")
        ## set the buttons
        self.setButton("GUI-fig/GamesModePage/ticTacToe.png",(438,156),(164,301),self.goTicTacToe)
        self.setButton("GUI-fig/GamesModePage/Checkers.png",(438,156),(643,301),None)
        self.setButton("GUI-fig/GamesModePage/comingSoon.png",(438,156),(164,486),None)
        self.setButton("GUI-fig/GamesModePage/comingSoon.png",(438,156),(643,486),None)

    def goTicTacToe(self):
        self.TTTpage = TicTacToeWidge()
        self.TTTpage.show()
        self.close()


class ShapeWidget(QWidget):
    def __init__(self,parent=None, position = (0,0) , size = (160,160),color = '#ff0000', is_cross = 0):
        super(ShapeWidget,self).__init__(parent)
        self.size = size
        self.color = color
        self.setGeometry(*position,*size )
        if (is_cross):
            self.pixmap = QPixmap("GUI-fig/tictactoe/cross.png")
        else:
            self.pixmap = QPixmap("GUI-fig/tictactoe/circle.png")
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(e.rect(), self.pixmap)

    def setSetting(self,size,color):
        self.size = size
        self.color = color

class TTTGridStatusWidget(QWidget):
    def __init__(self,parent=None):
        super(TTTGridStatusWidget,self).__init__(parent)
        position = (50,200)
        size = (300,100)
        self.setGeometry(*position,*size )
        self.player1_turn_img = QPixmap("GUI-fig/tictactoe/Player1turn.png")
        self.player2_turn_img = QPixmap("GUI-fig/tictactoe/Player2turn.png")
        self.player1_win_img = QPixmap("GUI-fig/tictactoe/Player1wins.png")
        self.player2_win_img = QPixmap("GUI-fig/tictactoe/Player2wins.png")
        self.pixmap = self.player1_turn_img

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(e.rect(), self.pixmap)

    def setSetting(self,val):
        if(val == 1):
            self.pixmap = self.player1_turn_img

        if(val == 2):
            self.pixmap = self.player2_turn_img

        if(val == 3):
            self.pixmap = self.player1_win_img

        if(val == 4):
            self.pixmap = self.player2_win_img
# TicTacToe grid Widge
class TTTGridWidget(QWidget):
    def __init__(self, parent=None):
        super(TTTGridWidget, self).__init__(parent)
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        # the mouse x and mouse y
        self.mouse_x = 0
        self.mouse_y = 0
        self.x = 367
        self.y = 234
        self.w = 480
        self.h = 480
        self.resolution = 3
        self.step = int(self.w / self.resolution)
        self.setGeometry(self.x, self.y, self.w , self.h )
        self.cur_shape = ShapeWidget(self)
        self.is_cross = 1
        #self.setGeometry(0, 0, 1245,787)
        self.check_win_table = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
        self.win_status = -1

        #self.label = QLabel(self)
        #self.label.resize(200, 40)
        self.show()

    def mouseMoveEvent(self, event):
        self.mouse_x = event.x()
        self.mouse_y = event.y()
        self.cur_shape.move(*self.mouseToGrid())
        #print((event.x(),event.y()))

    def mousePressEvent(self,event):
        (x,y) = self.mouseToGrid()
        x = int(x / self.step)
        y = int(y / self.step)
        print (x,y)

        if(self.win_status != -1):
            return

        self.check_win_table[x][y] = self.is_cross
        print (self.check_win_table)
        self.cur_shape = ShapeWidget(self,position =self.mouseToGrid(),is_cross = self.is_cross)
        if (self.is_cross == 1):
            self.is_cross = 0
            super().status.setSetting(2)
        else:
            self.is_cross = 1
            parent().status.setSetting(2)
        self.checkWin()

    def checkWin(self):
        # check if cross win
        for i in range(3):
            if (self.check_win_table[i][0] == 0 and self.check_win_table[i][1] == 0 and self.check_win_table[i][2] == 0) or (self.check_win_table[0][i] == 0 and self.check_win_table[1][i] == 0 and self.check_win_table[2][i] == 0):
                self.win_status = 0

            if (self.check_win_table[i][0] == 1 and self.check_win_table[i][1] == 1 and self.check_win_table[i][2] == 1) or (self.check_win_table[0][i] == 1 and self.check_win_table[1][i] == 1 and self.check_win_table[2][i] == 1):
                self.win_status = 1

        if ( (self.check_win_table[0][0] == self.check_win_table[1][1] and self.check_win_table[1][1] == self.check_win_table[2][2] ) or (self.check_win_table[0][2] == self.check_win_table[1][1] and self.check_win_table[1][1] == self.check_win_table[2][0]) ):
            self.win_status = self.check_win_table[1][1]



    def mouseToGrid(self):
        # change from mouse coordinate to the grid coordinate
        (x,y) = (self.mouse_x,self.mouse_y)
        x = int(x/self.step) * self.step
        y = int(y/self.step) * self.step
        return (x,y)

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawGrid(qp)
        qp.end()

    def drawGrid(self,qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        # draw columns
        for x in range(0,self.h + self.step,self.step):
            qp.drawLine(x,0,x,self.w)
            #print(x)
        for y in range(0,self.w + self.step,self.step):
            qp.drawLine(0,y,self.h,y)
            #print(x)


class TicTacToeWidge(ModeWidget):
    def __init__(self,parent = None):
        super().__init__()
        self.setLayout()
        self.grid = TTTGridWidget(self)
        self.status = TTTGridStatusWidget(self)

    def setLayout(self):
        self.resize(1245,787)
        self.setBackgroudColor()
        self.center()
        self.setGoFrontPageButton("GUI-fig/tictactoe/tictactoe.png")


if __name__ == '__main__':
    #node.start()
    app = QApplication(sys.argv)
    ex = TicTacToeWidge()
    ex.show()
    #ex = FrontPageWidget()
    sys.exit(app.exec_())
