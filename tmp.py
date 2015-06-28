# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import datetime

d = os.stat("test.txt").st_mtime
dt = datetime.datetime.fromtimestamp(d)

print dt
