## Problem definition
The problem we seek to solve in this repository is the existance of the predictive nature of the stock market.
And if, with the gathered data we can achive staisfying results in the prediction of the general trend of the market.

## Usage instructions
The virtual env is in venv
Before you start add the gekodriver to path: export PATH=$PATH:/media/tudor/"Dtata Archive"/"trading bot"/gekodriver
export PATH=$PATH:/media/tudor/Dtata Archive/Python_Projects/NSDQAPI/gekodriver"
To strat trhe guinnicorn server pls use the following command: **gunicorn --reload api** in the current directory

## Driver initialisation
First you need to download a selenium standalone server and run it using the following command:
 - **java -jar selenium-server-standalone-3.141.0.jar -role hub**

then you need to create a node using the folowing comand:
 - **java -Dwebdriver.firefox.driver=/media/tudor/"Dtata Archive"/Python_Projects/NSDQAPI/gekodriver -jar /media/tudor/"Dtata Archive"/Python_Projects/NSDQAPI/selenium-server-standalone-3.141.0.jar -role node -hub http://172.17.0.1:4444/grid/register/**
 
or, more generally:
 - **java -Dwebdriver.firefox.driver=gekodriver_path -jar jar_server_path -role node -hub jar_server_url**

## Docker server
If you prefer to run a docker server instead, run the following command:
 - **sudo docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-firefox:3.141.59-20200525**

It will download the needed server and automatically set it up for you

## Possible API's
- AlphaVantge
- NewsAPI (free version)
https://newsapi.org/v2/everything?q=apple&from=2020-05-12&to=2020-06-11&sortBy=popularity&apiKey=08bff187ca1b44c4b8974614952439b2

## Posible datasets:
- Reuters corpus v1
``` python
    from sklearn.datasets import fetch_rcv1
    rcv1 = fetch_rcv1()
```
- Reuters-21578 Text Categorization Collection :
https://kdd.ics.uci.edu/databases/reuters21578/reuters21578.html
https://www.kaggle.com/nltkdata/reuters

## API:

    - Get historical data: symbol, datefrom, dateto, country
    returns open, high, low, close, volume
    
    - Get news articles: symbol, no of articles, datefrom, dateto
    returns: News title, link, date, content

    - Get balance sheet: symbol, datefrom, dateto
    returns: 
        - date 
        - symbol 
        - fillingDate 
        - acceptedDate 
        - period 
        - cashAndCashEquivalents 
        - shortTermInvestments 
        - cashAndShortTermInvestments 
        - netReceivables 
        - inventory 
        - otherCurrentAssets 
        - totalCurrentAssets 
        - propertyPlantEquipmentNet 
        - goodwill 
        - intangibleAssets 
        - goodwillAndIntangibleAssets 
        - longTermInvestments 
        - taxAssets 
        - otherNonCurrentAssets 
        - totalNonCurrentAssets 
        - otherAssets 
        - totalAssets 
        - accountPayables 
        - shortTermDebt 
        - taxPayables 
        - deferredRevenue 
        - otherCurrentLiabilities 
        - totalCurrentLiabilities 
        - longTermDebt 
        - deferredRevenueNonCurrent 
        - deferredTaxLiabilitiesNonCurrent 
        - otherNonCurrentLiabilities 
        - totalNonCurrentLiabilities 
        - otherLiabilities 
        - totalLiabilities 
        - commonStock 
        - retainedEarnings 
        - accumulatedOtherComprehensiveIncomeLoss 
        - othertotalStockholdersEquity 
        - totalStockholdersEquity 
        - totalLiabilitiesAndStockholdersEquity 
        - totalInvestments 
        - totalDebt 
        - netDebt 
        - link 
        - finalLink

    - Get cash flow: symbol, datefrom, dateto
    returns:
        - date
        - symbol
        - fillingDate
        - acceptedDate
        - period
        - netIncome
        - depreciationAndAmortization
        - deferredIncomeTax
        - stockBasedCompensation
        - changeInWorkingCapital
        - accountsReceivables
        - inventory
        - accountsPayables
        - otherWorkingCapital
        - otherNonCashItems
        - netCashProvidedByOperatingActivities
        - investmentsInPropertyPlantAndEquipment
        - acquisitionsNet
        - purchasesOfInvestments
        - salesMaturitiesOfInvestments
        - otherInvestingActivites
        - netCashUsedForInvestingActivites
        - debtRepayment
        - commonStockIssued
        - commonStockRepurchased
        - dividendsPaid
        - otherFinancingActivites
        - netCashUsedProvidedByFinancingActivities
        - effectOfForexChangesOnCash
        - netChangeInCash
        - cashAtEndOfPeriod
        - cashAtBeginningOfPeriod
        - operatingCashFlow
        - capitalExpenditure
        - freeCashFlow
        - link
        - finalLink

    - Get institutional holders detailed profile: symbol, no
    returns: Name,Description,NoSharesTrillions,KeyPeople

    - Get income statement quarterly: symbol, datefrom, dateto
    returns:
        - date
        - symbol
        - fillingDate
        - acceptedDate
        - period
        - revenue
        - costOfRevenue
        - grossProfit
        - grossProfitRatio
        - researchAndDevelopmentExpenses
        - generalAndAdministrativeExpenses
        - sellingAndMarketingExpenses
        - otherExpenses
        - operatingExpenses
        - costAndExpenses
        - interestExpense
        - depreciationAndAmortization
        - ebitda
        - ebitdaratio
        - operatingIncome
        - operatingIncomeRatio
        - totalOtherIncomeExpensesNet
        - incomeBeforeTax
        - incomeBeforeTaxRatio
        - incomeTaxExpense
        - netIncome
        - netIncomeRatio
        - eps
        - epsdiluted
        - weightedAverageShsOut
        - weightedAverageShsOutDil
        - link
        - finalLink

    - Get institutional holders basic profile: symbol
    returns:
        - SharesOutstandingPCT
        - ShareoutstandingTotal
        - TotalHoldingsValue
        - ActivePositions
        - Holders
        - Shares
        - OWNER_NAME
        - DATE
        - SHARES_HELD
        - CHANGE(Shares)
        - CHANGE(%)
        - MARKET_VALUE

    - Get major holders information: symbol
    returns: 
        - % of Shares Held by All Insider
        - % of Shares Held by Institutions
        - % of Float Held by Institutions
        - Number of Institutions Holding Shares

    - Get company profile: symbol
    returns:
        - ModuleTitle
        - CompanyName
        - Symbol
        - Address
        - Phone
        - Industry
        - Sector
        - Region
        - CompanyDescription
        - KeyExecutives:
            - name
            - title
        - Number of employees
        - Subsidiaries

    - Get company summary: symbol
    returns:
        - Exchange
        - Sector
        - Industry
        - OneYrTarget
        - TodayHighLow
        - ShareVolume
        - AverageVolume
        - PreviousClose
        - FiftTwoWeekHighLow
        - MarketCap
        - PERatio
        - ForwardPE1Yr
        - EarningsPerShare
        - AnnualizedDividend
        - ExDividendDate
        - DividendPaymentDate
        - Yield

    - Get company sustainability: symbol
    returns:
        - palmOil
        - controversialWeapons
        - gambling
        - socialScore
        - nuclear
        - furLeather
        - alcoholic
        - gmo
        - catholic
        - socialPercentile
        - peerCount
        - governanceScore
        - environmentPercentile
        - animalTesting
        - tobacco
        - totalEsg
        - highestControversy
        - esgPerformance
        - coal
        - pesticides
        - adult
        - percentile
        - peerGroup
        - smallArms
        - environmentScore
        - governancePercentile
        - militaryContract
    
    - Get company recomandations: symbol, datefrom, dateto
    returns: Firm, ToGrade, FromGrade, Action

    - Get yahoo earnings estimates: symbol
    returns: No. of Analysts, Avg. Estimate, Low Estimate, High Estimate, Year Ago EPS

    - Get yahoo growth estimates: symbol
    returns: Current Estimate, 7 Days Ago, 30 Days Ago, 60 Days Ago, 90 Days Ago

    - Get yahoo revenue estimates: symbol
    returns: No. of Analysts, Avg. Estimate, Low Estimate, High Estimate, Year Ago Sales

    - Get yahoo risk estimate: symbol
    returns: Total ESG Risk score, Environment Risk Score, Social Risk Score, Governance Risk Score, Controversy Level (out of 5)

    - Get edgar 8-K data: symbol or CIK
    returns:
    - DocumentDate
    - Items
    - Document_url

    For more information  on the meaning of each item numbr, please consult this page: https://www.sec.gov/fast-answers/answersform8khtm.html


## Interesting papers:
https://pabloazar.com/
http://ceur-ws.org/Vol-862/FEOSWp4.pdf

## Potentially helpful projects

### PyTeaser
https://github.com/xiaoxu193/PyTeaser


PyTeaser takes any news article and extract a brief summary from it. It's based on the original Scala project.

Summaries are created by ranking sentences in a news article according to how relevant they are to the entire text. The top 5 sentences are used to form a "summary". Each sentence is ranked by using four criteria:

    Relevance to the title
    Relevance to keywords in the article
    Position of the sentence
    Length of the sentence

### Newspaper3k
https://github.com/codelucas/newspaper

Newspaper can extract and detect languages seamlessly. If no language is specified, Newspaper will attempt to auto detect a language.

```python
>>> from newspaper import Article

>>> url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
>>> article = Article(url)
>>> article.download()

>>> article.html
'<!DOCTYPE HTML><html itemscope itemtype="http://...'
>>> article.parse()

>>> article.authors
['Leigh Ann Caldwell', 'John Honway']

>>> article.publish_date
datetime.datetime(2013, 12, 30, 0, 0)

>>> article.text
'Washington (CNN) -- Not everyone subscribes to a New Year's resolution...'

>>> article.top_image
'http://someCDN.com/blah/blah/blah/file.png'

>>> article.movies
['http://youtube.com/path/to/link.com', ...]
```

Online demo:
http://newspaper-demo.herokuapp.com/

## Notebooks
The notebooks provide a simple insights and explorations of the relationships betwen the data.