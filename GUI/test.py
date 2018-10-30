
import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    #resize()方法调整窗口的大小。这离是250px宽150px高
    w.resize(250, 150)
    #move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
    w.move(300, 300)
    #设置窗口的标题
    w.setWindowTitle('Simple')
    #显示在屏幕上
    w.show()

    #系统exit()方法确保应用程序干净的退出
    #的exec_()方法有下划线。因为执行是一个Python关键词。因此，exec_()代替
    sys.exit(app.exec_())
