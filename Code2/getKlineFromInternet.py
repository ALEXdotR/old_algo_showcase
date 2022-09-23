#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 12:28:10 2022

@author: alex
"""

import os
import pandas as pd
from datetime import datetime
import time
import math

class getKlineFromInternet():
    def __init__(self,duration, yearNow, monthNow, interval):
        #duration = month retrospect
        self.duration,self.yearNow,self.monthNow, self.interval = duration, yearNow, monthNow, interval
    

    def pullData(self,t):
        time = t
        i = self.interval
        curl_cmd = f'curl -s "https://data.binance.vision/data/spot/monthly/klines/ETHUSDT/{i}/ETHUSDT-{i}-{time}.zip" -o ETHUSDT-{i}-{time}.zip'
        wget_cmd  = f'wget "https://data.binance.vision/data/spot/monthly/klines/ETHUSDT/{i}/ETHUSDT-{i}-{time}.zip"'
        unzip_cmd = f'unzip ETHUSDT-{i}-{time}'
        os.system(curl_cmd)
       # os.system(wget_cmd)
        os.system(unzip_cmd)
        data = pd.read_csv(f'ETHUSDT-{i}-{time}.csv', names=["openTime","openPrice","highPrice","lowPrice","closePrice","volumeBase","closeTime","volumeQuote","tradeQuantity","takerBuyBaseAssetVolume","takerBuyQuoteAssetVolume","ignore"])
        os.system(f'rm ETHUSDT-{i}-{time}.csv')
        os.system(f'rm ETHUSDT-{i}-{time}.zip')

        return data
    
    def recursivePullData(self):
        df = pd.DataFrame()
        _yearNow = self.yearNow
        _monthNow = self.monthNow
        for i in range(1,self.duration+1,1):
            if _monthNow-i == 0:
                _yearNow = _yearNow-1
                _monthNow = 12+i
            if math.floor((_monthNow-i)/10)>0:
                monthStr = str(_monthNow-i)
            else:
                monthStr = "0"+str(_monthNow-i)
            inputTime = str(_yearNow)+"-"+monthStr
            print(inputTime)
            outputDf = self.pullData(inputTime)
            print(outputDf.shape)
            df = df.append(outputDf)
        
        df.reset_index(inplace=True)
        
        return df