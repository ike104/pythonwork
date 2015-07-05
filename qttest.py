# -*- coding: utf-8 -*-
"""
Created on Sat Jul 04 20:57:12 2015

@author: ikechan
"""

#!/usr/bin/env python
# *-# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

import time

app = QtGui.QApplication(sys.argv)
widget = QtGui.QWidget()

widget.setGeometry(100, 100, 250, 100)
widget.setWindowTitle('progressbar')

max = 10
pbar = QtGui.QProgressBar(widget)
pbar.setGeometry(25, 40, 200, 25)
pbar.setRange(0, max)

widget.show()
widget.raise_()

for step in range(max + 1):
    pbar.setValue(step)
    app.processEvents()

    time.sleep(0.1) #test

app.exec_()

