# yahoo_options
yahoo_options.py is a command line tool for scraping option prices and related data from <a href=http://finance.yahoo.com/q/op>finance.yahooo.com</a>

It's written in Python 2.7.9 and can be used to scrape current options data for one or more tickers. List of tickers may be supplied as command line arguments.
For example

C:\>yahoo_options.py googl yhoo

If no command line arguments were supplied, user will be asked to enter one or more tickers separated by comma.

Enter ticker or tickers, separated by comma: googl,yhoo

Downloaded data are stored as a csv file, one file for each ticker. If file already exists, it will append the new data. 
