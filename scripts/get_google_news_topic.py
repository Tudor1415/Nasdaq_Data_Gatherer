import json
import re
import time

import requests
from pyvirtualdisplay import Display
from selenium import webdriver

import pandas as pd

display = Display(visible=0, size=(2000, 2000))
display.start()

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
    df = pd.read_csv("../DATA/nasdaq-listed-symbols.csv")
    names = df["Company Name"]
    urls = get_urls(names)
    data = {}
    for i in range(len(urls)):
        data[names[i]] = urls[i]

    open("../DATA/google_news_links.json", "w+").write(json.dumps(data))



driver = webdriver.Firefox()

get_topic_urls()
display.stop()
