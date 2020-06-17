import os
from datetime import datetime

def get_hour(now, future):
    return (now + future) % 12

change_hour = 0
open("logs.txt", "w+").write(change_hour)

if datetime.now().strftime('%H') == get_hour(open("logs.txt", "w+").read(), 1):
    change_hour = datetime.now().strftime('%H')
    open("logs.txt", "w+").write(change_hour)
    os.chdir("../../scrapy_spiders/news_scrapper/")
    os.system(f"scrapy crawl google_news")
    os.system(f"scrapy crawl google_news_coverages")
