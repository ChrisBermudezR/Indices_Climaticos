# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 18:27:11 2024

@author: CBermudezr
"""


import pandas as pd

data = pd.read_excel("Indices_Total_Manual.xlsx")

data['date']  = data['date'] .dt.strftime('%Y-%m-%d')

datasubset = data[['date', 'value', 'event', 'type']]

json_oni = datasubset.to_json(orient='columns', date_format='iso', force_ascii=False, indent=4)

datasubset.to_json("json_total.json",orient='columns', date_format='iso', force_ascii=False, indent=4)

subset_agosto = data.iloc[895,0:10]

json_oni2 = subset_agosto.to_json(orient='columns', date_format='iso', force_ascii=False, indent=4)

subset_agosto.to_json("json_tarjeta.json",orient='columns', date_format='iso', force_ascii=False, indent=4)
