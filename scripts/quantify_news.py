import json
import os
from datetime import datetime as dt

import pandas as pd

os.chdir("../DATA/news_articles/")

for file in os.listdir():
    news = json.loads(open(file, "r+").read())
    # , columns=['Title', 'Elapsed Time', 'Published Date', 'Link', 'Content']
    if "_links.json" not in file:
        news_df = pd.DataFrame.from_dict(news)
        # Expanding all the lists in the dataframe
        news_df = news_df.explode("Published_Date")
        news_df = news_df.explode("Title")
        news_df = news_df.explode("Link")
        news_df = news_df.explode("Content")
        # Turning Published_Date into datetime column
        try:
            news_df["Published_Date"] = news_df["Published_Date"].apply(lambda x: dt.strptime("".join(x.split(" ")[:3]), "%b%d,%Y"))
        except:
            print(f"Error {file}")
        # Counting the articles for each date
        dates_df = pd.DataFrame()
        dates = []; no_articles = []
        for key, df in news_df.groupby(["Published_Date"]):
            dates += [key]; no_articles += [len(df)]
        # news_df["Date"] = dates
        # news_df.set_index("Date")
        # news_df["No_Articles"] = no_articles

        # Merging the articles dataframe with the final one
        # final_df = pd.read_csv(f"../data_per_symbol/{file.split('.')[0]}/CSV/final.csv", sep="|")
        # final_df = pd.merge(final_df, dates_df, how='inner', left_index=True, right_index=True)
        # final_df.to_csv(f"../data_per_symbol/{file.split('.')[0]}/CSV/final.csv", sep="|", index=False)

        news_df.to_csv(f"../data_per_symbol/{file.split('.')[0]}/CSV/historical_news_articles.csv", sep="@", index=False)
        print(file)
        
