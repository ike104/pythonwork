# -*- coding: utf-8 -*-
from numpy import *
import pylab as plt

import matplotlib.font_manager
prop = matplotlib.font_manager.FontProperties(fname=r'C:\Windows\Fonts\meiryo.ttc', size=15)

x = linspace(-2*pi,2*pi,1000)
y = sin(x)/x+0.5

plt.title(u"sinc関数もどき",fontproperties=prop)
plt.plot(x, y, color="r", label=u"シフトしたSINC")
plt.legend(prop=prop)
plt.xlabel(u'ｘ軸',fontproperties=prop)
plt.xticks([-pi, -pi/2,0,pi/2,pi],['$-\pi$', '$-\pi/2$', '$0$', '$+\pi/2$',r'$+\pi$']) 
plt.text(0,1,u'日本語',fontproperties=prop,size=20)
plt.show()
