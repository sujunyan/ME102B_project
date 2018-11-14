
import sys
#from PyQt5.QtWidgets import QApplication, QWidget, QToolTip,QPushButton,QDesktopWidget,QInputDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore


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


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

## class for two modes
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


class BuildModeWidget(ModeWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.resize(1245,787)
        self.setBackgroudColor()
        self.center()
        self.setGoFrontPageButton("GUI-fig/BuildMode/BuildMode.png")


class GameModeWidget(ModeWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.resize(1245,787)
        self.setBackgroudColor()
        self.center()
        self.setGoFrontPageButton("GUI-fig/GamesModePage/GameMode.png")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FrontPageWidget()
    sys.exit(app.exec_())
