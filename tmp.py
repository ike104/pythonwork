# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt

dat = [10,20,10,40,100,12,67,33,11,0,40]
x   = range(len(dat))
xt  = [ str(s) + ' H' for s in x]
plt.ylim(0,100)
plt.xlim(-1,11)
plt.xticks(x,xt)
plt.axhline(50,color='r')
plt.bar(x,dat,align='center')