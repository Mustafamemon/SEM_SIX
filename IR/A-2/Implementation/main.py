
import re
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic, Qt
from PyQt5.QtWidgets import (QTableWidgetItem,QMessageBox) 	
from PyQt5.QtGui import QPalette

from reading_file import readFile
from query import Query

qtCreatorFile = "gui.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    text = ''
    output = ''
    

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)      
        self.text = self.lineEdit

        self.output = self.tableWidget
        self.pushButton_get_input.clicked.connect(self.outpu)
        self.pushButton.clicked.connect(self.readFile)
        self.pushButton.setStyleSheet(" QPushButton{ color : #1880ff; }");
        self.label_2.setStyleSheet("QLabel { color : #1880ff; }");
        self.label_3.setStyleSheet("QLabel { color : #1880ff; }");
        self.label_4.setStyleSheet("QLabel { color : #1880ff; }");
        self.pushButton_get_input.setStyleSheet("QPushButton { color : #1880ff; }");
    def readFile(self):
        self.pushButton_get_input.setEnabled(False)
        self.output.setRowCount(2)
        self.output.setColumnCount(1)
        self.output.setHorizontalHeaderLabels(['Processing'])
        header = self.output.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.output.setRowCount(2)
        self.output.setItem(0,0,QTableWidgetItem(str("processing start....")))   
        
        print('processing start....')
        readFile()
        
        self.output.setItem(1,0,QTableWidgetItem(str("processing complete...")))   
        
        print('processing complete....')
            
        self.pushButton_get_input.setEnabled(True)
        
    
    
    def outpu(self):
        s = self.text.text()
        answer = None
        
        if len(s) is 0 :
            self.AlertBox('Invalid Input','Please enter valid input')
        else:
            answer = Query(s)
            if answer is 0:
                self.AlertBox('Invalid Input','Please enter valid input')
            else:
                self.output.setRowCount(len(answer))
                self.output.setColumnCount(1)
                self.output.setHorizontalHeaderLabels(['doc ID'])
                header = self.output.horizontalHeader()       
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                
                for docID in answer:
                    inx = answer.index(docID)
                    self.output.setItem(inx,0,QTableWidgetItem(str(docID)))
        
                        
        
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

    
    