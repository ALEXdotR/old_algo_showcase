#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 14:56:46 2022

@author: alex
"""


from tradeToData import tradeWrangling
from getTradeFromInternet import getTradeFromInternet
from saveTradeData import saveTradeData



# Step 1.  getDataFromInternet
duration = 5
yearStart = 2022
monthStart = 3
data = getTradeFromInternet(duration, yearStart, monthStart).recursivePullData()


# Step 2. tradeWrangling
#tradeWrangling(time_interval)
time_interval = 60000
data = tradeWrangling(time_interval).tradeToData(data)

print(data)
# Step 3. saveData
jsonName = saveTradeData(yearStart, monthStart).saveToJson(data)