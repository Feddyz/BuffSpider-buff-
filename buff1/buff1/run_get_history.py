
"""读取data/gethistory.csv文件中作为internal_name,并根据internal_name从data/id_list中获取对应internal_name的id列表发送历史价格查询
    读取data/gethistory.csv文件
    读取data/gethistory.csv文件
    读取data/gethistory.csv文件

"""
import pandas as pd
from multiprocessing import Process
from scrapy.cmdline import execute
# 读取 CSV 文件
def read_csv():
    return pd.read_csv('data/gethistory.csv', names=['internal_names'], header=None)

# 定义一个函数来运行 Scrapy 命令
def run_spider(category):
    execute(['scrapy', 'crawl', 'buffhistory', '-a', f'intname={category}'])

if __name__ == '__main__':
    # 读取 CSV 文件
    intended_category = read_csv()

    # 提取类别列表
    cat_list = intended_category['internal_names']

    # 循环遍历每个类别
    for category in cat_list:
        # 创建并启动一个新进程运行 Scrapy 命令
        p = Process(target=run_spider, args=(category,))
        p.start()
        # 等待当前进程完成后再启动下一个进程
        p.join()

    # 打印 'end' 表示脚本运行结束
    print('end')