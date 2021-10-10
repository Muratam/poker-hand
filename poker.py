import matplotlib.pyplot as plt
from matplotlib.table import Table
import numpy as np
import random
import sys
from optparse import OptionParser
sys.path.append('./holdem_calc')
import holdem_calc

card_data = {
    # raise or fold: BB[0-1], SB[1-2], BTN[2-3], CO[3-4], HJ[4-5], UTG[5-6]
    "AA" : [6, 7], "KK" : [6, 7], "QQ": [6, 7], "JJ": [6, 6],
    "TT" : [6, 6], "99" : [6, 6], "88": [6, 5], "77": [6, 4],
    "66" : [6, 3], "55" : [6], "44": [3.9], "33": [3.2],
    "22" : [3],
    "AKs": [6, 7], "AQs": [6, 6], "AJs": [6, 6], "ATs": [6, 7],
    "A9s": [6, 3], "A8s": [6, 3], "A7s": [6], "A6s": [6],
    "A5s": [6, 7], "A4s": [6, 7], "A3s": [6, 7], "A2s": [6, 7],
    "KQs": [6, 7], "KJs": [6, 5], "KTs": [6, 4], "K9s": [6],
    "K8s": [4], "K7s": [4], "K6s": [3], "K5s": [3],
    "K4s": [3], "K3s": [3], "K2s": [3],
    "QJs": [6, 5], "QTs": [6, 3], "Q9s": [5], "Q8s": [4],
    "Q7s": [3], "Q6s": [3], "Q5s": [3], "Q4s": [1],
    "Q3s": [1], "Q2s": [1.9],
    "JTs": [6, 4], "J9s": [5], "J8s": [3.3], "J7s": [3],
    "J6s": [1], "J5s": [1], "J4s": [1], "J3s": [1],
    "J2s": [1],
    "T9s": [6, 3], "T8s": [4], "T7s": [3], "T6s": [2.3],
    "T5s": [1.1], "T4s": [1.1],
    "98s": [5.1], "97s": [4], "96s": [3], "95s": [1.2],
    "87s": [4], "86s": [3.1], "85s": [2.9],
    "76s": [4], "75s": [3], "74s": [1.1],
    "65s": [4, 5], "64s": [3], "63s": [1],
    "54s": [4], "53s": [1.7],
    "43s": [1.1],
    # raise or fold: BB[0-1], SB[1-2], BTN[2-3], CO[3-4], HJ[4-5], UTG[5-6]
    "AKo": [6, 7], "AQo": [6, 5], "AJo": [6, 3], "ATo": [6],
    "A9o": [4], "A8o": [3], "A7o": [3], "A6o": [3],
    "A5o": [3], "A4o": [3], "A3o": [1.1], "A2o": [1.1],
    "KQo": [6, 3], "KJo": [6], "KTo": [4.9], "K9o": [4],
    "K8o": [1.5], "K7o": [1], "K6o": [1], "K5o": [1.5],
    "K4o": [1.4],
    "QJo": [5.2], "QTo": [4.1], "Q9o": [3], "Q8o": [1.3],
    "Q7o": [1.1],
    "JTo": [4], "J9o": [3], "J8o": [1.5], "J7o": [1.1],
    "T9o": [3], "T8o": [1.5], "T7o": [1.1],
    "98o": [2], "97o": [1.5],
    "87o": [2],
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
        a0 = "♥♠◇♧"[s0] + f"{itocard[r0 % 13]}"
        a1 = "♥♠◇♧"[s1] + f"{itocard[r1 % 13]}"
        return a0, a1

def print_stat():
    itoseatpow  = [5, 4, 3, 2, 1, 0]
    itoseat = ["UG", "HJ", "CO", "BN", "SB", "BB"]
    # if random.random() < 0.1:
    #     print("### リンプイン ###")
    print("リレイズスタート時相手レイズ", end="：")
    for i in range(3):
        ok = ['ブラフ', "真"][int(random.random() < 0.7)]
        print(f"{ok} ", end="")
    print()
    r0, r1 = random_flop_get(0, True)
    print(f"{r0} {r1} : リレイズ")
    for i in range(6):
        power = itoseatpow[i] + random.random()
        r0, r1 = random_flop_get(power)
        text = f"{r0} {r1} : {itoseat[i]}({power:.1f})"
        if itoseat[i] == "SB":
            if random.random() < 0.5: text += " CALL"
            else: text += " BET"
        print(text)
    # print("BB: 相手の確率があればコール")
    # つまり、これ以上の倍率でいくと相手が乗ってしまう、ので、先に降ろす
    # フロップ時点(あと1枚で系)
    # 1/4 (フラッシュ)
    # 1/6 (ストレート)
    # 1/7 (任意の一枚がほしい)

def pick_raise(x, y):
    key = to_key(x, y)
    if not (key in card_data):
        return 0.0
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
    if v < 0.1 : return ""
    if v % 1.0 < 0.05: return v
    return f"{v:.1f}"

def plot_handrange():
    fig, ax = plt.subplots()
    fig.suptitle('UTG:6, HJ:5, CO:4, BTN:3, SB:2, BB:1')
    ax.set_axis_off()
    tb = Table(ax, bbox=[0,0,1,1])
    size = 1.0 / (13.0 + 2.0)
    for x in range(13):
        for y in range(13):
            edgecolor = 'none'
            text = pick_raise_text(x, y)
            if y == 8 or x == 8:
                edgecolor = "#ccc"
            tb.add_cell(x, y, size, size, text=text,
                        loc='center', facecolor=pick_reraise_color(x,y),
                        edgecolor=edgecolor)
    for cell in tb._cells:
        prop = tb._cells[cell].get_text()
        text = prop.get_text()
        try:
            v = 1.0 - float(text) * 6 // 6 / 6
            prop.set_color((v, v, v))
        except ValueError: pass
        prop.set_fontstyle('italic')

    for i in range(13):
        tb.add_cell(i, -1, size, size, text=itocard[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(i, 13, size, size, text=itocard[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(-1, i, size, size, text=itocard[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
        tb.add_cell(13, i, size, size, text=itocard[i], loc='center',
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
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.tick_params(labelsize=30)
    plt.show()


vs_rate_cards = [
    "AA", "KK", "QQ", "JJ",
    "AKs", "AKo", "AJs", "ATs",
    "A5s", "A2s", "KQs"
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

def get_run_data():
    data = """
    AA:AA:95:2:2
    AA:KK:0:81:18
    AA:QQ:0:80:19
    AA:JJ:0:80:19
    AA:AKo:1:91:6
    AA:AKs:1:87:11
    AA:AJs:1:86:12
    AA:ATs:1:86:12
    AA:KQs:0:82:17
    AA:A5s:1:86:12
    AA:A2s:1:87:11
    KK:AA:0:18:81
    KK:KK:95:2:2
    KK:QQ:0:80:18
    KK:JJ:0:80:19
    KK:AKo:0:69:29
    KK:AKs:0:65:33
    KK:AJs:0:67:32
    KK:ATs:0:67:32
    KK:KQs:1:85:13
    KK:A5s:0:66:33
    KK:A2s:0:67:32
    QQ:AA:0:18:80
    QQ:KK:0:18:81
    QQ:QQ:95:2:2
    QQ:JJ:0:81:18
    QQ:AKo:0:56:42
    QQ:AKs:0:53:46
    QQ:AJs:0:67:31
    QQ:ATs:0:67:32
    QQ:KQs:1:64:34
    QQ:A5s:0:66:33
    QQ:A2s:0:67:32
    JJ:AA:0:19:80
    JJ:KK:0:19:80
    JJ:QQ:0:18:81
    JJ:JJ:95:2:2
    JJ:AKo:0:56:42
    JJ:AKs:0:53:46
    JJ:AJs:1:64:33
    JJ:ATs:0:67:31
    JJ:KQs:0:53:46
    JJ:A5s:0:66:33
    JJ:A2s:0:67:32
    AKo:AA:1:6:91
    AKo:KK:0:29:69
    AKo:QQ:0:42:57
    AKo:JJ:0:42:57
    AKo:AKo:95:2:2
    AKo:AKs:90:2:7
    AKo:AJs:4:67:28
    AKo:ATs:4:66:28
    AKo:KQs:1:69:29
    AKo:A5s:4:65:29
    AKo:A2s:4:66:28
    AKs:AA:1:11:87
    AKs:KK:0:33:65
    AKs:QQ:0:46:53
    AKs:JJ:0:45:53
    AKs:AKo:90:7:2
    AKs:AKs:85:7:7
    AKs:AJs:4:68:26
    AKs:ATs:4:68:27
    AKs:KQs:1:70:28
    AKs:A5s:4:67:28
    AKs:A2s:4:68:26
    AJs:AA:1:12:86
    AJs:KK:0:32:67
    AJs:QQ:0:32:67
    AJs:JJ:1:33:64
    AJs:AKo:4:28:67
    AJs:AKs:4:26:68
    AJs:AJs:85:7:7
    AJs:ATs:7:66:26
    AJs:KQs:0:58:41
    AJs:A5s:7:64:28
    AJs:A2s:7:66:26
    ATs:AA:1:12:86
    ATs:KK:0:32:67
    ATs:QQ:0:32:67
    ATs:JJ:0:32:67
    ATs:AKo:4:28:66
    ATs:AKs:4:27:68
    ATs:AJs:7:26:66
    ATs:ATs:85:7:7
    ATs:KQs:0:58:41
    ATs:A5s:9:62:27
    ATs:A2s:9:63:26
    KQs:AA:0:17:82
    KQs:KK:1:13:85
    KQs:QQ:1:34:63
    KQs:JJ:0:46:53
    KQs:AKo:1:29:69
    KQs:AKs:1:27:71
    KQs:AJs:0:41:57
    KQs:ATs:0:41:58
    KQs:KQs:85:7:7
    KQs:A5s:0:42:56
    KQs:A2s:0:42:56
    A5s:AA:1:12:85
    A5s:KK:0:33:66
    A5s:QQ:0:33:66
    A5s:JJ:0:33:66
    A5s:AKo:4:29:65
    A5s:AKs:4:28:67
    A5s:AJs:7:28:64
    A5s:ATs:9:27:62
    A5s:KQs:0:56:43
    A5s:A5s:85:7:7
    A5s:A2s:38:36:25
    A2s:AA:1:11:87
    A2s:KK:0:32:67
    A2s:QQ:0:32:67
    A2s:JJ:0:32:67
    A2s:AKo:4:28:67
    A2s:AKs:4:26:68
    A2s:AJs:7:26:65
    A2s:ATs:9:26:63
    A2s:KQs:0:56:43
    A2s:A5s:38:25:36
    A2s:A2s:85:7:7
    """
    result = {}
    for d in data.replace(" ", "").strip().split("\n"):
        me, vs, tie, win, lose = d.split(":")
        if not(me in result): result[me] = {}
        result[me][vs] = [int(tie), int(win), int(lose)]
    return result

def plot_vs_rate():
    # 1vs1で勝負した際の勝率表(UTG-リレイズ)
    # スートは全て相手と異なるとする
    fig, ax = plt.subplots()
    fig.suptitle('Re-raise lose rate')
    ax.set_axis_off()
    cards = vs_rate_cards
    tb = Table(ax, bbox=[0,0,1,1])
    data = get_run_data()
    print(data)
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
        tb.add_cell(i, -1, size, size, text=cards[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(i, len(cards), size, size, text=cards[i], loc='center',
                    edgecolor='#ccc', facecolor='none')
        tb.add_cell(-1, i, size, size, text=cards[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
        tb.add_cell(len(cards), i, size, size, text=cards[i], loc='center',
                           edgecolor='#ccc', facecolor='none')
    tb.add_cell(-1, -1, size, size, text="\\", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(-1, len(cards), size, size, text="vs", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(len(cards), -1, size, size, text="me", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.add_cell(len(cards), len(cards), size, size, text="\\", loc='center',
                    edgecolor='#ccc', facecolor='none')
    tb.auto_set_font_size(False)
    tb.set_fontsize(12)
    ax.add_table(tb)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.tick_params(labelsize=30)
    plt.show()
    # 1vs1で勝負した際の勝率表(HJ)
    # [ポケット             ] [A+ハイ        ] [K    ] [A+ロースーテッド ]
    # AA, KK, QQ, JJ, TT, 99, AK, AQ, AJ, AT, KQ, KJ, A5, A4, A3, A2s
    # Axo, A{9-6}s,弱いポケットの強さも気になる


if __name__ == "__main__" :
    parser = OptionParser()
    parser.add_option("--handrange",
        help="show handrange table",
        action="store_true")
    parser.add_option("--vsrate",
        help="show vs rate table",
        action="store_true")
    (options, args) = parser.parse_args()
    if options.handrange:
        plot_handrange()
    elif options.vsrate:
        # run_to_data()
        plot_vs_rate()
    else:
        print_stat()
