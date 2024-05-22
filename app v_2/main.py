import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow,QStackedWidget
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QLabel,QPushButton,QRadioButton,QVBoxLayout,QGridLayout,QLineEdit,QSizePolicy,QLabel,QTableWidget,QTableWidgetItem
from PyQt6.QtGui import QPixmap,QIcon,QColor,QPalette
from PyQt6.QtCore import QPropertyAnimation,QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
import pymysql
from datetime import datetime
import pandas as pd

class showDates(QWidget):
    def __init__(self,button,a,username):
        super().__init__()
        self.button=button
        self.p=a
        self.username=username
        self.button[0].clicked.connect(lambda: self.open1)
        self.button[1].clicked.connect(lambda: self.open2)
        self.button[2].clicked.connect(lambda: self.open3)
        self.button[3].clicked.connect(lambda: self.open4)
        self.button[2].setText('Submit the Bid')
        self.button[3].setText('Show the Result')
        layout=QVBoxLayout()
        self.setLayout(layout)
        self.table=QTableWidget()
        self.label=QLabel('All the available dates you can bid for')
        if(self.username=='NO' or self.username=='BG1' or self.username=='BG2'):
            MODE='NO'
            self.table.setRowCount(90)
        else:
            MODE='VA'
            self.table.setRowCount(72)
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        cursor=db.cursor()
        cursor.execute(f'SELECT * FROM {MODE}data ORDER BY Month ASC,Date ASC,Hour ASC')
        results=cursor.fetchall()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['month','date','hour','covariance','value'])
        for i,(month,date,hour,covariance,value) in enumerate(results):
            self.table.setItem(i,0,QTableWidgetItem(str(month)))
            self.table.setItem(i, 1, QTableWidgetItem(str(date)))
            self.table.setItem(i, 2, QTableWidgetItem(str(hour)))
            self.table.setItem(i, 3, QTableWidgetItem(str(covariance)))
            self.table.setItem(i, 4, QTableWidgetItem(str(value)))
        self.label.setStyleSheet('color: rgb(255,255,255)')
        layout.addWidget(self.label)
        layout.addWidget(self.table)

    def open1(self):
        self.p.insertWidget(1,LoginWindow(self.p,self.button))
        self.p.setCurrentIndex(1)
    def open2(self):
        self.p.insertWidget(2,RegisterWindow(self.p,self.button))
        self.p.setCurrentIndex(2)
    def open3(self):
        self.p.insertWidget(4,MainApp(self.username,self.p,self.button))
        self.p.setCurrentIndex(4)
    def open4(self):
        print('hello')
        self.p.insertWidget(5,ResultApp(self.username,self.p,self.button))
        self.p.setCurrentIndex(5)
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
        self.button1[1].clicked.connect(lambda: self.open())
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
        layout.addWidget(self.status, 14, 0, 1, 4)

        self.button.clicked.connect(self.checkCredentials)
        self.button2 = QPushButton('Not a member? Sign Up')
        layout.addWidget(self.button2, 13, 2, 1, 4)
        self.button2.clicked.connect(lambda: self.open())

        self.mediaplayer = QMediaPlayer()
        self.vedio = QVideoWidget()
        layout.addWidget(self.vedio, 0, 0, 8, 8)
        self.mediaplayer.setSource(
            QUrl.fromLocalFile('Screen Recording 2024-05-19 at 11.52.05 AM (1).mp4'))
        self.mediaplayer.setVideoOutput(self.vedio)
        self.mediaplayer.play()
        self.mediaplayer.positionChanged.connect(self.check_position)

    def check_position(self, position):
        total_duration = self.mediaplayer.duration()
        if total_duration > 0:
            target_position = 0.9 * total_duration  # 90% of the total duration
            if position >= target_position:
                self.mediaplayer.setPosition(0)



    def open(self):
        self.p.insertWidget(2, RegisterWindow(self.p, self.button1))
        self.p.setCurrentIndex(2)

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
        self.button[0].clicked.connect(lambda : self.open())
        loadUi('Register1.ui', self)
        self.Status.setText('')
        self.SignUpt.clicked.connect(self.fillinfo)
        self.Mainphoto.setPixmap(QPixmap('Screenshot 2024-04-21 at 9.30.01 PM (1).png'))

    def open(self):
        self.p.insertWidget(1, LoginWindow(self.p, self.button))
        self.p.setCurrentIndex(1)

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
        self.p.setCurrentIndex(1)
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
        self.button[3].clicked.connect(self.open4)
        self.button[4].show()
        self.button[4].setPixmap(QPixmap('downlaod.jpg'))
        self.button[0].clicked.connect(self.open1)
        self.button[1].clicked.connect(self.open2)
        self.button[2].setText('Submit the Bid')
        self.button[2].clicked.connect(self.open3)
        self.setWindowTitle('Result Window')
        self.resize(700, 700)
        # map = QPixmap('Screenshot 2024-04-21 at 9.30.01 PM (1).png')
        # self.label.setPixmap(map)
        loadUi("Admin1.ui", self)
        self.SelectedButton.clicked.connect(lambda: self.show_data())
        self.PendingButton.clicked.connect(lambda:self.show_data())
        self.NonSelectedButton.clicked.connect(lambda:self.show_data())


    def open1(self):
        self.p.insertWidget(1,LoginWindow(self.p,self.button))
        self.p.setCurrentIndex(1)
    def open2(self):
        self.p.insertWidget(2,RegisterWindow(self.p,self.button))
        self.p.setCurrentIndex(2)
    def open3(self):
        self.p.insertWidget(4,MainApp(self.username,self.p,self.button))
        self.p.setCurrentIndex(4)
    def open4(self):
        self.p.insertWidget(6,showDates(self.button,self.p,self.username))
        self.p.setCurrentIndex(6)

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
                    self.table.setItem(p, 0,QTableWidgetItem(str(username)))
                    self.table.setItem(p, 1, QTableWidgetItem(str(price)))
                    self.table.setItem(p, 2, QTableWidgetItem(str(quantity)))
                    self.table.setItem(p, 3, QTableWidgetItem(str(fm)))
                    self.table.setItem(p, 4, QTableWidgetItem(str(to)))
                    self.table.setItem(p, 5, QTableWidgetItem(str(date)))
                    self.table.setItem(p, 6,QTableWidgetItem(str(result)))
                    p=p+1
        self.table.setRowCount(p)
class AdminApp(QWidget):
    def __init__(self,p,button):
        super().__init__()
        self.button=button
        self.button[0].show()
        self.button[1].show()
        self.button[2].hide()
        self.button[3].setText('Make a decision')
        self.button[3].show()
        self.button[4].setPixmap(QPixmap('downlaod.jpg'))
        self.button[4].show()
        self.button[0].clicked.connect(self.open1)
        self.button[1].clicked.connect(self.open2)
        self.p=p
        self.setWindowTitle('Admin Window')
        self.resize(400,400)
        loadUi("Admin1.ui", self)
        # map=QPixmap('Screenshot 2024-04-21 at 9.30.01 PM (1).png')
        # self.label.setPixmap(map)
        self.SelectedButton.clicked.connect(lambda: self.show_data())
        self.PendingButton.clicked.connect(lambda:self.show_data())
        self.NonSelectedButton.clicked.connect(lambda:self.show_data())

    def open1(self):
            self.p.insertWidget(1, LoginWindow(self.p, self.button))
            self.p.setCurrentIndex(1)

    def open2(self):
            self.p.insertWidget(2, RegisterWindow(self.p, self.button))
            self.p.setCurrentIndex(2)


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


    def makeresult(self):
        largest=0
        db = pymysql.connect(host='localhost', user='root', password='c24466fb', database='SCHOOL')
        off=0
        for i in range (3):
            cursor=db.cursor()
            query="SELECT Bid_Value FROM logindata LIMIT 1 OFFSET %s"
            cursor.execute(query,(i,))
            result=cursor.fetchone()
            if(int(result[0]))>largest:
                largest=int(result[0])
                off=i
        cursor = db.cursor()
        query = "SELECT Username FROM logindata LIMIT 1 OFFSET %s"
        cursor.execute(query, (off,))
        result = cursor.fetchone()
        username=result[0]
        self.label2.setText(f'Winner is the {username} with the {largest} bid')
        return
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
        self.button[0].clicked.connect(self.open1)
        self.button[1].clicked.connect(self.open2)
        self.button[3].setText('Show the available dates')
        self.button[3].clicked.connect(self.open3)
        self.button[4].show()
        self.button[4].setPixmap(QPixmap('downlaod.jpg'))
        self.setWindowTitle(f'Main App{username}')
        layout=QVBoxLayout()
        loadUi('MainApp.ui', self)
        self.NoButton.clicked.connect(self.no)
        self.YesButton.clicked.connect(self.yes)
        self.FinalButton.clicked.connect(self.final)
        self.b=False
        self.username=username
        self.SeeResultButton.clicked.connect(self.resultclick)
        self.button[2].clicked.connect(self.resultclick)

    def open1(self):
        self.p.insertWidget(1,LoginWindow(self.p,self.button))
        self.p.setCurrentIndex(1)
    def open2(self):
        self.p.insertWidget(2,RegisterWindow(self.p,self.button))
        self.p.setCurrentIndex(2)
    def open3(self):
        self.p.insertWidget(6,showDates(self.button,self.p,self.username))
        self.p.setCurrentIndex(6)

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

    def savedata(self,Price,Quantity,From,To,Date,Result):
        db = pymysql.connect(host='localhost', user='root', passwd='c24466fb', database='SCHOOL')
        cursor = db.cursor()
        data = (self.username,Price, Quantity, From,To, Date,Result)
        insert_query = "INSERT INTO storagedata (Username,Price,Quantity,FromHour,ToHour,Date,Result) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()


    def simplecheck(self,From,To):
        if((From<To) & (From<=24) & (From>0) & (To<=24) & (To>0)):
            return False
        print('MAA KI CHUT')
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
        if(min_date<result_date):
            print('MAA KI CHUT2')
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
                        Price INT,
                        Quantity INT,
                        FromHour INT,
                        ToHour INT,
                        Date VARCHAR(255),
                        Result VARCHAR(255)
                    )
                    """)
            self.savedata(self.Price1.text(), self.Quantity1.text(),self.From1.text(),self.To1.text(),self.Date1.date().toPyDate().strftime('%Y-%m-%d'),'PD')
            if(self.b):
                print('hello')
                self.savedata(self.Price2.text(), self.Quantity2.text(),self.From2.text(),self.To2.text(),self.Date2.date().toPyDate().strftime('%Y-%m-%d'),'PD')
                self.savedata(self.Price3.text(), self.Quantity3.text(),self.From3.text(),self.To3.text(),self.Date3.date().toPyDate().strftime('%Y-%m-%d'),'PD')
            self.label_2.setText('Bid Updated Successfully')
        else:
            self.label_2.setText('Something gone wrong')

    def resultclick(self):
        self.p.insertWidget(5,ResultApp(self.username,self.p,self.button))
        self.p.setCurrentIndex(5)
        return
class mainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 400)
        loadUi('graph_simulation.ui',self)
        self.PhotoLabel.setPixmap(QPixmap('downlaod.jpg'))
        self.label_16.setPixmap(QPixmap('images/icons8-patreon-50.png'))
        self.label_17.setPixmap(QPixmap('images/icons8-paypal-50.png'))
        self.label_18.setPixmap(QPixmap('images/icons8-youtube-studio-50.png'))
        self.pushButton_2.setIcon(QIcon('icons/thermometer.png'))
        self.pushButton_5.setIcon(QIcon('icons/octagon.png'))
        self.pushButton_9.setIcon(QIcon('icons/x.png'))
        self.pushButton_8.setIcon(QIcon('icons/maximize.png'))
        self.pushButton_7.setIcon(QIcon('icons/minimize.png'))
        self.pushButton_6.setIcon(QIcon('icons/align-center.png'))
        self.label_14.setPixmap(QPixmap('icons/pie-chart.png'))
        self.label_15.setPixmap(QPixmap('icons/smile.png'))
        self.pushButton.setIcon(QIcon('logout.png'))
        self.pushButton_4.setIcon(QIcon('acc.png'))
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
        # self.anim1 = QPropertyAnimation(self.frame, b'geometry')
        # self.anim1.setDuration(400)
        # self.anim1.setStartValue(QRect(self.frame.x(),self.frame.y(),self.frame.width(),self.frame.height()))
        # self.anim1.setEndValue(QRect(self.frame.x(), self.frame.y(), self.frame.width()-32, self.frame.height()))
        #
        # self.anim2 = QPropertyAnimation(self.frame_2, b'geometry')
        # self.anim2.setDuration(400)
        # self.anim2.setStartValue(QRect(self.frame_2.x(), self.frame_2.y(), self.frame_2.width(), self.frame_2.height()))
        # self.anim2.setEndValue(QRect(self.frame_2.x(), self.frame_2.y(), self.frame_2.width() + 32, self.frame_2.height()))
        #
        # self.anim2 = QPropertyAnimation(self.frame, b'geometry')
        # self.anim2.setDuration(400)
        # rect = self.frame.geometry()
        # self.anim2.setStartValue(rect)
        # rect=(0,0,500,500)
        # self.anim2.setEndValue(rect)

    def doit(self):
        if self.b==True:
            self.label.setText('')
            self.label_2.setText('')
            self.label_3.setText('')
            self.label_4.setText('')
            self.label_5.setText('')
            self.pushButton.setText('')
            self.pushButton_2.setText('')
            self.pushButton_5.setText('')
            self.pushButton_4.setText('')
            self.b=False
            self.frame.setFixedWidth(75)


        else:
            self.b=True
            self.label.setText('QT Charts')
            self.label_2.setText('Support Me')
            self.label_3.setText('Patreon')
            self.label_4.setText('Subscribe to Youtube')
            self.label_5.setText('Follow')
            self.pushButton.setText('Logout')
            self.pushButton_2.setText('Sign up with new id')
            self.pushButton_5.setText('Submit the Bid')
            self.pushButton_4.setText('Account Info')
            self.frame.setFixedWidth(200)

if __name__=='__main__':
    app = QApplication(sys.argv)
    widget = mainApp()
    widget.show()
    app.exec()
