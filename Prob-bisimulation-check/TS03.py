from PyQt5 import QtCore, QtGui, QtWidgets
from final_window2 import Ui_Final_window


class ThirdWindow(object):

    def openWindow(self):
        self.window3  = QtWidgets.QMainWindow()
        self.ui3 = Ui_Final_window()
        #self.get_nums()                             # it's important for get num function to be before Show function. 
        self.send_dict()
        self.ui3.setupUi(self.window3)                # Because it should deliver the number of cells. 
        self.window3.show()
        self.get_params()

    def get_nums(self):
        TS02 = self.lineEdit_edges.text()
        TS01 = self.TS01
        self.ui2.TS02 = TS02
        self.ui2.TS01 = TS01

    def get_params(self): 
        TS02 = int(self.TS02)  
        self.S = []
        self.L = []
        self.W = []                               # S = Start Nodes, L= label , W = WK , E = End Node .
        self.E = []                               # S = Start Nodes, L= label , W = WK , E = End Node .
       
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        s = 1 
        l = 2
        w = 3 
        e = 4
        for i in range(TS02):

            exec(f'self.S.append(self.lineEdit_{s}.text())')
            exec(f'self.L.append(self.lineEdit_{l}.text())')
            exec(f'self.W.append(self.lineEdit_{w}.text())')
            exec(f'self.E.append(self.lineEdit_{e}.text())')
            s+=4 
            l+=4
            w+=4
            e+=4
        self.S = [x.upper() for x in self.S]  # Start Nodes Should be in Upper Case
        self.L = [x.lower() for x in self.L ]
        self.W = [float(x) for x in self.W]
        self.E = [x.upper() for x in self.E]

    def graphshow(self):
        from TS02_graph import TS02_graph
        from PyQt5.QtGui import QPixmap
        self.get_params()

        res = self.check_props(self.S, self.L, self.W)
        different_start = self.check_letters_start()
        different_end = self.check_letters_end()
        different_letters = different_start and different_end

        if res and different_letters:
            TS02_graph(self.S, self.L, self.W, self.E)
            pixmap = QPixmap("TS02.gy.png")
            self.scene.addPixmap(pixmap)
            self.graphicsView.adjustSize()
        
        elif res and not different_letters : 
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error, Dont use The same Node names used in Previous Pr _1 ")
            msg.setInformativeText('Please recheck the Node names')
            msg.setWindowTitle("Error")
            msg.exec_()
            
        else:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error, One of Label Probs is not 1")
            msg.setInformativeText('Please recheck the probabilities')
            msg.setWindowTitle("Error")
            msg.exec_()

    def send_dict(self): 
        from convert_list_to_dict_08 import list2dict
        self.get_params()
        TS_02 = list2dict(self.S, self.L, self.W, self.E)
        self.ui3.TS_02 = TS_02
        self.ui3.TS_01 = self.TS_01

    def check_props(self, S,L,W):                                     # This function check if every node label summation is 1 . 
        # create a dictionary of nodes with their corresponding labels and probabilities
        node_dict = {}
        result = []
        for node, label, prob in zip(S, L, W):
            if node not in node_dict:
                node_dict[node] = {}
            if label not in node_dict[node]:
                node_dict[node][label] = prob
            else:
                node_dict[node][label] += prob

        # check if the summation of each label in a node is equal to 1
        for node, labels in node_dict.items():
            for prob in labels.values():
                if prob != 1:
                    #print("False")
                    result.append('False')
                    
                    #return False
                    break
            else:
                #print("True")
                result.append('True')
                #return True
        if len(set(result)) ==1 and result[0] == 'True':
            return True
        else:
            return False
    
    def check_letters_start(self):
        LN = self.TS_01
        LO = LN.target.values.tolist()
        LP = LN.Node.values.tolist()
        LQ = [*LO,*LP]
        LN2 = self.S
        for i in LN2 : 
            if i in LQ:
                return False
                break
        return True

    def check_letters_end(self):
        Ln = self.TS_01
        Lo = Ln.target.values.tolist()
        Lp = Ln.Node.values.tolist()
        Lq = [*Lo,*Lp]
        Ln2 = self.E
        for j in Ln2 :
            if j in Lq:
                return False
                break
        return True

    def update(self):
            SecondWindow = QtWidgets.QMainWindow()
            ui = ThirdWindow()
            ui.setupUi(SecondWindow,TS02=int(self.lineEdit_edges.text()))
            SecondWindow.show()

    def setupUi(self, SecondWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(993, 790)
        self.centralwidget = QtWidgets.QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 30, 650, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(560, 50, 421, 531))


        self.graphicsView.setMinimumHeight(531)                                                 ## Size flixbility
        self.graphicsView.setMinimumWidth(421)                                                  ## Size flixbility
        self.graphicsView.setMaximumHeight(2000)                                                ## Size flixbility
        self.graphicsView.setMaximumWidth(2000)                                                 ## Size flixbility

        self.graphicsView.setObjectName("graphicsView")
        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)               # important lines
        self.graphicsView.setScene(self.scene)                                  # important lines
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(620, 20, 300, 27))
        font = QtGui.QFont()
        font.setFamily("AR PL UKai CN")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(830, 720, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openWindow)                # Open The last Window 
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 720, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.graphshow)               # Refresh Button Function 

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(41, 71, 100, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(325, 71, 50, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(429, 71, 100, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(190, 71, 50, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")



        TS02 = int(self.TS02)

        k =1    # name of textboxes
        l = 6   # the label name of (:) label
        h = 110 # height for every line 

        for i in range(TS02):

            exec(f'self.lineEdit_{k} = QtWidgets.QLineEdit(self.centralwidget)')
            exec(f'self.lineEdit_{k}.setGeometry(QtCore.QRect(40, h, 111, 31))')
            exec(f'self.lineEdit_{k}.setObjectName("lineEdit_{k}")')
            k = k+1 

            exec(f'self.lineEdit_{k} = QtWidgets.QLineEdit(self.centralwidget)')
            exec(f'self.lineEdit_{k}.setGeometry(QtCore.QRect(160, h, 111, 31))')
            exec(f'self.lineEdit_{k}.setObjectName("lineEdit_{k}")')
            k = k+1 

            exec(f'self.label_{l} = QtWidgets.QLabel(self.centralwidget)')
            exec(f'self.label_{l}.setGeometry(QtCore.QRect(280, h-10, 31, 41))')
            font = QtGui.QFont()
            font.setPointSize(10)
            exec(f'self.label_{l}.setFont(font)')
            exec(f'self.label_{l}.setObjectName("label_{l}")')
            exec(f'self.label_{l}.setText(":")')

            exec(f'self.lineEdit_{k} = QtWidgets.QLineEdit(self.centralwidget)')
            exec(f'self.lineEdit_{k}.setGeometry(QtCore.QRect(290, h, 111, 31))')
            exec(f'self.lineEdit_{k}.setObjectName("lineEdit_{k}")')
            k = k+1 

            exec(f'self.lineEdit_{k} = QtWidgets.QLineEdit(self.centralwidget)')
            exec(f'self.lineEdit_{k}.setGeometry(QtCore.QRect(410, h, 111, 31))')
            exec(f'self.lineEdit_{k}.setObjectName("lineEdit_{k}")')
            k = k+1 
            h = h+40



        SecondWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SecondWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 993, 22))
        self.menubar.setObjectName("menubar")
        SecondWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SecondWindow)
        self.statusbar.setObjectName("statusbar")
        SecondWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)


    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "New transition system"))
        self.label.setText(_translate("SecondWindow", "Please enter the transitions on each line:"))
        self.label_7.setText(_translate("SecondWindow", "Transition system 02 Graph "))
        self.pushButton.setText(_translate("SecondWindow", "Next"))
        self.pushButton_2.setText(_translate("SecondWindow", "Show"))
        self.label_2.setText(_translate("SecondWindow", "Start Node"))
        self.label_4.setText(_translate("SecondWindow", "Prob"))
        self.label_5.setText(_translate("SecondWindow", "End Node"))
        self.label_3.setText(_translate("SecondWindow", "Label"))



if __name__ == "__main__":
    import sys
    import final_window
    app = QtWidgets.QApplication(sys.argv)
    SecondWindow = QtWidgets.QMainWindow()
    ui = ThirdWindow()
    ui.setupUi(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())
