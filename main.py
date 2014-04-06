import datetime
import argparse
from yfquery import YFQuery         
    
    
if __name__ == "__main__":
    now = datetime.datetime.now()
    print ("Running at time: " + str(now) + "\n")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tickers', nargs='+', help="List of stock tickers", metavar="tickers", required=True)
    parser.add_argument('-v', '--verbose', help="Print debug info", action="store_true")
    args = parser.parse_args()
        
    query = YFQuery(args.tickers, args.verbose)
    query.acquireAllData()
    query.dumpDataTable()