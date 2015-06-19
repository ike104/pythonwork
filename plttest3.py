# -*- coding: utf-8 -*-
from numpy import *
import pylab as plt

import matplotlib

import matplotlib.font_manager
prop = matplotlib.font_manager.FontProperties(fname=r'C:\Windows\Fonts\meiryo.ttc', size=15)


x = linspace(-2*pi,2*pi,1000)
y = sin(x)/x+0.5

plt.figure(figsize=(4,3),dpi=80)
plt.subplots_adjust(left=0.05,right=0.95)
plt.subplots_adjust(bottom=0.2,top=0.9)
plt.plot(x, y, color="r", label=u"SINC")
plt.legend(prop=prop)

plt.axis('tight')
plt.xlabel(u'角度[rad]',fontproperties=prop)
ax = plt.gca()
ax.invert_yaxis()
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.2f rad"))
#plt.xticks([-pi, -pi/2,0,pi/2,pi],['$-\pi$', '$-\pi/2$', '$0$', '$+\pi/2$',r'$+\pi$']) 

plt.savefig("norm.png")
plt.savefig("trans.png",transparent=True)

plt.show()

