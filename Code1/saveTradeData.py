import json
import pandas as pd
import os
from datetime import datetime



class saveTradeData():
    
    def __init__(self, yearNow, monthNow):
        self.time = "trade-"+str(yearNow)+"-"+str(monthNow)
        

    def saveToJson(self,df):
        if not os.path.exists('./data'):
            os.system('mkdir ./data')
        jsonName = f"./data/{self.time}.json"
        df.to_json(jsonName)
        
        return jsonName
    

        
    
        

