import matplotlib.pyplot as plt
from matplotlib.table import Table
import numpy as np
import random
import sys
from optparse import OptionParser
sys.path.append('./holdem_calc')
import holdem_calc

# 30BB, 0.5POT
card_data = {
    # raise or fold: BB[0-2], SB[1-2], BTN[2-3], CO[3-4], HJ[4-5], UTG[5-6]
    "AA" : [8, 7], "KK" : [8, 7], "QQ": [8, 7], "JJ": [8, 7],
    "TT" : [7.8, 7], "99" : [6.1, 6], "88": [6, 6], "77": [6, 6],
    "66" : [4.5, 6], "55" : [4, 6], "44": [2.6, 5], "33": [2, 5], "22": [2, 5],
    "AKs": [8, 7], "AQs": [8, 6], "AJs": [8, 6], "ATs": [8, 6],
    "A9s": [7.8, 6], "A8s": [7.8, 6], "A7s": [6, 5], "A6s": [7, 5],
    "A5s": [7, 6], "A4s": [7, 6], "A3s": [6.3, 5], "A2s": [6.1, 4],
    "KQs": [7.8, 6], "KJs": [7, 6], "KTs": [7, 6], "K9s": [6.2, 5],
    "K8s": [5.3, 4], "K7s": [5, 3], "K6s": [3.5, 3], "K5s": [3, 3],
    "K4s": [3, 3], "K3s": [2.9, 3], "K2s": [2, 3],
    "QJs": [7.8, 6], "QTs": [6.6, 5], "Q9s": [6.1, 5], "Q8s": [4, 3],
    "Q7s": [3], "Q6s": [2.7], "Q5s": [2], "Q4s": [2], "Q3s": [2], "Q2s": [2],
    "JTs": [6.8, 6], "J9s": [6.2, 5], "J8s": [3.2, 3], "J7s": [2],
    "J6s": [2], "J5s": [2], "J4s": [2], "J3s": [1.5], "J2s": [1.5],
    "T9s": [6.2, 5], "T8s": [3, 4], "T7s": [2, 3], "T6s": [2],
    "T5s": [1.5], "T4s": [1.5], "T3s": [1], "T2s": [1],
    "98s": [3, 3], "97s": [2], "96s": [2],
    "95s": [1.5], "94s": [1], "93s": [1], "92s": [0.5],
    "87s": [3, 3], "86s": [2], "85s": [2], "84s": [1.5],
    "83s": [0.5], "82s": [0.5],
    "76s": [2.3, 3], "75s": [2], "74s": [1.5], "73s": [1],
    "72s": [0.5],
    "65s": [2], "64s": [2], "63s": [1.5], "62s": [1],
    "54s": [2], "53s": [1.5], "52s": [1.5],
    "43s": [1.5], "42s": [1.5], "32s": [1.5],
    "AKo": [8, 7], "AQo": [8, 6], "AJo": [8, 6], "ATo": [6.6, 6],
    "A9o": [6, 3], "A8o": [4.9, 3], "A7o": [3.5, 3], "A6o": [3, 3],
    "A5o": [3, 3], "A4o": [3, 3], "A3o": [3, 3], "A2o": [2],
    "KQo": [7, 6], "KJo": [6.2, 5], "KTo": [6, 3], "K9o": [4, 3],
    "K8o": [3], "K7o": [2], "K6o": [2],
    "K5o": [1], "K4o": [1], "K3o": [1], "K2o": [1],
    "QJo": [6.3, 4], "QTo": [5, 3], "Q9o": [3], "Q8o": [2],
    "Q7o": [1], "Q6o": [0.5], "Q5o": [0.5],
    "Q4o": [0.5], "Q3o": [0.5], "Q2o": [0.5],
    "JTo": [3, 3], "J9o": [3], "J8o": [2], "J7o": [0.5],
    "J6o": [0], "J5o": [0], "J4o": [0], "J3o": [0], "J2o": [0],
    "T9o": [2, 3], "T8o": [2], "T7o": [0.5], "T6o": [0], "T5o": [0],
    "98o": [2], "97o": [1], "96o": [0.5],
    "95o": [0], "94o": [0], "93o": [0], "92o": [0],
    "87o": [2], "86o": [1], "85o": [0],
    "76o": [1.5], "75o": [0.5], "74o": [0],
    "65o": [1.5], "64o": [0],
    "54o": [1], "43o": [0],
    "T4o": [-1], "T3o": [-1], "T2o": [-2],
    "94o": [-2], "93o": [-2], "92o": [-2],
    "84o": [-2], "83o": [-2], "82o": [-2], "73o": [-2], "72o": [-2],
    "63o": [-2], "62o": [-2],
    "53o": [-1], "52o": [-2], "42o": [-2], "32o": [-2],
}


itocard = "AKQJT98765432"

def to_key(x, y):
    ix = itocard[x]
    iy = itocard[y]
    if x == y: return ix + iy
    elif x < y : return ix + iy + "s"
    else: return iy + ix + "o"

def random_flop_get(power, reraise=False):
    while True:
        r0 = random.choice([i for i in range(52)])
        s0 = int(r0 / 13)
        r1 = random.choice([i for i in range(52)])
        s1 = int(r1 / 13)
        if r0 == r1: continue
        k = to_key(r0 % 13, r1 % 13)
        if not (k in card_data): continue
        if reraise:
            if len(card_data[k]) == 1 : continue
            if card_data[k][1] < power: continue
        else:
            if card_data[k][0] < power: continue
        a0 = "????????????"[s0] + f"{itocard[r0 % 13]}"
        a1 = "????????????"[s1] + f"{itocard[r1 % 13]}"
        return a0, a1

def print_stat():
    itoseatpow  = [5, 4, 3, 2, 1, 0]
    itoseat = ["UG", "HJ", "CO", "BN", "SB", "BB"]
    print("??????????????????????????????????????????", end="???")
    for i in range(3):
        ok = ['?????????', "???"][int(random.random() < 0.7)]
        print(f"{ok} ", end="")
    print()
    r0, r1 = random_flop_get(0, True)
    print(f"{r0} {r1} : ????????????")
    for i in range(6):
        power = itoseatpow[i] + random.random()
        r0, r1 = random_flop_get(power)
        text = f"{r0} {r1} : {itoseat[i]}({power:.1f})"
        if itoseat[i] == "SB":
            if random.random() < 0.5: text += " CALL"
            else: text += " BET"
        print(text)
    for i in range(10):
        print(int(random.random() * 100), end=" ")
    print()

def pick_raise(x, y):
    key = to_key(x, y)
    if not (key in card_data):
        return -10.0
    d = card_data[key]
    return d[0]

def pick_reraise(x, y):
    key = to_key(x, y)
    if not (key in card_data):
        return 0.0
    d = card_data[key]
    if len(d) == 1: return 0.0
    return d[1]

def pick_reraise_color(x,y):
    v = pick_reraise(x, y)
    return plt.cm.Greens((v - 2)/ 5)

def pick_raise_text(x, y):
    v = pick_raise(x, y)
    if v < -9.0 : return ""
    if v % 1.0 < 0.05: return v
    return f"{v:.1f}"

def plot_handrange():
    fig, ax = plt.subplots()
    fig.suptitle('UTG:6/3o2s, HJ:5/1.5, CO:4/1, BTN:3/0.5, SB:0/2/3/4')
    ax.set_axis_off()
    tb = Table(ax, bbox=[0,0,1,1])
    size = 1.0 / (13.0 + 2.0)
    for x in range(13):
        for y in range(13):
            edgecolor = 'none'
            text = pick_raise_text(x, y)
            if y == 6 or x == 6:
                edgecolor = "#ccc"
            tb.add_cell(x, y, size, size, text=text,
                        loc='center', facecolor=pick_reraise_color(x,y),
                        edgecolor=edgecolor)
    for cell in tb._cells:
        prop = tb._cells[cell].get_text()
        text = prop.get_text()
        try:
            if float(text) < 0:
                prop.set_color((0.9, 0.6, 0.6))
            else:
                v = 0.6 - (float(text) - 1) * 6 // 6 / 6
                prop.set_color((v, v, v))
        except ValueError: pass
        prop.set_fontstyle('italic')

    for i in range(13):
        tb.add_cell(i, -2, size, size, text=itocard[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(i, 13, size, size, text=itocard[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(-2, i, size, size, text=itocard[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
        tb.add_cell(13, i, size, size, text=itocard[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
    tb.add_cell(-2, -2, size, size, text="o \ s", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(-2, 13, size, size, text="s", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(13, -2, size, size, text="o", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(13, 13, size, size, text="o \ s", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.auto_set_font_size(False)
    tb.set_fontsize(12)
    ax.add_table(tb)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.tick_params(labelsize=30)
    plt.show()


vs_rate_cards = [
    "AA", "KK", "QQ", "JJ", "TT", "99",
    "AKs", "AKo", "AJs", "ATs",
    "A5s", "A2s", "KQs", "65s"
]
def run_to_data():
    def to_example(card, me):
        if me:
            if card[0] == card[1] or card[2] == "o":
                return card[0]+"d", card[1]+"c"
            else:
                return card[0]+"d", card[1]+"d"
        else:
            if card[0] == card[1] or card[2] == "o":
                return card[0]+"h", card[1]+"s"
            else:
                return card[0]+"h", card[1]+"h"
    cards = vs_rate_cards
    for x in range(len(cards)):
        for y in range(len(cards)):
            c0 = cards[x]
            c1 = cards[y]
            ce0 = to_example(c0, True)
            ce1 = to_example(c1, False)
            rates = holdem_calc.module([ce0[0], ce0[1], ce1[0], ce1[1]], False)
            # Tie, Win, Lose
            print(f"{c0}:{c1}:{int(rates[0]*100)}:{int(rates[1]*100)}:{int(rates[2]*100)}")

# def get_win_rates():
#     f = open("result.txt", "w")
#     # AA:AKs:1:87:11 <- tie / win /lose
#     def writeout(cm0, cm1, ce0, ce1):
#         rates = holdem_calc.module([cm0, cm1, ce0, ce1], False)
#         f.write("")
#     def impl(i, j, k, l):
#         # dchs
#         if i == j:
#             cm0 = itocard[i] + "d"
#             cm1 = itocard[j] + "c"
#             if k == l:
#                 ce0 = itocard[i] + "h"
#                 ce1 = itocard[j] + "s"
#                 # 66 vs 44
#             else:
#                 for se in [True, False]:
#                     if se:
#                         # 66 vs 34s
#                         ce0 = itocard[i] + "h"
#                         ce1 = itocard[j] + "h"
#                     else:
#                         # 66 vs 34o
#         else:
#             if k == l:
#             else:
#         print(cm0, cm1, ce0, ce1)
#         c += 1
#     card_max = 3
#     # 1820??????
#     for i in range(card_max):
#         for j in range(i, card_max):
#             for k in range(j, card_max):
#                 for l in range(k, card_max):
#                     impl(i, j, k, l)


ranges = [
    "Re", "C-6", "C-5", "C-4", "R-3",
    "UTG", "HJ", "CO", "BTN", "SB"
]
def get_range(i):
    # ??????????????? UTG
    mays = {}
    h1 = 0 # heart ???1??????????????????????????????
    h2 = 0 # heart ???2??????????????????????????????
    all = 0
    pair = 0
    for k, v in card_data.items():
        if ranges[i] == "Re":
            if len(v) == 1: continue
            if v[1] < 7: continue
        if ranges[i] == "C-6":
            if len(v) == 1: continue
            if v[1] < 6: continue
        if ranges[i] == "C-5":
            if len(v) == 1: continue
            if v[1] < 5: continue
        if ranges[i] == "C-4":
            if len(v) == 1: continue
            if v[1] < 4: continue
        if ranges[i] == "R-3":
            if len(v) == 1: continue
            if v[1] < 3: continue
        if ranges[i] == "UTG" and v[0] <= 5.5: continue
        if ranges[i] == "HJ" and v[0] <= 4.5: continue
        if ranges[i] == "CO" and v[0] <= 3.5: continue
        if ranges[i] == "BTN" and v[0] <= 2.5: continue
        if ranges[i] == "SB" and v[0] <= 1.8: continue
        if not (k[0] in mays): mays[k[0]] = 0
        if not (k[1] in mays): mays[k[1]] = 0
        if k[0] == k[1]:
            all += 6
            mays[k[0]] += 6 # 4C3??????
            h1 += 3
            pair += 6
        elif k[2] == "s":
            all += 4
            mays[k[0]] += 4
            mays[k[1]] += 4 # 4?????????
            h1 += 1
            h2 += 1
        else:
            all += 12
            mays[k[0]] += 12
            mays[k[1]] += 12 # 4x3??????
            h1 += 6
    for k in [ _ for _ in mays.keys()]:
        mays[k] /= all

    result = []
    for k in itocard:
        if k in mays: result += [mays[k]]
        else: result += [0]
    result += [h1 / all]
    result += [h2 / all]
    result += [pair / all]
    return result


def plot_card_rate():
    # ??????????????????
    # reraise / call / SB, BTN, C0, HJ, UTG
    # BB[0-2], SB[1-2], BTN[2-3], CO[3-4], HJ[4-5], UTG[5-6]
    # 1vs1??????????????????????????????(UTG-????????????)
    # ?????????????????????????????????????????????
    ylabels = ranges
    xlabels = list(itocard) + ["???1", "???2", "Pair"]
    fig, ax = plt.subplots()
    fig.suptitle('Having Rate')
    ax.set_axis_off()
    cards = vs_rate_cards
    tb = Table(ax, bbox=[0,0,1,1])
    data = get_run_data()
    size = 1.0 / (len(cards) + 2.0)
    for x in range(len(ylabels)):
        rates = get_range(x)
        for y in range(len(xlabels)):
            edgecolor = 'none'
            if x == 5 or y == 13:
                edgecolor = '#ccc'
            text = f"{int(rates[y] * 100)}"
            color = plt.cm.Greens(rates[y] * 1.5)
            tb.add_cell(x, y, size, size, text=text,
                loc='center', facecolor=color,
                edgecolor=edgecolor)
    for i in range(len(xlabels)):
        tb.add_cell(-2, i, size, size, text=xlabels[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(len(ylabels), i, size, size, text=xlabels[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
    for i in range(len(ylabels)):
        tb.add_cell(i, -2, size, size, text=ylabels[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
        tb.add_cell(i, len(xlabels),  size, size, text=ylabels[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
    tb.add_cell(-2, -2, size, size, text="\\", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(-2, len(xlabels), size, size, text="c", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(len(ylabels), -2, size, size, text="pos", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(len(ylabels), len(xlabels), size, size, text="\\", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.auto_set_font_size(False)
    tb.set_fontsize(12)
    ax.add_table(tb)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.tick_params(labelsize=30)
    plt.show()

def get_run_data():
    data = """
    AA:AA:95:2:2
    AA:KK:0:81:18
    AA:QQ:0:80:18
    AA:JJ:0:80:19
    AA:TT:0:79:19
    AA:99:0:80:19
    AA:AKs:1:87:11
    AA:AKo:1:91:6
    AA:AJs:1:86:12
    AA:ATs:1:86:12
    AA:A5s:1:86:12
    AA:A2s:1:87:11
    AA:KQs:0:82:17
    AA:65s:0:76:22
    KK:AA:0:18:81
    KK:KK:95:2:2
    KK:QQ:0:81:18
    KK:JJ:0:80:19
    KK:TT:0:80:19
    KK:99:0:80:19
    KK:AKs:0:65:33
    KK:AKo:0:69:29
    KK:AJs:0:67:32
    KK:ATs:0:66:32
    KK:A5s:0:66:33
    KK:A2s:0:67:32
    KK:KQs:1:85:13
    KK:65s:0:76:22
    QQ:AA:0:18:80
    QQ:KK:0:18:81
    QQ:QQ:95:2:2
    QQ:JJ:0:81:18
    QQ:TT:0:80:19
    QQ:99:0:80:19
    QQ:AKs:0:53:46
    QQ:AKo:0:57:42
    QQ:AJs:0:67:32
    QQ:ATs:0:67:32
    QQ:A5s:0:66:33
    QQ:A2s:0:67:32
    QQ:KQs:1:64:34
    QQ:65s:0:76:23
    JJ:AA:0:19:80
    JJ:KK:0:18:80
    JJ:QQ:0:18:80
    JJ:JJ:95:2:2
    JJ:TT:0:80:18
    JJ:99:0:80:18
    JJ:AKs:0:53:45
    JJ:AKo:0:57:42
    JJ:AJs:1:64:33
    JJ:ATs:0:67:32
    JJ:A5s:0:66:33
    JJ:A2s:0:67:32
    JJ:KQs:0:53:46
    JJ:65s:0:76:22
    TT:AA:0:19:79
    TT:KK:0:19:80
    TT:QQ:0:18:80
    TT:JJ:0:18:80
    TT:TT:95:2:2
    TT:99:0:80:18
    TT:AKs:0:53:46
    TT:AKo:0:57:42
    TT:AJs:0:54:45
    TT:ATs:2:64:33
    TT:A5s:0:66:33
    TT:A2s:0:67:32
    TT:KQs:0:53:46
    TT:65s:0:77:22
    99:AA:0:19:80
    99:KK:0:19:80
    99:QQ:0:19:80
    99:JJ:0:18:80
    99:TT:0:18:80
    99:99:95:2:2
    99:AKs:0:52:47
    99:AKo:0:55:44
    99:AJs:0:52:47
    99:ATs:0:52:46
    99:A5s:0:65:34
    99:A2s:0:66:33
    99:KQs:0:52:47
    99:65s:0:77:21
    AKs:AA:1:11:87
    AKs:KK:0:33:65
    AKs:QQ:0:45:53
    AKs:JJ:0:45:53
    AKs:TT:0:45:53
    AKs:99:0:47:51
    AKs:AKs:85:7:7
    AKs:AKo:90:7:2
    AKs:AJs:4:69:26
    AKs:ATs:4:68:27
    AKs:A5s:4:67:28
    AKs:A2s:4:68:26
    AKs:KQs:1:70:27
    AKs:65s:0:59:39
    AKo:AA:1:6:92
    AKo:KK:0:29:69
    AKo:QQ:0:42:56
    AKo:JJ:0:42:57
    AKo:TT:0:42:57
    AKo:99:0:44:55
    AKo:AKs:90:2:6
    AKo:AKo:95:2:2
    AKo:AJs:4:67:28
    AKo:ATs:4:67:28
    AKo:A5s:4:65:29
    AKo:A2s:4:66:28
    AKo:KQs:1:69:29
    AKo:65s:0:57:41
    AJs:AA:1:12:86
    AJs:KK:0:32:67
    AJs:QQ:0:31:67
    AJs:JJ:1:33:64
    AJs:TT:0:45:53
    AJs:99:0:47:52
    AJs:AKs:4:26:68
    AJs:AKo:4:28:66
    AJs:AJs:85:7:7
    AJs:ATs:7:66:26
    AJs:A5s:7:64:28
    AJs:A2s:7:66:26
    AJs:KQs:0:57:41
    AJs:65s:0:60:38
    ATs:AA:1:12:86
    ATs:KK:0:32:67
    ATs:QQ:0:32:67
    ATs:JJ:0:32:67
    ATs:TT:2:33:64
    ATs:99:0:47:52
    ATs:AKs:4:26:68
    ATs:AKo:4:28:66
    ATs:AJs:7:26:66
    ATs:ATs:85:7:7
    ATs:A5s:9:62:27
    ATs:A2s:9:63:26
    ATs:KQs:0:57:41
    ATs:65s:0:61:38
    A5s:AA:1:12:86
    A5s:KK:0:33:66
    A5s:QQ:0:33:66
    A5s:JJ:0:33:66
    A5s:TT:0:33:66
    A5s:99:0:34:65
    A5s:AKs:4:27:67
    A5s:AKo:4:29:65
    A5s:AJs:7:28:64
    A5s:ATs:9:27:62
    A5s:A5s:85:7:7
    A5s:A2s:38:35:25
    A5s:KQs:0:56:43
    A5s:65s:2:66:31
    A2s:AA:1:11:87
    A2s:KK:0:32:67
    A2s:QQ:0:32:67
    A2s:JJ:0:32:67
    A2s:TT:0:32:67
    A2s:99:0:33:66
    A2s:AKs:4:26:68
    A2s:AKo:4:28:66
    A2s:AJs:7:26:66
    A2s:ATs:9:26:63
    A2s:A5s:38:25:36
    A2s:A2s:85:7:7
    A2s:KQs:0:56:42
    A2s:65s:0:54:45
    KQs:AA:0:17:82
    KQs:KK:1:13:85
    KQs:QQ:1:34:64
    KQs:JJ:0:46:53
    KQs:TT:0:46:53
    KQs:99:0:47:52
    KQs:AKs:1:28:70
    KQs:AKo:1:29:69
    KQs:AJs:0:41:58
    KQs:ATs:0:41:58
    KQs:A5s:0:43:56
    KQs:A2s:0:43:56
    KQs:KQs:85:7:7
    KQs:65s:0:60:38
    65s:AA:0:22:76
    65s:KK:0:22:77
    65s:QQ:0:22:76
    65s:JJ:0:22:77
    65s:TT:0:22:77
    65s:99:0:21:77
    65s:AKs:0:39:60
    65s:AKo:0:41:57
    65s:AJs:0:38:60
    65s:ATs:0:38:61
    65s:A5s:2:32:65
    65s:A2s:0:44:54
    65s:KQs:0:38:60
    65s:65s:85:7:7
    """
    result = {}
    for d in data.replace(" ", "").strip().split("\n"):
        me, vs, tie, win, lose = d.split(":")
        if not(me in result): result[me] = {}
        result[me][vs] = [int(tie), int(win), int(lose)]
    return result

def plot_vs_rate():
    # 1vs1??????????????????????????????(UTG-????????????)
    # ?????????????????????????????????????????????
    fig, ax = plt.subplots()
    fig.suptitle('Re-raise lose rate')
    ax.set_axis_off()
    cards = vs_rate_cards
    tb = Table(ax, bbox=[0,0,1,1])
    data = get_run_data()
    size = 1.0 / (len(cards) + 2.0)
    for x in range(len(cards)):
        for y in range(len(cards)):
            c0 = cards[x]
            c1 = cards[y]
            edgecolor = 'none'
            # if c0 == "AKo" or c1 == "AKo":
            #     edgecolor = "#ccc"
            # if c0 == "KQs" or c1 == "KQs":
            #     edgecolor = "#ccc"
            rates = data[c0][c1]
            text = f"{rates[2]}"
            color = plt.cm.Greens((rates[2]) / 100)
            tb.add_cell(x, y, size, size, text=text,
                loc='center', facecolor=color,
                edgecolor=edgecolor)
    for i in range(len(cards)):
        tb.add_cell(i, -2, size, size, text=cards[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(i, len(cards), size, size, text=cards[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(-2, i, size, size, text=cards[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
        tb.add_cell(len(cards), i, size, size, text=cards[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
    tb.add_cell(-2, -2, size, size, text="\\", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(-2, len(cards), size, size, text="vs", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(len(cards), -2, size, size, text="me", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(len(cards), len(cards), size, size, text="\\", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.auto_set_font_size(False)
    tb.set_fontsize(12)
    ax.add_table(tb)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.tick_params(labelsize=30)
    plt.show()


if __name__ == "__main__" :
    parser = OptionParser()
    # get_win_rates()
    parser.add_option("--handrange",
        help="show handrange table",
        action="store_true")
    parser.add_option("--vsrate",
        help="show vs rate table",
        action="store_true")
    parser.add_option("--cardrate",
        help="card rate table",
        action="store_true")
    (options, args) = parser.parse_args()
    if options.handrange:
        plot_handrange()
    elif options.vsrate:
        # run_to_data()
        plot_vs_rate()
    elif options.cardrate:
        plot_card_rate()
    else:
        print_stat()
