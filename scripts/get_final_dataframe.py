import datetime as dt
import os
from functools import reduce

import numpy as np
import pandas as pd

def get_normal_distribution(data):
    mu = data.mean()
    sigma = np.sqrt(sum([(i-mu)**2 for i in data.values])/data.shape[0])
    function = lambda x: 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (x - mu)**2 / (2 * sigma**2))
    return function

def getPercentageOfChange(values):
    return [round(values[i]/values[i-1], 3) for i in range(1,len(values[:-1]))]+ [None, None]

def get_trapezoidal_approximation(function, b1, b2):
     return sum([1e-2/2*(function(i)+function(i+1e-2)) for i in np.arange(b1,b2, 1e-2)])

def create_data_btwn_dates(group, st_date, end_date):
    df = group.set_index(st_date, drop=False)
    df = df.reindex(pd.date_range(df.index[0], end=df["End Date"][0], freq='d'))
    df = df.ffill()
    return df

for symbol in os.listdir('../DATA/data_per_symbol/')[os.listdir('../DATA/data_per_symbol/').index('ORLY'):]:
    # Loading all the data into dataframes

    # Time series data
    try:
        balance_sheet_quarterly = pd.read_csv(f'../DATA/data_per_symbol/{symbol}/CSV/balance_sheet_quarterly.csv', sep="@")
        balance_sheet_quarterly_exists = True
    except:
        balance_sheet_quarterly_exists = False
    try:
        cash_flow_df = pd.read_csv(f'../DATA/data_per_symbol/{symbol}/CSV/cash_flow_df.csv', sep="@")
        cash_flow_df_exists = True
    except:
        cash_flow_df_exists = False        
    try:
        edgar_8k_df = pd.read_csv(f'../DATA/data_per_symbol/{symbol}/CSV/edgar_8k_df.csv', sep="@")
        edgar_8k_df_exists = True
    except:
        edgar_8k_df_exists = False        
    try:
        historical_prices = pd.read_csv(f'../DATA/data_per_symbol/{symbol}/CSV/historical_prices.csv', sep="@")
        historical_prices_exists = True
    except:
        historical_prices_exists = False        
    try:
        income_statement_df = pd.read_csv(f'../DATA/data_per_symbol/{symbol}/CSV/income_statement_df.csv', sep="@")
        income_statement_df_exists = True
    except:
        income_statement_df_exists = False        

    # # Static data 
    # holders_detailed_profile_static_df = pd.read_csv('holders_detailed_profile_static_df.csv', sep="@")
    # institutional_holders_df_0_static = pd.read_csv('institutional_holders_df_0_static.csv', sep="@")
    # institutional_holders_df_1_static = pd.read_csv('institutional_holders_df_1_static.csv', sep="@")
    # institutional_holders_df_2_static = pd.read_csv('institutional_holders_df_2_static.csv', sep="@")
    # major_holders_df_static = pd.read_csv('major_holders_df_static.csv', sep="@")
    # profile_dict_df_static = pd.read_csv('profile_dict_df_static.csv', sep="@")
    # summary_df_static = pd.read_csv('summary_df_static.csv', sep="@")
    # sustainability_df_static = pd.read_csv('sustainability_df_static.csv', sep="@")
    # yahoo_earnings_estimate_df_static = pd.read_csv('yahoo_earnings_estimate_df_static.csv', sep="@")
    # yahoo_growth_estimate_df_static = pd.read_csv('yahoo_growth_estimate_df_static.csv', sep="@")
    # yahoo_revenue_estimate_df_static = pd.read_csv('yahoo_revenue_estimate_df_static.csv', sep="@")
    # yahoo_risk_static_df_static = pd.read_csv('yahoo_risk_static_df_static.csv', sep="@")

    if balance_sheet_quarterly_exists:
        balance_sheet_quarterly["Date"] = balance_sheet_quarterly["date"]
        balance_sheet_quarterly = balance_sheet_quarterly.drop("date", axis=1)
        balance_sheet_quarterly["Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d')) # Changing column from string to datetime
        balance_sheet_quarterly = balance_sheet_quarterly.sort_values(by="Date")
        # Dropping unnecessary columns and filling Nan
        balance_sheet_quarterly = balance_sheet_quarterly.drop(["fillingDate", "acceptedDate", "link", "finalLink"], axis=1)
        balance_sheet_quarterly = balance_sheet_quarterly.fillna(-99999)
        # Creating quarter date columns 
        balance_sheet_quarterly["Start Date"] = balance_sheet_quarterly["Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
        balance_sheet_quarterly["End Date"] = list(balance_sheet_quarterly["Date"].shift(-1))[:-1] + [dt.datetime.now().strftime('%Y-%m-%d')]
        balance_sheet_quarterly["End Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
        # Filling the dates in between quarters
        group = balance_sheet_quarterly.groupby("Date", as_index=False)
        balance_sheet_quarterly.set_index("Date")
        balance_sheet_quarterly = group.apply(create_data_btwn_dates, "Start Date", "End Date").reset_index(level=0, drop=True)

    if cash_flow_df_exists:
        cash_flow_df["Date"] = cash_flow_df["date"]
        cash_flow_df = cash_flow_df.drop("date", axis=1)
        cash_flow_df["Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d')) # Changing column from string to datetime
        cash_flow_df = cash_flow_df.sort_values(by="Date")
        # Dropping unnecessary columns and filling Nan
        cash_flow_df = cash_flow_df.drop(["fillingDate", "acceptedDate", "link", "finalLink"], axis=1)
        cash_flow_df = cash_flow_df.fillna(-99999)
        # Creating quarter date columns 
        cash_flow_df["Start Date"] = cash_flow_df["Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
        cash_flow_df["End Date"] = list(cash_flow_df["Date"].shift(-1))[:-1] + [dt.datetime.now().strftime('%Y-%m-%d')]
        cash_flow_df["End Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
        # Filling the dates in between quarters
        group = cash_flow_df.groupby("Date", as_index=False)
        cash_flow_df.set_index("Date")
        cash_flow_df = group.apply(create_data_btwn_dates, "Start Date", "End Date").reset_index(level=0, drop=True)

    if income_statement_df_exists:
        income_statement_df["Date"] = income_statement_df["date"]
        income_statement_df = income_statement_df.drop("date", axis=1)
        income_statement_df["Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d')) # Changing column from string to datetime
        income_statement_df = income_statement_df.sort_values(by="Date")
        # Dropping unnecessary columns and filling Nan
        income_statement_df = income_statement_df.drop(["fillingDate", "acceptedDate", "link", "finalLink"], axis=1)
        income_statement_df = income_statement_df.fillna(-99999)
        # Creating quarter date columns 
        income_statement_df["Start Date"] = income_statement_df["Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
        income_statement_df["End Date"] = list(income_statement_df["Date"].shift(-1))[:-1] + [dt.datetime.now().strftime('%Y-%m-%d')]
        income_statement_df["End Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
        # Filling the dates in between quarters
        group = income_statement_df.groupby("Date", as_index=False)
        income_statement_df.set_index("Date")
        income_statement_df = group.apply(create_data_btwn_dates, "Start Date", "End Date").reset_index(level=0, drop=True)

    if historical_prices_exists:     
        historical_prices["Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d')) # Changing column from string to datetime
        historical_prices = historical_prices.sort_values(by="Date")
        # Dropping unnecessary columns and filling Nan
        historical_prices = historical_prices.fillna(-99999)
        historical_prices = historical_prices.set_index("Date")

    final_df = historical_prices
    if balance_sheet_quarterly_exists:
        final_df = pd.merge(final_df, balance_sheet_quarterly, how='inner', left_index=True, right_index=True)
    if cash_flow_df_exists:
        final_df = pd.merge(final_df, cash_flow_df, how='inner', left_index=True, right_index=True)
    if income_statement_df_exists:
        final_df = pd.merge(final_df, income_statement_df, how='inner', left_index=True, right_index=True)

    print(final_df.head())
    final_df["prctChangeOPEN"] = getPercentageOfChange(final_df.OPEN)
    TargetProbability = [get_trapezoidal_approximation(get_normal_distribution(final_df["prctChangeOPEN"][i:i+30]),1, 2)for i in range(len(final_df["prctChangeOPEN"])-30)] 
    final_df["TargetProbability"] = TargetProbability + [None for i in range(len(final_df["OPEN"])-len(TargetProbability))]
    final_df.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/final.csv", sep="|")

    print(f"Done: {symbol}")