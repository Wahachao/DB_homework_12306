from functools import partial
import random

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet
import sys


class Result(QWidget):
    def __init__(self, sql, res, str):
        super(Result, self).__init__()
        self.bt_dict ={}
        self.res = res
        self.res_text = str
        self.sql = sql
        self.ini_ui()

    def set_res(self, res):
        self.res = res

    def set_title(self, str):
        self.res_text = str

    def ini_ui(self):

        self.res_title = QLabel(self.res_text)
        self.res_title.setStyleSheet("font:40px")
        self.ret_bt = QPushButton("返回")
        self.ret_bt.setFixedSize(80,60)

        self.line1 = QWidget()
        # self.line1.resize(400, 40)
        self.line1_layout = QHBoxLayout()
        self.line1.setLayout(self.line1_layout)
        self.line1_layout.addWidget(self.ret_bt, 4)
        self.line1_layout.addWidget(self.res_title, 1)

        self.res_w = QWidget()
        self.res_w.setFixedSize(400,780)
        self.res_layout = QVBoxLayout()
        self.res_w.setLayout(self.res_layout)
        self.res_layout.setAlignment(Qt.AlignTop)
        self.add()
        # self.set_bt()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.line1, 1)
        self.main_layout.addWidget(self.res_w, 8)

    def add(self):
        print(self.res)
        if len(self.res) == 0:
            self.res_layout.addWidget(QLabel("没有符合条件的车票"))
        else:
            for t in self.res:
                print(t)
                number = t[0]
                start = t[3]
                end = t[4]
                depart_time = str(t[1]).split(' ')[1:][0][:-3]
                arrive_time = str(t[2]).split(' ')[1:][0][:-3]
                rest = str(t[5])

                pix = QPixmap('./pic/ico.png')
                lb = QLabel()
                lb.setPixmap(pix)
                lb.resize(20,20)
                lb1 = QLabel(number)
                lb2 = QLabel(start)
                lb3 = QLabel(end)
                lb4 = QLabel(depart_time)
                lb5 = QLabel(arrive_time)
                lb6 = QLabel(rest)
                bt = QPushButton("购买")
                self.bt_dict[bt] = t

                line1 = QWidget()
                line1_layout = QHBoxLayout()
                line1_layout.setAlignment(Qt.AlignCenter)
                line1.setLayout(line1_layout)
                line1_layout.addWidget(lb1)
                line1_layout.addWidget(lb2)
                line1_layout.addWidget(lb)
                line1_layout.addWidget(lb3)

                line2 = QWidget()
                line2_layout = QHBoxLayout()
                line2_layout.setAlignment(Qt.AlignCenter)
                line2.setLayout(line2_layout)
                line2_layout.addWidget(lb4)
                line2_layout.addWidget(QLabel('-->'))
                line2_layout.addWidget(lb5)

                line3 = QWidget()
                line3_layout = QHBoxLayout()
                line3_layout.setAlignment(Qt.AlignCenter)
                line3.setLayout(line3_layout)
                line2_layout.addWidget(QLabel("余票"))
                line2_layout.addWidget(lb6)
                line2_layout.addWidget(bt)

                w = QWidget()
                w.setFixedSize(350,150)
                w.setObjectName("w")
                w.setStyleSheet('QWidget#w{border: 1px solid}')
                t_layout = QVBoxLayout()
                t_layout.setSpacing(0)
                t_layout.setAlignment(Qt.AlignTop)
                w.setLayout(t_layout)
                t_layout.addWidget(line1)
                t_layout.addWidget(line2)
                # t_layout.addWidget(line3)
                self.res_layout.addWidget(w)
        return 1