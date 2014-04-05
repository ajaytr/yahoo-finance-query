import datetime
# import simplejson as json
import prettytable
import yfquery

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
        

def dumpDataTable(resultList):
    """
    Dump data into a PrettyTable
    """
    
    table = prettytable.PrettyTable([
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
    print(table.get_string(sortby="Ticker"))
 
    
    
if __name__ == "__main__":
    now = datetime.datetime.now()
    print ("Running at time: " + str(now) + "\n")
    
    stockList = ["CRM", "WAGE", "YELP", "WDAY"]
    resultList = []
    for ticker in stockList:
        estimates, statistics, quote = yfquery.acquireData(ticker)        
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
