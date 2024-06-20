import pandas as pd

with open("id_list/weapons.csv", "w", encoding="utf-8") as csv:

    #pandas.read_csv("allitems.csv")
    weapons = pd.read_csv('internal_name/weapons.csv')
    internal_name_set = set(weapons['internal_name'])
    internal_name_list = sorted(internal_name_set)

    allitem_data = pd.read_csv('allitems.csv', usecols=['id','internal_name'])

    for weapon in internal_name_list:
        with open('id_list/'+weapon+'.csv','a',encoding='utf-8') as weaponcsv:
            idset = set()
            for index in range(1,22091):
                if str(allitem_data.loc[index]['internal_name']) == weapon :
                    idset.add(allitem_data.loc[index]['id'])
            idset = sorted(idset)
            for id in idset:

                weaponcsv.write(str(id)+'\n')


