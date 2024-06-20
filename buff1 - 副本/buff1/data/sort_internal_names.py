import pandas as pd

with open("internal_name/internal_names.csv", "w", encoding="utf-8") as csv:

    #pandas.read_csv("allitems.csv")
    df = pd.read_csv('allitems.csv', usecols=['internal_name'])
    internal_name_set = set(df['internal_name'])
    internal_name_list = sorted(internal_name_set)
    for internal_name in internal_name_list:
        csv.write(internal_name+'\n')
        # print(internal_name)
