
import re
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic, Qt
from PyQt5.QtWidgets import (QTableWidgetItem,QMessageBox) 	
from PyQt5.QtGui import QPalette , QIntValidator

from KMean import KMeanDriver
from KNN import KNNDriver


qtCreatorFile = "gui.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    test_data = 0
    train_data = 0
    K = 0
    choice = 0
    output = ''
    

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)      
        

        self.test_data  = self.lineEdit
        self.train_data = self.lineEdit_2
        self.K          = self.lineEdit_3
        self.test_data.setValidator(QIntValidator(1, 99))
        self.K.setValidator(QIntValidator(0, 9))
        
        self.test_data.textChanged.connect(self.setTrainData)
        self.train_data.setReadOnly(True)
        self.train_data.setText(str(100))
        
        
        
        self.radioButton.toggled.connect(lambda : self.Choice(1))
        self.radioButton_2.toggled.connect(lambda : self.Choice(2))
        
        self.output = self.tableWidget
        self.pushButton_get_input.clicked.connect(self.RunModel)
        # self.pushButton_get_input.setStyleSheet(" QPushButton{ color : #1880ff; }");
        # self.label_2.setStyleSheet("QLabel { color : #1880ff; }");
        # self.label_3.setStyleSheet("QLabel { color : #1880ff; }");
        # self.label_4.setStyleSheet("QLabel { color : #1880ff; }");
        self.pushButton_get_input.setStyleSheet("QPushButton { color : #1880ff; }");
    def setTrainData(self):
        value = self.test_data.text() is not '' and self.test_data.text() or 0
        self.train_data.setText(str(100 -  int(value)))
    def Choice(self,choice):
        self.choice = choice
        if self.choice is 2:
            self.test_data.setReadOnly(True)
            self.K.setReadOnly(True)
            self.K.setText('5')
            self.test_data.setText('')
            self.train_data.setText('')
        else:
            self.test_data.setReadOnly(False)
            self.K.setReadOnly(False)
            self.test_data.setText('')
            self.train_data.setText('100')
            self.K.setText('')
        


    def RunModel(self):
        
        
        if self.choice == 1 or self.choice == 2:
            self.output.setRowCount(1)
            self.output.setColumnCount(1)
            header = self.output.horizontalHeader()       
            Answer  = ''
        
        if self.choice == 1 :
            if self.train_data.text() == '' or self.test_data.text() == '' or self.K.text() == '':
                self.AlertBox('Invalid Input','Please Select One Option')   
                return 
            Answer =  KNNDriver(int(self.test_data.text()) / 100 , int(self.K.text()))
            self.output.setHorizontalHeaderLabels(['ACCURACY'])
        elif self.choice == 2:
            Answer =  KMeanDriver()
            self.output.setHorizontalHeaderLabels(['PURITY'])
        else:      
            self.AlertBox('Invalid Input','Please Select One Option')   
            return 
        
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.output.setItem(0,0,QTableWidgetItem(str(Answer)))
        
    
    def AlertBox(self,heading,message):
        buttonReply = QMessageBox.question(self,heading,message, QMessageBox.Ok)
        if buttonReply == QMessageBox.Ok:
            pass
        


        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

    
    