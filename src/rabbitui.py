#!/usr/bin/env python
import sys
import sqlite3
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4.QtGui import QTableWidgetItem, QMenu, QMessageBox

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

        self.issueTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.addButton, QtCore.SIGNAL('clicked()'), self.display_add)
        self.issueTable.customContextMenuRequested.connect(self.right_click)

    def display_add(self):
        a = AddDialog()
        a.exec()

    def load_rabbit(self):
        self.rabbit = Rabbit()
        issues = self.rabbit.issues()
        self.issueTable.setRowCount(len(issues))

        set_item = self.issueTable.setItem

        for i, issue in enumerate(issues):
            set_item(i, 0, QTableWidgetItem(str(issue.i_id)))
            set_item(i, 1, QTableWidgetItem(issue.type))
            set_item(i, 2, QTableWidgetItem(issue.date))
            set_item(i, 3, QTableWidgetItem(issue.status))
            set_item(i, 4, QTableWidgetItem(issue.priority))
            set_item(i, 5, QTableWidgetItem(issue.summary))

        self.issueTable.setWordWrap(True)
        self.issueTable.resizeColumnsToContents()

    def right_click(self, position):
        menu = QMenu()
        menu.addAction('Open')
        menu.addAction('Close')
        menu.addAction('Comment')
        menu.addSeparator()
        menu.addAction('Delete')
        menu.addAction('Modify')

        table = self.issueTable

        action = menu.exec_(self.issueTable.mapToGlobal(position))

        if action is None:
            return

        if action.text() == 'Open':
            items = table.selectedItems()
            items[3].setText('open')

            i_id = int(items[0].text())
            self.rabbit.open([i_id])

        elif action.text() == 'Close':
            items = table.selectedItems()
            items[3].setText('closed')

            i_id = int(items[0].text())
            self.rabbit.close([i_id])

        elif action.text() == 'Comment':
            dialog = QtGui.QInputDialog()
            dialog.setLabelText('Enter your comment:')
            dialog.exec()
            t = dialog.textValue()

            items = table.selectedItems()

            i_id = int(items[0].text())
            self.rabbit.comment(i_id, t)

        elif action.text() == 'Delete':
            result = QMessageBox.warning(self, 'Remove this Issue?', 'Are you sure you want delete this issue?', QMessageBox.Yes, QMessageBox.No)

            if result == QMessageBox.Yes:
                items = table.selectedItems()
                i_id = int(items[0].text())
                table.removeRow(table.currentRow())
                self.rabbit.delete(i_id)

        elif action.text() == 'Modify':
            pass
        elif action.text == 'Filter':
            pass


w = RabbitUI()

w.load_rabbit()

w.show()

sys.exit(app.exec_())
