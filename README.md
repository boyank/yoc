# yahoo_options

Recent changes in yahoo.com website design made the script useless as of this moment. I will try to fix the problem, but no promise as to the deadline for this.


yahoo_options.py is a command line tool for scraping financial options prices and related data from <a href=http://finance.yahoo.com/q/op>finance.yahoo.com</a>

It's written in Python 2.7.9 and also ported to Python 3.4 using 2to3 tool.

It can be used to scrape current options data for one or more tickers.
There are several ways to supply list of tickers (in order of priority):

-as command line arguments

-using config.ini file

-as user input during script execution.


Sample config.ini is included.

Here is an example how to supply list of tickers as command-line arguments:

C:\>yahoo_options.py googl yhoo

If no command line arguments were supplied, user will be asked to enter one or more tickers separated by comma.

_Enter ticker or tickers, separated by comma:_ googl,yhoo

It will try to use lxml parser (recommended) for the BeautifulSoup object if present. If lxml is not installed, it will use the default html.parser instead.

Downloaded data are stored as a csv file, one file for each ticker. If file already exists, it will append the new data. 
