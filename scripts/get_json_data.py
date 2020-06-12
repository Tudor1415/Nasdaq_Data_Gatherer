import json
import os

import requests

from get_edgar_data import *
from helpers import *

names = json.loads(open("../DATA/nasdaq100.json", "r+").read())["companyName"]
symbols = json.loads(open("../DATA/nasdaq100.json", "r+").read())["symbol"]
CIK = json.loads(open("../DATA/symbol_edgar_id.json", "r+").read())

for symbol in symbols:
    try:
        print(symbol)
        # os.mkdir(f'../DATA/data_per_symbol/{symbol}')

        # profile = get_company_profile(symbol)
        # dict = get_wikipedia_search_data_for_companies([profile["CompanyName"]])
        # profile.update(dict)
        # open(f'../DATA/data_per_symbol/{symbol}/profile.json', 'w+').write(json.dumps(profile))
        
        # historical_data = get_historical(symbol, "2020-01-01", "2020-06-10")
        # open(f'../DATA/data_per_symbol/{symbol}/historical_data.json', 'w+').write(json.dumps(historical_data))

        # summary = get_company_summary(symbol)
        # open(f'../DATA/data_per_symbol/{symbol}/summary.json', 'w+').write(json.dumps(summary))

        # yahoo_risk = get_yahoo_risk_analysis(symbol)
        # open(f'../DATA/data_per_symbol/{symbol}/yahoo_risk.json', 'w+').write(json.dumps(yahoo_risk))

        # yahoo_earnings_estimate = get_yahoo_earnings_estimate(symbol)
        # open(f'../DATA/data_per_symbol/{symbol}/yahoo_earnings_estimate.json', 'w+').write(json.dumps(yahoo_earnings_estimate))

        # yahoo_revenue_estimate = get_yahoo_revenue_estimate(symbol)
        # open(f'../DATA/data_per_symbol/{symbol}/yahoo_revenue_estimate.json', 'w+').write(json.dumps(yahoo_revenue_estimate))

        # yahoo_growth_estimate = get_yahoo_growth_estimate(symbol)
        # open(f'../DATA/data_per_symbol/{symbol}/yahoo_growth_estimate.json', 'w+').write(json.dumps(yahoo_growth_estimate))

        # major_holders = get_yahoo_major_holders(symbol)
        # open(f'../DATA/data_per_symbol/{symbol}/major_holders.json', 'w+').write(json.dumps(major_holders))

        # institutional_holders = get_nasdaq_institutional_holders(symbol)
        # open(f'../DATA/data_per_symbol/{symbol}/institutional_holders.json', 'w+').write(json.dumps(institutional_holders))
        institutional_holders = json.loads(open(f'../DATA/data_per_symbol/{symbol}/institutional_holders.json', 'r+').read())
        holders_detailed_profile = get_wikipedia_search_data_for_institution(institutional_holders[2]['OWNER_NAME'])
        open(f'../DATA/data_per_symbol/{symbol}/holders_detailed_profile.json', 'w+').write(json.dumps(holders_detailed_profile))

        # edgar_8k_data = get_edgar_8k_data(CIK[symbol])
        # open(f'../DATA/data_per_symbol/{symbol}/edgar_8k_data.json', 'w+').write(json.dumps(edgar_8k_data))

        # print(f"DONE {symbol}!")
    except:
        pass
