import urllib.request
import simplejson as json

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
