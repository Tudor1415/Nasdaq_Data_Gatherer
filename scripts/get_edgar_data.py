import json
import os
import re

import requests
from bs4 import BeautifulSoup, SoupStrainer

# symbols = ['CERN', 'FOXA', 'MU', 'AAPL', 'ADBE', 'ADI', 'ADP', 'ADSK', 'ALGN', 'ALXN', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'ANSS', 'ASML', 'ATVI', 'AVGO', 'BIDU', 'BIIB', 'BKNG', 'BMRN', 'CDNS', 'CDW', 'CHKP', 'CHTR', 'CMCSA', 'COST', 'CPRT', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTSH', 'CTXS', 'DLTR', 'DXCM', 'EA', 'EBAY', 'EXC', 'EXPE', 'FAST', 'FB', 'FISV', 'FOX', 'GILD', 'GOOG', 'GOOGL', 'IDXX', 'ILMN', 'INCY', 'INTC', 'INTU', 'ISRG', 'JD', 'KHC', 'KLAC', 'LBTYA', 'LBTYK', 'LRCX', 'LULU', 'MAR', 'MCHP', 'MDLZ', 'MELI', 'MNST', 'MSFT', 'MXIM', 'NFLX', 'NTAP', 'NTES', 'NVDA', 'NXPI', 'ORLY', 'PAYX', 'PCAR', 'PEP', 'PYPL', 'QCOM', 'REGN', 'ROST', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'SPLK', 'SWKS', 'TCOM', 'TMUS', 'TSLA', 'TTWO', 'TXN', 'UAL', 'ULTA', 'VRSK', 'VRSN', 'VRTX', 'WBA', 'WDAY', 'WDC', 'XEL', 'XLNX', 'ZM']
# ids = json.loads(open("../DATA/symbol_edgar_id.json", "r+").read())

def get_edgar_8k_items(url):
    """
    This function returns a list of all the 8-K items, date and document link for an 8-K document given its url
    """
    response = requests.get("https://www.sec.gov/"+url)
    if response.status_code == 200:                                                                                                                                                                 
        soup = BeautifulSoup(response.text,'html.parser')
        info = soup.find_all("div", {"class":"info"})
        date = info[3].text
        items = re.findall(r"Item\s\d.\d*", info[4].text)
        documentLink = soup.find_all("td", {"scope":"row"})[2].select_one("a")["href"]
        
    return date, items, documentLink

def get_edgar_8k_data(id):
    """
    This function returns a list of all the 8-K documents for a company given its CIK
    """
    return_dict = {"Date":[], "Items":[], "documentLink":[]}
    i = 1; page = 0; urls = [] 

    while i>0:
        if page < 1:
            link = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000{id}&type=8-K&dateb=&owner=exclude&count=40" 
        else:
            link = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000{id}&type=8-K&dateb=&owner=exclude&start={page*40}&count=40"
        response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'})
        if response.status_code == 200:                                                                                                                                                          
            soup = BeautifulSoup(response.text,'html.parser')
    
            # Fetches all the documents urls
            for url in soup.find_all('a'):
                if url.has_attr('href') and f"/Archives/edgar/data/{id}" in url['href']:
                    urls.append(url['href'])
            i-=1

            if soup.find("input", {"value":"Next 40"}):
                print(f"Next, page {page}!")
                i+=1; page+=1
        else:
            print(f"Error code: {response.status_code}")

    for url in urls:
        date, items, documentLink = get_edgar_8k_items(url)
        return_dict["Date"].append(date)
        return_dict["Items"].append(items)
        return_dict["documentLink"].append(documentLink)

    return return_dict


# print(get_edgar_8k_data("320193"))    

def get_balance_sheet_table(table):
    trs = table.find_all("tr")
    object_list = [] # List of all the objects in a table
    column_list = ["Cash and cash equivalents",
                   "Marketable securities",
                   "Inventories",
                   "Total assets",
                   "Total liabilities"] # List of all the desired columns

    # Getting all the objects in the table
    for tr in trs:
        for td in tr.find_all("td")[:-2]:
            font = td.select_one("div > font")
            if font:
                object_list.append(font.text)

    object_list = object_list[object_list.index('Cash and cash equivalents'):]
    number_list = re.findall(r"\d+,\d+", "".join(object_list).replace(u'\xa0',' ')) # List of all the numbers in the object_list
    category_list = re.findall(r"([A-Z][^$0-9,:]+)", "".join(object_list).replace(u'\xa0',' ')) # List of all the categories in he table
    unwanted_category_list = [i.replace(":","") for i in re.findall(r"([A-Z][^$0-9,]+:)", "".join(object_list).replace(u'\xa0',' '))]
    
    category_list = [i for i in category_list if not i in unwanted_category_list]

    for i in column_list:
        print(number_list[category_list.index(i)])

    return False

def get_edgar_10q_content(documentUrl):
    """
    This function returns a list of all the 8-K items, date and document link for an 8-K document given its url
    """
    response = requests.get("https://www.sec.gov"+documentUrl)
    balanceSheet = response.text.split("BALANCE SHEETS")[1].split("</table>")[0] + "</table>"
    cashFlow = response.text.split("CASH FLOW")[1].split("</table>")[0] + "</table>"

    if response.status_code == 200:  
        balanceSheetSoup = BeautifulSoup(balanceSheet,'html.parser')  
        cashFlowSoup = BeautifulSoup(cashFlow,'html.parser')

        balanceSheetTable = balanceSheetSoup.findAll("table")[0]
        cashFlowTable = cashFlowSoup.findAll("table")[0]

        get_balance_sheet_table(balanceSheetTable)




# print(get_edgar_10q_content("/Archives/edgar/data/320193/000032019319000010/a10-qq1201912292018.htm"))

def get_edgar_10q_items(url):
    """
    This function returns a list of all the 8-K items, date and document link for an 8-K document given its url
    """
    response = requests.get("https://www.sec.gov"+url)
    if response.status_code == 200:                                                                                                                                                                 
        soup = BeautifulSoup(response.text,'html.parser')
        info = soup.find_all("div", {"class":"info"})
        date = info[3].text
        documentLinks = soup.find_all("td", {"scope":"row"})[2].find_all("a")
        for i in documentLinks:
            if f"Archivesedgardata" == "".join(i["href"].split("/")[1:4]):
                return date, i["href"]
            else:
                return False, False


# print(get_edgar_10q_items("/Archives/edgar/data/320193/000091205700023442/"))
def get_edgar_10q_data(id):
    """
    This function returns a list of all the 8-K documents for a company given its CIK
    """
    return_dict = {"Date":[], "documentLink":[]}
    i = 1; page = 0; urls = [] 

    while i>0:
        if page < 1:
            link = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000{id}&type=10-Q&dateb=&owner=exclude&count=40" 
        else:
            link = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000{id}&type=10-Q&dateb=&owner=exclude&start={page*40}&count=40"
        response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'})
        if response.status_code == 200:                                                                                                                                                          
            soup = BeautifulSoup(response.text,'html.parser')
    
            # Fetches all the documents urls
            for url in soup.find_all('a'):
                if url.has_attr('href') and f"Archivesedgardata{id}" == "".join(url['href'].split("/")[1:5]):
                    urls.append(url['href'])
            i-=1

            if soup.find("input", {"value":"Next 40"}):
                print(f"Next, page {page}!")
                i+=1; page+=1
        else:
            print(f"Error code: {response.status_code}")

    for i, url in enumerate(urls):
        date, documentLink = get_edgar_10q_items(url)
        if date and documentLink:
            return_dict["Date"].append(date)
            return_dict["documentLink"].append(documentLink)
            print(f"Done document {i}")

    return return_dict

# print(get_edgar_10q_data("320193"))
# https://www.sec.gov/cgi-bin/browse-edgar?CIK=AAPL&Find=Search&owner=exclude&action=getcompany
# https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1754301&type=8-K&dateb=&owner=exclude&count=100
# https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=8-K%25&dateb=&owner=exclude&start=100&count=100
