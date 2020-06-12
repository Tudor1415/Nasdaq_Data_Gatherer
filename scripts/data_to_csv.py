import pandas as pd
import json
import os

def json_to_dict(data):
    return_dict = {}
    for key in data[0]:
        return_dict[key] = []
    for row in data:
        for key, item in row.items():
            return_dict[key].append(item)
    return return_dict

def flip_dict_major_holders(data):
    return_dict = {}
    for i in data["Type"]:
        return_dict[i] = []
    for i, data in enumerate(data["Percentage"]):
        return_dict[list(return_dict.keys())[i]].append(data)
    return return_dict

def get_profile_to_dict(profile):
    return_dict = {}; executives = []
    for key in profile:
        return_dict[key] = []
    for key, item in profile.items():
        if not key == "KeyExecutives": 
            return_dict[key].append(item)
        else:
            for item in item:
               executives.append((item["name"], item["title"]))
            return_dict[key].append(executives)
    return return_dict

def get_recommandations_to_dict(recomandations):
    return_dict = {}
    for i in recomandations:
        return_dict[i] = []
    for key, group in recomandations.items():
        for _, item in group.items():
            return_dict[key].append(item)
    return return_dict

def get_summary_to_dict(summary):
    return_dict = {}
    for key, item in summary.items():
        return_dict[key] = [item]
    return return_dict

def get_yahoo_risk_to_dict(risk):
    return {"Total_ESG_Risk_score":[risk[0]], "Environment_Risk_Score":[risk[1]], "Social_Risk_Score":[risk[2]], "Governance_Risk_Score":[risk[3]], "Controversy_Level":[risk[4]]}

for symbol in os.listdir("../DATA/data_per_symbol/"):
    print(symbol)
    os.mkdir(f"../DATA/data_per_symbol/{symbol}/CSV")

    try:
        balance_sheet = json.loads(open(f"../DATA/data_per_symbol/{symbol}/balance_sheet_quarterly.json", "r+").read())
        balance_sheet_dict = json_to_dict(balance_sheet)
        balance_sheet_df = pd.DataFrame.from_dict(balance_sheet_dict)
        balance_sheet_df.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/balance_sheet_quarterly.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        cash_flow = json.loads(open(f"../DATA/data_per_symbol/{symbol}/cash_flow_quarterly.json", "r+").read())
        cash_flow_dict = json_to_dict(cash_flow)
        cash_flow_df = pd.DataFrame.from_dict(cash_flow_dict)
        cash_flow_df.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/cash_flow_df.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        edgar_8k = json.loads(open(f"../DATA/data_per_symbol/{symbol}/edgar_8k_data.json", "r+").read())
        edgar_8k_df = pd.DataFrame.from_dict(edgar_8k)
        edgar_8k_df.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/edgar_8k_df.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        historical_prices = pd.read_csv(f"../DATA/data_per_symbol/{symbol}/historical_prices.csv", sep="|")
        historical_prices.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/historical_prices.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        holders_detailed_profile_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/holders_detailed_profile.json", "r+").read())
        holders_detailed_profile_static_df = pd.DataFrame.from_dict(holders_detailed_profile_static)
        holders_detailed_profile_static_df.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/holders_detailed_profile_static_df.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        income_statement = json.loads(open(f"../DATA/data_per_symbol/{symbol}/income_statement_quarterly.json", "r+").read())
        income_statement_dict = json_to_dict(income_statement)
        income_statement_df = pd.DataFrame.from_dict(income_statement_dict)
        income_statement_df.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/income_statement_df.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        institutional_holders_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/institutional_holders.json", "r+").read())
        institutional_holders_df_0_static = pd.DataFrame.from_dict(institutional_holders_static[0])
        institutional_holders_df_1_static = pd.DataFrame.from_dict(institutional_holders_static[1])
        institutional_holders_df_2_static = pd.DataFrame.from_dict(institutional_holders_static[2])
        institutional_holders_df_2_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/institutional_holders_df_2_static.csv", index=False, sep="@")
        institutional_holders_df_1_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/institutional_holders_df_1_static.csv", index=False, sep="@")
        institutional_holders_df_0_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/institutional_holders_df_0_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        major_holders_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/major_holders.json", "r+").read())
        major_holders_dict_static = flip_dict_major_holders(major_holders_static)
        major_holders_df_static = pd.DataFrame.from_dict(major_holders_dict_static)
        major_holders_df_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/major_holders_df_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        profile_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/profile.json", "r+").read())
        profile_dict_static = get_profile_to_dict(profile_static)
        profile_dict_df_static = pd.DataFrame.from_dict(profile_dict_static)
        profile_dict_df_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/profile_dict_df_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        recommandations_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/recommendations.json", "r+").read())
        recommandations_dict_static = get_recommandations_to_dict(recommandations_static)
        recommandations_dict_static_df = pd.DataFrame.from_dict(recommandations_dict_static)
        recommandations_dict_static_df.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/recommandations_dict_static_df.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        summary_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/summary.json", "r+").read())
        summary_dict_static = get_summary_to_dict(summary_static)
        summary_df_static = pd.DataFrame.from_dict(summary_dict_static)
        summary_df_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/summary_df_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        sustainability_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/sustainability.json", "r+").read())
        sustainability_dict_static = get_summary_to_dict(sustainability_static["Value"])
        sustainability_df_static = pd.DataFrame.from_dict(sustainability_dict_static)
        sustainability_df_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/sustainability_df_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        yahoo_earnings_estimate_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/yahoo_earnings_estimate.json", "r+").read())
        yahoo_earnings_estimate_df_static = pd.DataFrame.from_dict(yahoo_earnings_estimate_static)
        yahoo_earnings_estimate_df_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/yahoo_earnings_estimate_df_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        yahoo_growth_estimate_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/yahoo_growth_estimate.json", "r+").read())
        yahoo_growth_estimate_df_static = pd.DataFrame.from_dict(yahoo_growth_estimate_static)
        yahoo_growth_estimate_df_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/yahoo_growth_estimate_df_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        yahoo_revenue_estimate_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/yahoo_revenue_estimate.json", "r+").read())
        yahoo_revenue_estimate_df_static = pd.DataFrame.from_dict(yahoo_revenue_estimate_static)
        yahoo_revenue_estimate_df_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/yahoo_revenue_estimate_df_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")
    try:
        yahoo_risk_static = json.loads(open(f"../DATA/data_per_symbol/{symbol}/yahoo_risk.json", "r+").read())
        yahoo_risk_static_df_static = pd.DataFrame.from_dict(get_yahoo_risk_to_dict(yahoo_risk_static))
        yahoo_risk_static_df_static.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/yahoo_risk_static_df_static.csv", index=False, sep="@")
    except:
        print(f"Error {symbol}!")

    print(f"Done {symbol}!")