import sys
import os
import time
import PyQt6
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import mysql.connector as sql
from PyQt6.QtWidgets import QMainWindow,QApplication, QWidget, QTableWidget,QPushButton,QVBoxLayout, QHeaderView, QTableWidgetItem, QLineEdit, QTextEdit, QLabel, QGridLayout, QSizePolicy, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
import pymysql
from PyQt6 import uic
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QFile, QIODevice, QResource
from PyQt6.uic import loadUi
from datetime import datetime
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSizeGrip,QCheckBox
from PyQt6.QtWidgets import QRadioButton



class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Register1.ui', self)
        self.setWindowTitle('Register Window')
        self.resize(400,400)
        self.Status.setText('')
        self.SignUpt.clicked.connect(self.fillinfo)
        map = QPixmap('Screenshot 2024-04-21 at 9.30.01 PM (1).png')
        self.Mainphoto.setPixmap(map)
        map1=QIcon('settings.svg')
        map2 = QIcon('menu.svg')
        map3 = QIcon('maximize.svg')
        map4 = QIcon('minimize.svg')
        map5 = QIcon('home.svg')
        map6= QIcon('x.svg')

        self.Settings.setIcon(map1)
        self.Menu.setIcon(map2)
        self.Maximize.setIcon(map3)
        self.Minimize.setIcon(map4)
        self.Home.setIcon(map5)
        self.Cross.setIcon(map6)

        self.Cross.clicked.connect(lambda: self.close())
        self.Minimize.clicked.connect(lambda :self.showMinimized())
        self.Maximize.clicked.connect(lambda : self.showMaximized())
        QSizeGrip(self.size_grip)



    def fillinfo(self):
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        self.Status.setText('Connection Set')

        if not db.open:
            self.Status.setText('No Connection not found')

        # cursor = db.cursor()
        # cursor.execute("""
        #         CREATE TABLE logindata(
        #             id INT AUTO_INCREMENT PRIMARY KEY,
        #             Username VARCHAR(255),
        #             Password VARCHAR(255),
        #             Email VARCHAR(255),
        #             minlimit VARCHAR(255)
        #         )
        #         """)

        if(self.Passwordt.text()=='' or self.Usernamet.text()=='' or self.Emailt.text()==''):
            self.Status.setText('Not a valid Input')
            return
        if(self.Passwordt.text()!=self.ConfirmPasswordt.text()):
            self.Status.setText('Passwords are not matching')
            return
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        self.Status.setText('Connection Set')

        if not db.open:
            self.Status.setText('No Connection not found')

        cursor = db.cursor()
        data = (self.Usernamet.text(),self.Passwordt.text(),self.Emailt.text(),'1999-01-01')
        insert_query = "INSERT INTO logindata (Username,Password,Email,minlimit) VALUES(%s,%s,%s,%s)"
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()
        self.App=MainApp(self.Usernamet.text())
        self.App.show()

class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Window')
        self.resize(400,400)
        loadUi("Admin1.ui", self)
        map=QPixmap('Screenshot 2024-04-21 at 9.30.01 PM (1).png')
        self.label.setPixmap(map)
        map1=QIcon('settings.svg')
        self.Settings.setIcon(map1)
        map2=QIcon('home.svg')
        self.Home.setIcon(map2)
        map3=QIcon('menu.svg')
        self.Menu.setIcon(map3)
        map4=QIcon('x.svg')
        self.Cross.setIcon(map4)
        self.Minimize.setIcon(QIcon('minimize.svg'))
        self.Maximize.setIcon(QIcon('maximize.svg'))
        self.Cross.clicked.connect(lambda :self.close())
        self.Minimize.clicked.connect(lambda: self.showMinimized())
        self.Maximize.clicked.connect(lambda: self.showMaximized())
        self.SelectedButton.clicked.connect(lambda: self.show_data())
        self.PendingButton.clicked.connect(lambda:self.show_data())
        self.NonSelectedButton.clicked.connect(lambda:self.show_data())


    def show_data(self):
        label = ['Username','Price', 'Quantity', 'FromHour','ToHour', 'Date']
        self.table.setColumnCount(len(label))
        self.table.setHorizontalHeaderLabels(label)
        db = pymysql.connect(host='localhost', user='root', password='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        query = "SELECT Username,Price, Quantity,FromHour,ToHour,Date, Result FROM storagedata"
        cursor.execute(query)
        results = cursor.fetchall()
        self.table.setRowCount(len(results))
        p=0
        self.table.clearContents()
        for i, (username, price, quantity, fm ,to, date, result) in enumerate(results):
            fromDate = self.FromDate.date().toPyDate()
            fromDate = datetime(fromDate.year, fromDate.month, fromDate.day)
            toDate = self.ToDate.date().toPyDate()
            toDate = datetime(toDate.year, toDate.month, toDate.day)
            if ((datetime.strptime(date, '%Y-%m-%d') >= fromDate) and (datetime.strptime(date, '%Y-%m-%d')<=toDate)):
                if((self.SelectedButton.isChecked() and result=="YES") or (self.NonSelectedButton.isChecked() and result=='NO') or (self.PendingButton.isChecked() and result=='PD')):
                    self.table.setItem(p,0,QTableWidgetItem(str(username)))
                    self.table.setItem(p, 1, QTableWidgetItem(str(price)))
                    self.table.setItem(p, 2, QTableWidgetItem(str(quantity)))
                    self.table.setItem(p, 3, QTableWidgetItem(str(fm)))
                    self.table.setItem(p, 4, QTableWidgetItem(str(to)))
                    self.table.setItem(p, 5, QTableWidgetItem(str(date)))
                    self.table.setItem(p,6,QTableWidgetItem(str(result)))
                    p=p+1
        self.table.setRowCount(p)


    # def makeresult(self):
    #     largest=0
    #     db = pymysql.connect(host='localhost', user='root', password='c24466fb', database='SCHOOL')
    #     off=0
    #     for i in range (3):
    #         cursor=db.cursor()
    #         query="SELECT Bid_Value FROM logindata LIMIT 1 OFFSET %s"
    #         cursor.execute(query,(i,))
    #         result=cursor.fetchone()
    #         if(int(result[0]))>largest:
    #             largest=int(result[0])
    #             off=i
    #     cursor = db.cursor()
    #     query = "SELECT Username FROM logindata LIMIT 1 OFFSET %s"
    #     cursor.execute(query, (off,))
    #     result = cursor.fetchone()
    #     username=result[0]
    #     self.label2.setText(f'Winner is the {username} with the {largest} bid')
    #     return

class MainApp(QWidget):
    def __init__(self,username):
        super().__init__()
        self.setWindowTitle(f'Main App{username}')
        self.resize(400,200)
        layout=QVBoxLayout()
        uic.loadUi('MainApp.ui', self)
        self.NoButton.clicked.connect(self.no)
        self.YesButton.clicked.connect(self.yes)
        self.FinalButton.clicked.connect(self.final)
        self.b=False
        self.username=username
        self.SeeResultButton.clicked.connect(self.resultclick)
    def yes(self):
        self.YesButton.hide()
        self.NoButton.hide()
        self.b=True
    def no(self):
        self.From2.hide()
        self.To2.hide()
        self.From3.hide()
        self.To3.hide()
        self.Price2.hide()
        self.Quantity2.hide()
        self.Price3.hide()
        self.Quantity3.hide()
        self.YesButton.hide()
        self.NoButton.hide()
        self.Date2.hide()
        self.Date3.hide()
        self.b=False

    def savedata(self,Price,Quantity,From,To,Date,Result):
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        data = (self.username,Price, Quantity, From,To, Date,Result)
        insert_query = "INSERT INTO storagedata (Username,Price,Quantity,FromHour,ToHour,Date,Result) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()


    def simplecheck(self,From,To):
        if(From>To):
            return True
        if(From>=24 or From<0):
            return True
        if(To>=24 or To<0):
            return True
        return False


    def check(self):
        print(self.From1.text())
        print(self.From1.text)
        print(int(self.From1.text()))
        if(self.simplecheck(int(self.From1.text()),int(self.To1.text()))):
            return False
        if (self.b):
            if( self.simplecheck(int(self.From2.text()),int(self.To2.text()))):
                return False
            if ( self.simplecheck(int(self.From3.text()), int(self.To3.text()))):
                return False
        min_value=str(self.Date1.date().toPyDate().strftime('%Y-%m-%d'))
        print(min)
        if(self.b):
            if(min_value>self.Date2.date().toPyDate().strftime('%Y-%m-%d') ):
                min_value=self.Date2.date().toPyDate().strftime('%Y-%m-%d')
            if (min_value > self.Date3.date().toPyDate().strftime('%Y-%m-%d')):
                min_value =self.Date3.date().toPyDate().strftime('%Y-%m-%d')
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        input_query=f"SELECT minlimit from logindata WHERE Username='{self.username}'"
        cursor.execute(input_query)
        results=cursor.fetchall()
        # I have to update the min date also.
        min_date = datetime.strptime(min_value, '%Y-%m-%d')
        result_date = datetime.strptime(results[0][0], '%Y-%m-%d')
        if(min_date<=result_date):
            print('yes')
            return False
        else:
            print("here is the result")
            print(results[0][0])
            print("here is the min")
            print(min_value)
            db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
            cursor = db.cursor()
            input_query2 = "UPDATE logindata SET minlimit=%s WHERE Username=%s"
            cursor.execute(input_query2, (str(min_value), self.username))
            db.commit()
            db.close()
            return True


    def final(self):
        print('Yes1')
        if(self.check()):
            # db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
            # cursor = db.cursor()
            # cursor.execute("""
            #         CREATE TABLE storagedata(
            #             id INT AUTO_INCREMENT PRIMARY KEY,
            #             Username VARCHAR(255),
            #             Price INT,
            #             Quantity INT,
            #             FromHour INT,
            #             ToHour INT,
            #             Date VARCHAR(255),
            #             Result VARCHAR(255)
            #         )
            #         """)
            self.savedata(self.Price1.text(), self.Quantity1.text(),self.From1.text(),self.To1.text(),self.Date1.date().toPyDate().strftime('%Y-%m-%d'),'NO')
            if(self.b):
                self.savedata(self.Price2.text(), self.Quantity2.text(),self.From2.text(),self.To2.text(),self.Date2.date().toPyDate().strftime('%Y-%m-%d'),'NO')
                self.savedata(self.Price3.text(), self.Quantity3.text(),self.From3.text(),self.To3.text(),self.Date3.date().toPyDate().strftime('%Y-%m-%d'),'NO')
            self.label_2.setText('Bid Updated Successfully')
        else:
            self.label_2.setText('Something gone wrong')

    def resultclick(self):
        self.resultapp=ResultApp(self.username)
        self.resultapp.show()

class ResultApp(QWidget):
    def __init__(self,username):
        super().__init__()
        self.username=username
        self.setWindowTitle('Result Window')
        loadUi("Admin1.ui", self)
        map=QPixmap('Screenshot 2024-04-21 at 9.30.01 PM (1).png')
        self.label.setPixmap(map)
        map1=QIcon('settings.svg')
        self.Settings.setIcon(map1)
        map2=QIcon('home.svg')
        self.Home.setIcon(map2)
        map3=QIcon('menu.svg')
        self.Menu.setIcon(map3)
        map4=QIcon('x.svg')
        self.Cross.setIcon(map4)
        self.Minimize.setIcon(QIcon('minimize.svg'))
        self.Maximize.setIcon(QIcon('maximize.svg'))
        self.Cross.clicked.connect(lambda :self.close())
        self.Minimize.clicked.connect(lambda: self.showMinimized())
        self.Maximize.clicked.connect(lambda: self.showMaximized())
        self.SelectedButton.clicked.connect(lambda: self.show_data())
        self.PendingButton.clicked.connect(lambda:self.show_data())
        self.NonSelectedButton.clicked.connect(lambda:self.show_data())


    def show_data(self):
        label = ['Username','Price', 'Quantity', 'FromHour','ToHour', 'Date']
        self.table.setColumnCount(len(label))
        self.table.setHorizontalHeaderLabels(label)
        db = pymysql.connect(host='localhost', user='root', password='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        query = "SELECT Username,Price, Quantity,FromHour,ToHour,Date, Result FROM storagedata WHERE username=%s"
        cursor.execute(query,self.username)
        results = cursor.fetchall()
        self.table.setRowCount(len(results))
        p=0
        self.table.clearContents()
        for i, (username, price, quantity, fm ,to, date, result) in enumerate(results):
            fromDate = self.FromDate.date().toPyDate()
            fromDate = datetime(fromDate.year, fromDate.month, fromDate.day)
            toDate = self.ToDate.date().toPyDate()
            toDate = datetime(toDate.year, toDate.month, toDate.day)
            if ((datetime.strptime(date, '%Y-%m-%d') >= fromDate) and (datetime.strptime(date, '%Y-%m-%d')<=toDate)):
                if((self.SelectedButton.isChecked() and result=="YES") or (self.NonSelectedButton.isChecked() and result=='NO') or (self.PendingButton.isChecked() and result=='PD')):
                    self.table.setItem(p,0,QTableWidgetItem(str(username)))
                    self.table.setItem(p, 1, QTableWidgetItem(str(price)))
                    self.table.setItem(p, 2, QTableWidgetItem(str(quantity)))
                    self.table.setItem(p, 3, QTableWidgetItem(str(fm)))
                    self.table.setItem(p, 4, QTableWidgetItem(str(to)))
                    self.table.setItem(p, 5, QTableWidgetItem(str(date)))
                    self.table.setItem(p,6,QTableWidgetItem(str(result)))
                    p=p+1
        self.table.setRowCount(p)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Window')
        self.resize(600,200)
        layout=QGridLayout()
        self.setLayout(layout)

        self.labels={}
        self.lineedits={}
        self.labels['Username']=QLabel('Username')
        self.labels['Password']=QLabel('Password')
        self.labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

        self.lineedits['Username']=QLineEdit()
        self.lineedits['Password']=QLineEdit()
        self.lineedits['Username'].setPlaceholderText('Username')
        self.lineedits['Password'].setPlaceholderText('Password')
        self.lineedits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.labels['Username'],   0, 0, 1 , 1)
        layout.addWidget(self.lineedits['Username'],    0, 1, 1, 3)
        layout.addWidget(self.labels['Password'],   1, 0, 1,1)
        layout.addWidget(self.lineedits['Password'],    1,1,1,3)

        self.button=QPushButton('Login')
        layout.addWidget(self.button, 2, 2, 1,1)
        self.status=QLabel('')
        layout.addWidget(self.status,2,0,1,2)

        self.button.clicked.connect(self.checkCredentials)
        self.button2=QPushButton('Not a member? Sign Up')
        layout.addWidget(self.button2, 3,2,1,1)
        self.button2.clicked.connect(self.open)

    def open(self):
        self.myregister=RegisterWindow()
        self.myregister.show()

    def checkCredentials(self):
        username = self.lineedits['Username'].text()
        password = self.lineedits['Password'].text()
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        query = "SELECT * FROM logindata WHERE Username=%s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            if result[2] == password:
                self.status.setText("Password is correct")
                if not (username =="Admin"):
                    self.app1 = MainApp(username)
                    self.app1.show()
                    self.close()
                else:
                    self.app1=AdminApp()
                    self.app1.show()
                    self.close()
            else:
                self.status.setText("Password is not correct")
        else:
            self.status.setText("Username not found")

        cursor.close()
        db.close()



app=QApplication(sys.argv)
QResource.registerResource("resources.qrc")
app.setStyle('Fusion')
darkPalette = QPalette()
darkPalette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
darkPalette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
darkPalette.setColor(QPalette.ColorRole.Base, QColor(4, 42, 433))
darkPalette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
darkPalette.setColor(QPalette.ColorRole.ToolTipBase,QColor(255, 255, 255))
darkPalette.setColor(QPalette.ColorRole.ToolTipText,QColor(255, 255, 255))
darkPalette.setColor(QPalette.ColorRole.Text,QColor(255, 255, 255))
darkPalette.setColor(QPalette.ColorRole.Dark, QColor(35, 35, 35))
darkPalette.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
darkPalette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 533))
darkPalette.setColor(QPalette.ColorRole.ButtonText,QColor(255, 255, 255))
darkPalette.setColor(QPalette.ColorRole.BrightText,QColor(255, 255, 255))
darkPalette.setColor(QPalette.ColorRole.Link, QColor(42, 10, 2100))
darkPalette.setColor(QPalette.ColorRole.Highlight, QColor(42, 10, 210))
darkPalette.setColor(QPalette.ColorRole.HighlightedText,QColor(255, 255, 255))
darkPalette.setColor(QPalette.ColorRole.PlaceholderText, QColor(127, 127, 127))
app.setPalette(darkPalette)
window=LoginWindow()
window.show()
app.exec()




# Add the Register Window.
# Three boxes to enter the value 1. Dollar per MWh (Price) 2.Quantity (MWh) 3.Continous Hours (0-23) 4. Date(it cannot be previous date and today date) [only for 2 decimal points].
# Do you want to bid for one block or multiple blocks.[Restricted to 3 blocks] (12 boxes) (1,2 are not allowed).
# Put a geographic graph with 6 nodes and name them and put factory symbols on them.
# Make background dark.
# Users can also see his Price, Quantity and hour.
# Result page for the User.
# Add the .ui file make it executable file.
# https://www.youtube.com/watch?v=20ed0Ytkxuw

# Resizing of the stuffs.
# Result Page for User mei filters add karne hai.
# Executable file banani hai.
# Graph banna hai.
# Achha ui banna hai.






