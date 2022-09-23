#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 13:01:17 2022

@author: alex
"""
import json
import pandas as pd
import os
from datetime import datetime

class saveKlineData():
    
    def __init__(self, yearNow, monthNow):
        self.time = "kline-"+str(yearNow)+"-"+str(monthNow)
        

    def saveToJson(self,df):
        if not os.path.exists('./data'):
            os.system('mkdir ./data')
        jsonName = f"./data/{self.time}.json"
        df.to_json(jsonName)
        
        return jsonName