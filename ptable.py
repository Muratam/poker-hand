import matplotlib.pyplot as plt
from matplotlib.table import Table
import numpy as np

# 1人以上脱落 and 20BB以上: 普通に
# よくあるフリップ後の確率が知りたい

# $ python3 ptable.py
# 99, 21, 32, 32, 43, 01, 44, 33 # 確率的に動くためのもの
# 相手のレイズ：「1はブラフ」「2は真」「3はブラフ」 #
# UG: ♤K ♥K /
# HJ: ♤K ♥K /
# CO: ♤K ♥K /
# BN: ♤9 ♥9 /
# SB: ♤9 ♥9 / / [RAISE/ CALL]
# BB: ♤9 ♥9 /   []
# no additional card (50%)


data = {
    # raise or fold: BB[0-1], SB[1-2], BTN[2-3], CO[3-4], HJ[4-5], UTG[5-6]
    # 自分がSB <= 傾斜あり50%くらいでコールから入った方がいい(相手はランダムハンドであるため)
    # reraise rate
    # 自分がBB <= スーテッド{4以上の01コネクタ,A}, 全ポケットでレイズにコール
    "AA" : [6, 5], "KK" : [6, 5], "QQ": [6, 5], "JJ": [6, 4.8],
    "TT" : [6, 4], "99" : [6, 4], "88": [6, 3], "77": [6, 2],
    "66" : [6, 5], "55" : [6], "44": [3.9], "33": [3.2],
    "22" : [3],
    "AKs": [6, 5], "AQs": [6, 4.4], "AJs": [6, 4.9], "ATs": [6, 5],
    "A9s": [6], "A8s": [6], "A7s": [6], "A6s": [6],
    "A5s": [6, 5], "A4s": [6, 5], "A3s": [6], "A2s": [6],
    "KQs": [6, 5], "KJs": [6, 4.1], "KTs": [6], "K9s": [6],
    "K8s": [4], "K7s": [4], "K6s": [3], "K5s": [3],
    "K4s": [3], "K3s": [3], "K2s": [3],
    "QJs": [6], "QTs": [6], "Q9s": [5], "Q8s": [4],
    "Q7s": [3], "Q6s": [3], "Q5s": [3], "Q4s": [1],
    "Q3s": [1], "Q2s": [2],
    "JTs": [6], "J9s": [5], "J8s": [3.3], "J7s": [3],
    "J6s": [1], "J5s": [1], "J4s": [1], "J3s": [1],
    "J2s": [1],
    "T9s": [6], "T8s": [4], "T7s": [3], "T6s": [2.3],
    "T5s": [1.1], "T4s": [1.1],
    "98s": [5.1], "97s": [4], "96s": [3], "95s": [1.2],
    "87s": [4], "86s": [3.1], "85s": [2.9],
    "76s": [4], "75s": [3], "74s": [1.1],
    "65s": [4], "64s": [3], "63s": [1],
    "54s": [4], "53s": [1.7],
    "43s": [1.1],
    # raise or fold: BB[0-1], SB[1-2], BTN[2-3], CO[3-4], HJ[4-5], UTG[5-6]
    "AKo": [6, 5], "AQo": [6, 4.4], "AJo": [6], "ATo": [6],
    "A9o": [4], "A8o": [3], "A7o": [3], "A6o": [3],
    "A5o": [3], "A4o": [3], "A3o": [1.1], "A2o": [1.1],
    "KQo": [6], "KJo": [6], "KTo": [4.9], "K9o": [1.9],
    "K8o": [1.5], "K7o": [1], "K6o": [1], "K5o": [1.5],
    "K4o": [1.4],
    "QJo": [5.2], "QTo": [4.1], "Q9o": [3], "Q8o": [1.3],
    "Q7o": [1.1],
    "JTo": [4], "J9o": [3], "J8o": [1.5], "J7o": [1.1],
    "T9o": [3], "T8o": [1.5], "T7o": [1.1],
    "98o": [2], "97o": [1.5],
    "87o": [2],
}


itoc = "AKQJT98765432"
itoseat = ["UG", "HJ", "CO", "BN", "SB", "BB"]
itoNum  = []

def to_key(x, y):
    ix = itoc[x]
    iy = itoc[y]
    if x == y: return ix + iy
    elif x < y : return ix + iy + "s"
    else: return iy + ix + "o"

# def random_flop_get():



def pick_raise(x, y):
    key = to_key(x, y)
    if not (key in data):
        return 0.0
    d = data[key]
    return d[0]

def pick_reraise(x, y):
    key = to_key(x, y)
    if not (key in data):
        return 0.0
    d = data[key]
    if len(d) == 1: return 0.0
    return d[1]


def pick_reraise_color(x,y):
    v = pick_reraise(x, y)
    return plt.cm.Greens(v / 6)

def pick_raise_text(x, y):
    v = pick_raise(x, y)
    if v < 0.1 : return ""
    if v % 1.0 < 0.05: return v
    return f"{v:.1f}"

def plot():
    plt.rcParams['font.family'] = 'Courier'
    plt.tick_params(labelsize=30)
    fig, ax = plt.subplots()
    fig.suptitle('UTG:5.5, HJ:4.5, CO:3.5, BTN:2.5, SB:1.5, BB:0.5')
    ax.set_axis_off()
    tb = Table(ax, bbox=[0,0,1,1])
    size = 1.0 / 13.0
    for x in range(13):
        for y in range(13):
            edgecolor = 'none'
            if x == 6 or y == 6: edgecolor = "#ccc"
            tb.add_cell(x, y, size, size, text=pick_raise_text(x, y),
                        loc='center', facecolor=pick_reraise_color(x,y),
                        edgecolor=edgecolor)
    for cell in tb._cells:
        prop = tb._cells[cell].get_text()
        text = prop.get_text()
        try:
            v = 1.0 - float(text) / 6
            prop.set_color((v, v, v))
        except ValueError: pass
        prop.set_fontstyle('italic')

    for i in range(13):
        tb.add_cell(i, -1, size, size, text=itoc[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(i, 13, size, size, text=itoc[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(-1, i, size, size, text=itoc[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
        tb.add_cell(13, i, size, size, text=itoc[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
    tb.add_cell(-1, -1, size, size, text="o \ s", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(-1, 13, size, size, text="s", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(13, -1, size, size, text="o", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(13, 13, size, size, text="o \ s", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.auto_set_font_size(False)
    tb.set_fontsize(12)
    ax.add_table(tb)
    plt.show()


plot()
