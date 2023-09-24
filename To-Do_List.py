from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
from PyQt5 import uic
import mysql.connector as mdb
from win32gui import *

class views(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("P32.ui", self)
        self.setWindowTitle("p2")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.main_con = self.findChild(QTextEdit,"main_con")
        self.main_title = self.findChild(QLabel,"main_title")
        self.collapse = self.findChild(QPushButton,"collapse")
        self.n = 0
        self.collapse.clicked.connect(self.cls)
        self.con = mdb.connect(host="localhost", user="root", passwd="drumStick_4011", database="tdl2", auth_plugin='mysql_native_password')
        self.curs = self.con.cursor()

    
    def added(self,text,text1,m):
        self.main_con.setPlainText(text)
        self.main_title.setText(text1)
        self.n = m
    
    def cls(self):
        q = f"select task_name,task_cont from tasks where sr_no = '{self.n+1}'"
        self.curs.execute(q)
        result = self.curs.fetchall()
        value = result[0][1]
        self.pt = 1
        if value != self.main_con.toPlainText():
            q = f"update tasks set task_cont = '{self.main_con.toPlainText()}' where sr_no = '{self.n+1}';"
            self.curs.execute(q)
            self.con.commit()
        else:
            pass
        self.close()

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("TDL.ui", self)
        self.setWindowTitle("To-Do List")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(480,50)
        #self.setWindowFlag(QtCore.Qt.Tool)
        #self.setWindowOpacity(0.1)

        self.m = 0
        self.ext = self.findChild(QPushButton,"ext")
        self.exp = self.findChild(QPushButton,"exp")
        self.task_input = self.findChild(QLineEdit, "task_in")
        self.add = self.findChild(QPushButton, "add")
        self.finish = self.findChild(QPushButton, "sub")
        self.lst_vw = self.findChild(QListWidget,"task_out")
        self.warning = self.findChild(QLabel,"warning")
        self.warning.setHidden(True)
        self.st = 0
        self.swt = 0
        self.task_input.setPlaceholderText("Task")
        self.con = mdb.connect(host="localhost", user="root", passwd="drumStick_4011", database="tdl2", auth_plugin='mysql_native_password')
        self.curs = self.con.cursor()
        q = f"select task_name,task_cont from tasks"
        self.curs.execute(q)
        result = self.curs.fetchall()
        if result == []:
            self.lst_vw.addItem("No Tasks")
        else:
            rows = len(result)
            ele = result[0]
            columns = (len(ele))
            for k in range(rows):
                tup = result[k]
                self.lst_vw.addItem(tup[0])

        self.ext.clicked.connect(self.out)
        self.finish.clicked.connect(self.deletion)
        self.add.clicked.connect(self.adding)
        self.exp.clicked.connect(self.cl)
        self.lst_vw.itemClicked.connect(self.pl)
        self.oldPos = self.pos()
        self.w = views()
        self.show()

    def out(self):
        self.close()
        self.w.close()

    #To-Do List functions
    def cl(self):
        #full size
        if self.st == 0:
            width = 480
            height = 480
            self.setFixedSize(width,height)
            self.st = 1
            self.exp.setText(">")
        #collapsed
        else:
            width = 480
            height = 50
            self.setFixedSize(width,height)
            self.st = 0
            self.exp.setText("<")
            self.w.close()
        
    #Task Description
    def pl(self,l):
        self.lst_vw.setFixedSize(461,381)
        self.warning.setHidden(True)
        #full size
        #This checks to see of the window is closed and opens it
        if self.swt == 0:
            self.swt = 1
            self.m = self.lst_vw.currentRow()
            self.w.show()
            x = self.x()
            y = self.y()
            self.pt = 0
            self.n_x = QPoint(x+490,y)
            self.w.move(self.n_x.x(),self.n_x.y())
            q = f"select task_name,task_cont from tasks where sr_no = '{self.m+1}'"
            self.curs.execute(q)
            result = self.curs.fetchall()
            print(result)
            value = result[0][1]
            value1 = result[0][0]
            self.w.added(value,value1,self.m)
        #This case is for when the window is already open
        else:
            #When the same item is clicked again, results in closing of the window
            if l == self.lst_vw.item(self.m):
                self.swt = 0
                self.w.close()
            #When a different item is clicked, result in display of the information of the selected item
            else:
                self.m = self.lst_vw.currentRow()
                q = f"select task_name,task_cont from tasks where sr_no = '{self.m+1}'"
                self.curs.execute(q)
                result = self.curs.fetchall()
                value = result[0][1]
                value1 = result[0][0]
                self.w.added(value,value1,self.m)          
        

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        x = self.x() + delta.x()
        y = self.y() + delta.y()
        self.move(x,y)
        self.n_x = QPoint(x+490,y)
        self.w.move(self.n_x.x(),self.n_x.y())
        self.oldPos = event.globalPos()
        window_handle = FindWindow(None, "To-Do List")
        window_rect = GetWindowRect(window_handle)        

    def deletion(self):
        self.w.close()
        self.lst_vw.setFixedSize(461,381)
        self.warning.setHidden(True)
        self.m = self.lst_vw.currentRow()
        q = f"delete from tasks where sr_no = '{self.m+1}'"
        self.curs.execute(q)
        self.con.commit()

        strai = ["set @num :=0", "update tasks set sr_no = @num :=(@num+1);", "alter table tasks auto_increment=1;"]
        for i in strai:
            q = i
            self.curs.execute(q)
            self.con.commit()

        self.lst_vw.clear()
        q = f"select task_name from tasks"
        self.curs.execute(q)
        result = self.curs.fetchall()
        if result == []:
            self.lst_vw.addItem("No Tasks")
        else:
            rows = len(result)
            ele = result[0]
            columns = (len(ele))
            for k in range(rows):
                tup = result[k]
                self.lst_vw.addItem(tup[0])
        self.swt = 0

    def adding(self):
        self.lst_vw.setFixedSize(461,381)
        self.warning.setHidden(True)
        t_inptt = self.task_input.text()
        self.task_input.clear()
        self.curs = self.con.cursor()
        if t_inptt != "":
            self.task_input.setPlaceholderText("Task")
            q = f"insert into tasks(task_name,task_cont) values('{t_inptt}','')"
            self.curs.execute(q)
            self.con.commit()
            self.lst_vw.clear()
            q = f"select task_name from tasks"
            self.curs.execute(q)
            result = self.curs.fetchall()
            rows = len(result)
            ele = result[0]
            columns = (len(ele))
            for k in range(rows):
                tup = result[k]
                self.lst_vw.addItem(tup[0])
            strai = ["set @num :=0", "update tasks set sr_no = @num :=(@num+1);", "alter table tasks auto_increment=1;"]
            for i in strai:
                q = i
                self.curs.execute(q)
                self.con.commit()
        else:
            self.task_input.setPlaceholderText("Invalid")


app = QApplication(sys.argv)
UIWindow = mainwindow()
app.exec_()

#By Sahil Dave
