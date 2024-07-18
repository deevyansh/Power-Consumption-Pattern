import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow,QStackedWidget
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QLabel,QPushButton,QRadioButton,QVBoxLayout,QHBoxLayout,QGridLayout,QLineEdit,QSizePolicy,QLabel,QTableWidget,QTableWidgetItem,QHeaderView
from PyQt6.QtGui import QPixmap,QIcon,QColor,QPalette,QImage
from PyQt6.QtCore import QPropertyAnimation,QUrl,Qt
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from datetime import datetime
from marketalgo import economic
import os
import sqlite3
import cv2
from PyQt6.QtCore import QTimer
import pandas as pd

username=""
button=[]
a=""
loginapp=""
registerapp=""
mainapp=""
showapp=""
resultapp=""
adminapp=""
makedecision=''

# path="/Users/deevyanshkhadria/Downloads/COL/graph_simulation_app"
print("I am working in the directory   - ",os.getcwd())
path=str(input("Please enter the path to the app folder from this directory"))


def open1():
    global a
    global loginapp

    a.setCurrentIndex(1)
    button[0].hide()
    button[2].hide()
    button[3].hide()
    button[1].show()
    button[4].hide()
    button[1].clicked.connect(lambda: open2())
    loginapp.start()
def open2():
    global a
    a.setCurrentIndex(2)
    global button
    global registerapp
    button = button
    button[1].hide()
    button[2].hide()
    button[3].hide()
    button[0].show()
    button[4].hide()
    button[0].setText('Login Here')
    button[0].clicked.connect(lambda: open1())
    registerapp.start()
def open3():
    global a
    a.setCurrentIndex(3)
    global button
    global username
    global mainapp
    button[0].show()
    button[0].setText('Logout')
    button[1].show()
    button[2].show()
    button[2].setText('Show my results')
    button[3].show()
    button[0].clicked.connect(lambda: open1())
    button[1].clicked.connect(lambda: open2())
    button[3].setText('Show the available dates')
    button[3].clicked.connect(lambda: open4())
    button[4].show()
    button[4].setPixmap(QPixmap('icons/downlaod.jpg'))
    button[2].clicked.connect(lambda: open5())
    mainapp.start()
def open4():
    global a
    global showapp
    a.setCurrentIndex(4)
    global button
    button[0].clicked.connect(lambda: open1())
    button[1].clicked.connect(lambda: open2())
    button[2].show()
    button[2].clicked.connect(lambda: open3())
    button[3].hide()
    button[2].setText('Submit the Bid')
    showapp.start()
def open5():
    global a
    a.setCurrentIndex(5)
    global button
    button[0].show()
    button[1].show()
    button[2].show()
    button[3].show()
    button[3].setText('Show available Dates')
    button[3].clicked.connect(lambda: open4())
    button[4].show()
    button[4].setPixmap(QPixmap('icons/downlaod.jpg'))
    button[0].clicked.connect(lambda: open1())
    button[1].clicked.connect(lambda: open2())
    button[2].setText('Submit the Bid')
    button[2].clicked.connect(lambda: open3())
    global resultapp
    resultapp.start()
def open6():
    global a
    a.setCurrentIndex(6)
    global button
    global adminapp
    button[0].show()
    button[0].setText('Logout')
    button[1].show()
    button[2].hide()
    button[3].setText('Clear the Market')
    button[3].show()
    button[3].clicked.connect(lambda: open7())
    button[4].setPixmap(QPixmap('icons/downlaod.jpg'))
    button[4].show()
    button[0].clicked.connect(lambda: open1())
    button[1].clicked.connect(lambda: open2())
    adminapp.start()
def open7():
    global a
    global button
    global makedecision
    button = button
    button[2].hide()
    button[3].show()
    button[3].setText('SEE MORE BID')
    button[3].clicked.connect(open6)  # admin app wala laga denge
    a.setCurrentIndex(7)
    makedecision.start()

class MakeDecision(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(path,"AllUI/MakeDec.ui"), self)
        global a
        self.MakeResult.clicked.connect(self.do1)
        self.pushButton_2.clicked.connect(self.do2)

    def start(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.Hour.setText('')
        self.Date1.setDate(datetime.today())
        self.Power.setText('')
        self.Hour.setText('')
        self.label.setStyleSheet('color: rgb(0,0,0)')
        self.label_2.setStyleSheet('color: rgb(0,0,0)')
        self.LBL3.setStyleSheet('color: rgb(0,0,0)')
        self.LBL4.setStyleSheet('color: rgb(0,0,0)')

    def check(self,list):
        sum=0
        for i in range (len(list)):
            sum+=list[i]
        return sum
    def do1(self):
        if((self.Hour.text()=='') & (self.Power.text()=='')):
            self.label_4.setText('Something gone wrong')
            return
        else:
            PD = float(self.Power.text())
            db = sqlite3.connect(os.path.join(path,'SCHOOL.db'))
            cursor=db.cursor()
            input_query1='SELECT * FROM storagedata WHERE FROMHour= ? AND Result= ? AND Date= ?'
            data1=(self.Hour.text(),'PD',self.Date1.date().toPyDate().strftime(format='%Y-%m-%d'))
            cursor.execute(input_query1,data1)
            results=cursor.fetchall()
            if(len(results)==0):
                self.LBL4.setText('No Remaining Bids for this date')
                return
            print(results)
            username_list=['' for _ in range (0,len(results))]
            price_list=[0 for _ in range (0,len(results))]
            PD_max=[0 for _ in range (0,len(results))]
            PD_min=[0 for _ in range (0,len(results))]
            for i,(id,username,price,quantity,fromhour,tohour,date,result,temp) in enumerate(results):
                username_list[i]=str(username)
                price_list[i]=float(price)
                PD_min[i]=0
                PD_max[i]=float(quantity)
            if (self.check(PD_max) <PD):
                self.table.clear()
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                self.LBL4.setText('No enough Bids..')
                return
            (A,B,C,D)=economic(PD,PD_min,PD_max,price_list)
            for i in range (len(B)):
                B[i]=round(float(B[i]),4)
            self.LBL4.setStyleSheet('color : rgba(255,255,255)')
            self.table.setColumnCount(4)
            self.table.setRowCount(len(C))
            self.table.setHorizontalHeaderLabels(['Market Participant ID','Price','Quantity Bid','QuantityAccepted'])
            self.table.setColumnWidth(0,150)
            self.table.setColumnWidth(2,150)
            self.table.setColumnWidth(1,150)
            self.table.setColumnWidth(3,150)
            for i in range (len(C)):
                self.table.setItem(i,0,QTableWidgetItem(str(results[C[i]][1])))
                self.table.setItem(i, 1, QTableWidgetItem(str(results[C[i]][2])))
                self.table.setItem(i, 2, QTableWidgetItem(str(results[C[i]][3])))
                self.table.setItem(i, 3, QTableWidgetItem(str(B[C[i]])))

            self.LBL4.setText('Market Clear Algorithm successfully completed..')
            self.B=B
            self.list=username_list
            for i in range(self.table.rowCount()):
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j);
                    if item:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    def do2(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.LBL4.setText('Market is Cleared')

        db = sqlite3.connect(os.path.join(path,'SCHOOL.db'))
        cursor = db.cursor()
        for i in range(len(self.B)):
            print('Processing index', i)
            print(self.list[i])
            input_query1 = 'UPDATE storagedata SET Result=?, Quantity_selected=? WHERE Username=?'

            if self.B[i] != 0:
                data1 = ("YES", self.B[i], self.list[i])
                print('Updating row with YES:', data1)
            else:
                data1 = ("NO", self.B[i], self.list[i])
                print('Updating row with NO:', data1)
            cursor.execute(input_query1, data1)

        db.commit()
        cursor.close()
class showDates(QWidget):
    def __init__(self):
        super().__init__()
        global a
        global username
        layout=QVBoxLayout()
        self.setLayout(layout)
        self.table=QTableWidget()
        self.b=QPushButton('CHECK THE TABLE NOW')
        self.label=QLabel('All the available dates you can bid for')

        self.label.setStyleSheet('color: rgb(0,0,0)')
        layout.addWidget(self.label)
        layout.addWidget(self.table)
        layout.addWidget(self.b)
        self.b.clicked.connect(lambda: self.do1())
    def start(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.clear()
        self.b.show()


    def do1(self):
        self.b.hide()
        global username
        MODE = username
        if (MODE == 'ST' or MODE == 'QF' or MODE == ''):
            MODE = 'VA'
        db = sqlite3.connect(os.path.join(path,'SCHOOL.db'))
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM {MODE}data ORDER BY Month ASC,Date ASC,Hour ASC')
        results = cursor.fetchall()
        self.table.setRowCount(len(results))
        self.table.setColumnCount(5)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 180)
        self.table.setColumnWidth(0, 100)
        self.table.setHorizontalHeaderLabels(['Month', 'Date', 'Fromhour', 'Tohour', 'Quantity(KW)'])
        for i, (month, date, hour, covariance, value) in enumerate(results):
            value = round(float(value), 4)
            self.table.setItem(i, 0, QTableWidgetItem(str(month)))
            self.table.setItem(i, 1, QTableWidgetItem(str(date)))
            self.table.setItem(i, 2, QTableWidgetItem(str(hour)))
            self.table.setItem(i, 3, QTableWidgetItem(str(hour + 1)))
            self.table.setItem(i, 4, QTableWidgetItem(str(value)))
        for i in range (self.table.rowCount()):
            for j in range (self.table.columnCount()):
                item = self.table.item(i,j);
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        global a
        global username
        self.setWindowTitle('Login Window')
        layout = QGridLayout()
        self.setLayout(layout)
        self.labels = {}
        self.lineedits = {}
        self.labels['Username'] = QLabel('Username')
        self.labels['Password'] = QLabel('Password')
        self.labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineedits['Username'] = QLineEdit()
        self.lineedits['Password'] = QLineEdit()
        self.lineedits['Username'].setPlaceholderText('Username')
        self.lineedits['Password'].setPlaceholderText('Password')
        self.labels['Username'].setStyleSheet('color: white')
        self.labels['Password'].setStyleSheet('color: white')
        self.lineedits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.labels['Username'], 9, 1, 1, 1)
        layout.addWidget(self.lineedits['Username'], 9, 3, 1, 4)
        layout.addWidget(self.labels['Password'], 10, 1, 1, 1)
        layout.addWidget(self.lineedits['Password'], 10, 3, 1, 4)

        self.button = QPushButton('Login')
        layout.addWidget(self.button, 11, 2, 1, 4)
        self.status = QLabel('')
        self.status.setStyleSheet('color :rgb(255,255,255)')
        layout.addWidget(self.status, 14, 0, 1, 4)

        self.video_label = QLabel()
        layout.addWidget(self.video_label, 0, 0, 8, 8)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button.clicked.connect(self.checkCredentials)
        self.button2 = QPushButton('Not a member? Sign Up')
        layout.addWidget(self.button2, 13, 2, 1, 4)
        self.button2.clicked.connect(lambda: open2())
        self.video_path = os.path.join(path,'icons/Screen Recording 2024-05-19 at 11.52.05 AM (1).mp4')
        self.cap = cv2.VideoCapture(self.video_path)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(15)
        self.desired_width = 650
        self.desired_height = 400

    def start(self):
        self.status.setText('')
        self.lineedits['Username'].setText('')
        self.lineedits['Password'].setText('')
        self.labels['Username'].setStyleSheet('color: rgb(0,0,0)')
        self.labels['Password'].setStyleSheet('color: rgb(0,0,0)')
        self.status.setStyleSheet('color: rgb(0,0,0)')

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
                # Convert the frame to QImage
            frame = cv2.resize(frame, (self.desired_width, self.desired_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_image))
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


    def check_position(self, position):
        total_duration = self.mediaplayer.duration()
        if total_duration > 0:
            target_position = 0.8 * total_duration  # 80% of the total duration
            if position >= target_position:
                self.mediaplayer.setPosition(0)

    def checkCredentials(self):
        print("hello i am here in login checking credentials")
        global username
        username = self.lineedits['Username'].text()
        print("USERNAME",username)
        password = self.lineedits['Password'].text()
        db=sqlite3.connect(os.path.join(path,'SCHOOL.db'))
        cursor = db.cursor()
        query = "SELECT * FROM logindata WHERE Username=?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            if result[2] == password:
                self.status.setText("Password is correct")
                if not (username == "Admin"):
                    print("username signning up", username)
                    open3()
                else:
                    print("username signning up", username)
                    open6()
            else:
                self.status.setText("Password is not correct")
        else:
            self.status.setText("Username not found")
        cursor.close()
        db.close()
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        global a
        loadUi(os.path.join(path,'AllUI/Register1.ui'), self)
        self.Status.setStyleSheet('color: rgb(255,255,255)')
        self.SignUpt.clicked.connect(self.fillinfo)
        self.Mainphoto.setPixmap(QPixmap(os.path.join(path,'icons/Screenshot 2024-04-21 at 9.30.01 PM (1).png')))

    def start(self):
        self.Username.setStyleSheet('color: rgb(0,0,0)')
        self.Email.setStyleSheet('color: rgb(0,0,0)')
        self.Password.setStyleSheet('color: rgb(0,0,0)')
        self.Status.setStyleSheet('color: rgb(0,0,0)')
        self.ConfirmPassword.setStyleSheet('color: rgb(0,0,0)')
        self.Status.setText('')

    def fillinfo(self):
        db=sqlite3.connect(os.path.join(path,'SCHOOL.db'))
        cursor = db.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS logindata(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    Username VARCHAR(255),
                    Password VARCHAR(255),
                    Email VARCHAR(255),
                    minlimit VARCHAR(255)
                )
                """)
        if(self.Passwordt.text()=='' or self.Usernamet.text()=='' or self.Emailt.text()==''):
            self.Status.setText('Not a valid Input')
            return
        if(self.Passwordt.text()!=self.ConfirmPasswordt.text()):
            self.Status.setText('Passwords are not matching')
            return
        cursor = db.cursor()
        data = (self.Usernamet.text(),self.Passwordt.text(),self.Emailt.text(),'1999-01-01')
        insert_query = "INSERT INTO logindata (Username,Password,Email,minlimit) VALUES(?,?,?,?)"
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()
        open1()
class ResultApp(QWidget):
    def __init__(self):
        super().__init__()
        global a
        global username
        self.setWindowTitle('Result Window')
        self.resize(700, 700)
        loadUi(os.path.join(path,"AllUI/Admin1.ui"), self)
        self.SelectedButton.clicked.connect(lambda: self.show_data())
        self.PendingButton.clicked.connect(lambda:self.show_data())
        self.NonSelectedButton.clicked.connect(lambda:self.show_data())
        self.FromDate.dateChanged.connect(lambda:self.show_data())
        self.ToDate.dateChanged.connect(lambda: self.show_data())
    def start(self):
        self.FromDate.setDate(datetime.today())
        self.ToDate.setDate(datetime.today())
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.clear()
        self.lbl2.setStyleSheet('color: rgb(0,0,0)')
        self.lbl4.setStyleSheet('color: rgb(0,0,0)')
        self.lbl5.setStyleSheet('color: rgb(0,0,0)')


    def show_data(self):
        global username
        label = ['Market Participant ID','Price', 'Quantity', 'FromHour','ToHour', 'Date','Result','Quantity_Selected']
        self.table.setColumnCount(len(label))
        self.table.setHorizontalHeaderLabels(label)
        db=sqlite3.connect(os.path.join(path,'SCHOOL.db'))
        cursor = db.cursor()
        query = "SELECT Username,Price,Quantity,FromHour,ToHour,Date,Result,Quantity_selected FROM storagedata WHERE username=?"
        data=(username,)
        cursor.execute(query,data)
        results = cursor.fetchall()
        self.table.setRowCount(len(results))
        p=0
        self.table.clearContents()
        for i, (username, price, quantity, fm ,to, date, result,quantity_s) in enumerate(results):
            fromDate = self.FromDate.date().toPyDate()
            fromDate = datetime(fromDate.year, fromDate.month, fromDate.day)
            toDate = self.ToDate.date().toPyDate()
            toDate = datetime(toDate.year, toDate.month, toDate.day)
            if ((datetime.strptime(date, '%Y-%m-%d') >= fromDate) and (datetime.strptime(date, '%Y-%m-%d')<=toDate)):
                if((self.SelectedButton.isChecked() and result=="YES") or (self.NonSelectedButton.isChecked() and result=='NO') or (self.PendingButton.isChecked() and result=='PD')):
                    self.table.setItem(p, 0,QTableWidgetItem(str(username)))
                    self.table.setItem(p, 1, QTableWidgetItem(str(price)))
                    self.table.setItem(p, 2, QTableWidgetItem(str(quantity)))
                    self.table.setItem(p, 3, QTableWidgetItem(str(fm)))
                    self.table.setItem(p, 4, QTableWidgetItem(str(to)))
                    date=datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
                    self.table.setItem(p, 5, QTableWidgetItem(str(date)))
                    self.table.setItem(p, 6,QTableWidgetItem(str(result)))
                    self.table.setItem(p, 7, QTableWidgetItem(str(quantity_s)))
                    p=p+1
        self.table.setRowCount(p)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(7, 150)
        for i in range (self.table.rowCount()):
            for j in range (self.table.columnCount()):
                item = self.table.item(i,j);
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
class AdminApp(QWidget):
    def __init__(self):
        super().__init__()
        global a
        self.setWindowTitle('Admin Window')
        self.resize(400,400)
        loadUi(os.path.join(path,"AllUI/Admin1.ui"), self)
        self.SelectedButton.clicked.connect(lambda: self.show_data())
        self.PendingButton.clicked.connect(lambda:self.show_data())
        self.NonSelectedButton.clicked.connect(lambda:self.show_data())
        self.FromDate.dateChanged.connect(lambda: self.show_data())
        self.ToDate.dateChanged.connect(lambda: self.show_data())

    def start(self):
        self.FromDate.setDate(datetime.today())
        self.ToDate.setDate(datetime.today())
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.table.clear()
        self.lbl2.setStyleSheet('color: rgb(0,0,0)')
        self.lbl4.setStyleSheet('color: rgb(0,0,0)')
        self.lbl5.setStyleSheet('color: rgb(0,0,0)')



    def show_data(self):
        label = ['Market Participant ID','Price', 'Quantity', 'FromHour','ToHour', 'Date','Result','Quantity_Selected']
        self.table.setColumnCount(len(label))
        self.table.setHorizontalHeaderLabels(label)
        db=sqlite3.connect(os.path.join(path,'SCHOOL.db'))
        cursor = db.cursor()
        query = "SELECT Username,Price, Quantity,FromHour,ToHour,Date, Result,Quantity_selected FROM storagedata"
        cursor.execute(query)
        results = cursor.fetchall()
        self.table.setRowCount(len(results))
        p=0
        self.table.clearContents()
        for i, (username, price, quantity, fm ,to, date, result,quantity_s) in enumerate(results):
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
                    date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
                    self.table.setItem(p, 5, QTableWidgetItem(str(date)))
                    self.table.setItem(p, 6, QTableWidgetItem(str(result)))
                    self.table.setItem(p, 7, QTableWidgetItem(str(quantity_s)))
                    p=p+1
        self.table.setRowCount(p)
        self.table.setRowCount(p)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(7, 150)
        for i in range (self.table.rowCount()):
            for j in range (self.table.columnCount()):
                item = self.table.item(i,j);
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        global a
        global username
        self.setWindowTitle(f'Main App{username}')
        layout=QVBoxLayout()
        loadUi(os.path.join(path,os.path.join(path,'AllUI/MainApp.ui')), self)
        self.NoButton.clicked.connect(self.no)
        self.YesButton.clicked.connect(self.yes)
        self.FinalButton.clicked.connect(self.final)
        self.SeeResultButton.clicked.connect(lambda: open4())

    def start(self):
        self.fr5.show()
        self.frm_3.show()
        self.YesButton.show()
        self.NoButton.show()
        self.Text.setText('Select Single or Multiple Bid')
        self.label_2.setText('')
        self.Quantity1.setText('')
        self.Price1.setText('')
        self.To1.setText('')
        self.From1.setText('')
        self.Quantity2.setText('')
        self.Price2.setText('')
        self.From2.setText('')
        self.To2.setText('')
        self.Quantity3.setText('')
        self.Price3.setText('')
        self.From3.setText('')
        self.To3.setText('')
        self.Date1.setDate(datetime.today())
        self.Date2.setDate(datetime.today())
        self.Date3.setDate(datetime.today())
        self.Welcome.setStyleSheet('color: rgb(0,0,0)')
        self.Text.setStyleSheet('color: rgb(0,0,0)')
        self.LBL3.setStyleSheet('color: rgb(0,0,0)')
        self.LBL4.setStyleSheet('color: rgb(0,0,0)')
        self.LBL5.setStyleSheet('color: rgb(0,0,0)')
        self.LBL6.setStyleSheet('color: rgb(0,0,0)')
        self.LBL7.setStyleSheet('color: rgb(0,0,0)')
        self.label_2.setStyleSheet('color: rgb(0,0,0)')

        self.b=False
        return


    def yes(self):
        self.Text.setText('Please enter your Price, Quantity and Hours')
        self.YesButton.hide()
        self.NoButton.hide()
        self.b=True
    def no(self):
        self.Text.setText('Please enter your Price, Quantity and Hours')
        self.fr5.hide()
        self.frm_3.hide()
        self.NoButton.hide()
        self.YesButton.hide()
        self.b=False

    def savedata(self,Price,Quantity,From,To,Date,Result,temp):
        global username
        db=sqlite3.connect(os.path.join(path,'SCHOOL.db'))
        cursor = db.cursor()
        data = (username,Price, Quantity, From,To, Date,Result,temp)
        insert_query = "INSERT INTO storagedata (Username,Price,Quantity,FromHour,ToHour,Date,Result,Quantity_selected) VALUES(?,?,?,?,?,?,?,?)"
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()


    def simplecheck(self,From,To):
        if((From<To) & (From<=24) & (From>0) & (To<=24) & (To>0)):
            return False
        return True

    def check(self):
        global username
        if(self.simplecheck(int(self.From1.text()),int(self.To1.text()))):
            self.label_2.setText('Hours are not in correct order in 1st Bid')
            return False
        if (self.b):
            if( self.simplecheck(int(self.From2.text()),int(self.To2.text()))):
                self.label_2.setText('Hours are not in correct order in 2nd Bid')
                return False
            if ( self.simplecheck(int(self.From3.text()), int(self.To3.text()))):
                self.label_2.setText('Hours are not in correct order in 3rd Bid')
                return False
        min_value=str(self.Date1.date().toPyDate().strftime('%Y-%m-%d'))
        if(self.b):
            if(min_value>self.Date2.date().toPyDate().strftime('%Y-%m-%d') ):
                min_value=self.Date2.date().toPyDate().strftime('%Y-%m-%d')
            if (min_value > self.Date3.date().toPyDate().strftime('%Y-%m-%d')):
                min_value =self.Date3.date().toPyDate().strftime('%Y-%m-%d')
        db=sqlite3.connect(os.path.join(path,'SCHOOL.db'))
        cursor = db.cursor()
        input_query=f"SELECT minlimit from logindata WHERE Username=?"
        data=(username,)
        cursor.execute(input_query,data)
        results=cursor.fetchall()
        min_date = datetime.strptime(min_value, '%Y-%m-%d')
        result_date = datetime.strptime(results[0][0], '%Y-%m-%d')
        if(min_date<result_date):
            self.label_2.setText('Your Bids are in the past.Please check month, days ,hour you are bidding.')
            return False
        else:
            input_query2 = "UPDATE logindata SET minlimit=? WHERE Username=?"
            cursor.execute(input_query2, (str(min_value),username))
            db.commit()
            cursor.close()
            return True

    def goodcheck2(self,Date,Month,From,To,MODE):
        for i in range (int(From),int(To)):
            db=sqlite3.connect(os.path.join(path,'SCHOOL.db'))
            cursor=db.cursor()
            input_query1=(f'SELECT * FROM {MODE}data WHERE Date=? AND Month=? AND Hour=?')
            data=(Date,Month,i)
            cursor.execute(input_query1,data)
            result=cursor.fetchall()
            if(len(result)==0):
                return False

    def goodcheck(self):
        global username
        MODE='VA'
        pyqt_date = self.Date1.date()
        datetime_obj = pyqt_date.toPyDate()
        Date = datetime_obj.day
        Month=datetime_obj.month
        if(username=='NO' or username=='BG1' or username=='BG2'):
            MODE='NO'
        if(self.goodcheck2(self.Date1.date().toPyDate().day,self.Date1.date().toPyDate().month,self.From1.text() ,self.To1.text(),MODE)==False):
            self.label_2.setText('Your 1st Bid is not available.Please Check your hour,days,months')
            return False
        if(self.b):
            if (self.goodcheck2(self.Date2.date().toPyDate().day, self.Date2.date().toPyDate().month,self.From1.text(),self.To1.text(),MODE ) == False):
                self.label_2.setText('Your 2nd Bid is not available.Please Check your hour,days,months')
                return False
            if (self.goodcheck2(self.Date2.date().toPyDate().day, self.Date3.date().toPyDate().month, self.From1.text(),self.To1.text(),MODE) == False):
                self.label_2.setText('Your 3rd Bid is not available.Please Check your hour,days,months')
                return False
        return True

    def final(self):
        if(self.goodcheck()):
          if(self.check()):
            db = sqlite3.connect(os.path.join(path,'SCHOOL.db'))
            cursor = db.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS storagedata(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        Username VARCHAR(255),
                        Price FLOAT,
                        Quantity FLOAT,
                        FromHour INT,
                        ToHour INT,
                        Date VARCHAR(255),
                        Result VARCHAR(255),
                        Quantity_selected FLOAT
                    )
                    """)
            self.savedata(self.Price1.text(), self.Quantity1.text(),self.From1.text(),self.To1.text(),self.Date1.date().toPyDate().strftime('%Y-%m-%d'),'PD',0)
            if(self.b):
                print('hello')
                self.savedata(self.Price2.text(), self.Quantity2.text(),self.From2.text(),self.To2.text(),self.Date2.date().toPyDate().strftime('%Y-%m-%d'),'PD',0)
                self.savedata(self.Price3.text(), self.Quantity3.text(),self.From3.text(),self.To3.text(),self.Date3.date().toPyDate().strftime('%Y-%m-%d'),'PD',0)
            self.label_2.setText('Bid Updated Successfully')
        else:
            return
class GeneralApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 400)
        print(os. getcwd() )
        loadUi(os.path.join(path,'AllUI/generalApp.ui'),self)
        self.label_16.setPixmap(QPixmap(os.path.join(path,'images/icons8-patreon-50.png')))
        self.PhotoLabel.setPixmap(QPixmap(os.path.join(path,'icons/downlaod.jpg')))
        self.label_17.setPixmap(QPixmap(os.path.join(path,'images/icons8-youtube-studio-50.png')))
        self.label_18.setPixmap(QPixmap(os.path.join(path,'images/icons8-paypal-50.png')))
        self.pushButton_2.setIcon(QIcon(os.path.join(path,'icons/thermometer.png')))
        self.pushButton_5.setIcon(QIcon(os.path.join(path,'icons/octagon.png')))
        self.pushButton_9.setIcon(QIcon(os.path.join(path,'icons/x.png')))
        self.pushButton_8.setIcon(QIcon(os.path.join(path,'icons/maximize.png')))
        self.pushButton_7.setIcon(QIcon(os.path.join(path,'icons/minimize.png')))
        self.pushButton_6.setIcon(QIcon(os.path.join(path,'icons/align-center.png')))
        self.label_14.setPixmap(QPixmap(os.path.join(path,'icons/pie-chart.png')))
        self.label_15.setPixmap(QPixmap(os.path.join(path,'icons/smile.png')))
        self.pushButton.setIcon(QIcon(os.path.join(path,'icons/logout.png')))
        self.pushButton_4.setIcon(QIcon(os.path.join(path,'icons/Acc.png')))
        layout=QVBoxLayout()
        self.a.setLayout(layout)

        global button
        button=[self.pushButton,self.pushButton_2,self.pushButton_5,self.pushButton_4,self.PhotoLabel]


        global loginapp
        loginapp=LoginWindow()
        self.a.insertWidget(1, loginapp)

        global registerapp
        registerapp=RegisterWindow()
        self.a.insertWidget(2, registerapp)

        global mainapp
        mainapp=MainApp()
        self.a.insertWidget(3, mainapp)

        global showapp
        showapp=showDates()
        self.a.insertWidget(4, showapp)

        global resultapp
        resultapp=ResultApp()
        self.a.insertWidget(5, resultapp)

        global adminapp
        adminapp=AdminApp()
        self.a.insertWidget(6, adminapp)

        global makedecision
        makedecision=MakeDecision()
        self.a.insertWidget(7, makedecision)

        self.pushButton_7.clicked.connect(lambda :self.showMaximized())
        self.pushButton_8.clicked.connect(lambda: self.showMinimized())
        self.pushButton_9.clicked.connect(lambda :self.close())
        self.pushButton_6.clicked.connect(lambda : self.doit())

        self.b=True

        global a
        a = self.a
        open1()

    def doit(self):
        if self.b==True:
            self.label.hide()
            self.label_2.hide()
            self.label_3.hide()
            self.label_4.hide()
            self.label_5.hide()
            self.pushButton.hide()
            self.pushButton_2.hide()
            self.pushButton_5.hide()
            self.pushButton_4.hide()
            self.b=False
            self.frame.setFixedWidth(80)


        else:

            self.b=True
            self.label.show()
            self.label_2.show()
            self.label_3.show()
            self.label_4.show()
            self.label_5.show()
            self.pushButton.show()
            self.pushButton_2.show()
            self.pushButton_5.show()
            self.pushButton_4.show()
            self.frame.setFixedWidth(200)

if __name__=='__main__':
    app = QApplication(sys.argv)
    widget = GeneralApp()
    widget.show()
    app.exec()
