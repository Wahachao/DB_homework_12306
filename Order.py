from functools import partial

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
from qt_material import apply_stylesheet
import sys
from SQL import *


class Order(QWidget):
    def __init__(self, sql):
        super(Order, self).__init__()
        self.sql = sql
        self.bt_dict = {}
        self.w_dict ={}
        self.ini()
        self.resize(450, 840)

    def set(self):
        self.order_list = self.sql.execute(
            f'select distinct ticket_id, Ticket.number, departure, destination, depart_time, arrive_time,coach,seat from `Order`,Ticket where ID = \'{self.sql.id}\' and Ticket.number=`Order`.number;')

    def ini(self):
        self.order_layout = QHBoxLayout()
        self.setLayout(self.order_layout)
        self.set()
        self.add()

    def add(self):
        self.list_layout = QVBoxLayout()
        for t in self.order_list:
            t_layout = QGridLayout()
            t_layout.setSpacing(8)

            t_layout.addWidget(QLabel(t[1]), 1, 1)
            t_layout.addWidget(QLabel(f"{t[2]}-->{t[3]}"), 1, 2)
            t_layout.addWidget(QLabel("订单号: " + str(t[0])), 1, 6)
            t_layout.addWidget(QLabel(str(t[4])[:-3] + ' -- ' + str(t[5])[:-3]), 2, 1, 2, 6)
            # t_layout.addWidget(QLabel(str(t[5]).split(' ')[1][:-3]), 1, 4)
            t_layout.addWidget(QLabel("乘车人"), 4, 1)
            t_layout.addWidget(QLabel(self.sql.id), 4, 2)
            t_layout.addWidget(QLabel("车厢号"), 4, 3)
            t_layout.addWidget(QLabel(str(t[6])), 4, 4)
            t_layout.addWidget(QLabel("座位号"), 4, 5)
            t_layout.addWidget(QLabel(str(t[7])), 4, 6)
            self.bt = QPushButton("退票")
            t_layout.addWidget(self.bt,5,1)
            self.bt_dict[self.bt] = str(t[0])

            w = QWidget()
            w.setFixedSize(370, 130)
            w.setObjectName('w')
            w.setStyleSheet('QWidget#w{border: 1px solid}')
            w.setLayout(t_layout)
            self.w_dict[self.bt] = w
            self.list_layout.addWidget(w)

        self.list = QWidget()
        self.list.setLayout(self.list_layout)
        self.list_layout.setSpacing(20)
        self.list_layout.setAlignment(Qt.AlignTop)
        self.order_layout.addWidget(self.list)
        self.set_ret_bt()

    def refresh(self):
        item_list = list(range(self.order_layout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.order_layout.itemAt(i)
            self.order_layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        self.set()
        self.add()

    def set_ret_bt(self):
        for bt in self.bt_dict.keys():
            bt.clicked.connect(lambda :self.ret_clicked(self.bt))

    def ret_clicked(self, bt):
        print("returning...")
        ticket_id = self.bt_dict[bt]
        print(ticket_id)
        self.sql.execute(f"delete from `Order` where ticket_id=\'{ticket_id}\';")
        QMessageBox.information(self, "通知", "退票成功", QMessageBox.Yes, QMessageBox.Yes)
        number = self.sql.execute(f"select number from `Order` where ticket_id=\'{ticket_id}\';")
        self.sql.execute(f"update Ticket set rest=rest+1 where number='{number}'")
        self.w_dict[bt].hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sql = SQL()
    sql.connect('localhost', 'root', 'Whc00119', '12306')
    order = sql.execute('select * from `Order` where ID = \'005\'')
    w = Order(sql)
    w.show()
    sys.exit(app.exec_())
