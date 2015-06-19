import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()          #Figureオブジェクトを作成。
fig.text(0.4,0.95,"subplot(321)")
ax1 = fig.add_subplot(321)#AxesSubplotオブジェクトの作成（プロットする領域）。
ax1.text(20,1,"No1",size=20)
x = np.linspace(1,100,100)
y = np.log(x)
ax1.plot(x,y)            #axにプロット

ax2 = fig.add_subplot(322)#AxesSubplotオブジェクトの作成（プロットする領域）。
x = np.linspace(1,100,100)
ax2.text(30,20,"No2",color='r',size=20)
y = x
ax2.plot(x,y)            #axにプロット

ax3 = fig.add_subplot(323)#AxesSubplotオブジェクトの作成（プロットする領域）。
x = np.linspace(1,100,100)
ax3.text(30,30*30,"No3",color='g',size=20)
y = x*x
ax3.plot(x,y)            #axにプロット

ax4 = fig.add_subplot(324)#AxesSubplotオブジェクトの作成（プロットする領域）。
x = np.linspace(1,100,100)
ax4.text(30,1/30+0.2,"No4",color='c',size=20)
y = 1/x
ax4.plot(x,y)            #axにプロット

ax5 = fig.add_subplot(325)#AxesSubplotオブジェクトの作成（プロットする領域）。
x = np.linspace(1,100,100)
ax5.text(30,30*30*(30-10),"No5",color='y',size=20)
y = x*x*(x-10)
ax5.plot(x,y)            #axにプロット

plt.savefig("subplot.png")
plt.show()
