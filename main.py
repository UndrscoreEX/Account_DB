import sqlite3
from sqlite3 import Error
import sys
from PyQt6.QtWidgets import QApplication,QWidget,QBoxLayout,QVBoxLayout, QMainWindow,QLineEdit
from PyQt6.QtCore import Qt
from PyQt6 import uic
from PyQt6 import QtWidgets


#   to do:
#   add enter key press actions
#   encryption
#   add username/pw change
#   check that input email is an email

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
    def __init__(self,record):
        super().__init__()
        self.record = record
        uic.loadUi('result.ui',self)
        cursor.execute("""SELECT service, username, email, password FROM passwords WHERE service = ?""",(self.record,))
        self.full_record = cursor.fetchone()
        print(self.full_record)
        self.text = f"""    \tService: {self.full_record[0]}
                        Username: {self.full_record[1]}
                        Email: {self.full_record[2]}
                        Passwords: {self.full_record[3]}"""
        self.textEdit.setText(self.text)
        self.label.setText(f"Record for: {self.full_record[0]}")
        self.pushButton.clicked.connect(self.end)

    def end(self):
        # the self.destroy callback won't work from the __init__
        self.destroy()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui',self)
        self.error_1.hide()
        self.search.clicked.connect(self.pull_up_record)
        self.pushButton_2.clicked.connect(self.delete_from_db)
        self.pushButton.clicked.connect(self.create_record)
        self.error_2.hide()
        self.lineEdit.setPlaceholderText('facebook, gmail, ...')
        # self.initUI()


    def search_db(self):
        # check if entry exists - general
        self.error_2.hide()
        cursor.execute("""SELECT service FROM passwords""")
        db_services = cursor.fetchall()

        # the query result comes out as tuples.
        db_services = [x[0] for x in db_services]
        print("SV check: the services are:",db_services)
        return db_services

    def delete_from_db(self):
    #     delete entry from db
        db_services = self.search_db()
        if self.lineEdit.text().lower() in db_services:
            print('trying to delete')
            cursor.execute("""
            DELETE FROM passwords WHERE service=?""", (self.lineEdit.text().lower(),))
            db.commit()
            print("deleted")
            self.error_2.show()

        else:
            self.error_1.show()
            print("not there")

    def pull_up_record(self):
        # pull up list of DB services
        db_services = self.search_db()
        if self.lineEdit.text().lower() in db_services:
            self.error_1.hide()
            print('yeah its here')
            self.result = self.lineEdit.text().lower()
            self.result_window = ResultWindow(self.result)
            self.result_window.show()
        else:
            self.error_1.show()

    def create_record(self):
        #create a new record
        db_services = self.search_db()
        print(db_services)
        self.add_record = AddWindow(db_services)
        self.add_record.show()

    def enter_key_press(self, event):
        print('asdf')

class AddWindow(QWidget):
    def __init__(self, services):
        super().__init__()
        uic.loadUi('add_entry.ui', self)
        self.services = services
        self.error.hide()
        self.pushButton.clicked.connect(self.update_db)
        self.pushButton_2.clicked.connect(self.end)
        self.label_6.hide()
        # setting the order
        self.setTabOrder(self.input1serv, self.input2usr)
        self.setTabOrder(self.input2usr, self.input3email)
        self.setTabOrder(self.input3email, self.input4pw)
        self.setTabOrder(self.input4pw, self.pushButton)
        self.input1serv.setPlaceholderText('facebook')
        self.input2usr.setPlaceholderText('ethan')
        self.input3email.setPlaceholderText('somethingsomething@gmail.com')
        self.input4pw.setPlaceholderText('temp1234')



    def end(self):
        # the self.destroy callback won't work from the __init__
        self.destroy()

    def update_db(self):
        service_input = self.input1serv.text().lower()
        username = self.input2usr.text()
        email = self.input3email.text()
        password = self.input4pw.text()
        if service_input not in self.services:

            if service_input not in self.services and service_input and password:
                # allows the adding of a new record if there is a clean service and a service + pw entered.
                cursor.execute("""
                INSERT INTO passwords(service, username, email, password)
                VALUES(?,?,?,?)
                """, (service_input,username,email,password))

                # record_id = cursor.lastrowid
                print('added')
                db.commit()
                cursor.execute("""SELECT * FROM passwords""")
                print(cursor.fetchall())

                self.error.hide()
                self.label_6.show()

            else:
                print('no pw/service entered')
                self.error.show()
        else:
            print('already a record for that')
            self.error.show()

class LogInWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui',self)
        self.error.hide()
        self.name_input = self.lineEdit
        self.pw_input = self.lineEdit_2
        self.pushButton.clicked.connect(self.log_in)
        self.keyPressEvent= self.keypressed
    def log_in(self):
        # After the username and pw function is set, we can check them here (in a better way than a simple == statement)
        if self.name_input.text() == "" and self.pw_input.text() == "":
            self.w = MainWindow()
            self.w.show()
            self.destroy()
        else:
            self.error.show()


    # still trying to figure out the enter keypress to click the login button.
    # def keypressed(self,event):
    #     if event.key() == QtCore.Qt.Key_Enter:
    #         self.log_in()

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
