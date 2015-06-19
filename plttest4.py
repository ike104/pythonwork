import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick

x = np.arange(1,1000,1)
y = 10e-7*x

fig, ax=plt.subplots(figsize=(5*1.618,5))
ax.plot(x,y)

ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
ax.yaxis.offsetText.set_fontsize(10)
ax.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
plt.grid(True)
plt.show()
