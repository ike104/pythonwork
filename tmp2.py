# -*- coding: utf-8 -*-
"""
Created on Wed Jul 01 09:32:09 2015

@author: ikeda

バタワース特性HPF を設計し時間波形、周波数特性を確認する

"""

import numpy as np
import matplotlib.pylab as plt
from scipy import signal 
import math


cutoff = 0.3 # nyquist周波数で正規化されたカットオフ周波数
b, a = signal.butter(5,cutoff,'high')


pi = math.pi

sz  = 1    # total sec
spl = 1000 # sample freq. [Hz]
fnq = spl/2 # nyquist freq [Hz]

r = np.random.randn(sz*spl)
t = np.array(range(sz*spl))

f1 = 0.01 # nyquist周波数で正規化された信号周波数
s1 = np.sin(2 * pi * f1*fnq * t/spl)
f2 = 0.1 # # nyquist周波数で正規化された信号周波数
s2 = np.sin(2 * pi * f2*fnq * t/spl)

sn = s1+s2+r/10 #ノイズと信号を合成

# 時間軸の入力波形を表示
plt.plot(sn,alpha=0.5,label='signal+noise')
plt.plot(s1,alpha=0.8,label='signal '+str(f1) + 'Hz')
plt.plot(s2,alpha=0.8,label='signal '+str(f2) + 'Hz')
plt.legend()
plt.show()

# 時間軸応答を求める
plt.plot(sn,alpha=0.5,label='signal ' + str(f1) + ' + ' +str(f2) + \
                'Hz' + ' + noise') 
#j  = signal.lfilter(b,a,sn)
j  = signal.filtfilt(b,a,sn)
plt.plot(j,alpha=0.9,label='Filtered') 
plt.legend()
#plt.ylim(-3,3)
plt.show()

# 周波数応答を求める
w,h = signal.freqz(b,a)
plt.plot(w,20*np.log10(abs(h)))
plt.xscale('log')
plt.xlim(0.01*pi,pi)
plt.ylim(-80,10)
#
plt.title('BUtterworth filter response')
plt.xlabel('Normalized Frequency [rad/s]')
plt.ylabel('Ampletude [dB]')
plt.margins(0,0.1)
plt.grid(which='both',axis='both')
plt.axvline(cutoff*pi,color='green')
plt.show()
