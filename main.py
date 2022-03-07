import sqlite3
from sqlite3 import Error
import sys
from PyQt6.QtWidgets import QApplication,QWidget,QBoxLayout,QVBoxLayout, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6 import uic

# DB SETUP:
# creates or opens db
db = sqlite3.connect("records.db")
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords(
        id INTEGER PRIMARY KEY,
        service TEXT,
        username TEXT,
        email TEXT,
        password TEXT
    )
''')
db.commit()

class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('result.ui',self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui',self)
        self.error_1.hide()
        self.search.clicked.connect(self.db_check)

    def search_db(self,service):
        # pull up list of DB services
        cursor.execute("""SELECT service,username,email,password FROM passwords WHERE service=?""", (service,))
        # print(cursor.fetchone())
        return cursor.fetchone()
    def db_check(self):
        cursor.execute("""SELECT service FROM passwords""")
        db_services = cursor.fetchall()
        print(db_services)
        if self.lineEdit.text() in db_services[0]:
            self.result = db_services[0][0]
            print('yeah its here', db_services[0][0])
            self.result_window = ResultWindow()
            self.result_window.show()


        else:
            self.error_1.show()




class LogInWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui',self)
        self.error.hide()
        self.name_input = self.lineEdit
        self.pw_input = self.lineEdit_2
        self.pushButton.clicked.connect(self.log_in)

    def log_in(self):
        if self.name_input.text() == "temp" and self.pw_input.text() == "1234":
            self.w = MainWindow()
            self.w.show()
            self.destroy()
        else:
            self.error.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = LogInWindow()
    myApp.show()
    app.exec()




# # insert values
# service = "Facebook"
# username = "tempuser"
# email = "send.your.money.to.me@hotmail.com"
# password = 'temp'
#
# cursor.execute("""
#     INSERT INTO passwords(service, username, email, password)
#     VALUES(?,?,?,?)""", (service,username,email,password)
# )
# db.commit()

# db query
# cursor.execute("""SELECT service,username,email,password FROM passwords WHERE service=?""",(service,))
# select = cursor.fetchall()
