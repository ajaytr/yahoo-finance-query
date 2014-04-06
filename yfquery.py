import urllib.request
import simplejson as json
import prettytable


class YFQuery:
    YFQUERY_DEBUG = False
    
    def __init__(self, stockTickerList):
        self.stockTickerList = stockTickerList
        self.resultList = []
        
        
    def __fetch(self, url):
        """ Private function to fetch data from given URL """
        req = urllib.request.Request(url)
        data = json.loads(urllib.request.urlopen(req).read())
        print(json.dumps(data, sort_keys=True, indent=4 * ' ')) if YFQuery.YFQUERY_DEBUG else 0
        return data
    
    
    def __convertToFloat(self, strNum):
        """ Some Yahoo Finance numbers end with B or M.  Convert to the
            appropriate floating pt value """
        
        if strNum.endswith('B'):
            return float(strNum[:-1]) * 1000000000
        elif strNum.endswith('M'):
            return float(strNum[:-1]) * 1000000
        else:
            return float(strNum)
    
    
    def dumpDataTable(self):
        """ Dump data into a PrettyTable """
        
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
        
        for stock in self.resultList:
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


    def requestAnalystEstimates(self, stockTicker):
        """ Form a Yahoo Finance Query for Analyst Estimates data in the REST format """
        
        url = "http://query.yahooapis.com/v1/public/yql?q=SELECT%20*%20FROM%20yahoo.finance.analystestimate%20WHERE%20symbol%3D'{0}'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=".format(stockTicker)
        data = self.__fetch(url)
        return data["query"]["results"]["results"]
    
    
    def requestKeyStatistics(self, stockTicker):
        """ Form a Yahoo Finance Query for Key Statistics data in the REST format """
    
        url = "http://query.yahooapis.com/v1/public/yql?q=SELECT%20*%20FROM%20yahoo.finance.keystats%20WHERE%20symbol%3D'{0}'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=".format(stockTicker)
        data = self.__fetch(url)
        return data["query"]["results"]["stats"]


    def requestQuoteData(self, stockTicker):
        """ Form a Yahoo Finance Query for Quote data in the REST format """
        
        url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quote%20where%20symbol%3D'{0}'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=".format(stockTicker)
        data = self.__fetch(url)
        return data["query"]["results"]["quote"]
    
    
    def acquireAllData(self):
        """ Wrapper function for all the other data aquisition functions """
        
        for ticker in self.stockTickerList:
            print("Acquiring data for: ", ticker) if YFQuery.YFQUERY_DEBUG else 0

            estimates = self.requestAnalystEstimates(ticker)
            statistics = self.requestKeyStatistics(ticker)
            quote = self.requestQuoteData(ticker)
                    
            stock = {
                'Ticker'        : quote["symbol"],
                'ClosingPrice'  : float(quote["LastTradePriceOnly"]),
                'MarketCap'     : float(statistics["MarketCap"]["content"]),
                'CurrentPE'     : float(quote["LastTradePriceOnly"]) / float(estimates["EarningsEst"]["AvgEstimate"]["CurrentYear"]),
                'ForwardPE'     : float(quote["LastTradePriceOnly"]) / float(estimates["EarningsEst"]["AvgEstimate"]["NextYear"]),
                'CurrentPS'     : float(statistics["MarketCap"]["content"]) / self.__convertToFloat(estimates["RevenueEst"]["AvgEstimate"]["CurrentYear"]),
                'ForwardPS'     : float(statistics["MarketCap"]["content"]) / self.__convertToFloat(estimates["RevenueEst"]["AvgEstimate"]["NextYear"]),
                'ROA'           : statistics["ReturnonAssets"]["content"],
                'ROE'           : statistics["ReturnonEquity"]["content"]
            }
            self.resultList.append(stock)
