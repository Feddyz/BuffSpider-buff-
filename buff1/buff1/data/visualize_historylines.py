
import matplotlib as mpl
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.preprocessing import StandardScaler
def avg(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)
internal_name = 'weapon_ak47.csv'
if len(sys.argv)>1:
    internal_name = sys.argv[1]
dtypes={
    'price':int,
    'time':int,
    'id':int
}
column_names = ['price','time','id']

data_history = pd.read_csv('buffpricehistory/'+internal_name,header=None,names=column_names)


data = {
    # 'name':'history_price',
    # 'structure':[[1,2,3],[1,2,3]]
}
history_array = data_history.values.tolist()
for record in history_array:
    if str(record[2]) in data:
        # key = id
        if record[1] not in data[str(record[2])][0]:
            data[str(record[2])][0].append(record[1])  # date
            data[str(record[2])][1].append(record[0])  # price

    else:
        data[str(record[2])] = [[],[]]
        if record[1] not in data[str(record[2])][0]:
            data[str(record[2])][0].append(record[1])  # date
            data[str(record[2])][1].append(record[0])  # price

'''for id in data:

    min_val = min(data[str(id)][1])
    if min_val<=0:min_val = 1
    max_val = max(max(data[str(id)][1]),1)
    # 归一化列表
    list1 = [(float(x) - min_val) / (max_val - min_val) for x in data[str(id)][1]]
    data[str(id)][1] = list1'''
mpl.rcParams['legend.fontsize'] = 10

#for history in data:

fig = plt.figure()
ax = fig.add_subplot(projection='3d')


theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)

z = np.linspace(-2, 2, 100)
r = z ** 2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
ax.plot(x, y, z, label='parametric curve')
ax.legend()
plt.show()
