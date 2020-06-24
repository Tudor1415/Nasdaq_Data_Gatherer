import os
from datetime import datetime

def get_hour(now, future):
    return (int(now) + future) % 24

os.chdir("../../scrapy_spiders/news_scrapper/")

with open("manager_logs.txt", "w+") as f:
    f.write(datetime.now().strftime('%H'))
    f.close()
os.system(f"scrapy crawl google_news")
os.system(f"scrapy crawl google_news_coverages")

while True:
    with open("manager_logs.txt", "r+") as f:
        next_hour = get_hour(f.read(), 1)
        f.close()
    if datetime.now().strftime('%H') == next_hour :
            change_hour = datetime.now().strftime('%H')
            with open("manager_logs.txt", "w+") as f:
                f.write(str(change_hour))
            os.chdir("../../scrapy_spiders/news_scrapper/")
            os.system(f"scrapy crawl google_news")
            os.system(f"scrapy crawl google_news_coverages")
