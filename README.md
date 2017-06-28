# yoc (yahoo option chains)

version 2, works with yahoo.com website design since July 2016.

### Quick start

yahoo_options.py is a command line tool for scraping financial options prices and related data from <a href=http://finance.yahoo.com/>finance.yahoo.com</a>

It's written in Python 2.7 and also ported to Python 3.4 using 2to3 tool.

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

Downloaded data are stored as a csv file, one file for each ticker. If file already exists, it will append the new data.

### Advanced usage

In ver.2 it requests and gets response in json format. See included json_response_GOOGL.json for sample of the json response. As you can see there are a lot more data available. One can easily change the script to parse the json and extract any of these data. All you need to do is to amend the get_json_data() to return the desired data. Eventually you will need to change slightly also the main function.

### Pandas DataReader

I have recently discovered that <a href=https://github.com/pydata/pandas-datareader>pandas-datareader</a> suports download of options data from <a href=http://finance.yahoo.com/>finance.yahoo.com</a>. It is still designated as Experimenal, but you should <a href=https://pandas-datareader.readthedocs.io/en/latest/remote_data.html>check the Docs</a> if you are interested in downloading and crunchig/analyze the data.

