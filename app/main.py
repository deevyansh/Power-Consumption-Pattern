# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6 import uic
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui',self)
        self.setWindowTitle('MyApp1')
        self.Button.clicked.connect(self.sayhello)
    def sayhello(self):
        inputtext=self.input.text()
        self.output.setText(f'{inputtext}MKC')

app=QApplication(sys.argv)
window=MyApp()
window.show()
app.exec()
