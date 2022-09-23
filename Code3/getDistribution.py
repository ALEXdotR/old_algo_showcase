import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

class getDistribution():
    def __init__(self,data,duration, yearStart, monthStart,interval):
        self.data , self.interval,self.duration,self.yearStart, self.monthStart= data,interval,duration,yearStart, monthStart
        
    def plotDistribution(self):
        self.data['highDelta'] = (self.data.highPrice-self.data.openPrice)/self.data.openPrice*100
        self.data['lowDelta'] = (self.data.lowPrice-self.data.openPrice)/self.data.openPrice*100
        #newData = pd.concat([self.data.highDelta, self.data.lowDelta], ignore_index=True)
        plt.title(f'{self.interval} - {self.yearStart}-{self.monthStart}  Duration: {self.duration}')
        
        
        histHigh= np.histogram(self.data['highDelta'], bins=500)
        histHighDist = scipy.stats.rv_histogram(histHigh)
        ax1 = self.data['highDelta'].plot.hist(bins=500, alpha=0.5)
        histLow= np.histogram(self.data['lowDelta'], bins=100)
        histLowDist = scipy.stats.rv_histogram(histLow)
        ax2 = self.data['lowDelta'].plot.hist(bins=100, alpha=0.5)

        return histHighDist,histLowDist, ax1,ax2,self.data['highDelta'],self.data['lowDelta']