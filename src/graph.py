# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 01:39:31 2020
@author: amannirala13
"""
import sys
import threading as th
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('dark_background')
fig = plt.figure()
fig.canvas.set_window_title('Crack Detection Live')
ax = fig.add_subplot(1,1,1)

surface_threshold = float(sys.argv[1])

def animate(i):
    try:
        graph_data = open('log.data', 'r').read()
    except:
        print("Log file missing")
        SystemExit()
    lines = graph_data.split(',')
    lines.pop()
    lines = list(map(float,lines))
    ax.clear()
    plt.title("Live surface level data")
    plt.axhline(y = surface_threshold, color = 'y', linestyle = '-')
    ax.plot([i for i in range(len(lines))],lines, 'm-')

ani = animation.FuncAnimation(fig, lambda i:th.Thread(target=animate(i), daemon=True).start(), interval = 400)
plt.show()