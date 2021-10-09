import matplotlib.pyplot as plt
from matplotlib.table import Table
import numpy as np

# 1人以上脱落 and 20BB以上: 普通に
# - ポジション別レイズ表
# - ポジション別リレイズ表
# -
# -
# 20BB以上 or 0人脱落 -> かなりタイトに

def plot():
    fig, ax = plt.subplots()
    ax.set_axis_off()
    tb = Table(ax, bbox=[0,0,1,1])
    size = 1.0 / 13.0
    for x in range(13):
        for y in range(13):
            v = (x + y) / 26
            color = plt.cm.Greens_r(v)
            tb.add_cell(x, y, size, size, text="aa",
                        loc='center', facecolor=color, edgecolor='none')
    names = "AKQJT98765432"
    for i in range(13):
        tb.add_cell(i, -1, size, size, text=names[i], loc='center',
                    edgecolor='none', facecolor='none')
        tb.add_cell(i, 13, size, size, text=names[i], loc='center',
                    edgecolor='none', facecolor='none')
        tb.add_cell(-1, i, size, size, text=names[i], loc='center',
                           edgecolor='none', facecolor='none')
        tb.add_cell(13, i, size, size, text=names[i], loc='center',
                           edgecolor='none', facecolor='none')
    tb.add_cell(-1, -1, size, size, text="o \ s", loc='center',
                    edgecolor='none', facecolor='none')
    ax.add_table(tb)
    plt.show()

plot()
