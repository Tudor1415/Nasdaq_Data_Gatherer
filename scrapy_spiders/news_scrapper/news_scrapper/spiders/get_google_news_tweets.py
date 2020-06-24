# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import os

class GetGoogleNewsTweetsSpider(scrapy.Spider):
    name = 'get_google_news_tweets'
    allowed_domains = ['news.google.com']
    start_urls = ['https://news.google.com/' + i.split("./")[1] for i in pd.read_csv("DATA/news_coverings.csv", sep="|")["links"]]

    def parse(self, response):
        df = pd.DataFrame()
        df["tweet"] = response.css("div.ifw3f::text").getall()
        df["covering_link"] = response.request.url
        df["tweet"] = df["tweet"].explode()
        if "relevant_tweets.csv" in os.listdir("DATA"):
            exists = True
            past_data = pd.read_csv("DATA/relevant_tweets.csv", sep="|")
        else:
            exists = False
        if exists:
            past_data = past_data.append(df)
            past_data = past_data.drop_duplicates()
            past_data.to_csv("DATA/relevant_tweets.csv", sep="|", index=False)
        else:
            df.to_csv("DATA/relevant_tweets.csv", sep="|", index=False)

        print(response.css("div.ifw3f::text").getall())
