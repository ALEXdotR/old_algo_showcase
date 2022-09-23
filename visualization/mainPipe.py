from getKlineFromInternet import getKlineFromInternet
from getDistribution import getDistribution
import scipy.stats

# Step 1.  getDataFromInternet
duration = 5
yearStart = 2022
monthStart = 2
interval = '15m'

data = getKlineFromInternet(duration, yearStart, monthStart,interval).recursivePullData()
histHighDist,histLowDist, ax1,ax2, highData, lowData= getDistribution(data,duration, yearStart, monthStart,interval).plotDistribution()

info = highData.describe()
print(info)


