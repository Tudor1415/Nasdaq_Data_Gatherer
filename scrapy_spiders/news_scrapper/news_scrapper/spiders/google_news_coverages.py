# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import os
import pandas as pd

try:
    # coverages_links = ['https://news.google.com/' + i.split("./")[1] for i in pd.read_csv("DATA/news_coverings.csv", sep="|")["links"]]
    coverages_links = []

except:
    coverages_links = []

class GoogleNewsCoveragesSpider(scrapy.Spider):
    name = 'google_news_coverages'
    allowed_domains =  ['https://news.google.com/']
    start_urls = coverages_links

    def parse(self, response):
        return_dict = {"Links":[], "Titles":[], "Coverage_links":[]}

        links = response.css("h4 > a::attr(href)").getall()
        titles = response.css("h4 > a::text").getall()
        for i, link in enumerate(links):
            return_dict["Links"] += [link]
            return_dict["Titles"] += [titles[i]]
            return_dict["Coverage_links"] += [response.request.url]

        return_df = pd.DataFrame.from_dict(return_dict)
        return_df.reset_index(drop=True, inplace=True)
        if "training_articles_links.csv" in os.listdir("DATA"):
            exists = True
            past_data = pd.read_csv("DATA/training_articles_links.csv", sep="|")
        else:
            exists = False
        if exists:
            past_data = past_data.append(return_df)
            past_data = past_data.drop_duplicates()
            past_data.to_csv("DATA/training_articles_links.csv", sep="|", index=False)
        else:
            return_df.to_csv("DATA/training_articles_links.csv", sep="|", index=False)
