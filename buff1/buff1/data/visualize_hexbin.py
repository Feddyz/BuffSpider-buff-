"""
===============
hexbin(x, y, C)
===============
Make a 2D hexagonal binning plot of points x, y.

See `~matplotlib.axes.Axes.hexbin`.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas
import pandas as pd

# plt.style.use('seaborn')

# make data: correlated + noise
np.random.seed(1)

# plot:

# fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
def avg(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)
data = pd.read_csv('test_internal_name_list.csv',names = None,)
data.columns=['internal_name','page']
for internal_name in data['internal_name']:
    datasource = pd.read_csv('overall/'+internal_name+'.csv',header = None,usecols=[5,8]) # sell_num , ratio
    datasource.columns=['sell_num','ratio']
    x = datasource['sell_num'].values.tolist()
    y = datasource['ratio'].values.tolist()
    print(len(y))
    print(len(x))
    print(type(x))  # 输出列表的类型
    print(type(y))
    index_del = []
    avgx = avg(x)
    avgy = avg(y)
    for i in range(0,len(x)):
        if x[i] > 2*avgx:
            x[i] = 2*avgx
        if y[i]>2*avgy:
            y[i] = 2*avgy

    print(internal_name)
    print(len(y))
    print(len(x))
    print(x)  # 输出列表的类型
    print(y)

    fig, ax = plt.subplots(figsize=(8,8 ), dpi=200)

    plt.xlabel('Available quantity')
    plt.ylabel('Price Ratio (International/CN)')
    #plt.text(0.5, 0.5, '测试test', ha='center', va='center', fontsize=12, color='red')
    #ax.set(xlim=(1, 1500), ylim=(0, 5000))
    ax.hexbin(x, y, gridsize=[30,15])
    plt.title(internal_name)
    plt.show()
