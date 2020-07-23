import argparse
import os
from collections import defaultdict

import pandas as pd

from helpers import *


def get_symbols(names=[], slices=""):
    global symbols; global CIK
    df = pd.read_csv("../DATA/cik_ticker.csv", sep="|")
    df = df.loc[df["Exchange"] == "NASDAQ"]
    if len(names) == 0 and len(slices) == 0:
        symbols = df["Ticker"]
        CIK = df["CIK"]
    if len(names) > 0:
        symbols = names
        CIK = [df.loc[df["Ticker"] == i]["CIK"] for i in names]

def get_profile_to_csv(file_name):
    tmp = defaultdict(list)

    for symbol in symbols:
        try:
            # profile = get_company_profile(symbol)
            # # dict_wiki = get_wikipedia_search_data_for_companies([profile["CompanyName"]])
            institutional_holders = get_nasdaq_institutional_holders(symbol)[2]
            # tmp["ModuleTitle"].append(profile["ModuleTitle"])
            # tmp["CompanyName"].append(profile["CompanyName"])
            # tmp["Symbol"].append(profile["Symbol"])
            # tmp["Address"].append(profile["Address"])
            # tmp["Phone"].append(profile["Phone"])
            # tmp["Industry"].append(profile["Industry"])
            # tmp["Sector"].append(profile["Sector"])
            # tmp["Region"].append(profile["Region"])
            # # tmp["Number_of_employees"].append(dict_wiki["Number_of_employees"])
            # # tmp["Subsidiaries"].append(dict_wiki["Subsidiaries"])
            # # tmp["CompanyDescription"].append(profile["CompanyDescription"])k
            # tmp["KeyExecutives"].append([(i["name"], i["title"]) for i in profile["KeyExecutives"]])
            ih = []
            for idx, value in enumerate(institutional_holders["OWNER_NAME"]):
                ih.append((value, institutional_holders["MARKET_VALUE"][idx]))
            tmp["Institutional Holders"].append(ih)
            # profile = pd.DataFrame.from_dict(tmp)
            print(f"Done {symbol}")
            # if file_name in os.listdir("../DATA/"):
            #     old_df = pd.read_csv(f"../DATA/{file_name}", sep="|")
            #     old_df = pd.concat([old_df, profile], axis=0)
            #     old_df = old_df.Symbol.drop_duplicates()
            #     old_df.to_csv(f"../DATA/{file_name}", sep="|", index=False)
            # else:
            #     profile.to_csv(f"../DATA/{file_name}", sep="|", index=False)
        except:
            print("ERROR")

    return tmp

if __name__ == "__main__":
    symbols=[]; CIK=[]
    get_symbols()
    profiles = get_profile_to_csv("profiles.csv")
    old_df = pd.read_csv(f"../DATA/profiles.csv", sep="|", index=False)
    old_df["Institutional Holders"] = profiles["Institutional Holders"]
    old_df.to_csv(f"../DATA/profiles.csv", sep="|", index=False)
