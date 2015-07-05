# -*- coding: utf-8 -*-
"""
Created on Sun Jul 05 23:09:57 2015

@author: ikechan
"""

#!env python
import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)

widget = QtGui.QWidget()
widget.resize(300, 300)
widget.setWindowTitle('PyQt 1')
widget.show()

sys.exit(app.exec_())