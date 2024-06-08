
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from TS01 import Ui_FirstWindow

class Ui_WelcomeWindow(object):
    def openWindow(self):
        self.window  = QtWidgets.QMainWindow()
        self.ui = Ui_FirstWindow()
        self.get_nums()                             # it's important for get num function to be before Show function. 
        self.ui.setupUi(self.window)                # Because it should deliver the number of cells. 
        self.window.show()

    
    def get_nums(self):
        TS01 = self.lineEdit.text()
        TS02 = self.lineEdit_2.text()
        self.ui.TS01 = TS01                          # sendiing variables to the next Window
        self.ui.TS02 = TS02



    def setupUi(self, WelcomeWindow):
        WelcomeWindow.setObjectName("WelcomeWindow")
        WelcomeWindow.resize(1100, 307)
        self.centralwidget = QtWidgets.QWidget(WelcomeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 461, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(20, 20, 1100, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 221, 91))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 221, 91))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(230, 120, 113, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(230, 180, 113, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.Onlyint = QIntValidator(1,100)
        self.lineEdit.setValidator(self.Onlyint)
        self.lineEdit_2.setValidator(self.Onlyint)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)

        self.pushButton.clicked.connect(self.openWindow)                 #  Apply Button Function. 

        self.pushButton.setGeometry(QtCore.QRect(480, 230, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        WelcomeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WelcomeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 509, 22))
        self.menubar.setObjectName("menubar")
        WelcomeWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WelcomeWindow)
        self.statusbar.setObjectName("statusbar")
        WelcomeWindow.setStatusBar(self.statusbar)

        self.retranslateUi(WelcomeWindow)
        QtCore.QMetaObject.connectSlotsByName(WelcomeWindow)

    def retranslateUi(self, WelcomeWindow):
        _translate = QtCore.QCoreApplication.translate
        WelcomeWindow.setWindowTitle(_translate("WelcomeWindow", "Prob. Bisimulation check"))
        self.label_1.setText(_translate("WelcomeWindow", "Welcome to our bisimulation check program, you can first "
                                                         "enter the Number of transitions of each transition system:"))
        self.label_2.setText(_translate("WelcomeWindow", "Transition system 01 :"))
        self.label_3.setText(_translate("WelcomeWindow", "Transition system 02 :"))
        self.pushButton.setText(_translate("WelcomeWindow", "Next"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WelcomeWindow = QtWidgets.QMainWindow()
    ui = Ui_WelcomeWindow()
    ui.setupUi(WelcomeWindow)
    WelcomeWindow.show()
    sys.exit(app.exec_())