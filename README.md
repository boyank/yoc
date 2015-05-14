# yahoo_options
yahoo_options.py is a command line tool for scraping financial options prices and related data from <a href=http://finance.yahoo.com/q/op>finance.yahoo.com</a>

It's written in Python 2.7.9 and also ported to Python 3.4 using 2to3 tool.

It can be used to scrape current options data for one or more tickers.
There are several ways to supply list of tickers (in order of priority):
-using config.ini file
-as command line arguments
-as user input during script execution.

Sample config.ini is included.

Here is an example how to supply list of tickers as command-line arguments:

C:\>yahoo_options.py googl yhoo

If no command line arguments were supplied, user will be asked to enter one or more tickers separated by comma.

_Enter ticker or tickers, separated by comma:_ googl,yhoo

Downloaded data are stored as a csv file, one file for each ticker. If file already exists, it will append the new data. 
