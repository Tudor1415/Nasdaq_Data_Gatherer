from newspaper import Article
from newspaper import Config
import json

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent

def get_article(url):
    page = Article(url, config=config)
    page.download()
    page.parse()
    page.nlp()

    return page.publish_date, page.keywords, page.summary

def get_training_articles():
    return_dict = {"Date":[], "Keywords":[], "Summary":[], "Coverage_link":[]}
    articles = json.loads(open("../DATA/training/training_articles_links.json", "r+").read())
    urls = ["https://news.google.com/" + i["link"].split("./")[1] for i in articles]
    coverage_links = [i["coverage_link"] for i in articles]
    errors = 0
    for i, url in enumerate(urls):
        try:
            date, keywords, summary = get_article(url)
            return_dict["Date"].append(date)
            return_dict["Keywords"].append(keywords)
            return_dict["Summary"].append(summary)
            return_dict["Coverage_link"].append(coverage_links[i])
            print(f"Done: {i}, Errors: {errors}")
        except:
            errors += 1
    open("../DATA/training/articles_content.json", "w+").write(json.dumps(return_dict))
    return return_dict
