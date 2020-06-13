import os
import time

import requests
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class NasdaqDataStreamer():
    '''
    - (SYM) The symbol of the stock 
    - (RT) Real time stock price data:
    Select between PreMarket, RealTime, AfterHours
    - (KD) Nasdaq "Key Data" (High, Low, Market Cap, Share Volume, Previous Close , etc...)
    - (NWS) Get the latest news headlines 
    Specify the length 
    - (PEG) Price/Earnings & PEG Ratios
    - (PR) Press Releases Headlines 
    Specify the time limit (1mo, 6mo, YTD, 1Y, 5Y, MAX)
    - (FI) Financials such as Income Statement Balance Sheet, Cash Flow, Financial Ratios
    - (QEPS) Quarterly and yearly earnings per share
    - (OC) Option chain table
    - (SI) Short interest 
    - (IH) Institutional Holdings
    - (OS) Ownership summary
    - (ALL) All of the possible data
    '''
    def __init__(self, settings, remote=False, verbose = True):
        self.requestedData = settings
         
        self.nasdaqUrl_KeyData = f'https://www.nasdaq.com/market-activity/stocks/{settings["SYM"].lower()}'
        self.nasdaqUrl_RealTime = f'https://www.nasdaq.com/market-activity/stocks/{settings["SYM"].lower()}/real-time'
        self.nasdaqUrl_AfterHours = f'https://www.nasdaq.com/market-activity/stocks/{settings["SYM"].lower()}/after-hours'
        self.nasdaqUrl_PreMarket = f'https://www.nasdaq.com/market-activity/stocks/{settings["SYM"].lower()}/pre-market'
        self.nasdaqUrl_News = f'https://www.nasdaq.com/market-activity/stocks/{settings["SYM"].lower()}/news-headlines'
        self.nasdaqUrl_PressReleases = f'https://www.nasdaq.com/market-activity/stocks/{settings["SYM"].lower()}/press-releases'
        self.nasdaqUrl_HistoriCalQuotes = f'https://www.nasdaq.com/market-activity/stocks/{settings["SYM"].lower()}/historical'

        self.nasdaqRealTimeBrowser = 0 
        self.nasdaqAfterHoursBrowser = 0 
        self.nasdaqPreMarketBrowser = 0 
        self.nasdaqKeyDataBrowser = 0 
        self.nasdaqNewsBrowser = 0 
        self.nasdaqPressReleasesBrowser = 0 
        self.nasdaqPEGBrowser = 0 
        self.allBrowsers = 0

        self.display = Display(visible=0, size=(2000, 2000))
        self.display.start()

        self.remote = remote
        self.verbose = verbose

    def update(self, settings):
        self.requestedData = settings 
        
    def run(self):
        data = {}
        if "RT" in self.requestedData.keys():
            self._init_browser("RealTime")
            if self.requestedData["RT"] == "RealTime":
                data["RT"] = self._getRealTimePrice()
            self._close_browser("RealTime")

        if "RT" in self.requestedData.keys():
            self._init_browser("AfterHours")
            if self.requestedData["RT"] == "AfterHours":
                data["RT"] = self._getAfterHoursPrice()
            self._close_browser("AfterHours")

        if "RT" in self.requestedData.keys():
            self._init_browser("PreMarket")
            if self.requestedData["RT"] == "PreMarket":
                data["RT"] = self._getPreMarketPrice()
            self._close_browser("PreMarket")

        if "KD" in self.requestedData.keys():
            self._init_browser("KeyData")
            data["KD"] = self._getKeyData()
            self._close_browser("KeyData")

        if "NWS" in self.requestedData.keys():
            self._init_browser("News")
            data["NWS"] = self._getNews()
            self._close_browser("News")

        if "PR" in self.requestedData.keys():
            self._init_browser("PressReleases")
            data["PR"] = self._getPressReleases()
            self._close_browser("PressReleases")


        return data

    def _init_browser(self, names):
        if "KeyData" in names :
            self.allBrowsers += 1
            if self.remote == True:
                self.nasdaqKeyDataBrowser = webdriver.Remote(command_executor="http://0.0.0.0:4444/wd/hub", desired_capabilities=DesiredCapabilities().FIREFOX)
            else: 
                self.nasdaqKeyDataBrowser = webdriver.Firefox()
            if not self.nasdaqKeyDataBrowser.current_url == self.nasdaqUrl_KeyData:
                self.nasdaqKeyDataBrowser.get(self.nasdaqUrl_KeyData)
                self.nasdaqKeyDataBrowser.execute_script("window.scrollTo(0, 750)") 
                time.sleep(1.25)
                self.nasdaqKeyDataBrowser.find_element_by_id("_evidon-accept-button").click()

        elif "RealTime" in names:
            self.allBrowsers += 1
            if self.remote == True:
                self.nasdaqRealTimeBrowser = webdriver.Remote(command_executor="http://0.0.0.0:4444/wd/hub", desired_capabilities=DesiredCapabilities().FIREFOX)
            else: 
                self.nasdaqRealTimeBrowser = webdriver.Firefox()
            if not self.nasdaqRealTimeBrowser.current_url == self.nasdaqUrl_RealTime:
                self.nasdaqRealTimeBrowser.get(self.nasdaqUrl_RealTime)
                self.nasdaqRealTimeBrowser.execute_script("window.scrollTo(0, 750)") 
                time.sleep(1.25)
                self.nasdaqRealTimeBrowser.find_element_by_id("_evidon-accept-button").click()

        elif "AfterHours" in names:
            self.allBrowsers += 1
            if self.remote == True:
                self.nasdaqAfterHoursBrowser = webdriver.Remote(command_executor="http://0.0.0.0:4444/wd/hub", desired_capabilities=DesiredCapabilities().FIREFOX)
            else: 
                self.nasdaqAfterHoursBrowser = webdriver.Firefox()
            if not self.nasdaqAfterHoursBrowser.current_url == self.nasdaqUrl_AfterHours:
                self.nasdaqAfterHoursBrowser.get(self.nasdaqUrl_AfterHours)
                self.nasdaqAfterHoursBrowser.execute_script("window.scrollTo(0, 750)") 
                time.sleep(1.25)
                self.nasdaqAfterHoursBrowser.find_element_by_id("_evidon-accept-button").click()

        elif "PreMarket" in names:
            self.allBrowsers += 1
            if self.remote == True:
                self.nasdaqPreMarketBrowser = webdriver.Remote(command_executor="http://0.0.0.0:4444/wd/hub", desired_capabilities=DesiredCapabilities().FIREFOX)
            else: 
                self.nasdaqPreMarketBrowser = webdriver.Firefox()
            if not self.nasdaqPreMarketBrowser.current_url == self.nasdaqUrl_PreMarket:
                self.nasdaqPreMarketBrowser.get(self.nasdaqUrl_PreMarket)
                self.nasdaqPreMarketBrowser.execute_script("window.scrollTo(0, 750)") 
                time.sleep(1.25)
                self.nasdaqPreMarketBrowser.find_element_by_id("_evidon-accept-button").click()

        elif "News" in names:
            self.allBrowsers += 1
            if self.remote == True:
                self.nasdaqNewsBrowser = webdriver.Remote(command_executor="http://0.0.0.0:4444/wd/hub", desired_capabilities=DesiredCapabilities().FIREFOX)
            else: 
                self.nasdaqNewsBrowser = webdriver.Firefox()
            if not self.nasdaqNewsBrowser.current_url == self.nasdaqUrl_News:
                self.nasdaqNewsBrowser.get(self.nasdaqUrl_News)
                self.nasdaqNewsBrowser.execute_script("window.scrollTo(0, 750)") 
                time.sleep(1.25)
                self.nasdaqNewsBrowser.find_element_by_id("_evidon-accept-button").click()
                

        elif "PressReleases" in names:
            self.allBrowsers += 1
            if self.remote == True:
                self.nasdaqPressReleasesBrowser = webdriver.Remote(command_executor="http://0.0.0.0:4444/wd/hub", desired_capabilities=DesiredCapabilities().FIREFOX)
            else: 
                self.nasdaqPressReleasesBrowser = webdriver.Firefox()
            if not self.nasdaqPressReleasesBrowser.current_url == self.nasdaqUrl_PressReleases:
                self.nasdaqPressReleasesBrowser.get(self.nasdaqUrl_PressReleases)
                self.nasdaqPressReleasesBrowser.execute_script("window.scrollTo(0, 750)") 
                time.sleep(1.25)
                self.nasdaqPressReleasesBrowser.find_element_by_id("_evidon-accept-button").click()

    def _close_browser(self, name):
        if name == "KeyData":
            self.allBrowsers -= 1 
            self.nasdaqKeyDataBrowser.close()

        elif name == "RealTime":
            self.allBrowsers -= 1 
            self.nasdaqRealTimeBrowser.close()

        elif name == "AfterHours":
            self.allBrowsers -= 1 
            self.nasdaqAfterHoursBrowser.close()

        elif name == "PreMarket":
            self.allBrowsers -= 1 
            self.nasdaqPreMarketBrowser.close()

        elif name == "News":
            self.allBrowsers -= 1 
            self.nasdaqNewsBrowser.close()

        elif name == "PressReleases":
            self.allBrowsers -= 1 
            self.nasdaqPressReleasesBrowser.close()
        
        if self.allBrowsers == 0:
            self.display.stop()


    def _getRealTimePrice(self):
        if self.nasdaqRealTimeBrowser != 0:
            transaction_time = self.nasdaqRealTimeBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/div[2]/table/tbody/tr[1]/td[1]")[0].text
            transaction_price = self.nasdaqRealTimeBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/div[2]/table/tbody/tr[1]/td[2]")[0].text
            transaction_volume = self.nasdaqRealTimeBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/div[2]/table/tbody/tr[2]/td[3]")[0].text
            return {"Time": transaction_time, "Price": transaction_price, "Volume": transaction_volume}
        else:
            print("Please init the borwser with the function self.init_browser('RealTime')")
            return "Error" 

    def _getAfterHoursPrice(self):
        if self.nasdaqAfterHoursBrowser != 0:          
            transaction_time = self.nasdaqAfterHoursBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[2]")[0].text
            transaction_price = self.nasdaqAfterHoursBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/div[2]/table/tbody/tr[1]/td[2]")[0].text
            transaction_volume = self.nasdaqAfterHoursBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/div[2]/table/tbody/tr[2]/td[3]")[0].text       
            return {"Time": transaction_time, "Price": transaction_price, "Volume": transaction_volume}
        else:
            print("Please init the borwser with the function self.init_browser('AfterHours')")
            return "Error" 

    def _getPreMarketPrice(self):
        if self.nasdaqPreMarketBrowser != 0:    
            transaction_time = self.nasdaqPreMarketBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[2]")[0].text
            transaction_price = self.nasdaqPreMarketBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[2]")[0].text
            transaction_volume = self.nasdaqPreMarketBrowser.find_elements_by_xpath("/html/body/div[3]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr[1]/td[3]")[0].text
            return {"Time": transaction_time, "Price": transaction_price, "Volume": transaction_volume}
        else:
            print("Please init the borwser with the function self.init_browser('PreMarket')")
            return "Error" 

    def _getKeyData(self):
        if self.nasdaqKeyDataBrowser != 0:    
            Exchange = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(1) > td:nth-child(2)").text
            Sector = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(2) > td:nth-child(2)").text
            Industry = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(3) > td:nth-child(2)").text
            YrTarget = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(4) > td:nth-child(2)").text
            TDHL = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(5) > td:nth-child(2)").text
            ShareVolume = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(6) > td:nth-child(2)").text
            AverageVolumeLabel = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(7) > td:nth-child(2)").text
            PreviousClose = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(8) > td:nth-child(2)").text
            FTWeekHL = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(2) > tr:nth-child(9) > td:nth-child(2)").text

            MarketCap = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(3) > tr:nth-child(1) > td:nth-child(2)").text
            ForwardPEYR = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(3) > tr:nth-child(2) > td:nth-child(2)").text
            EPS = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(3) > tr:nth-child(3) > td:nth-child(2)").text
            AnnualizedDividend = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(3) > tr:nth-child(4) > td:nth-child(2)").text
            ExDividendRate = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(3) > tr:nth-child(5) > td:nth-child(2)").text
            DividendPayDate = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(3) > tr:nth-child(6) > td:nth-child(2)").text
            CurrectYield = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(3) > tr:nth-child(7) > td:nth-child(2)").text
            Beta = self.nasdaqKeyDataBrowser.find_element_by_css_selector("tbody.summary-data__table-body:nth-child(3) > tr:nth-child(8) > td:nth-child(2)").text

            return {"Exchange": Exchange,"Sector": Sector,"Industry": Industry,"1 Year Target": YrTarget,"Today's High/Low": TDHL,"Share Volume": ShareVolume,"Average Volume Label": AverageVolumeLabel,"Previous Close": PreviousClose,"52 Week High/Low": FTWeekHL,"Market Cap": MarketCap,"Forward P/E 1 Yr.": ForwardPEYR,"Earnings Per Share": EPS,"Annualized Dividend": AnnualizedDividend,"Ex Dividend Rate": ExDividendRate,"Dividend Pay Date": DividendPayDate,"Currect Yield": CurrectYield,"Beta": Beta}
        else:
            print("Please init the borwser with the function self.init_browser('KeyData')")
            return "Error" 

    def _getNews(self):
        if self.nasdaqNewsBrowser != 0:    
            data = {"Title": [],"Elapsed Time": [],"Published Date":[], "Link": [], "Content":[]}
            page = 2

            for i in range(int(self.requestedData['NWS'])):
                try:
                    NewsTitle =  WebDriverWait(self.nasdaqNewsBrowser,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,f"li.quote-news-headlines__item:nth-child({i%8+1}) > a:nth-child(1) > p:nth-child(2) > span:nth-child(1)"))).text
                    ElapsedTime =  WebDriverWait(self.nasdaqNewsBrowser,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,f"li.quote-news-headlines__item:nth-child({i%8+1}) > a:nth-child(1) > span:nth-child(1)"))).text
                    Link =  WebDriverWait(self.nasdaqNewsBrowser,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,f"li.quote-news-headlines__item:nth-child({i%8+1}) > a:nth-child(1)"))).get_attribute("href")

                    # NewsTitle = self.nasdaqNewsBrowser.find_element_by_css_selector(f"li.quote-news-headlines__item:nth-child({i%8+1}) > a:nth-child(1) > p:nth-child(2) > span:nth-child(1)").text
                    # ElapsedTime = self.nasdaqNewsBrowser.find_element_by_css_selector(f"li.quote-news-headlines__item:nth-child({i%8+1}) > a:nth-child(1) > span:nth-child(1)").text
                    # Link = self.nasdaqNewsBrowser.find_element_by_css_selector(f"li.quote-news-headlines__item:nth-child({i%8+1}) > a:nth-child(1)").get_attribute("href")
        
                    # response = requests.get(Link, headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'})
                    # Time, ContentSTR = self._get_News_Content(response.text, i)

                    data["Title"].append(NewsTitle)
                    data["Elapsed Time"].append(ElapsedTime)
                    # data["Published Date"].append(Time)
                    data["Link"].append(Link)
                    # data["Content"].append(ContentSTR)
                except:
                    pass
                
                if i%8 == 0 and i!=0:
                    try:
                        WebDriverWait(self.nasdaqNewsBrowser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f".pagination__next"))).click()
                        # WebDriverWait(self.nasdaqNewsBrowser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"button.pagination__page:nth-child({page})"))).click()
                        if self.verbose:
                            print(f"Page change to: {page}, {self.requestedData['SYM']}")
                        else:
                            open("nasdaq_data_logs.txt", "w+").write(f"Page change to: {page}, {self.requestedData['SYM']}")
                        page += 1
                        time.sleep(0.75)
                    except Exception as e:
                        print(f"Error: {e}")
                        print("Error turning page!")
                        return data

            return data
        else:
            print("Please init the borwser with the function self.init_browser('News')")
            return "Error" 

    def _get_News_Content(self, text, articles):
        soup = BeautifulSoup(text, 'html.parser')
        j = 1; Content = []
        Time = soup.find_all("time", class_="timestamp__date")[0].text
        while True:
            try:
                Content.append(soup.select_one(f"div.body__content>p:nth-child({j})").text)
                j+=1
            except:
                print(f"Done article: {articles}, paragraphs: {j}")
                Content.append("END")
                break
        return  Time, ''.join(Content)

    def _getPressReleases(self):
        if self.nasdaqPressReleasesBrowser != 0:    
            data = {"Title": [],"Elapsed Time": [],"Link": []}
            if self.requestedData['PR'] > 4:
                self.requestedData['PR'] = 4

            for i in range(1,self.requestedData['PR']+1):
                NewsTitle = self.nasdaqPressReleasesBrowser.find_elements_by_xpath(f"/html/body/div[2]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[1]/div[{i}]/div/div[2]/h3/a/span")[0].text
                ElapsedTime = self.nasdaqPressReleasesBrowser.find_elements_by_xpath(f"/html/body/div[2]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[1]/div[1]/div/div[{i}]/div[2]")[0].text
                Link = self.nasdaqPressReleasesBrowser.find_elements_by_xpath(f"/html/body/div[2]/div/main/div/div[5]/div[2]/div/div[1]/div/div[1]/div[1]/div[{i}]/div/div[2]/h3/a")[0].get_attribute("href")
                data["Title"].append(NewsTitle)
                data["Elapsed Time"].append(ElapsedTime)
                data["Link"].append(Link)
            return data
        else:
            print("Please init the borwser with the function self.init_browser('PressReleases')")
            return "Error" 
