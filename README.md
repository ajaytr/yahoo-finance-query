Simple Python 3 script for querying data from Yahoo finance apis.
Uses: simplejson, prettytable - you must have these installed.

Will retrieve data from Yahoo Finance's Quote page, as well as the Key Statistics page and the Analyst Estimates page


usage: main.py [-h] -t tickers [tickers ...] [-v]

optional arguments:
-h, --help            show this help message and exit
-t tickers [tickers ...], --tickers tickers [tickers ...]
                      List of stock tickers
-v, --verbose         Print debug info
