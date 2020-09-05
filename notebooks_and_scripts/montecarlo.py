import pandas as pd
import numpy as np

data = pd.read_csv("../DATA/training/stocks/AAPL.csv", sep="|")[-100:]
def getPercentageOfChange(values):
    return np.array([np.ln(values[i]/values[i-1]) for i in range(1,len(values))])

def getDrift(values):
    return np.array([i-np.var(values)/2 for i in values])
change = getPercentageOfChange(data)
drift = 
np.==