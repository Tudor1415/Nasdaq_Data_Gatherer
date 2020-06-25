import json
import math
import time as t
from datetime import datetime

import cryptocompare as ctc
import investpy
import pandas as pd
import requests


class CryptocompareDataStreamer:
    '''
    Summary: This class makes cryptocompare api calls easyer with only one function.
    Arguments: You need to provide a settings dictionary
    Methods: Run() -> this is the main function
    Settings:   settings['Symbol'] -> This is the coin's symbol
                settings['Columns'] -> This is the columns that you want
                settings['DataType'] -> This is the datatype: Historical or Live
                settings['Duration'] -> This is the time periode for your data
                settings['Frequency'] -> This is the frequency of your data ex: Day, Hour, Minute
                settings['Name'] -> This is the name of your csv file. It will automaticlly be saved in 'Data/'
                settings['Currency'] -> This is the currency you want bitcoin to be converted to ex: USD, Eur, etc...
    '''
    def __init__(self, settings):
        self.sym = settings['Symbol']
        self.columns = settings['Columns']
        self.dataType = settings['DataType']
        self.frequency = settings['Frequency']
        self.duration = settings['Duration']
        self.name = settings['Name']
        self.curr = settings['Currency']
        self.data = None
        self.choices = {'Day': ctc.get_historical_price_day,
                            'Hour': ctc.get_historical_price_hour,
                            'Minute': ctc.get_historical_price_minute}

    def run(self):
        '''
        Description: This method returns or saves live stock data for your symbol
        '''
        data = pd.DataFrame()
        if self.dataType == 'Live':  # Get live data
            for i in range(self.duration):
                apiCall = ctc.get_price(self.sym, curr=self.curr, full=True)[
                    'RAW'][self.sym][self.curr]
                apiDf = pd.DataFrame(apiCall, index=[i])
                data = pd.concat([data, apiDf], ignore_index=True, sort=True)
                index = [i for i in range(len(data.open))]
                data['Index'] = index
                data = data.loc[:, self.columns]
                data.columns = map(lambda x: str(x).upper(), data.columns)
                if self.name:
                    data.to_csv(f"Data/{self.name}.csv", encoding='utf-8', sep="|")
                t.sleep(1)

        elif self.dataType == 'Historical':  # Get historical data
            apiCall = self.choices[self.frequency](
                self.sym, curr=self.curr, limit=self.duration)
            data = pd.DataFrame(apiCall)
            index = [i for i in range(len(data.open))]
            data['Index'] = index
            data.columns = map(lambda x: str(x).upper(), data.columns)
            if self.name:
                data.to_csv(f"Data/{self.name}.csv", encoding='utf-8', sep="|")

        self.data = data
        return data


class InvestpyDataStreamer:
    '''
    Summary: This class makes investipy api calls easyer with only one function.
    Arguments: You need to provide a settings dictionary
    Methods: Run() -> this is the main function
    Settings:   settings['Stock'] -> This is the stoks name
                settings['Type'] -> This is the data type ex: Stock, Index or Fund
                settings['Country'] -> This is the stoks country
                settings['Timeperiod'] -> This is the desired timeperiod
                settings['DataType'] -> This is the datatype ex: Recent or Historical data
                settings['Name'] -> This is the name of your csv file. It will automaticlly be saved in 'Data/'
    '''
    def __init__(self, settings):
        self.stock = settings['Stock']
        self.country = settings['Country']
        self.from_date, self.to_date = settings['Timeperiod']
        self.dataType = settings['DataType']
        self.type = settings['Type']
        self.choices = {'Stock': {'Recent': investpy.get_stock_recent_data,
                                  'Historical': investpy.get_stock_historical_data},
                        'Index': {'Recent': investpy.get_index_recent_data,
                                  'Historical': investpy.get_index_historical_data}}
        self.name = settings['Name']
        self.data = None

    def run(self):
        data = pd.DataFrame()
        if self.dataType == 'Recent':
            data = self.choices[self.type]['Recent'](
                stock=self.stock, country=self.country)
            index = [i for i in range(len(data.Open))]
            data['Index'] = index
            data.columns = map(lambda x: str(x).upper(), data.columns)
            if self.name:
                data.to_csv(f"Data/{self.name}.csv", encoding='utf-8', sep="|")

        elif self.dataType == 'Historical':
            data = self.choices[self.type]['Historical'](
                stock=self.stock, country=self.country, from_date=self.from_date,
                to_date=self.to_date)
            index = [i for i in range(len(data.Open))]
            data['Index'] = index
            data.columns = map(lambda x: str(x).upper(), data.columns)
            if self.name:
                data.to_csv(self.name, encoding='utf-8', sep="|")

        self.data = data
        return data

symbols = json.loads(open("../DATA/nasdaq100.json", "r+").read())["symbol"]
for symbol in symbols:
    settingsStocks = {}
    settingsStocks['Stock'] = symbol
    settingsStocks['Type'] = 'Stock'
    settingsStocks['Country'] = 'united states'
    settingsStocks['Timeperiod'] = [
        '01/01/2012', datetime.now().strftime("%d/%m/%Y")]
    settingsStocks['DataType'] = 'Historical'
    settingsStocks['Name'] = f"../DATA/data_per_symbol/{symbol}/historical_prices.csv"  

    streamer = InvestpyDataStreamer(settingsStocks)
    print(streamer.run())
