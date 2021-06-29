import csv
import pandas as pd
from operator import itemgetter
import statistics
import math

# ============File I/O====================
string = str(input())
data = list(csv.reader(open(string)))
# =========end of File I/O================

# 讀入最原始的檔案到prelist(一條column的形式)
prelist = []
for i in data:
    prelist.append(i)


# 將剛剛讀到一條column的資料轉成row放入rowlist，並將value轉成impedance change
rowlist = []
for i in range(len(prelist)):
    rowlist.append(float(prelist[i][0])*1000/2)

# 將原本的rowlist進行微分, 因為每個資料點相隔的時間為1/2000sec, 故微分需乘上2000
list = []
for i in range(len(rowlist)-1):
    list.append((rowlist[i+1] - rowlist[i])*2000)

print('height: ')
h = float(input())
print('weight: ')
w = float(input())


# 下面開始求C點、B-X
flag = 1  # flag == 1 means not yet pass 0.08
Cmaxlist = []  # Cmaxlist用來存放所有C點的值，最後可以取平均算出(delta Zc/delta t)max
BXlist = []    # BXlist 用來存放所有B-X之間的距離，最後可以取平均得到T(LVE)
tmp = []       # tmp 用來存放，找C點時，使用到波峰附近所有點的資訊
for i in range(1000, len(list)):  # 前面幾項數據有雜訊，故我們捨棄前1000項的data
    if(float(list[i]) > 30):
        flag = 0
        tmp.append({'value': float(list[i]), 'index': i})

    elif(float(list[i]) < 30 and flag == 0):
        t = sorted(tmp, key=itemgetter('value'), reverse=True)
        # print(t[0]['value'])
        if(t[0]['value'] < 50):
            Cmaxlist.append((t[0]['value']))

        # 下面程式碼開始找B點位置
        # 方法為從剛剛找到的C點位置往前回推直到ICG signal經過0的時候即為B點
        b = -1
        for j in range(t[0]['index'], 0, -1):
            if(list[j] > 0):
                continue
            else:
                b = j
                break

        # 下面程式碼開始找X點位置
        # 我們從剛剛找到的C點位置往後推分別找出第一次和第二次ICG signal通過-0.01的點
        # find first index where its value pass through -0.01
        first = -1
        second = -1
        for j in range(t[0]['index'], len(list), 1):
            if(list[j] < -10):
                first = j
                break
            else:
                continue
        # find second index where its value pass through -0.01
        for j in range(first, len(list), 1):
            if(list[j] > -10):
                second = j
                break
            else:
                continue

        # 找出first和second之間所有的點，並從這些數據中找出值最小的點即為X點
        lowest = []
        for j in range(first, second, 1):
            lowest.append({'value': float(list[j]), 'index': j})
        ans = sorted(lowest, key=itemgetter('value'))

        # 將(X點index - B點index)即為B-X之間的訊號數量，在乘以1/2000sec，就可得到T(LVE)
        if(len(ans) > 0):
            BXlist.append((ans[0]['index'] - b)/2000)

        tmp.clear()
        flag = 1

# 將偏誤的資料篩掉
finalBXlist = []
for i in range(len(BXlist)):
    if(BXlist[i] < 0.3):
        finalBXlist.append((BXlist[i]))

# 找出C點平均和B-X平均
Cmax = statistics.mean(Cmaxlist)
BX = statistics.mean(finalBXlist)

print(string+' results: ')
print('Cmax: ', Cmax)
print('B-X: ', BX)

# SV calculation
SV = ((0.17*h/100)**3)*(math.sqrt(w/(h/100*h/100*24)))
SV = SV/4.25
SV = SV/22.7
SV = SV*BX*Cmax*1000000
print('SV: ', SV)
