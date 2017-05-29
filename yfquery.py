import prettytable
import simplejson as json
import requests

class YFQuery:
    YFQUERY_DEBUG = False
    
    def __init__(self, stockTickerList, verbose):
        self.stockTickerList = stockTickerList
        self.resultList = []
        YFQuery.YFQUERY_DEBUG = verbose


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


    def requestQuoteData(self, stockTicker):
        """ Form a Yahoo Finance Query for Quote data in the REST format """

        req_url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22{}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='.format(stockTicker)

        req = requests.Request(method='GET', url=req_url)
        prepared = req.prepare();
        req_session = requests.Session()
        data = req_session.send(prepared)
        jdata = json.loads(data.text)
        print(json.dumps(jdata, sort_keys=True, indent=4 * ' ')) if YFQuery.YFQUERY_DEBUG else 0

        try:
            if "quote" in jdata["query"]["results"]:
                return jdata["query"]["results"]["quote"]
        except:
            print("Problem acquiring Quote Data for", stockTicker)
            return None
    
    
    def acquireAllData(self):
        """ Wrapper function for all the other data aquisition functions """
                
        for ticker in self.stockTickerList:
            print("Acquiring data for: ", ticker) if YFQuery.YFQUERY_DEBUG else 0

            quote = self.requestQuoteData(ticker)
            if None in (quote):
                print("Cannot fetch data for", ticker)
                continue

            stock = {
                'Ticker'        : quote["symbol"],
                'ClosingPrice'  : float(quote["LastTradePriceOnly"]),
                'MarketCap'     : self.__convertToFloat(quote["MarketCapitalization"]),
                'CurrentPE'     : self.__convertToFloat(quote["PERatio"]),
                'ForwardPE'     : self.__convertToFloat(quote["PriceEPSEstimateNextYear"]),
                'CurrentPS'     : self.__convertToFloat(quote["PriceSales"]),
                'ForwardPS'     : 0,
                'ROA'           : 0,
                'ROE'           : 0
            }
            self.resultList.append(stock)
