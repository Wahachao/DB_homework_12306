from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import sys
from SQL import *


class User(QWidget):
    def __init__(self, sql):
        super(User, self).__init__()
        self.sql = sql
        self.parse()
        self.ini()

    def parse(self):
        self.user_info = self.sql.execute(f"select Name,ID,Phone,Gender from Passenger where ID={self.sql.id};")

        self.user_info = self.user_info[0]
        print(self.user_info)
        self.name = self.user_info[0]
        self.id = self.user_info[1]
        print(self.id)
        self.phone = self.user_info[2]
        self.gender = self.user_info[3]
    def ini(self):
        self.resize(450, 840)
        self.bt1 = QPushButton("更改资料")
        self.bt1.clicked.connect(self.slide)

        layout = QVBoxLayout()
        self.lb_name = QLabel(f"姓名: {self.name}")
        self.label_id = QLabel(f"证件号: {self.id}")
        self.label_phone = QLabel(f"联系方式: {self.phone}")
        self.label_gender = QLabel(f"性别: {self.gender}")
        layout.addWidget(self.lb_name)
        layout.addWidget(self.label_id)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.label_gender)
        layout.addWidget(self.bt1)
        layout.setAlignment(Qt.AlignTop)

        self.user = QWidget()
        self.user.setLayout(layout)

        layout2 = QGridLayout()
        layout2.setAlignment(Qt.AlignTop)
        layout2.addWidget(QLabel("证件号"), 1, 1)
        layout2.addWidget(QLabel("姓名"), 2, 1)
        layout2.addWidget(QLabel("联系方式"), 3, 1)
        layout2.addWidget(QLabel("性别"), 4, 1)
        self.t1 = QLineEdit()
        self.t1.setText(self.name)
        self.t3 = QLineEdit()
        self.t3.setText(self.phone)
        self.t4 = QComboBox()
        self.t4.addItems(['male', 'female'])
        layout2.addWidget(QLabel(self.id), 1, 2)
        layout2.addWidget(self.t1, 2, 2)
        layout2.addWidget(self.t3, 3, 2)
        layout2.addWidget(self.t4, 4, 2)
        self.bt = QPushButton("确定更改")
        layout2.addWidget(self.bt, 5, 1, 5, 2)
        self.bt.clicked.connect(self.change)
        self.ch = QWidget()
        self.ch.setLayout(layout2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.user)
        main_layout.addWidget(self.ch)
        self.ch.hide()
        self.user.show()
        self.setLayout(main_layout)

    def slide(self):
        self.user.hide()
        self.ch.show()

    def change(self):
        str = f'update Passenger set Name = \'{self.t1.text()}\',Phone=\'{self.t3.text()}\',Gender=\'{self.t4.currentText()}\' where ID=\'{self.id}\';'
        self.sql.execute(str)
        self.refresh()
        self.ch.hide()
        print('hide')

    def refresh(self):
        print('select * from Passenger where name = \'' + self.name + '\'')
        self.user_info = self.sql.execute('select * from Passenger where name = \'' + self.name + '\'')[0]
        self.parse()
        print("refreshing...")
        self.lb_name.setText(f"姓名: {self.name}")
        self.label_id.setText(f"证件号: {self.id}")
        self.label_phone.setText(f"联系方式: {self.phone}")
        self.label_gender.setText(f"性别: {self.gender}")
        print(self.user_info)

        self.user.show()
