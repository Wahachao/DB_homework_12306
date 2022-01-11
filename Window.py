from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qt_material import apply_stylesheet
import sys
from Search import *
from Order import *
from SQL import *
from User import *
from Result import *


class Window(QWidget):
    def __init__(self, sql):
        super(Window, self).__init__()
        self.sql = sql
        self.ini_ui()

    def ini_ui(self):
        self.setFixedSize(450, 900)

        palette1 = QtGui.QPalette()
        palette1.setColor(self.backgroundRole(), QColor(0, 0, 0))

        self.search = Search(sql=self.sql)
        self.search.search_bt.clicked.connect(self.search_func)
        # self.add_shadow(self.search)

        self.order = Order(sql)
        self.order.set()

        self.order.hide()

        self.user = User(sql)
        self.user.hide()

        self.banner_bt1 = QPushButton()
        self.banner_bt1.setText("首页")
        self.banner_bt1.setFixedSize(100, 60)

        self.banner_bt2 = QPushButton()
        self.banner_bt2.setText("订单")
        self.banner_bt2.setFixedSize(100, 60)

        self.banner_bt3 = QPushButton()
        self.banner_bt3.setText("我的")
        self.banner_bt3.setFixedSize(100, 60)

        self.banner_bt1.clicked.connect(self.show_search)
        self.banner_bt2.clicked.connect(self.show_order)
        self.banner_bt3.clicked.connect(self.show_info)

        self.banner = QWidget()
        self.banner.setObjectName('banner')
        self.banner.setStyleSheet("QWidget#banner{border:1px};")
        self.banner_layout = QHBoxLayout()
        self.banner.setContentsMargins(0, 0, 0, 0)
        self.banner.setLayout(self.banner_layout)
        self.banner_layout.addWidget(self.banner_bt1)
        self.banner_layout.addWidget(self.banner_bt2)
        self.banner_layout.addWidget(self.banner_bt3)

        self.main_layout = QVBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.search, 10)
        self.main_layout.addWidget(self.order, 10)
        self.main_layout.addWidget(self.user, 10)
        self.main_layout.addWidget(self.banner, 1)

    def search_func(self):
        search_sentence = self.search.search()
        res = sql.execute(search_sentence)
        print(self.search.ret_str())
        self.result = Result(sql=self.sql, res=res, str=self.search.ret_str())
        self.set_bt()
        self.result.ret_bt.clicked.connect(self.ret)
        self.main_layout.removeWidget(self.banner)
        self.main_layout.addWidget(self.result)
        self.main_layout.addWidget(self.banner)

        self.search.hide()
        self.result.show()

    def ret(self):
        self.result.hide()
        self.search.show()

    def set_bt(self):
        for bt in self.result.bt_dict.keys():
            bt.clicked.connect(partial(self.buy_clicked, bt))



    def buy_clicked(self, bt):
        print('buying...')
        t = self.result.bt_dict[bt]
        rest = t[5]
        if rest == 0:
            print("fail to buy")
            QMessageBox.information(self, "通知", "没有余票", QMessageBox.Yes, QMessageBox.Yes)
        else:
            if self.buy(t) == 1:
                print('succeed to buy')
                QMessageBox.information(self, "通知", "购买成功", QMessageBox.Yes, QMessageBox.Yes)
                self.result.hide()
                self.order.refresh()
                self.order.show()



    def buy(self, t):
        number = t[0]
        seat_taken = self.sql.execute(f"select coach,seat from `Order` where number='{number}';")
        print(seat_taken)
        coach, seat = (random.randint(1, 14), random.randint(1, 17))
        while (coach, seat) in seat_taken:
            coach, seat = (random.randint(1, 14), random.randint(1, 17))
        ticket_id_exist = self.sql.execute(f"select ticket_id from `Order` where number='{number}';")
        ticket_id = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
            random.randint(0, 9))
        if ticket_id in ticket_id_exist:
            ticket_id = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
                random.randint(0, 9))
        info = f"('{ticket_id}','{number}','{self.sql.id}',{coach},{seat})"
        # print(info)
        sql_sentence = f"insert into `Order` (`ticket_id`,`number`,`ID`,`coach`,`seat`) value {info};"
        self.sql.execute(sql_sentence)
        self.sql.execute(f"update Ticket set rest=rest-1 where number='{number}'")
        return 1

    def show_search(self):
        # print('show search')
        self.resize(450, 900)
        self.search.show()
        self.order.hide()
        self.user.hide()

    def show_order(self):
        self.resize(450, 900)
        self.search.hide()
        self.user.hide()
        self.order.refresh()
        self.order.show()

    def show_info(self):
        self.resize(450, 900)
        self.search.hide()
        self.order.hide()
        self.user.show()

    def add_shadow(self, main_widget):
        # 添加阴影
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(30)  # 阴影半径
        self.effect_shadow.setColor(QtCore.Qt.gray)  # 阴影颜色
        main_widget.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中


if __name__ == '__main__':
    sql = SQL()
    sql.connect('localhost', 'root', 'Whc00119', '12306')
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    w = Window(sql)
    w.show()
    sys.exit(app.exec_())
