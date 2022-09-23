#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 00:19:56 2022

@author: alex
"""


from klineToData import tradeWrangling
from getKlineFromInternet import getKlineFromInternet
from saveKlineData import saveKlineData



# Step 1.  getDataFromInternet
duration = 5
yearStart = 2022
monthStart = 3
interval = "15m"
data = getKlineFromInternet(duration, yearStart, monthStart, interval).recursivePullData()


# Step 2. tradeWrangling
#tradeWrangling(time_interval)
# time_interval = 60000
data = tradeWrangling(data).klineToData()

print(data)
# Step 3. saveData
jsonName = saveKlineData(yearStart, monthStart).saveToJson(data)