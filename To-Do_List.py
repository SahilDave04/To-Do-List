from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic
import sys
import mysql.connector as mdb


class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("TDL.ui", self)
        self.setWindowTitle("To-Do List")
        #self.setFixedHeight(1010)
        #self.setFixedWidth(600)

        self.task_input = self.findChild(QLineEdit, "task_in")
        self.due_in = self.findChild(QLineEdit,"due")
        self.warning = self.findChild(QLabel,"warn")
        self.add = self.findChild(QPushButton, "add")
        self.finish = self.findChild(QPushButton, "finish")
        self.out = self.findChild(QTableWidget,"task_out")

        self.warning.setHidden(True)

        con = mdb.connect(host="localhost", user="root", passwd= "your password", database="database name",auth_plugin='mysql_native_password')
        curs = con.cursor()
        q = f"select task,due_in from p_tasks"
        curs.execute(q)
        result = curs.fetchall()
        print(result)
        if result == []:
            self.out.horizontalHeader().setVisible(False)
            self.out.setRowCount(1)
            self.out.setColumnCount(1)
            self.out.setItem(0, 0, QTableWidgetItem("No Tasks :)"))
        else:
            rows = len(result)
            print(rows)
            ele = result[0]
            columns = (len(ele))
            print(columns)
            self.out.setRowCount(rows)
            self.out.setColumnCount(columns)
            self.out.setHorizontalHeaderLabels(["Task", "Due Date"])
            self.out.horizontalHeader().setVisible(True)
            for k in range(rows):
                for l in range(columns):
                    tup = result[k]
                    self.out.setItem(k, l, QTableWidgetItem(str(tup[l])))
                    self.out.setColumnWidth(700, 300)

        self.finish.clicked.connect(self.deletion)
        self.add.clicked.connect(self.adding)
        self.showMaximized()

    def deletion(self):
        m = self.out.currentRow()
        print("m"+str(m))
        con = mdb.connect(host="localhost", user="root", passwd= "your password", database="database name",auth_plugin='mysql_native_password')
        curs = con.cursor()
        q = f"delete from p_tasks where sr_no = '{m+1}'"
        curs.execute(q)
        con.commit()

        strai = ["set @num :=0", "update p_tasks set sr_no = @num :=(@num+1);", "alter table p_tasks auto_increment=1;"]
        for i in strai:
            q = i
            curs.execute(q)
            con.commit()
        q = f"select task,due_in from p_tasks"
        curs.execute(q)
        result = curs.fetchall()
        print(result)
        if result == []:
            self.out.horizontalHeader().setVisible(False)
            self.out.clear()
            self.out.setRowCount(1)
            self.out.setColumnCount(1)
            self.out.setItem(0, 0, QTableWidgetItem("No Task :)"))

        else:
            rows = len(result)
            print(rows)
            ele = result[0]
            columns = (len(ele))
            print(columns)
            self.out.setRowCount(rows)
            self.out.setColumnCount(columns)
            self.out.setHorizontalHeaderLabels(["Task", "Due Date"])
            self.out.horizontalHeader().setVisible(True)
            for k in range(rows):
                for l in range(columns):
                    tup = result[k]
                    self.out.setItem(k, l, QTableWidgetItem(str(tup[l])))
                    self.out.setColumnWidth(700, 300)

    def adding(self):
        t_inptt = self.task_input.text()
        d_inptt = self.due_in.text()
        self.task_input.clear()
        self.due_in.clear()
        print(t_inptt)
        if t_inptt != "" and d_inptt == "":
            self.warning.setText("Enter Due Date !")
            self.warning.setHidden(False)
        elif t_inptt == "" and d_inptt != "":
            self.warning.setText("Enter Task !")
            self.warning.setHidden(False)
        elif t_inptt == "" and d_inptt == "":
            self.warning.setText("Enter Task and Due Date !")
            self.warning.setHidden(False)
        else:
            self.warning.setHidden(True)
            con = mdb.connect(host="localhost", user="root", passwd= "your password", database="database name",auth_plugin='mysql_native_password')
            curs = con.cursor()
            q = f"insert into p_tasks(task,due_in) values('{t_inptt}','{d_inptt}')"
            curs.execute(q)
            con.commit()
            q = f"select task,due_in from p_tasks"
            curs.execute(q)
            result = curs.fetchall()
            print(result)
            rows = len(result)
            print(rows)
            ele = result[0]
            columns = (len(ele))
            print(columns)
            self.out.setRowCount(rows)
            self.out.setColumnCount(columns)
            self.out.setHorizontalHeaderLabels(["Task", "Due Date"])
            self.out.horizontalHeader().setVisible(True)
            for k in range(rows):
                for l in range(columns):
                    tup = result[k]
                    self.out.setItem(k, l, QTableWidgetItem(str(tup[l])))
                    self.out.setColumnWidth(700, 300)

app = QApplication(sys.argv)
UIWindow = mainwindow()
app.exec_()

#By Sahil Dave
