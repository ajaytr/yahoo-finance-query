from datetime import datetime
import urllib.request
import simplejson as json
from prettytable import PrettyTable

def getAnalystEstimates(stockTicker):
    """
    Form a Yahoo Finance Query for Analyst Estimates data in the REST format
    """
    
    url = "http://query.yahooapis.com/v1/public/yql?q=SELECT%20*%20FROM%20yahoo.finance.analystestimate%20WHERE%20symbol%3D'{0}'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=".format(stockTicker)
    req = urllib.request.Request(url)
    data = json.loads(urllib.request.urlopen(req).read())
    return data["query"]["results"]["results"]


def getKeyStatistics(stockTicker):
    """
    Form a Yahoo Finance Query for Key Statistics data in the REST format
    """

    url = "http://query.yahooapis.com/v1/public/yql?q=SELECT%20*%20FROM%20yahoo.finance.keystats%20WHERE%20symbol%3D'{0}'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=".format(stockTicker)
    req = urllib.request.Request(url)
    data = json.loads(urllib.request.urlopen(req).read())
    return data["query"]["results"]["stats"]
    

def getQuoteData(stockTicker):
    """
    Form a Yahoo Finance Query for Quote data in the REST format
    """
    
    url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quote%20where%20symbol%3D'{0}'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=".format(stockTicker)
    req = urllib.request.Request(url)
    data = json.loads(urllib.request.urlopen(req).read())
    return data["query"]["results"]["quote"]


def convertToFloat(strNum):
    """
    Some Yahoo Finance numbers end with B or M.  Convert to the appropriate
    floating pt value
    """
    
    if strNum.endswith('B'):
        return float(strNum[:-1]) * 1000000000
    elif strNum.endswith('M'):
        return float(strNum[:-1]) * 1000000
    else:
        return float(strNum)
        

def acquireData(stockTicker):
    """
    Wrapper function for all the other data aquisition functions
    """
    
    # print("Acquiring data for: ", stockTicker)
    
    # Get Analyst Estimates
    est = getAnalystEstimates(stockTicker)
    # print(json.dumps(estimates, sort_keys=True, indent=4 * ' '))

    # Get Key Statistics
    stats = getKeyStatistics(stockTicker)
    # print(json.dumps(statistics, sort_keys=True, indent=4 * ' '))
    
    # Get Quote Data
    quote = getQuoteData(stockTicker)
    # print(json.dumps(quote, sort_keys=True, indent=4 * ' '))
    
    return est, stats, quote
    
 
def dumpDataTable(resultList):
    """
    Dump data into a PrettyTable
    """
    
    table = PrettyTable([
         "Ticker", 
         "Closing Price", 
         "Market Cap (B)", 
         "P/E", 
         "Fwd P/E", 
         "P/S", 
         "Fwd P/S", 
         "ROA", 
         "ROE"
    ])
    table.align["Ticker"] = "l"
    
    for stock in resultList:
        table.add_row([
            stock["Ticker"], 
            stock["ClosingPrice"], 
            "{0:.2f}".format(stock["MarketCap"] / 1000000000), 
            "{0:.2f}".format(stock["CurrentPE"]),
            "{0:.2f}".format(stock["ForwardPE"]),
            "{0:.2f}".format(stock["CurrentPS"]),
            "{0:.2f}".format(stock["ForwardPS"]),
            stock["ROA"],
            stock["ROE"]
        ])    
    print(table)
    
    
if __name__ == "__main__":
    now = datetime.now()
    print ("Running at time: " + str(now) + "\n")
    
    stockList = ["CRM", "WAGE", "YELP", "WDAY"]
    resultList = []
    for ticker in stockList:
        estimates, statistics, quote = acquireData(ticker)        
        stock = {
            'Ticker'        : quote["symbol"],
            'ClosingPrice'  : float(quote["LastTradePriceOnly"]),
            'MarketCap'     : float(statistics["MarketCap"]["content"]),
            'CurrentPE'     : float(quote["LastTradePriceOnly"]) / float(estimates["EarningsEst"]["AvgEstimate"]["CurrentYear"]),
            'ForwardPE'     : float(quote["LastTradePriceOnly"]) / float(estimates["EarningsEst"]["AvgEstimate"]["NextYear"]),
            'CurrentPS'     : float(statistics["MarketCap"]["content"]) / convertToFloat(estimates["RevenueEst"]["AvgEstimate"]["CurrentYear"]),
            'ForwardPS'     : float(statistics["MarketCap"]["content"]) / convertToFloat(estimates["RevenueEst"]["AvgEstimate"]["NextYear"]),
            'ROA'           : statistics["ReturnonAssets"]["content"],
            'ROE'           : statistics["ReturnonEquity"]["content"]
        }
        resultList.append(stock)

    # print(json.dumps(resultList, sort_keys=True, indent=4 * ' '))
    dumpDataTable(resultList)
