import pymysql


class SQL():
    name = ''
    id = ''

    def connect(self, host, user, pw, db):
        self.conn = pymysql.connect(host=host, user=user, password=pw, database=db)
        self.cursor = self.conn.cursor()
        self.name = user
        self.get_id()
        print(self.id)
        print("connect")

    def execute(self, str):
        print(str)
        self.cursor.execute(str)
        self.conn.commit()
        return self.cursor.fetchall()

    def get_id(self):
        self.cursor.execute('select ID from Passenger where name=\'' + self.name + '\';')
        self.id = self.cursor.fetchall()
        self.id = self.id[0][0]


if __name__ == '__main__':
    sql = SQL()
    sql.connect('localhost', 'whc', '666', '12306')
    print(sql.execute('select * from Ticket'))
