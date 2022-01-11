from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet
import sys
from SQL import *


class Search(QWidget):
    def __init__(self, sql):
        super().__init__()
        self.sql = sql
        self.ini_ui()
        self.ini_data()

    def ini_ui(self):
        # self.resize(450, 840)
        self.logo_px = QPixmap('./pic/logo.png')
        self.logo_lb = QLabel()
        self.logo_lb.setFixedSize(50, 50)
        self.logo_lb.setScaledContents(True)
        self.logo_lb.setPixmap(self.logo_px)
        self.title = QLabel("12306中国铁路")
        self.title.setStyleSheet("font:40px")

        self.line0 = QWidget()
        self.line0_layout = QHBoxLayout()
        self.line0_layout.setAlignment(Qt.AlignCenter)
        self.line0.setLayout(self.line0_layout)
        self.line0_layout.addWidget(self.logo_lb)
        self.line0_layout.addWidget(self.title)

        self.cb1 = QComboBox()
        self.cb1.setFixedSize(150, 50)
        self.cb2 = QComboBox()
        self.cb2.setFixedSize(150, 50)
        self.pix = QPixmap('./pic/ico.png')
        self.lb = QLabel()
        self.lb.setPixmap(self.pix)

        self.line1 = QWidget()
        self.line1_layout = QHBoxLayout()
        self.line1.setLayout(self.line1_layout)
        self.line1_layout.addWidget(self.cb1, 3)
        self.line1_layout.addWidget(self.lb, 1)
        self.line1_layout.addWidget(self.cb2, 3)
        self.line1_layout.setSpacing(20)
        self.line1.setContentsMargins(0, 0, 0, 0)
        self.line1_layout.setAlignment(Qt.AlignCenter)

        self.lb2 = QLabel("日期")
        self.le1 = QLineEdit()
        self.le2 = QLineEdit()
        self.le3 = QLineEdit()

        self.line2_layout = QHBoxLayout()
        self.line2 = QWidget()
        self.line2.setLayout(self.line2_layout)
        self.line2_layout.addWidget(self.lb2, 1)
        self.line2_layout.addWidget(self.le1, 2)
        self.line2_layout.addWidget(self.le2, 2)
        self.line2_layout.addWidget(self.le3, 2)
        self.line2.setContentsMargins(0, 0, 0, 0)

        self.search_bt = QPushButton("查询")
        self.search_bt.setFixedSize(300,40)
        self.line3 = QWidget()
        self.line3_layout = QHBoxLayout()
        self.line3.setLayout(self.line3_layout)
        self.line3_layout.addWidget(self.search_bt)
        self.line3_layout.setAlignment(Qt.AlignCenter)

        self.search_layout = QVBoxLayout()
        self.search_w = QWidget()
        self.search_w.setLayout(self.search_layout)

        self.search_layout.addWidget(self.line0, 1)
        self.search_layout.addWidget(self.line1, 8)
        self.search_layout.addWidget(self.line2, 8)
        self.search_layout.addWidget(self.line3, 8)
        self.search_layout.setSpacing(20)
        self.search_w.setFixedSize(400, 400)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.search_w,10)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.main_layout)

    def set_sql(self, sql):
        self.sql = sql

    def ini_data(self):
        self.depart_list = ["北京", "上海", '广州', "南京", "徐州", "西安", "武汉", "杭州", "成都"]
        self.des_list = ["北京", "上海", '广州', "南京", "徐州", "西安", "武汉", "杭州", "成都"]
        print(self.depart_list)
        print(self.des_list)
        self.cb1.addItems(self.depart_list)
        self.cb2.addItems(self.des_list)

    def search(self):
        print('searching...')
        str = 'select * from Ticket where '
        start = 'departure = \'' + self.cb1.currentText() + '\' and '
        end = 'destination = \'' + self.cb2.currentText() + '\' and '
        date = self.time_parser(self.le1.text(), self.le2.text(), self.le3.text())
        self.str = str + start + end + date + ';'
        # self.str = 'select * from T where Start = \'北京\' and End = \'上海\' and Time >= \'2021:10:1 00:00:00\' and Time < \'2021:10:1 23:59:59\'';
        print(self.str)
        return self.str

    def time_parser(self, y, m, d):
        time_1 = 'depart_time >= \'' + y + ':' + m + ':' + d + ' 00:00:00\''
        time_2 = ' and depart_time < \'' + y + ':' + m + ':' + d + ' 23:59:59\''
        return time_1 + time_2

    def ret_str(self):
        res_text = self.cb1.currentText() + ' -> ' + self.cb2.currentText()
        return res_text


if __name__ == '__main__':
    sql = SQL()
    sql.connect('localhost', 'root', 'Whc00119', '12306')
    app = QApplication(sys.argv)
    w = Search(sql)
    w.show()
    w.set_sql(sql)
    sys.exit(app.exec_())
