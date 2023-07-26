from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
from PyQt5 import uic
import sys
import mysql.connector as mdb
#from playsound import playsound

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("TDL.ui", self)
        self.setWindowTitle("To-Do List")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #self.setWindowFlag(QtCore.Qt.Tool)
        #self.setWindowOpacity(0.1)

        self.ext = self.findChild(QPushButton,"ext")
        self.exp = self.findChild(QPushButton,"exp")
        self.task_input = self.findChild(QLineEdit, "task_in")
        self.phl = self.findChild(QLabel,"first")
        self.add = self.findChild(QPushButton, "add")
        self.finish = self.findChild(QPushButton, "sub")
        self.lst_vw = self.findChild(QListWidget,"task_out")
        self.st = 0
        self.task_input.setPlaceholderText("Task")
        con = mdb.connect(host="localhost", user="root", passwd="password", database="database name", auth_plugin='mysql_native_password')
        curs = con.cursor()
        q = f"select task,due_in from p_tasks"
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
        self.phl.setText(self.lst_vw.item(0).text())
        self.oldPos = self.pos()
        self.show()

    def out(self):
        self.close()

    def cl(self):
        if self.st == 0:
            width = 480
            height = 480
            self.setFixedSize(width,height)
            self.st = 1
            self.exp.setText(">")
            self.phl.setText(self.lst_vw.item(0).text())
            self.phl.setHidden(True)
        else:
            width = 480
            height = 50
            self.setFixedSize(width,height)
            self.st = 0
            self.exp.setText("<")
            self.phl.setText(self.lst_vw.item(0).text())
            self.phl.setHidden(False)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def deletion(self):
        m = self.lst_vw.currentRow()
    
        con = mdb.connect(host="localhost", user="root", passwd="password", database="database name",auth_plugin='mysql_native_password')
        curs = con.cursor()
        q = f"delete from p_tasks where sr_no = '{m+1}'"
        curs.execute(q)
        con.commit()

        strai = ["set @num :=0", "update p_tasks set sr_no = @num :=(@num+1);", "alter table p_tasks auto_increment=1;"]
        for i in strai:
            q = i
            curs.execute(q)
            con.commit()

        self.lst_vw.clear()
        q = f"select task,due_in from p_tasks"
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
        t_inptt = self.task_input.text()
        self.task_input.clear()
        con = mdb.connect(host="localhost", user="root", passwd="password", database="database name",auth_plugin='mysql_native_password')
        curs = con.cursor()
        if t_inptt != "":
            self.task_input.setPlaceholderText("Task")
            q = f"insert into p_tasks(task,due_in) values('{t_inptt}','0')"
            curs.execute(q)
            con.commit()
            self.lst_vw.clear()
            q = f"select task,due_in from p_tasks"
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
