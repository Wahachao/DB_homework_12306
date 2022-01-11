import sys
from PyQt5.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self, ):
        super(QWidget, self).__init__()
        self.number = 0
        w = QWidget(self)

        ##创建一个滚动条
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.topFiller)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        w.setLayout(self.vbox)

        self.resize(300, 500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
