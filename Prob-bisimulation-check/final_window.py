# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'final_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from TS03 import ThirdWindow


class Ui_Final_window(QtWidgets.QWidget):

    def graphshow(self):
        from PyQt5.QtGui import QPixmap
        pixmap1 = QPixmap("TS01.gy.png")
        self.scene1.addPixmap(pixmap1)
        pixmap2 = QPixmap("TS02.gy.png")
        self.scene2.addPixmap(pixmap2)
        self.results()
        

    def results(self):
        from bisimilar_test_improved import bisimilarity_test

        equivalence_classes, laufzeit = bisimilarity_test(self.TS_01,self.TS_02)
        self.label_4.setText('The equivalence classes are = ' + equivalence_classes)
        self.label_5.setText('Running Time = ' + laufzeit + ' seconds')


    def get_nums(self,TT):
        TS02 = self.TS02
        TS01 = self.TS01
        self.ui2.TS02 = TT
        self.ui2.TS01 = TS01
        self.ui2.TS_01 = self.TS_01

    def openWindow(self):
        self.window2  = QtWidgets.QMainWindow()
        self.ui2 = ThirdWindow()
        self.get_nums(self.TTT)                               # it's important for get num function to be before Show function.
        self.ui2.setupUi(self.window2)                # Because it should deliver the number of cells. 
        self.window2.show()

    def take_new(self):
        name,done1  =QtWidgets.QInputDialog.getInt(
            self,'New transition system Edges' , 'Please enter the number of transitions for the new transition system : ')
        if done1 : 
            print("Done  : " ,name)
            self.TTT = name
            self.openWindow()
            

    def setupUi(self, Final_window):
        Final_window.setObjectName("Final_window")
        Final_window.resize(1660, 750)
        self.centralwidget = QtWidgets.QWidget(Final_window)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 50, 800, 500))

        self.graphicsView.setMinimumHeight(500)                                                 ## Size flixbility
        self.graphicsView.setMinimumWidth(570)                                                  ## Size flixbility
        self.graphicsView.setMaximumHeight(3000)                                                ## Size flixbility
        self.graphicsView.setMaximumWidth(3000)                                                 ## Size flixbility


        self.graphicsView.setObjectName("graphicsView")
        self.scene1 = QtWidgets.QGraphicsScene(self.centralwidget)               # important lines
        self.graphicsView.setScene(self.scene1)                                  # important lines   
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(840, 50, 800, 500))

        self.graphicsView_2.setMinimumHeight(500)                                                 ## Size flixbility
        self.graphicsView_2.setMinimumWidth(370)                                                  ## Size flixbility
        self.graphicsView_2.setMaximumHeight(3000)                                                ## Size flixbility
        self.graphicsView_2.setMaximumWidth(3000)                                                 ## Size flixbility

        self.graphicsView_2.setObjectName("graphicsView_2")
        self.scene2 = QtWidgets.QGraphicsScene(self.centralwidget)               # important lines
        self.graphicsView_2.setScene(self.scene2)                                # important lines   
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 20, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1120, 20, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 590, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(562, 690, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.graphshow)                     # update graphs
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(720, 690, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(Final_window.close)                      # Exit button
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 560, 1000, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)                     # identical result labels
        self.label_5.setGeometry(QtCore.QRect(30, 590, 4000, 80))
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        ###########################
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(878, 690, 150, 30))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton")
        self.pushButton_3.clicked.connect(self.take_new)                     # Replay Button
        ##########################


        Final_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Final_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 22))
        self.menubar.setObjectName("menubar")
        Final_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Final_window)
        self.statusbar.setObjectName("statusbar")
        Final_window.setStatusBar(self.statusbar)

        self.retranslateUi(Final_window)
        QtCore.QMetaObject.connectSlotsByName(Final_window)

    def retranslateUi(self, Final_window):
        _translate = QtCore.QCoreApplication.translate
        Final_window.setWindowTitle(_translate("Final_window", "Result"))
        self.label.setText(_translate("Final_window", "Transition system 01"))
        self.label_2.setText(_translate("Final_window", "Transition system 02"))
        self.label_3.setText(_translate("Final_window", ""))
        self.pushButton.setText(_translate("Final_window", "Show Result"))
        self.pushButton_2.setText(_translate("Final_window", "Exit"))
        self.pushButton_3.setText(_translate("Final_window", "Replay"))
        self.label_4.setText(_translate("Final_window", "Select one from the following options:"))
        self.label_5.setText(_translate("Final_window", "To show the result, please click on “Show Result” \n" "To end the program, please click on “Exit” \n"
                                                        "To compare the first transition system with another transition system, please click on “Replay” " ))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Final_window = QtWidgets.QMainWindow()
    ui = Ui_Final_window()
    ui.setupUi(Final_window)
    Final_window.show()
    sys.exit(app.exec_())
