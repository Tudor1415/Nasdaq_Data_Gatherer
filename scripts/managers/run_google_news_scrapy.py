import os
from datetime import datetime

def get_hour(now, future):
    return (int(now) + future) % 12

with open("logs.txt", "w+") as f:
    f.write(datetime.now().strftime('%H'))
os.chdir("../../scrapy_spiders/news_scrapper/")
os.system(f"scrapy crawl google_news")
os.system(f"scrapy crawl google_news_coverages")

while True:
        if datetime.now().strftime('%H') == get_hour(open("logs.txt", "r+").read(), 1):
                change_hour = datetime.now().strftime('%H')
                open("logs.txt", "w+").write(str(change_hour))
                os.chdir("../../scrapy_spiders/news_scrapper/")
                os.system(f"scrapy crawl google_news")
                os.system(f"scrapy crawl google_news_coverages")
