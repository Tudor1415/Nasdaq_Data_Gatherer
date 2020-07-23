import numpy as np
import pandas as pd
import pandas_ta as ta
import os

def get_normal_distribution(data):
    mu = data.mean()
    sigma = np.sqrt(sum([(i-mu)**2 for i in data.values])/data.shape[0])
    function = lambda x: 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (x - mu)**2 / (2 * sigma**2))
    return function

def getPercentageOfChange(values):
    return [round(values[i]/values[i-1], 3) for i in range(1,len(values[:-1]))]+ [None, None]

def get_trapezoidal_approximation(function, b1, b2):
    return sum([5e-3/2*(function(i)+function(i+5e-3)) for i in np.arange(b1,b2, 5e-3)])

def rename_historical_prices():
    # Renaimg Files by coresponding sector
    df = pd.read_csv('../DATA/profiles.csv', sep='|')
    print(df.head(5))
    for file in os.listdir("../DATA/historical_prices"):
        print(file)
        symbol = file.split(".")[0]
        sector = df.loc[df["Symbol"] == symbol]["Sector"].values[0]
        print(sector)
        os.rename(f"../DATA/historical_prices/{file}",f"../DATA/historical_prices/{sector}_{symbol}.csv")

def get_historical_cumalative_prices_per_sector(sector_t):
    df = pd.DataFrame(); i=0
    for file in os.listdir("../DATA/historical_prices"):
        sector = file.split("_")[0]
        if sector_t == sector:
            if i == 0:
                df = pd.read_csv("../DATA/historical_prices/" + file, sep="|")
                df.drop("INDEX", inplace=True, axis=1)
            else:
                temp = pd.read_csv("../DATA/historical_prices/" + file, sep="|")
                temp.drop("INDEX", inplace=True, axis=1)
                for key, row in temp.iterrows():
                    try:
                        row1 = df.loc[df["Date"] == row["Date"]].values[0][1:]
                        new = [row1[i] + value for i, value in enumerate(list(row.values[1:])) if not type(value) == str ]
                        new.insert(5, row1[5])
                        new = [row[0]] + new
                        df.loc[df["Date"] == str(row["Date"])] = new
                    except:
                        # print(df.loc[df["Date"] == row["Date"]].values)
                        pass
            df = df.sort_values(by="Date")
            df.index.name = None
            df.to_csv(f"../DATA/historical_prices/sectors/{sector}.csv", sep="|")
            print(f"../DATA/historical_prices/sectors/{sector}.csv")
            i+=1

sectors = {}
sectors["BasicIndustries"] = pd.read_csv("../DATA/historical_prices/sectors/Basic Industries.csv", sep="|")
sectors["CapitalGoods"] = pd.read_csv("../DATA/historical_prices/sectors/Capital Goods.csv", sep="|")
sectors["PublicUtilities"] = pd.read_csv("../DATA/historical_prices/sectors/Public Utilities.csv", sep="|")
sectors["Technology"] = pd.read_csv("../DATA/historical_prices/sectors/Technology.csv", sep="|")
sectors["Transportation"] = pd.read_csv("../DATA/historical_prices/sectors/Transportation.csv", sep="|")
sectors["nan"] = pd.read_csv("../DATA/historical_prices/sectors/nan.csv", sep="|")
sectors["Miscellaneous"] = pd.read_csv("../DATA/historical_prices/sectors/Miscellaneous.csv", sep="|")
sectors["HealthCare"] = pd.read_csv("../DATA/historical_prices/sectors/Health Care.csv", sep="|")
sectors["Finance"] = pd.read_csv("../DATA/historical_prices/sectors/Finance.csv", sep="|")
sectors["Energy"] = pd.read_csv("../DATA/historical_prices/sectors/Energy.csv", sep="|")
sectors["ConsumerServices"] = pd.read_csv("../DATA/historical_prices/sectors/Consumer Services.csv", sep="|")
sectors["ConsumerNonDurables"] = pd.read_csv("../DATA/historical_prices/sectors/Consumer Non-Durables.csv", sep="|")
sectors["ConsumerDurables"] = pd.read_csv("../DATA/historical_prices/sectors/Consumer Durables.csv", sep="|")


for symbol in os.listdir('../DATA/data_per_symbol/'):
    try:
        # Load data
        df = pd.read_csv(f'../DATA/data_per_symbol/{symbol}/CSV/final.csv', sep='|',  index_col=False)
        sector = pd.read_csv('../DATA/data_per_symbol/AAPL/CSV/profile_dict_df_static.csv', sep='@')["Sector"]
        df.drop(df.columns[df.columns.str.contains('_y',case = False)],axis = 1, inplace = True)
        df.drop(df.columns[df.columns.str.contains('_x',case = False)],axis = 1, inplace = True)
        df.drop(df.columns[df.columns.str.contains('.1',case = False)],axis = 1, inplace = True)
        # Getting sector statistics
        sec = sectors[sector[0]]
        df = pd.merge(df, sec, right_on=['Date'], left_on=['Unnamed: 0'], how='outer', suffixes=["", "_Sector"])
        df.dropna(inplace=True)
        df = df.drop("Unnamed: 0_Sector", axis=1)
        df = df.set_index("Unnamed: 0") 

        df.ta.adjusted = "OPEN_Sector"
        df.ta.log_return(cumulative=True, append=True, suffix="_SECTOR")
        df.ta.slope(append=True, suffix="_SECTOR")
        df.ta.fwma(length=30, append=True, suffix="_SECTOR")
        df.ta.stoch(length=30, append=True, suffix="_SECTOR")
        df.ta.rsi(length=30, append=True, suffix="_SECTOR")
        df.ta.sma(length=100, append=True, suffix="_SECTOR")
        df.ta.ema(length=100, append=True, suffix="_SECTOR")
        df.ta.sma(length=200, append=True, suffix="_SECTOR")
        df.ta.ema(length=200, append=True, suffix="_SECTOR")
        df.ta.sma(length=350, append=True, suffix="_SECTOR")
        df.ta.ema(length=350, append=True, suffix="_SECTOR")
        df.ta.fwma(length=75, append=True, suffix="_SECTOR")
        df.ta.stoch(length=75, append=True, suffix="_SECTOR")
        df.ta.rsi(length=75, append=True, suffix="_SECTOR")

        df.drop(df.columns[df.columns.str.contains('_Sector',case = True)],axis = 1, inplace = True)

        # Calculate Returns and append to the df DataFrame
        df.ta.adjusted = 'OPEN'
        df.ta.log_return(cumulative=True, append=True)
        df.ta.percent_return(cumulative=False, append=True)
        df.ta.sma(length=30, append=True)
        df.ta.ao(length=30, append=True)
        df.ta.bias(length=30, append=True)
        df.ta.cg(length=30, append=True)
        df.ta.tsi(append=True)
        df.ta.entropy(length=30,append=True)
        df.ta.vwap(length=30, append=True)
        df.ta.stdev(length=30, append=True)
        df.ta.zscore(length=30, append=True)
        df.ta.efi(length=30, append=True)
        df.ta.sma(length=100, append=True, suffix="_SECTOR")
        df.ta.ema(length=100, append=True, suffix="_SECTOR")
        df.ta.sma(length=200, append=True, suffix="_SECTOR")
        df.ta.ema(length=200, append=True, suffix="_SECTOR")
        df.ta.sma(length=350, append=True, suffix="_SECTOR")
        df.ta.ema(length=350, append=True, suffix="_SECTOR")
        df.ta.ao(length=75, append=True)
        df.ta.bias(length=75, append=True)
        df.ta.cg(length=75, append=True)
        df.ta.tsi(append=True)
        df.ta.entropy(length=75,append=True)
        df.ta.vwap(length=75, append=True)
        df.ta.stdev(length=75, append=True)
        df.ta.zscore(length=75, append=True)
        df.ta.efi(length=75, append=True)



        df["prctChangeOPEN"] = getPercentageOfChange(df.OPEN)
        TargetProbability = [get_trapezoidal_approximation(get_normal_distribution(df["prctChangeOPEN"][i:i+5]),1, 2)for i in range(len(df["prctChangeOPEN"])-5)] 
        df["TargetProbability"] = TargetProbability + [None for i in range(len(df["OPEN"])-len(TargetProbability))]


        df.dropna(inplace=True)
        df = df.drop(["INDEX", "End Date", "Start Date", "CURRENCY", "symbol", "period", "Date"], axis=1)
        # print(df)
        df.to_csv(f"../DATA/training/stocks/{symbol}.csv", sep="|")
        print(f"Done {symbol}!")
    except:
        print(f"Error {symbol}!")


