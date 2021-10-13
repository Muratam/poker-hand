import numpy as np
import matplotlib.pyplot as plt

def plot():
    # 横軸: オールイン勝率
    # 縦軸: オールイン期待値
    all_ignore_rate = 0
    # 色: 残り人数
    # ドット度合い：BB
    ps = []
    for left in [2,3,4,5,6]:
        l = (left - 2) / 4 / 2
        color = (l, l, l)
        for bb in [5, 20, 40]:
            style=None
            if bb == 5:style="dotted"
            if bb == 20:style="dashed"
            if bb == 40:style="solid"
            xaxis = [_ for _ in range(100)]
            exps = []
            for wi in xaxis:
                win_rate = wi / 100.0
                e0 = all_ignore_rate * 18.0 / bb
                e1 = (1.0-all_ignore_rate)
                e1 *= win_rate*(5.333*left - 2.666) - 4.0 * (left - 1.0)
                e = e0 + e1
                exps.append(e)
            p = plt.plot(xaxis, exps, linewidth=2, linestyle=style,color=color)
        ps.append(p)
    print(ps)
    plt.legend([ _[0] for _ in ps], ("2","3","4","5","6"))
    plt.grid(color='b', linestyle=':', linewidth=0.3)
    plt.show()


# 折れ線グラフを出力
# left = np.array([1, 2, 3, 4, 5])
# height = np.array([100, 300, 200, 500, 400])
# p1 = plt.plot(left, height, linewidth=2)
# p2 = plt.plot(left, height/2, linewidth=2, linestyle="dashed")
# plt.legend((p1[0], p2[0]), ("Class 1", "Class 2"), loc=2)
plot()
