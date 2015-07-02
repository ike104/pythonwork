# -*- coding: utf-8 -*-
"""
Created on Thu Jul 02 08:55:58 2015

@author: ikeda
"""

def getDiff(ch):
    i0 = 0
    i1 = 0
    d00 = []
    d01 = []
    for i in ch:
        d = i[0] - i0
        d00.append(d)
        i0 = i[0]
        
        d = i[1] - i1         
        d01.append(d)
        i1 = i[1]
    return [d00,d01]

def checkLeap(d,thresh):
    d0 = 0  
    idx = 0
    idxes = []
    for i in d:
        delta = i-d0
        d0 = i        
        idx = idx + 1        
        if abs(delta)>thresh:
            idxes.append([idx-1, delta])
    return idxes
    
import pandas as pd

ctstAll = pd.read_csv('ctst_150701.070043.0.txt',header=0,delim_whitespace=True, \
    names=['date','msec','nsec','nch','ct0','st0'\
       ,'ct1','st1','ct2','st2','ct3','st3'])


ctst = ctstAll.head(5000)
import matplotlib.pylab as plt

ch0 = []
ch1 = []
ch2 = []
ch3 = []
for i in range(len(ctst)):
    ch0.append([ctst['ct0'][i],ctst['st0'][i]])
    ch1.append([ctst['ct1'][i],ctst['st1'][i]])
    ch2.append([ctst['ct2'][i],ctst['st2'][i]])
    ch3.append([ctst['ct3'][i],ctst['st3'][i]])


#d00,d01 = getDiff(ch0)
#plt.plot(d00)
#plt.plot(d01)
#plt.title('Diff ct[n]-ct[n-1] st[n]-st[n-1] Ch0 ')
#plt.show()

#d10,d11 = getDiff(ch1)
print "CT0"
#er = checkLeap(d10,20)
#checkLeap(d11,50)

#plt.plot(d10)
#plt.plot(d11)
#plt.title('Diff ct[n]-ct[n-1] st[n]-st[n-1] Ch1 ')
#plt.show()

d20,d21 = getDiff(ch2)
#plt.plot(d20)
er = checkLeap(d21,20)

plt.plot(d21)
plt.title('Diff ct[n]-ct[n-1] st[n]-st[n-1] Ch2 ')
plt.show()

#d30,d31 = getDiff(ch3)
#plt.plot(d30)
#plt.plot(d31)
#plt.title('Diff ct[n]-ct[n-1] st[n]-st[n-1] Ch3 ')
#plt.show()

