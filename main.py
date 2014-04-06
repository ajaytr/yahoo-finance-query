import datetime
from yfquery import YFQuery         
    
    
if __name__ == "__main__":
    now = datetime.datetime.now()
    print ("Running at time: " + str(now) + "\n")
    
    stockList = ["CRM", "WAGE", "YELP", "WDAY"]
    
    query = YFQuery(stockList)
    query.acquireAllData()
    query.dumpDataTable()