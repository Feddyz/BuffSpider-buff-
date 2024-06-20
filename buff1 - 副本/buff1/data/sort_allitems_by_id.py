import pandas as pd

with open("id_list/weapons.csv", "w", encoding="utf-8") as csv:

    #pandas.read_csv("allitems.csv")
    weapons = pd.read_csv('internal_name/weapons.csv')
    internal_name_set = set(weapons['internal_name'])
    internal_name_list = sorted(internal_name_set)

    allitem_data = pd.read_csv('allitems.csv', usecols=['id','short_name','internal_name'])
    allitem_data = allitem_data.sort_values('id', ascending=True)


    allitem_data.to_csv('allitems_sorted.csv', index=False)




