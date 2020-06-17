import io
import json
import mimetypes
import os
import uuid

import falcon
import msgpack

import pandas as pd

api = application = falcon.API()

class GetNasdaq100(object):

    def on_get(self, req, resp):
        data = json.loads(open("DATA/nasdaq100.json", "r+").read())
        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_201

class GetGoogleNewsLinks(object):

    def on_get(self, req, resp):
        data = json.loads(open("DATA/google_news_links.json", "r+").read())
        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_201

class GetTrainingNewsCoverings(object):

    def on_get(self, req, resp):
        try:
            data = json.loads(open(f"DATA/training/news_coverings.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetNasdaqHistoricalNewsLinks(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/news_articles/{symbol}_links.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404
    
class GetBalanceSheetQuarterly(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/balance_sheet_quarterly.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetCashFlowQuarterly(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/cash_flow_quarterly.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetIncomeStatementQuarterly(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/income_statement_quarterly.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetHistoricalPrices(object):
    def df_to_json(self, df):
        return_dict = {"Date":[],"OPEN":[],"HIGH":[],"LOW":[],"CLOSE":[],"VOLUME":[],"CURRENCY":[],"INDEX":[]}
        for i in df.columns:
            for value in df[i].values:
                return_dict[i].append(value)
        return return_dict

    def on_get(self, req, resp, symbol):
        try:
            df = pd.read_csv(f"DATA/data_per_symbol/{symbol.upper()}/historical_prices.csv", sep="|")
            data = self.df_to_json(df)
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetHoldersDetailedProfiles(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/holders_detailed_profile.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetInstitutionalHolders(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/institutional_holders.json", "r+").read())
            print(data)
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetMajorHolders(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/major_holders.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetProfile(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/profile.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetRecommendations(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/recommendations.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetSummary(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/summary.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetSustainability(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/sustainability.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetYahooEarningsEstimate(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/yahoo_earnings_estimate.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetYahooGrowthEstimate(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/yahoo_growth_estimate.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetYahooRevenueEstimate(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/yahoo_revenue_estimate.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404

class GetYahooRiskEstimate(object):

    def on_get(self, req, resp, symbol):
        try:
            data = json.loads(open(f"DATA/data_per_symbol/{symbol.upper()}/yahoo_risk.json", "r+").read())
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_201
        except:
            resp.body = "ERROR, FILE DOESN'T EXIST!"
            resp.status = falcon.HTTP_404



# Info
get_nasdaq_100 = GetNasdaq100()
get_google_news_links = GetGoogleNewsLinks()
get_training_news_coverings = GetTrainingNewsCoverings()
get_nasdaq_historical_news_links = GetNasdaqHistoricalNewsLinks()
# Timseries
get_balance_sheet_q = GetBalanceSheetQuarterly()
get_cash_flow_q = GetCashFlowQuarterly()
get_income_statement_q = GetIncomeStatementQuarterly()
# get_historical_prices_daily = GetHistoricalPrices()
# Non-timeseries
get_holders_detailed_profile = GetHoldersDetailedProfiles()
get_institutional_holders = GetInstitutionalHolders()
get_major_holders = GetMajorHolders()
get_profile = GetProfile()
get_summary = GetSummary()
get_sustainability = GetSustainability()
# Possible timeseries
get_recommendations = GetRecommendations()
get_yahoo_earnings_estimate = GetYahooEarningsEstimate()
get_yahoo_growth_estimate = GetYahooGrowthEstimate()
get_yahoo_revenue_estimate = GetYahooRevenueEstimate()
get_yahoo_risk_estimate = GetYahooRiskEstimate()

api.add_route('/info/nasdaq_100', get_nasdaq_100)
api.add_route('/info/google_news_links', get_google_news_links)
api.add_route('/info/training_news_coverings', get_training_news_coverings)
api.add_route('/info/nasdaq_historical_news_links/{symbol}', get_nasdaq_historical_news_links)
api.add_route('/timeseries/balance_sheet_q/{symbol}', get_balance_sheet_q)
api.add_route('/timeseries/cash_flow_q/{symbol}', get_cash_flow_q)
api.add_route('/timeseries/income_statement_q/{symbol}', get_income_statement_q)
# api.add_route('/timeseries/historical_prices_daily/{symbol}', get_historical_prices_daily)
api.add_route('/static/holders_detailed_profile/{symbol}', get_holders_detailed_profile)
api.add_route('/static/institutional_holders/{symbol}', get_institutional_holders)
api.add_route('/static/major_holders/{symbol}', get_major_holders)
api.add_route('/static/profile/{symbol}', get_profile)
api.add_route('/static/summary/{symbol}', get_summary)
api.add_route('/static/sustainability/{symbol}', get_sustainability)
api.add_route('/possible_timeseries/recommendations/{symbol}', get_recommendations)
api.add_route('/possible_timeseries/yahoo_earnings_estimate/{symbol}', get_yahoo_earnings_estimate)
api.add_route('/possible_timeseries/yahoo_growth_estimate/{symbol}', get_yahoo_growth_estimate)
api.add_route('/possible_timeseries/yahoo_revenue_estimate/{symbol}', get_yahoo_revenue_estimate)
api.add_route('/possible_timeseries/yahoo_risk_estimate/{symbol}', get_yahoo_risk_estimate)
