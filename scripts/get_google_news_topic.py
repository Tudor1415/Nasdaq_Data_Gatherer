import json
import re
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_nasdaq100():
    """
    Service: NASDAQ
    """
    return_dict = {}
    response = requests.get(f"https://api.nasdaq.com/api/quote/list-type/nasdaq100")

    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        date = data["date"]
        for i in data["data"]["rows"]:
            for j in list(i.keys()):
                if not j in list(return_dict.keys()):
                    return_dict[j] = []
                return_dict[j].append(i[j])
        return date, return_dict

    elif response.status_code == 404:
        return "Not Found."


def get_urls(names):
    """
    Please give the name of the company, not the symbol
    """
    urls = []; errors = 0
    for name in names:
        try:
            string = name.split(". ")[0]

            if "Common Stock" in string:
                string = string.replace("Common Stock", " ")
            if ".com" in string:
                string = string.replace(".com", " ")
            if "Incorporated" in string:
                string = string.replace("Incorporated", " ")
            if "Class A" in string:
                string = string.replace("Class A", " ")
            if "Class B" in string:
                string = string.replace("Class B", " ")
            if "Class C" in string:
                string = string.replace("Class C", " ")
            if "Class D" in string:
                string = string.replace("Class D", " ")
            if "Corporation" in string:
                string = string.replace("Corporation", " ")
            if "Ordinary Shares" in string:
                string = string.replace("Ordinary Shares", " ")                

            print(string)
            driver.get(f"https://news.google.com/search?q={string}&hl=en-US&gl=US&ceid=US%3Aen")
            time.sleep(0.75)
            urls.append(driver.find_element_by_css_selector('.NAv2Bc').get_attribute('href'))
        except:
            errors += 1
            urls.append("Error")
            print(f"Error with {name}!")

    print(f"Number of errors: {errors}")  
    return urls

def get_topic_urls():
    names = get_nasdaq100()[1]["companyName"]
    urls = get_urls(names)
    data = {}
    for i in range(len(urls)):
        data[names[i]] = urls[i]

    open("../DATA/google_news_links.json", "w+").write(json.dumps(data))



driver = webdriver.Remote(command_executor='http://172.17.0.1:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)

get_topic_urls()
