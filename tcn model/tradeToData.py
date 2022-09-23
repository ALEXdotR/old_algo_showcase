import pandas as pd
import os
import math
import numpy as np



"""
path = "//home//ubuntu//works//data"
dir_list = os.listdir(path)

def concat(dir_list):
    df = pd.DataFrame(columns=["trade_id","price","qty","quoteQty","time","isBestMaker","isBestMatch"])
    for i in dir_list:
        df2 = pd.read_csv(f'data\{i}.csv',names=["trade_id","price","qty","quoteQty","time","isBestMaker","isBestMatch"])
        df = pd.concat([df, df2])
    return df
"""


class tradeWrangling():
    
    def tradeToData(self, _df):
        df = _df
        df = df.drop(columns=['qty', 'isBestMaker','isBestMatch',])
        print("Grouping dataset ... ...")
        df["time"] = df["time"].apply(lambda x: math.floor(x/self.ti))
        #df["isBestMaker"]= df["isBestMaker"].apply(lambda x: 0 if (x==False) else 1)
        #df["isBestMatch"]= df["isBestMatch"].apply(lambda x: 0 if (x==False) else 1)
        df = df.groupby('time').agg(price=pd.NamedAgg(column="price", aggfunc="mean"),
                                    quoteQty=pd.NamedAgg(column="quoteQty", aggfunc="sum"),
                                    sd_price=pd.NamedAgg(column="price", aggfunc="std"),
                                    sd_quoteQty=pd.NamedAgg(column="quoteQty", aggfunc="std")
                                    #isBestMaker=pd.NamedAgg(column="isBestMaker", aggfunc="mean"),
                                    #isBestMatch=pd.NamedAgg(column="isBestMatch", aggfunc="mean"),
                                    #qty=pd.NamedAgg(column="qty", aggfunc="sum")
                                    )
        df["delta_percent_price"]= df["price"].pct_change()*100
        df['sd_price'] = df['sd_price'].replace(np.nan, 0)
        df['sd_quoteQty'] = df['sd_quoteQty'].replace(np.nan, 0)
        print("Inserting missing transcations ... ...")
        
        secondFullDf = pd.DataFrame(index = np.arange(df.index.min(), df.index.max()+1), columns=["price","quoteQty","sd_price","sd_quoteQty","delta_percent_price"])
    
        haveIndex = df.index.intersection(secondFullDf.index)
        notHaveIndex = secondFullDf.index.difference(df.index)
        
    
        df = df.append(secondFullDf.loc[notHaveIndex,:])
        
        for index,row in df[df['price'].isnull()].iterrows():
            df.at[index,'quoteQty'] = 0
            df.at[index, 'sd_price'] = 0
            df.at[index,'sd_quoteQty'] = 0
            df.at[index,'delta_percent_price'] = 0
            df.at[index,'price'] = df.at[index-1 , 'price']
    
        
    
        """
        for i in range(df.index[0],df.index[-1]+1):
            if i not in df.index:
                s = {'price': df.iloc[n-1].price, 'qty': 0, 'quoteQty': 0,
                     #"isBestMaker":0,"isBestMatch":0,
                     "sd_quoteQty":0,"precent_price":0,"sd_price":0,} 
                s = pd.DataFrame([s])
                s.index = [i]
                df = df.append(s)
                df = df.sort_index()
            n+=1
            """
        return df
    
    def __init__(self, timeInterval):
        #time interval in ms
        self.ti = timeInterval

    
    