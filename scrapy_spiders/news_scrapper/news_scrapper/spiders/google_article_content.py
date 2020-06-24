# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import os
try:
    articles_links = ['https://news.google.com/' + i.split("./")[1] for i in pd.read_csv("DATA/training_articles_links.csv", sep="|")["Links"]]
except:
    articles_links = []

class GoogleArticleContentSpider(scrapy.Spider):
    name = 'google_article_content'
    allowed_domains = ['*']
    start_urls = articles_links


    def parse(self, response):
        link = response.css('a::attr(href)').getall()[-2]
        req = scrapy.http.Request(link, callback=self.page_summary)
        # print("///")
        # print(req)

    def page_summary(self, response):
        return_dict = {"summary":["".join(response.css('p::text').getall()[:2])]}
        return_df = pd.DataFrame.from_dict(return_dict)
        if "article_summary.csv" in os.listdir("DATA"):
            exists = True
            past_data = pd.read_csv("DATA/article_summary.csv", sep="|")
        else:
            exists = False
        if exists:
            past_data = past_data.append(return_df)
            past_data = past_data.drop_duplicates()
            past_data.to_csv("DATA/article_summary.csv", sep="|", index=False)
        else:
            return_df.to_csv("DATA/article_summary.csv", sep="|", index=False)
