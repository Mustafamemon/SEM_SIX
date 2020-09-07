# import stemming as s 
# import inverted_index as  inv_ind
# import and_or_not_oper as oper

import re
import stemming as s
import positional_index as pos_ind
import inverted_index as  inv_ind
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic, Qt
from PyQt5.QtWidgets import (QTableWidgetItem,QMessageBox) 	
from PyQt5.QtGui import QPalette


qtCreatorFile = "gui.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

    




class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    which_query = 0
    text = ''
    output = ''
    filePath = ''


    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)      
        self.filePath = "E:\Fast\SEM 6\IR\Assign - 1"
        self.text = self.lineEdit

        self.output = self.tableWidget
        self.pushButton_get_input.clicked.connect(self.outpu)
        self.pushButton.clicked.connect(self.readFile)
        self.radioButton_boolean.toggled.connect(self.boolean)
        self.radioButton_positional.toggled.connect(self.positional)
        self.radioButton_phrasal.toggled.connect(self.phrasal)
        self.pushButton.setStyleSheet(" QPushButton{ color : #1880ff; }");
        self.label_2.setStyleSheet("QLabel { color : #1880ff; }");
        self.label_3.setStyleSheet("QLabel { color : #1880ff; }");
        self.label_4.setStyleSheet("QLabel { color : #1880ff; }");
        self.radioButton_boolean.setStyleSheet("QRadioButton { color : #1880ff; }");
        self.radioButton_positional.setStyleSheet("QRadioButton { color : #1880ff; }");
        self.radioButton_phrasal.setStyleSheet("QRadioButton { color : #1880ff; }");
        self.pushButton_get_input.setStyleSheet("QPushButton { color : #1880ff; }");
    def readFile(self):
        self.pushButton_get_input.setEnabled(False)
        
        f=open(self.filePath+"\Stopword-List.txt", "r")
        
        if os.path.exists(self.filePath+"\pos_index.json"):
            os.remove(self.filePath+"\pos_index.json")
            

        stop_word  = f.read()
        stop_word  = stop_word.split('\n')
        stop_word = [i for i in stop_word if i]
        content = ""
        special_char = ['.',' ',',','[',']','(',')','"',':','?','','-']
        self.output.setRowCount(2)
        self.output.setColumnCount(1)
        self.output.setHorizontalHeaderLabels(['Processing'])
        header = self.output.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.output.setItem(0,0,QTableWidgetItem(str("processing documents ...")))   
        for doc_no in range(0,56):
            f=open(self.filePath+'\Trump Speechs\speech_'+str(doc_no)+".txt", "r")
            content         =  f.read()
            content = content.split('\n')[1]
            
            content_list    =  re.split(r'(\.|,|\[|\]|—| |:|\(|\)|"|\?|\\n|-)+',content)
            r_special_char  =  list(set(content_list)-set(special_char))
            r_stop_word     =  list(set(r_special_char) - set(stop_word))
            stem_list       =  s.stemming_word(r_stop_word)
            # posting_dic     =   inv_ind.inverted_index(stem_list,doc_no)
            for char in special_char:           
                content_list = list(filter(lambda a: a != char, content_list))
            
            stop_stem_list =  s.stemming_word(content_list)
            postion_dic    =  pos_ind.postional_index(stem_list,doc_no,stop_stem_list)
            
            print("processing doc no ...",doc_no)

        self.output.setItem(1,0,QTableWidgetItem(str("processing complete")))   
            
        self.pushButton_get_input.setEnabled(True)
        
    
    def boolean(self,selected):
        if selected:
            self.which_query = 1

    def phrasal(self,selected):
        if selected:
            self.which_query = 2

    def positional(self,selected):
        if selected:
            self.which_query = 3
    
    def outpu(self):
        s = self.text.text()
        answer = None
        
        if len(s) is 0:
            self.AlertBox('Invalid Input','Please enter valid input')
        elif self.which_query is 0 :
            self.AlertBox('No Query Selected','Please select quert')
        elif self.which_query is 1:
            answer = inv_ind.inverted_output(s)
            if answer is not 1:
                self.output.setRowCount(len(answer))
                self.output.setColumnCount(1)
                self.output.setHorizontalHeaderLabels(['doc ID'])
                header = self.output.horizontalHeader()       
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                
                for docID in answer:
                    inx = answer.index(docID)
                    self.output.setItem(inx,0,QTableWidgetItem(str(docID)))
        elif self.which_query is 2:
            s = s + ' /0'
            answer = pos_ind.postional_output(s)
        elif self.which_query is 3:
           answer = pos_ind.postional_output(s)
        if answer is 1:
            self.AlertBox('Key Not Found','Please enter a valid key')
        elif self.which_query is not 0 and  self.which_query is not 1:
            self.output.setRowCount(len(answer))
            self.output.setColumnCount(2)
            self.output.setHorizontalHeaderLabels(['doc ID','Word Index'])
            header = self.output.horizontalHeader()       
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            
            for row in answer:
                inx = answer.index(row)
                row = list(row)
                docID = row[0]
                row.pop(0)
                word_index = row 
                s = [str(i) for i in row] 
                word_index = ",".join(s) 
                self.output.setItem(inx,1,QTableWidgetItem(word_index))   
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

    
    