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
from PyQt6.QtCore import QRect
from functools import partial

class RegisterWindow(QWidget):
    def __init__(self,p,button):
        super().__init__()
        self.button = button
        self.button[1].hide()
        self.button[2].hide()
        self.button[3].hide()
        self.button[0].show()
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
        cursor = db.cursor()
        data = (self.Usernamet.text(),self.Passwordt.text(),self.Emailt.text(),'1999-01-01')
        insert_query = "INSERT INTO logindata (Username,Password,Email,minlimit) VALUES(%s,%s,%s,%s)"
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()
        self.p.setCurrentIndex(1)
        # self.App=MainApp(self.Usernamet.text())
        # self.App.show()



class AdminApp(QWidget):
    def __init__(self,p):
        super().__init__()
        self.p=p
        self.setWindowTitle('Admin Window')
        self.resize(400,400)
        loadUi("Admin1.ui", self)
        # map=QPixmap('Screenshot 2024-04-21 at 9.30.01 PM (1).png')
        # self.label.setPixmap(map)
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

        # self.anim1=QPropertyAnimation(self.fr3,b'geometry')
        # self.anim1.setDuration(400)
        # react=self.fr3.geometry()
        # self.anim1.setStartValue(react)
        # react.translate(0,-120)
        # self.anim1.setEndValue(react)

        # self.anim2 = QPropertyAnimation(self.frame_2, b'geometry')
        # self.anim2.setDuration(400)
        # react = self.frame_2.geometry()
        # self.anim2.setStartValue(react)
        # react.setHeight(react.height() - 100)
        # self.anim2.setEndValue(react)
    def open1(self):
        self.p.insertWidget(1,LoginWindow(self.p,self.button))
        self.p.setCurrentIndex(1)
    def open2(self):
        self.p.insertWidget(2,RegisterWindow(self.p,self.button))
        self.p.setCurrentIndex(2)

    def yes(self):
        self.YesButton.hide()
        self.NoButton.hide()
        self.b=True
    def no(self):
        self.Text.setText('Please enter your Price, Quantity and Hours')
        self.fr5.hide()
        self.fr6.hide()
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
        self.p.insertWidget(5,ResultApp(self.username,self.p,self.button))
        self.p.setCurrentIndex(5)
        return


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
        self.button[0].clicked.connect(self.open1)
        self.button[1].clicked.connect(self.open2)
        self.button[2].setText('Make a Deal')
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



class LoginWindow(QWidget):
    def __init__(self,p,button):
        super().__init__()
        self.button1 = button
        self.button1[0].hide()
        self.button1[2].hide()
        self.button1[3].hide()
        self.button1[1].show()
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
            QUrl.fromLocalFile('Screen Recording 2024-05-10 at 3.57.47 PM (online-video-cutter.com).mp4'))
        self.mediaplayer.setVideoOutput(self.vedio)
        self.mediaplayer.play()
        self.mediaplayer.playbackStateChanged.connect(lambda: self.mediaplayer.play())


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
                    self.p.setCurrentIndex(3)
            else:
                self.status.setText("Password is not correct")
        else:
            self.status.setText("Username not found")
        cursor.close()
        db.close()



class mainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.resize(400, 400)
        loadUi('graph_simulation.ui',self)
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
        self.pushButton.setIcon(QIcon('png-clipart-computer-icons-desktop-others-miscellaneous-angle.png'))
        self.pushButton_4.setIcon(QIcon('acc.jpeg'))
        layout=QVBoxLayout()
        self.a.setLayout(layout)
        button=[self.pushButton,self.pushButton_2,self.pushButton_5,self.pushButton_4]
        self.a.insertWidget(2, RegisterWindow(self.a,button))
        self.a.insertWidget(3,AdminApp(self.a))
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

        else:
            self.b=True
            self.label.setText('QT Charts')
            self.label_2.setText('Support Me')
            self.label_3.setText('Patreon')
            self.label_4.setText('Subscribe to Youtube')
            self.label_5.setText('Follow')
            self.pushButton.setText('Logout')
            self.pushButton_2.setText('Sign up with new id')
            self.pushButton_5.setText('Make a new Deal')
            self.pushButton_4.setText('Account Info')



if __name__=='__main__':
    app = QApplication(sys.argv)
    widget = mainApp()
    widget.show()
    app.exec()
