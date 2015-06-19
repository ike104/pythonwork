# -*- coding: utf-8 -*-
from numpy import *
import pylab as plt

import matplotlib


x = arange(0,10,0.1)
y = sin(x)

fig, ax = plt.subplots()
ax.plot(x,y)
ax.grid(True)
plt.savefig("grid.png")

