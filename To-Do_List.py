from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
from PyQt5 import uic
import sys
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
        con = mdb.connect(host="localhost", user="root", passwd="", database="tdl2", auth_plugin='mysql_native_password')
        curs = con.cursor()
    
    def added(self,text,text1):
        self.main_con.setPlainText(text)
        self.main_title.setText(text1)

    def add2(self,text):
        self.add_tsk.setHidden(False)
        self.main_title.setText(text)

    def get_val(self):
        txt = self.main_con.toPlainText()
        return txt

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
        self.view = self.findChild(QPushButton,"view")
        self.warning = self.findChild(QLabel,"warning")
        self.warning.setHidden(True)
        self.st = 1
        self.pt = 1
        self.task_input.setPlaceholderText("Task")
        con = mdb.connect(host="localhost", user="root", passwd="", database="tdl2", auth_plugin='mysql_native_password')
        curs = con.cursor()
        q = f"select task_name,task_cont from tasks"
        curs.execute(q)
        result = curs.fetchall()
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
        self.view.clicked.connect(self.pl)
        self.oldPos = self.pos()
        self.w = views()
        self.show()

    def out(self):
        self.close()
        self.w.close()

    #To-Do List function
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
    def pl(self):
        self.view.setFixedSize(31,381)
        self.lst_vw.setFixedSize(421,381)
        self.warning.setHidden(True)
        self.m = self.lst_vw.currentRow()
        #full size
        if self.pt == 1:
            if self.m != -1:
                self.w.show()
                x = self.x()
                y = self.y()
                self.pt = 0
                self.n_x = QPoint(x+490,y)
                self.w.move(self.n_x.x(),self.n_x.y())
                self.view.setText("S\nA\nV\nE\n \nA\nN\nD\n \nC\nL\nO\nS\nE")
                con = mdb.connect(host="localhost", user="root", passwd="", database="tdl2",auth_plugin='mysql_native_password')
                curs = con.cursor()
                q = f"select task_name,task_cont from tasks where sr_no = '{self.m+1}'"
                curs.execute(q)
                result = curs.fetchall()
                value = result[0][1]
                value1 = result[0][0]
                self.w.added(value,value1)
                #print(value,value1)
            else:
                self.view.setFixedSize(31,361)
                self.lst_vw.setFixedSize(421,361)
                self.warning.setHidden(False)
                print("problem")

        #collapsed
        else:
            self.view.setText("S\nH\nO\nW")
            con = mdb.connect(host="localhost", user="root", passwd="", database="tdl2",auth_plugin='mysql_native_password')
            curs = con.cursor()
            q = f"select task_name,task_cont from tasks where sr_no = '{self.m+1}'"
            curs.execute(q)
            result = curs.fetchall()
            value = result[0][1]
            self.pt = 1
            #print(self.w.get_val())
            if value != self.w.get_val():
                q = f"update tasks set task_cont = '{self.w.get_val()}' where sr_no = '{self.m+1}';"
                curs.execute(q)
                con.commit()
            else:
                pass
            self.w.close()

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
        self.view.setText("S\nH\nO\nW")
        self.view.setFixedSize(31,381)
        self.lst_vw.setFixedSize(421,381)
        self.warning.setHidden(True)
        self.m = self.lst_vw.currentRow()
    
        con = mdb.connect(host="localhost", user="root", passwd="", database="tdl2",auth_plugin='mysql_native_password')
        curs = con.cursor()
        q = f"delete from tasks where sr_no = '{self.m+1}'"
        curs.execute(q)
        con.commit()

        strai = ["set @num :=0", "update tasks set sr_no = @num :=(@num+1);", "alter table tasks auto_increment=1;"]
        for i in strai:
            q = i
            curs.execute(q)
            con.commit()

        self.lst_vw.clear()
        q = f"select task_name from tasks"
        curs.execute(q)
        result = curs.fetchall()
        if result == []:
            self.lst_vw.addItem("No Tasks")
        else:
            rows = len(result)
            ele = result[0]
            columns = (len(ele))
            for k in range(rows):
                tup = result[k]
                self.lst_vw.addItem(tup[0])

    def adding(self):
        self.view.setFixedSize(31,381)
        self.lst_vw.setFixedSize(421,381)
        self.warning.setHidden(True)
        t_inptt = self.task_input.text()
        self.task_input.clear()
        con = mdb.connect(host="localhost", user="root", passwd="", database="tdl2",auth_plugin='mysql_native_password')
        curs = con.cursor()
        if t_inptt != "":
            self.task_input.setPlaceholderText("Task")
            q = f"insert into tasks(task_name,task_cont) values('{t_inptt}','')"
            curs.execute(q)
            con.commit()
            self.lst_vw.clear()
            q = f"select task_name from tasks"
            curs.execute(q)
            result = curs.fetchall()
            rows = len(result)
            ele = result[0]
            columns = (len(ele))
            for k in range(rows):
                tup = result[k]
                self.lst_vw.addItem(tup[0])
            
        else:
            self.task_input.setPlaceholderText("Invalid")

app = QApplication(sys.argv)
UIWindow = mainwindow()
app.exec_()

#By Sahil Dave
