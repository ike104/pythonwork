# -*- coding: utf-8 -*-
"""
Created on Sun Jul 05 23:12:30 2015

@author: ikechan
"""

#!env python
import sys
from PyQt4 import QtGui, QtCore


class QuitButton(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle('Close button')

        cb = QtGui.QPushButton('Close', self)
        cb.setGeometry(10, 10, 60, 35)

        cb.clicked.connect(QtGui.qApp.quit)


app = QtGui.QApplication(sys.argv)
b = QuitButton()
b.show()
sys.exit(app.exec_())