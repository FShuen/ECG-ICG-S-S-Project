import csv
import pandas as pd
from operator import itemgetter

# ==============File I/O===================
string = str(input())
data = list(csv.reader(open(string)))
# ==========end of File I/O================

# 將ECG檔案讀進同一個list中，忽略掉第一個column(時間)，
# 把每秒鐘2000筆資料接在一起
list = []
for i in range(180):
    for j in range(2001):
        if(j != 0):
            list.append(data[i][j])

# 整理好的ECG數據寫出檔案 "mod_原檔名.csv"
with open('mod_'+string, 'w') as f:
    write = csv.writer(f)
    write.writerow(list)

# 計算ECG中R點的Y值
rrlist = []   # rrlist 是將每一個R-R interval紀錄下來，也就是RRI series
flag = 1      # flag == 1 means not yet pass 0
old = -1      # old 用來記錄上一個R點的index
new = 0       # new 用來記錄目前找到R點的index
tmp = []      # 將兩次通過0的點全部記錄下來
for i in range(len(list)):
    if(float(list[i]) > 0):
        flag = 0
        tmp.append({'value': float(list[i]), 'index': i})  # value 和 index 都存

    elif(float(list[i]) < 0 and flag == 0):
        t = sorted(tmp, key=itemgetter('value'), reverse=True)  # 排序
        new = t[0]['index']  # t[0]['index] 為tmp中最高點的index，也就是R點index
        tmp.clear()
        t.clear()
        flag = 1
        if(old != -1):
            rrlist.append(new - old)
        old = new

# 將偏誤的資料篩掉
R_Rseries = []
for i in rrlist:
    if(i > 500):
        R_Rseries.append(i/2000)

# 把RRI series寫出檔案 "RRI_原檔名.csv"
with open('RRI_'+string, 'w') as f:
    write = csv.writer(f)
    write.writerow(R_Rseries)
