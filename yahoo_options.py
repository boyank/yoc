#!/usr/bin/env python

import urllib2
import time
from random import randrange
from datetime import datetime
from datetime import date
from datetime import timedelta
import sys
import csv
import json
import os
import ConfigParser


def read_config():
    """Read configuration file config.ini

    :return: tickers as list
    """
    my_parser = ConfigParser.ConfigParser()
    my_parser.read('config.ini')
    try:
        tickers_list = my_parser.get('Tickers', 'TickerList')
        tickers_list.replace(' ', '').replace(';', ',').split(',')
        if ticker_list == ['']: # config.ini had an empty TickerList
            return None
        else:
            return ticker_list
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        return None


def create_link(ticker, expiration_date=None):
    srv = randrange(1, 3, 1)  # select randomly to use query1 or query2
    if expiration_date:
        link = 'https://query{}.finance.yahoo.com/v7/finance/options/{}?date={}'.format(srv, ticker, expiration_date)
    else:
        link = 'https://query{}.finance.yahoo.com/v7/finance/options/{}'.format(srv, ticker)
    return link


def get_json_data(ticker, expiration_date=None, return_value='all'):
    url = create_link(ticker, expiration_date=expiration_date)
    try:
        chain_json = json.load(urllib2.urlopen(url))
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        print 'Unable to retrieve required data.'
        print 'Possible reasons:\n1. No Internet connection - check and/or try again later.'
        print '2. No such ticker {0}\n3. There are no options for ticker {0}'.format(ticker)
        return []
    if chain_json['optionChain']['result']:
        if return_value == 'expiration dates':
            return chain_json['optionChain']['result'][0]['expirationDates']
        elif return_value == 'options':
            return chain_json['optionChain']['result'][0]['options'][0]
        else:
            return chain_json
    else:
        return []


def main(ticker):

    # change header_template to include the fields you want from fieldnames
    # i.e. the full list of possible fields

    header_template = ('Date', 'Expire Date', 'Option Type', 'Strike', 'Contract Name', 'Last', 'Bid', 'Ask', 'Change',
                       '%Change', 'Volume', 'Open Interest', 'Implied Volatility')
    all_fields = {'Implied Volatility': 'impliedVolatility', 'Last Trade Date': 'lastTradeDate',
                  'Contract Size': 'contractSize', 'Last': 'lastPrice', 'Contract Name': 'contractSymbol',
                  'In The Money': 'inTheMoney', 'Bid': 'bid', 'Ask': 'ask', 'Volume': 'volume',
                  'Currency': 'currency', 'Expire Date': 'expiration', '%Change': 'percentChange',
                  'Strike': 'strike', 'Open Interest': 'openInterest', 'Change': 'change', 'Date': 'todayDate',
                  'Option Type': 'optionType'}

    csv.register_dialect('yahoo', delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')

    # retrieve or create list of fieldnames
    file_name = '{}.csv'.format(ticker)
    if os.path.isfile(file_name):  # already there is file from previous download
        found_file = True
        with open(file_name, 'r') as f:
            current_headers = csv.DictReader(f).fieldnames
            try:
                wr_fieldnames = [all_fields[flnm] for flnm in current_headers]
            except KeyError:
                print 'The header line has been changed and at lest one field is unknown.'
                wr_fieldnames = []
    else:
        wr_fieldnames = [all_fields[fldnm] for fldnm in header_template]  # create fieldnames from header_template
        found_file = False

    # write to file
    if wr_fieldnames:
        with open(file_name, 'a') as f:
            my_writer = csv.DictWriter(f, fieldnames=wr_fieldnames, dialect='yahoo')
            # add headers if new file
            if not found_file:
                f.writelines('{}\n'.format(','.join(header_template)))
            expire_dates = get_json_data(ticker, return_value='expiration dates')

            # loop trough all expire dates
            for exp_date in expire_dates:
                ed = datetime.strftime(date(1970, 1, 1) + timedelta(seconds=int(exp_date)), '%d.%m.%Y')
                print 'Ticker and expire date: {}, {}'.format(ticker, ed)
                options_data = get_json_data(ticker, expiration_date=exp_date, return_value='options')
                for opt_type in ('calls', 'puts'):
                    for option in options_data.setdefault(opt_type, []):
                        option = {key:value for key, value in option.iteritems() if key in wr_fieldnames}
                        option['optionType'] = opt_type.upper()[:-1]
                        option['todayDate'] = datetime.strftime(date.today(), '%d.%m.%Y')
                        option['expiration'] = ed
                        my_writer.writerow(option)
                time.sleep(1)


if __name__ == '__main__':
    # check if config.ini exists and if not found check if any command line arguments were supplied
    tickers = None
    if len(sys.argv) > 1:  # command line arguments available
        tickers = sys.argv[1:]
    elif os.path.exists('config.ini'):  # no command line arguments, check for config.ini
        tickers = read_config()
    if not tickers:  # no config.ini or command line arguments
        tickers = raw_input('Enter ticker or tickers, separated by comma: ').replace(' ', '').split(',')  # ask user
    if tickers[0].lower() != 'quit':  # check if user decided to quit
        for tkr in tickers:  # loop trough tickers
            print '\nStart download for ticker {}'.format(tkr.upper())
            main(tkr)
        raw_input('Download complete. Press any key...')
