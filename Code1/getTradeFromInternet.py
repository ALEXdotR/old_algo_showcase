import os
import pandas as pd
from datetime import datetime
import time
import math

class getTradeFromInternet():
    def __init__(self,duration,yearNow, monthNow):
        #duration = month retrospect
        self.duration,self.yearNow,self.monthNow = duration, yearNow, monthNow
    

    def pullData(self,t):
        time = t
        curl_cmd = f'curl -s "https://data.binance.vision/data/spot/monthly/trades/ETHUSDT/ETHUSDT-trades-{time}.zip" -o ETHUSDT-trades-{time}.zip'
        wget_cmd  = f'wget "https://data.binance.vision/data/spot/monthly/trades/ETHUSDT/ETHUSDT-trades-{time}.zip"'
        unzip_cmd = f'unzip ETHUSDT-trades-{time}'
        os.system(curl_cmd)
       # os.system(wget_cmd)
        os.system(unzip_cmd)
        data = pd.read_csv(f'ETHUSDT-trades-{time}.csv', names=["trade_id","price","qty","quoteQty","time","isBestMaker","isBestMatch"])
        os.system(f'rm ETHUSDT-trades-{time}.csv')
        os.system(f'rm ETHUSDT-trades-{time}.zip')

        return data
    
    def recursivePullData(self):
        df = pd.DataFrame()
        yearNow = self.yearNow
        monthNow = self.monthNow
        for i in range(1,self.duration+1,1):
            if monthNow-i == 0:
                yearNow = yearNow-1
                monthNow = 12+i
            if math.floor((monthNow-i)/10)>0:
                monthStr = str(monthNow-i)
            else:
                monthStr = "0"+str(monthNow-i)
            inputTime = str(yearNow)+"-"+monthStr
            print(inputTime)
            outputDf = self.pullData(inputTime)
            print(outputDf.shape)
            df = df.append(outputDf)
            
        return df
    

        