import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow,QStackedWidget
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QLabel,QPushButton,QRadioButton,QVBoxLayout,QHBoxLayout,QGridLayout,QLineEdit,QSizePolicy,QLabel,QTableWidget,QTableWidgetItem
from PyQt6.QtGui import QPixmap,QIcon,QColor,QPalette
from PyQt6.QtCore import QPropertyAnimation,QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
import pymysql
from datetime import datetime
from marketalgo import economic
import os
import pandas as pd

def open1(p,button):
    p.insertWidget(1, LoginWindow(p, button))
    p.setCurrentIndex(1)
def open2(p,button):
    p.insertWidget(2,RegisterWindow(p,button))
    p.setCurrentIndex(2)
def open3(p,button,username):
    p.insertWidget(4,MainApp(username,p,button))
    p.setCurrentIndex(4)
def open4(p,button,username):
    p.insertWidget(5,ResultApp(username,p,button))
    p.setCurrentIndex(5)
def open5(p,button,username):
    p.insertWidget(6,showDates(button,p,username))
    p.setCurrentIndex(6)

class MakeDecision(QWidget):
    def __init__(self,p,button):
        super().__init__()
        loadUi("AllUI/MakeDec.ui", self)
        self.p=p
        self.button=button
        self.MakeResult.clicked.connect(self.do1)
        self.pushButton_2.clicked.connect(self.do2)
        self.button[3].setText('SEE MORE BID')
        self.button[3].clicked.connect(lambda : self.openin())
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
            db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
            cursor=db.cursor()
            input_query1='SELECT * FROM storagedata WHERE FROMHour=(%s) AND Result=(%s) AND Date=(%s)'
            data1=(self.Hour.text(),'PD',self.Date1.date().toPyDate().strftime(format='%Y-%m-%d'))
            cursor.execute(input_query1,data1)
            results=cursor.fetchall()
            if(len(results)==0):
                self.label_4.setText('No Remaining Bids for this date')
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
                self.label_4.setText('No enough Bids..')
                return
            (A,B,C,D)=economic(PD,PD_min,PD_max,price_list)
            print(A,B,C,D)
            print('got the the answer')
            self.label_4.setStyleSheet('color : rgba(255,255,255)')
            self.table.setColumnCount(4)
            self.table.setRowCount(len(C))
            self.table.setHorizontalHeaderLabels(['Market Participant ID','Price','Quantity Bid','QuantityAccepted'])
            for i in range (len(C)):
                self.table.setItem(i,0,QTableWidgetItem(str(results[C[i]][1])))
                self.table.setItem(i, 1, QTableWidgetItem(str(results[C[i]][2])))
                self.table.setItem(i, 2, QTableWidgetItem(str(results[C[i]][3])))
                self.table.setItem(i, 3, QTableWidgetItem(str(B[C[i]])))
            self.results=results
            self.C=C
            self.D=D
            self.label_4.setText('Market Clear Algorithm successfully completed..')
            self.B=B


    def do2(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.label_4.setText('Market is Cleared')
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        input_query1 = 'UPDATE storagedata SET Result=%s , Quantity_selected=%s WHERE id=%s'
        for i in range(len(self.B)):
            if(self.B[i]!=0):
                data1 = ('YES',self.B[i],(self.results)[i][0])
                cursor.execute(input_query1,data1)
            else:
                data1 = ('NO',self.B[i],(self.results)[i][0])
                cursor.execute(input_query1,data1)
        db.commit()
        cursor.close()
    def openin(self):
        self.p.insertWidget(3,AdminApp(self.p,self.button))
        self.p.setCurrentIndex(3)
class showDates(QWidget):
    def __init__(self,button,a,username):
        super().__init__()
        button[0].clicked.connect(lambda: open1(a,button))
        button[1].clicked.connect(lambda: open2(a,button))
        button[2].show()
        button[2].clicked.connect(lambda: open3(a,button,username))
        button[3].hide()
        button[2].setText('Submit the Bid')
        layout=QVBoxLayout()
        self.setLayout(layout)
        self.table=QTableWidget()
        self.label=QLabel('All the available dates you can bid for')
        MODE=username
        if(MODE=='ST' or MODE=='QF'):
            MODE='VA'
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        cursor=db.cursor()
        cursor.execute(f'SELECT * FROM {MODE}data ORDER BY Month ASC,Date ASC,Hour ASC')
        results=cursor.fetchall()
        self.table.setRowCount(len(results))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['month','date','hour','Quantity(KW)'])
        for i,(month,date,hour,covariance,value) in enumerate(results):
            self.table.setItem(i,0,QTableWidgetItem(str(month)))
            self.table.setItem(i, 1, QTableWidgetItem(str(date)))
            self.table.setItem(i, 2, QTableWidgetItem(str(hour)))
            self.table.setItem(i, 3, QTableWidgetItem(str(value)))
        self.label.setStyleSheet('color: rgb(255,255,255)')
        layout.addWidget(self.label)
        layout.addWidget(self.table)
class LoginWindow(QWidget):
    def __init__(self,p,button):
        super().__init__()
        self.button1 = button
        self.button1[0].hide()
        self.button1[2].hide()
        self.button1[3].hide()
        self.button1[1].show()
        self.button1[4].hide()
        self.p=p
        self.button1[1].clicked.connect(lambda: open2(self.p,self.button1))
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

        self.button.clicked.connect(self.checkCredentials)
        self.button2 = QPushButton('Not a member? Sign Up')
        layout.addWidget(self.button2, 13, 2, 1, 4)
        self.button2.clicked.connect(lambda: open2(self.p,self.button1))

        self.mediaplayer = QMediaPlayer()
        self.vedio = QVideoWidget()
        layout.addWidget(self.vedio, 0, 0, 8, 8)
        self.mediaplayer.setSource(
            QUrl.fromLocalFile('icons/Screen Recording 2024-05-19 at 11.52.05 AM (1).mp4'))
        self.mediaplayer.setVideoOutput(self.vedio)
        self.mediaplayer.play()
        self.mediaplayer.positionChanged.connect(self.check_position)

    def check_position(self, position):
        total_duration = self.mediaplayer.duration()
        if total_duration > 0:
            target_position = 0.9 * total_duration  # 90% of the total duration
            if position >= target_position:
                self.mediaplayer.setPosition(0)

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
                if not (username == "Admin"):
                    self.p.insertWidget(4, MainApp(username,self.p,self.button1))
                    self.p.setCurrentIndex(4)
                else:
                    self.p.insertWidget(3, AdminApp(self.p,self.button1))
                    self.p.setCurrentIndex(3)
            else:
                self.status.setText("Password is not correct")
        else:
            self.status.setText("Username not found")
        cursor.close()
        db.close()
class RegisterWindow(QWidget):
    def __init__(self,p,button):
        super().__init__()
        self.button = button
        self.button[1].hide()
        self.button[2].hide()
        self.button[3].hide()
        self.button[0].show()
        self.button[4].hide()
        self.p=p
        self.button[0].setText('Go to Login Page')
        self.button[0].clicked.connect(lambda: open1(self.p,self.button))
        loadUi('AllUI/Register1.ui', self)
        self.Status.setText('')
        self.Status.setStyleSheet('color: rgb(255,255,255)')
        self.SignUpt.clicked.connect(self.fillinfo)
        self.Mainphoto.setPixmap(QPixmap('icons/Screenshot 2024-04-21 at 9.30.01 PM (1).png'))

    def fillinfo(self):
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
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
        insert_query = "INSERT INTO logindata (Username,Password,Email,minlimit) VALUES(%s,%s,%s,%s)"
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()
        open1(self.p,self.button)
class ResultApp(QWidget):
    def __init__(self,username,p,button):
        super().__init__()
        self.p=p
        self.username=username
        self.button=button
        self.button[0].show()
        self.button[1].show()
        self.button[2].show()
        self.button[3].show()
        self.button[3].setText('Show available Dates')
        self.button[3].clicked.connect(lambda : open5(self.p,self.button,self.username))
        self.button[4].show()
        self.button[4].setPixmap(QPixmap('icons/downlaod.jpg'))
        self.button[0].clicked.connect(lambda: open1(self.p,self.button))
        self.button[1].clicked.connect(lambda: open2(self.p,self.button))
        self.button[2].setText('Submit the Bid')
        self.button[2].clicked.connect(lambda : open3(self.p,self.button,self.username))
        self.setWindowTitle('Result Window')
        self.resize(700, 700)
        # map = QPixmap('Screenshot 2024-04-21 at 9.30.01 PM (1).png')
        # self.label.setPixmap(map)
        loadUi("AllUI/Admin1.ui", self)
        self.SelectedButton.clicked.connect(lambda: self.show_data())
        self.PendingButton.clicked.connect(lambda:self.show_data())
        self.NonSelectedButton.clicked.connect(lambda:self.show_data())

    def show_data(self):
        label = ['Market Participant ID','Price', 'Quantity', 'FromHour','ToHour', 'Date','Result','Quantity_Selected']
        self.table.setColumnCount(len(label))
        self.table.setHorizontalHeaderLabels(label)
        db = pymysql.connect(host='localhost', user='root', password='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        query = "SELECT Username,Price, Quantity,FromHour,ToHour,Date, Result,Quantity_selected FROM storagedata WHERE username=%s"
        cursor.execute(query,self.username)
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
                    self.table.setItem(p, 5, QTableWidgetItem(str(date)))
                    self.table.setItem(p, 6,QTableWidgetItem(str(result)))
                    self.table.setItem(p, 7, QTableWidgetItem(str(quantity_s)))
                    p=p+1
        self.table.setRowCount(p)
class AdminApp(QWidget):
    def __init__(self,p,button):
        super().__init__()
        self.button=button
        self.button[0].show()
        self.button[1].show()
        self.button[2].hide()
        self.button[3].setText('Clear the Market')
        self.button[3].show()
        self.button[3].clicked.connect(lambda :self.openin())
        self.button[4].setPixmap(QPixmap('icons/downlaod.jpg'))
        self.button[4].show()
        self.p = p
        self.button[0].clicked.connect(lambda: open1(self.p,self.button))
        self.button[1].clicked.connect(lambda : open2(self.p,self.button))
        self.setWindowTitle('Admin Window')
        self.resize(400,400)
        loadUi("AllUI/Admin1.ui", self)
        self.SelectedButton.clicked.connect(lambda: self.show_data())
        self.PendingButton.clicked.connect(lambda:self.show_data())
        self.NonSelectedButton.clicked.connect(lambda:self.show_data())
    def openin(self):
        self.p.insertWidget(7,MakeDecision(self.p,self.button))
        self.p.setCurrentIndex(7)

    def show_data(self):
        label = ['Market Participant ID','Price', 'Quantity', 'FromHour','ToHour', 'Date','Result','Quantity_Selected']
        self.table.setColumnCount(len(label))
        self.table.setHorizontalHeaderLabels(label)
        db = pymysql.connect(host='localhost', user='root', password='c24466fb', database='SCHOOL')
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
                    self.table.setItem(p, 5, QTableWidgetItem(str(date)))
                    self.table.setItem(p, 6, QTableWidgetItem(str(result)))
                    self.table.setItem(p, 7, QTableWidgetItem(str(quantity_s)))

                    p=p+1
        self.table.setRowCount(p)
class MainApp(QWidget):
    def __init__(self,username,p,button):
        super().__init__()
        self.button=button
        self.p=p
        self.button[0].show()
        self.button[1].show()
        self.button[2].show()
        self.button[2].setText('Show my results')
        self.button[3].show()
        self.button[0].clicked.connect(lambda :open1(self.p,self.button))
        self.button[1].clicked.connect(lambda: open2(self.p,self.button))
        self.button[3].setText('Show the available dates')
        self.button[3].clicked.connect(lambda: open5(self.p,self.button,self.username))
        self.button[4].show()
        self.button[4].setPixmap(QPixmap('icons/downlaod.jpg'))
        self.setWindowTitle(f'Main App{username}')
        layout=QVBoxLayout()
        loadUi('AllUI/MainApp.ui', self)
        self.NoButton.clicked.connect(self.no)
        self.YesButton.clicked.connect(self.yes)
        self.FinalButton.clicked.connect(self.final)
        self.b=False
        self.username=username
        self.SeeResultButton.clicked.connect(lambda: open4(self.p,self.button,self.username))
        self.button[2].clicked.connect(lambda: open4(self.p,self.button,self.username))

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
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        data = (self.username,Price, Quantity, From,To, Date,Result,temp)
        insert_query = "INSERT INTO storagedata (Username,Price,Quantity,FromHour,ToHour,Date,Result,Quantity_selected) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()


    def simplecheck(self,From,To):
        if((From<To) & (From<=24) & (From>0) & (To<=24) & (To>0)):
            return False
        print('Error1')
        return True

    def check(self):
        if(self.simplecheck(int(self.From1.text()),int(self.To1.text()))):
            return False
        if (self.b):
            if( self.simplecheck(int(self.From2.text()),int(self.To2.text()))):
                return False
            if ( self.simplecheck(int(self.From3.text()), int(self.To3.text()))):
                return False
        min_value=str(self.Date1.date().toPyDate().strftime('%Y-%m-%d'))
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
        min_date = datetime.strptime(min_value, '%Y-%m-%d')
        result_date = datetime.strptime(results[0][0], '%Y-%m-%d')
        print(min_date)
        print(result_date)
        print('date')
        if(min_date<result_date):
            print('Error2')
            return False
        else:
            input_query2 = "UPDATE logindata SET minlimit=%s WHERE Username=%s"
            cursor.execute(input_query2, (str(min_value), self.username))
            db.commit()
            cursor.close()
            return True

    def goodcheck2(self,Date,Month,From,To,MODE):
        for i in range (int(From),int(To)):
            db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
            cursor=db.cursor()
            input_query1=(f'SELECT * FROM {MODE}data WHERE Date=%s AND Month=%s AND Hour=%s')
            data=(Date,Month,i)
            cursor.execute(input_query1,data)
            result=cursor.fetchall()
            if(len(result)==0):
                return False

    def goodcheck(self):
        MODE='VA'
        pyqt_date = self.Date1.date()
        datetime_obj = pyqt_date.toPyDate()
        Date = datetime_obj.day
        Month=datetime_obj.month
        if(self.username=='NO' or self.username=='BG1' or self.username=='BG2'):
            MODE='NO'
        if(self.goodcheck2(self.Date1.date().toPyDate().day,self.Date1.date().toPyDate().month,self.From1.text(),self.To1.text(),MODE)==False):
            return False
        if(self.b):
            if (self.goodcheck2(self.Date2.date().toPyDate().day, self.Date2.date().toPyDate().month,self.From1.text(),self.To1.text(),MODE ) == False):
                return False
            if (self.goodcheck2(self.Date2.date().toPyDate().day, self.Date3.date().toPyDate().month, self.From1.text(),self.To1.text(),MODE) == False):
                return False
        return True


    def final(self):
        print('Yes1')
        print(self.check())
        print(self.goodcheck())
        if(self.goodcheck() & self.check()):
            print('idhar kese??')
            db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
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
            self.label_2.setText('Something gone wrong')
class mainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 400)
        print(os. getcwd() )
        loadUi('AllUI/graph_simulation.ui',self)
        self.label_16.setPixmap(QPixmap('images/icons8-patreon-50.png'))
        self.PhotoLabel.setPixmap(QPixmap('icons/downlaod.jpg'))
        self.label_17.setPixmap(QPixmap('images/icons8-youtube-studio-50.png'))
        self.label_18.setPixmap(QPixmap('images/icons8-paypal-50.png'))
        self.pushButton_2.setIcon(QIcon('icons/thermometer.png'))
        self.pushButton_5.setIcon(QIcon('icons/octagon.png'))
        self.pushButton_9.setIcon(QIcon('icons/x.png'))
        self.pushButton_8.setIcon(QIcon('icons/maximize.png'))
        self.pushButton_7.setIcon(QIcon('icons/minimize.png'))
        self.pushButton_6.setIcon(QIcon('icons/align-center.png'))
        self.label_14.setPixmap(QPixmap('icons/pie-chart.png'))
        self.label_15.setPixmap(QPixmap('icons/smile.png'))
        self.pushButton.setIcon(QIcon('icons/logout.png'))
        self.pushButton_4.setIcon(QIcon('icons/Acc.png'))
        layout=QVBoxLayout()
        self.a.setLayout(layout)
        button=[self.pushButton,self.pushButton_2,self.pushButton_5,self.pushButton_4,self.PhotoLabel]
        self.a.insertWidget(2, RegisterWindow(self.a,button))
        self.a.insertWidget(3,AdminApp(self.a,button))
        self.a.insertWidget(1, LoginWindow(self.a, button))
        self.a.setCurrentIndex(1)
        self.pushButton_7.clicked.connect(lambda :self.showMaximized())
        self.pushButton_8.clicked.connect(lambda: self.showMinimized())
        self.pushButton_9.clicked.connect(lambda :self.close())
        self.pushButton_6.clicked.connect(lambda : self.doit())
        self.b=True

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
    widget = mainApp()
    widget.show()
    app.exec()
