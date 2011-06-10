#!/usr/bin/env python
import sys
import sqlite3
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

from rabbit import *

app = QtGui.QApplication(sys.argv)

Ui_MainWindow, Qt_MainWindow = uic.loadUiType('mainwindow.ui');
Ui_AddWindow, Qt_AddWindow = uic.loadUiType('add.ui');

class Issue:
    i_id = None
    i_type = None
    status = None
    priority = None
    summary = None
    description = None
    comments = []

    def __init__(self):
        pass


class AddDialog(Qt_AddWindow, Ui_AddWindow):
    def __init__(self):
        super(Qt_AddWindow, self).__init__()
        self.setupUi(self)
        self.setModal(True)

        self.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.add)

    def add(self):
        print('asdf')

    def issue(self):
        pass


class RabbitUI(Qt_MainWindow, Ui_MainWindow):
    def __init__(self):
        super(Qt_MainWindow, self).__init__()

        self.setupUi(self)
        self.setWindowTitle('Rabbit GUI')

        self.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.display_add)

    def display_add(self):
        a = AddDialog()
        a.exec()


w = RabbitUI()
w.show()

sys.exit(app.exec_())
