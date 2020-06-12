import json
import re
from datetime import datetime, timedelta

import bs4
import requests

import wikipedia
import wptools


def get_historical(symbol, fromdate, todate, metadata=False):
    """ 
    Service: NASDAQ
    Maximum interval is about 3 years, please do multiple requests.
    Date layout : YYYY-MM-DD
    """
    return_dict = {"high":[], "low":[], "open":[], "close":[],"volume":[],"dateTime":[],"value":[]}
    response = requests.get(f"https://api.nasdaq.com/api/quote/{symbol.upper()}/chart?assetclass=stocks&fromdate={fromdate}&todate={todate}")

    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        chart = data["chart"]
        for i in chart:
            return_dict["high"].append(i["z"]["high"])
            return_dict["low"].append(i["z"]["low"])
            return_dict["open"].append(i["z"]["open"])
            return_dict["close"].append(i["z"]["close"])
            return_dict["volume"].append(i["z"]["volume"])
            return_dict["dateTime"].append(i["z"]["dateTime"])
            return_dict["value"].append(i["z"]["value"])

        if metadata:
            meta = {}
            for i in list(data.keys())[:-1]:
                meta[i] = data[i]
            return meta, return_dict
        else:
            return return_dict
    elif response.status_code == 404:
        return "Not Found."
    
# print(get_historical("ABT","2020-01-10", "2020-06-10"))

def get_company_profile(symbol):
    """
    Service: NASDAQ
    Returns the comany's profile given a symbol. Th profile contains the following info:
    ModuleTitle, CompanyName, Symbol, Address, Phone, Industry, Sector, Region, CompanyDescription, KeyExecutives
    """
    symbol = symbol.upper()
    return_dict = {}
    response = requests.get(f"https://api.nasdaq.com/api/company/{symbol}/company-profile")

    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        
        for i in list(data.keys()):
            return_dict[i] = data[i]["value"]
        return return_dict

    elif response.status_code == 404:
        return "Not Found."

# print(get_company_profile("AaPL"))

def get_realtime_price(*symbols, markettype=False):
    """
    Service: NASDAQ
    Return the following info for an array of symbols:
    symbol, companyName, lastSalePrice, netChange, percentageChange, deltaIndicator, lastTradeTimestamp, volume
    """
    return_dict = {}
    response = requests.get(f"https://api.nasdaq.com/api/quote/watchlist?{''.join(['symbol='+i.lower()+ '|stocks&' for i in symbols])}")
    if response.status_code == 200:
        data = json.loads(response.text)["data"]

        for i in data:
            for j in list(i.keys()):
                if not j in list(return_dict.keys()):
                    return_dict[j] = []
                return_dict[j].append(i[j])
        return return_dict

    elif response.status_code == 404:
        return "Not Found."

# print(get_realtime_price('aapl','tsla','msft'))

def get_nasdaq100():
    """
    Service: NASDAQ
    """
    return_dict = {}
    response = requests.get(f"https://api.nasdaq.com/api/quote/list-type/nasdaq100")

    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        date = data["date"]
        for i in data["data"]["rows"]:
            for j in list(i.keys()):
                if not j in list(return_dict.keys()):
                    return_dict[j] = []
                return_dict[j].append(i[j])
        return date, return_dict

    elif response.status_code == 404:
        return "Not Found."

# print(get_nasdaq100())

def get_company_summary(symbol):
    """
    Service: NASDAQ
    Returns the folowing info for a given symbol:
    - Exchange, Sector, Industry, OneYrTarget, TodayHighLow, ShareVolume, AverageVolume, PreviousClose, 
    - FiftTwoWeekHighLow, MarketCap, PERatio, ForwardPE1Yr, EarningsPerShare, AnnualizedDividend, 
    - ExDividendDate, DividendPaymentDate, Yield, Beta
    """
    symbol = symbol.upper()
    return_dict = {}
    response = requests.get(f"https://api.nasdaq.com/api/quote/{symbol}/summary?assetclass=stocks")

    if response.status_code == 200:
        data = json.loads(response.text)["data"]["summaryData"]
        for i in list(data.keys()):
            return_dict[i] = data[i]["value"]
        return return_dict

    elif response.status_code == 404:
        return "Not Found."
    
# print(get_company_summary("aapl"))

def get_latest_articles(num):
    """
    Service: NASDAQ
    Returns a lsit of a specified number of articles recently punlished
    """
    url = f'https://www.nasdaq.com/api/v1/recent-articles/31942/{num}'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    elif response.status_code == 404:
        return "Not Found."

# print(get_latest_articles(20))

def get_yahoo_risk_analysis(symbol):
    """
    Service: YAHOO
    This function returns the:
    - totalRisk: str
    - environmentalRisk: str
    - socialRisk: str
    - govermentRisk: str
    - controveryLvl: str
    According to yahoo finance, see example webpage:
    https://finance.yahoo.com/quote/TSLA/sustainability?p=TSLA
    """
    symbol = symbol.upper()
    response = requests.get(f"https://finance.yahoo.com/quote/{symbol}/sustainability?p={symbol}")

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text,features="html.parser")
        try:
            totalRisk = soup.select_one('div.Mend\(5px\):nth-child(1)').text
            envRisk = soup.select_one('div.W\(22\%\):nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)').text
            socialRisk = soup.select_one('div.Va\(t\):nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)').text
            govRisk = soup.select_one('div.Va\(t\):nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)').text
            controversyLvl = soup.select_one('.Mt\(42px\) > div:nth-child(1) > div:nth-child(1)').text
            return totalRisk, envRisk, socialRisk, govRisk, controversyLvl
        except:
            pass

    elif response.status_code == 404:
        return "Not Found."
# print(get_yahoo_analysys('tsla'))

def get_yahoo_earnings_estimate(symbol):
    """
    Service: YAHOO
    This function returns the:
    - Row_Name: str
    - Current_Quarter: str
    - Next_Quarter: str
    - Current_Year: str
    - Next_Year: str
    According to yahoo finance, see example webpage:
    https://finance.yahoo.com/quote/TSLA/analysis?p=TSLA
    """
    symbol = symbol.upper()
    return_dict = {"Row_Name":[], "Current_Quarter":[], "Next_Quarter":[], "Current_Year":[], "Next_Year":[]}
    response = requests.get(f"https://finance.yahoo.com/quote/{symbol}/analysis?p={symbol}")

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text,features="html.parser")
        for i in range(1,6):
            return_dict["Row_Name"].append(soup.select_one(f'table.BdB:nth-child(2) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(1) > span:nth-child(1)').text)
            return_dict["Current_Quarter"].append(soup.select_one(f'table.BdB:nth-child(2) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(2) > span:nth-child(1)').text)
            return_dict["Next_Quarter"].append(soup.select_one(f'table.BdB:nth-child(2) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(3) > span:nth-child(1)').text)
            return_dict["Current_Year"].append(soup.select_one(f'table.BdB:nth-child(2) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(4) > span:nth-child(1)').text)
            return_dict["Next_Year"].append(soup.select_one(f'table.BdB:nth-child(2) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(5) > span:nth-child(1)').text)
        return return_dict
    elif response.status_code == 404:
        return "Not Found."

# print(get_yahoo_earnings_estimate('tsla'))

def get_yahoo_revenue_estimate(symbol):
    """
    Service: YAHOO
    This function returns the:
    - Row_Name: str
    - Current_Quarter: str
    - Next_Quarter: str
    - Current_Year: str
    - Next_Year: str
    The different rows are:
    **No. of Analysts**, **Avg. Estimate**, **Low Estimate**, **High Estimate**, **Year Ago Sales**
    According to yahoo finance, see example webpage:
    https://finance.yahoo.com/quote/TSLA/analysis?p=TSLA
    """
    symbol = symbol.upper()
    return_dict = {"Row_Name":[], "Current_Quarter":[], "Next_Quarter":[], "Current_Year":[], "Next_Year":[]}
    response = requests.get(f"https://finance.yahoo.com/quote/{symbol}/analysis?p={symbol}")

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text,features="html.parser")
        for i in range(1,6):
            return_dict["Row_Name"].append(soup.select_one(f'table.W\(100\%\):nth-child(3) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(1) > span:nth-child(1)').text)
            return_dict["Current_Quarter"].append(soup.select_one(f'table.W\(100\%\):nth-child(3) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(2) > span:nth-child(1)').text)
            return_dict["Next_Quarter"].append(soup.select_one(f'table.W\(100\%\):nth-child(3) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(3) > span:nth-child(1)').text)
            return_dict["Current_Year"].append(soup.select_one(f'table.W\(100\%\):nth-child(3) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(4) > span:nth-child(1)').text)
            return_dict["Next_Year"].append(soup.select_one(f'table.W\(100\%\):nth-child(3) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(5) > span:nth-child(1)').text)
        return return_dict
    elif response.status_code == 404:
        return "Not Found."

# print(get_yahoo_revenue_estimate('tsla'))

def get_yahoo_growth_estimate(symbol):
    """
    Service: YAHOO
    This function returns the predictions for the:
    - Symbol: str
    - Industry: str
    - S&P 500: str
    - Sector: str
    The different rows are:
    **Current Estimate**, **7 Days Ago**, **30 Days Ago**, **60 Days Ago**, **90 Days Ago**
    According to yahoo finance, see example webpage:
    https://finance.yahoo.com/quote/TSLA/analysis?p=TSLA
    """
    symbol = symbol.upper()
    return_dict = {"Row_Name":[], "Current_Quarter":[], "Next_Quarter":[], "Current_Year":[], "Next_Year":[]}
    response = requests.get(f"https://finance.yahoo.com/quote/{symbol}/analysis?p={symbol}")

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text,features="html.parser")
        for i in range(1,6):
            return_dict["Row_Name"].append(soup.select_one(f'table.W\(100\%\):nth-child(6) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(1) > span:nth-child(1)').text)
            return_dict["Current_Quarter"].append(soup.select_one(f'table.W\(100\%\):nth-child(6) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(2)').text)
            return_dict["Next_Quarter"].append(soup.select_one(f'table.W\(100\%\):nth-child(6) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(3)').text)
            return_dict["Current_Year"].append(soup.select_one(f'table.W\(100\%\):nth-child(6) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(4)').text)
            return_dict["Next_Year"].append(soup.select_one(f'table.W\(100\%\):nth-child(6) > tbody:nth-child(2) > tr:nth-child({i}) > td:nth-child(5)').text)
        return return_dict
    elif response.status_code == 404:
        return "Not Found."

# print(get_yahoo_growth_estimate('tsla'))

def get_yahoo_major_holders(symbol):
    """
    Service: YAHOO
    This function returns the data for the:
    - % of Shares Held by All Insider: str
    - % of Shares Held by Institutions: str
    - % of Float Held by Institutions: str
    - Number of Institutions Holding Shares: str

    According to yahoo finance, see example webpage:
    https://finance.yahoo.com/quote/TSLA/holders?p=TSLA
    """
    symbol = symbol.upper()
    return_dict = {"Percentage":[], "Type":[]}
    response = requests.get(f"https://finance.yahoo.com/quote/{symbol}/holders?p={symbol}")

    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text,features="html.parser")
        for i in range(1,5):
            return_dict["Percentage"].append(soup.select_one(f'.Pb\(30px\) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child({i}) > td:nth-child(1)').text)
            return_dict["Type"].append(soup.select_one(f'.Pb\(30px\) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child({i}) > td:nth-child(2)').text)
        return return_dict
    elif response.status_code == 404:
        return "Not Found."

# print(get_yahoo_major_holders('tsla'))

def get_nasdaq_institutional_holders(symbol):
    """
    Service: NASDAQ
    This function returns the data of the institutional holders:
    - OwnershipSummary: dict
    - Positions: dict
    - HoldingsTransactions: dict

    According to yahoo finance, see example webpage:
    https://finance.yahoo.com/quote/TSLA/holders?p=TSLA
    """
    symbol = symbol.upper()

    OwnershipSummary = {"SharesOutstandingPCT":[],"ShareoutstandingTotal":[],"TotalHoldingsValue":[]}
    Positions = {"ActivePositions":[],"Holders":[],"Shares":[]}
    HoldingsTransactions = {"OWNER_NAME":[],"DATE":[],"SHARES_HELD":[], "CHANGE(Shares)":[], "CHANGE(%)":[], "MARKET_VALUE":[]}

    response = requests.get(f"https://api.nasdaq.com/api/company/{symbol.upper()}/institutional-holdings?limit=5&type=TOTAL")

    if response.status_code == 200:
        data = json.loads(response.text)['data']

        for i in data["ownershipSummary"]:
            OwnershipSummary[i].append(data["ownershipSummary"][i]['value'])
        
        for i in data["activePositions"]["rows"]:
            Positions["ActivePositions"].append(i["positions"])
            Positions["Holders"].append(i["holders"])
            Positions["Shares"].append(i["shares"])
        
        for i in data["newSoldOutPositions"]["rows"]:
            Positions["ActivePositions"].append(i["positions"])
            Positions["Holders"].append(i["holders"])
            Positions["Shares"].append(i["shares"])
        
        for i in data["holdingsTransactions"]["table"]["rows"]:
            HoldingsTransactions["OWNER_NAME"].append(i["ownerName"])
            HoldingsTransactions["DATE"].append(i["date"])
            HoldingsTransactions["SHARES_HELD"].append(i["sharesHeld"])
            HoldingsTransactions["CHANGE(Shares)"].append(i["sharesChange"])
            HoldingsTransactions["CHANGE(%)"].append(i["sharesChangePCT"])
            HoldingsTransactions["MARKET_VALUE"].append(i["marketValue"])


        return OwnershipSummary, Positions, HoldingsTransactions

    elif response.status_code == 404:
        return "Not Found."

# print(get_nasdaq_institutional_holders('tsla'))

def get_google_entity_search(api_key, query):
    """
    Service: GOOGLE
    This function returns the data for the:
    - Name
    - Wiki link
    - Description 
    """
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 1,
        'indent': True,
        'key': api_key,
    }
    response = json.loads(requests.get(service_url, params=params).text)
    
    try:
        name = response["itemListElement"][0]["result"]["name"]
        description = response["itemListElement"][0]["result"]["description"]
    except:
        name = None; description = None
    try:
        url = response["itemListElement"][0]["result"]["detailedDescription"]["url"]
        title = bs4.BeautifulSoup(requests.get(url).text, "html.parser").title.string.replace(" - Wikipedia", "")
    except:
        title = None; url = None

    return name, url, title, description

# print(get_google_entity_search("AIzaSyBbJdYxfmF2AFNP36ZCtxrz8Lef_lMta5M", "Vanguard Group Inc."))

def get_wikipedia_search_data_for_institution(institutions_name:list):
    """
    Service: WIKIPEDIA
    This function returns the data for the:
    - Description
    - Number of shares held
    - CEO Name 

    According to wikipedia
    """

    return_dict = {"Name":[], "Description":[], "NoShare(Trillion)":[], "KeyPeople":[]}
    
    def get_info(name, return_dict):
        key_people = []
        return_dict["Name"].append(name)
        try:
            return_dict["Description"].append(page.summary)
        except:
            return_dict["Description"].append("NO INFO")
        try:
            data = re.findall(r"\$(\d+).(\d+)", wppage.data["infobox"]['aum'])
            return_dict["NoShare(Trillion)"].append(''.join(data[0][0]+"."+data[0][1]))
        except:
            return_dict["NoShare(Trillion)"].append("NO INFO")
        try:
            for i in re.findall(r"\[\[\s*(.*?)(?=\s*\]\]|$)", wppage.data["infobox"]['key_people']):
                key_people.append(i)
            return_dict["KeyPeople"].append(key_people)
        except:
            return_dict["KeyPeople"].append("NO INFO")

    for name in institutions_name:
        print(name)
        title = get_google_entity_search("AIzaSyBbJdYxfmF2AFNP36ZCtxrz8Lef_lMta5M", name)[2]
        try:
            page = wikipedia.page(title)
            wppage = wptools.page(title).get_parse()
            get_info(name, return_dict)
        except:
            print('Error')
            return_dict["Name"].append(name)
            return_dict["Description"].append("NO INFO")
            return_dict["NoShare(Trillion)"].append("NO INFO")
            return_dict["KeyPeople"].append("NO INFO")


    return return_dict
                
# print(get_wikipedia_search_data_for_institution(['BLACKROCK INC.']))


def get_wikipedia_search_data_for_companies(institutions_name:list):
    """
    Service: WIKIPEDIA
    This function returns the data for the:
    - Number_of_employees
    - Subsidiaries Companies

    According to wikipedia
    """

    return_dict = {"Number_of_employees":[], "Subsidiaries":[]}
    
    def get_info(return_dict):
        try:
            for i in re.findall(r"\d,\d+",wppage.data["infobox"]['num_employees']):
                return_dict["Number_of_employees"].append(i)
        except:
            return_dict["Number_of_employees"].append("NO INFO")
        try:
            for i in re.findall(r"(?=((?<![A-Za-z.])[A-Z][a-z.]*[\s-][A-Z][a-z.]*))", wppage.data["infobox"]['subsid']):
                return_dict["Subsidiaries"].append(i)
        except:
            return_dict["Subsidiaries"].append("NO INFO")

        
    for name in institutions_name:
        print(name)
        title = get_google_entity_search("AIzaSyBbJdYxfmF2AFNP36ZCtxrz8Lef_lMta5M", name)[2]
        try:
            wppage = wptools.page(title).get_parse()
            get_info(return_dict)
        except:
            print('Error')
            return_dict["Number_of_employees"].append("NO INFO")
            return_dict["Subsidiaries"].append("NO INFO")
       


    return return_dict

# print(get_wikipedia_search_data_for_companies(["Activision Blizzard, Inc"]))
# https://api.nasdaq.com/api/company/TSLA/company-profile
# https://api.nasdaq.com/api/quote/TSLA/info?assetclass=stocks
# https://api.nasdaq.com/api/quote/TSLA/quote-bar?assetclass=stocks&
# https://api.nasdaq.com/api/market-info
# https://www.nasdaq.com/api/v1/article-by-symbol/31942 -> stock symbol id
# https://api.nasdaq.com/api/quote/TSLA/chart?assetclass=stocks&fromdate=2018-07-07&todate=2020-05-31
# https://api.nasdaq.com/api/quote/TSLA/summary?assetclass=stocks
# https://api.nasdaq.com/api/quote/watchlist?symbol=aapl|stocks&symbol=tsla|stocks&
# https://api.nasdaq.com/api/quote/TSLA/chart?assetClass=stocks&
# https://api.nasdaq.com/api/quote/TSLA/extended-trading?assetclass=stocks&markettype=post
# https://www.nasdaq.com/api/v1/upcoming-event-by-symbol/31942 -> stock symbol id
# https://www.nasdaq.com/api/v1/article-by-symbol/31942
# https://api.nasdaq.com/api/quote/TSLA/info?assetclass=stocks
# https://www.nasdaq.com/api/v1/recent-articles/31942/100
# https://api.nasdaq.com/api/quote/list-type/nasdaq100
