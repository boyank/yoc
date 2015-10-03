#!/usr/bin/env python

import urllib2
import time
from datetime import datetime
from datetime import date
import sys
import csv
import os
import ConfigParser
from bs4 import BeautifulSoup


def read_config():
    """Read configuration file config.ini

    :return: tickers as list
    """
    my_parser = ConfigParser.ConfigParser()
    my_parser.read('config.ini')
    try:
        tickers_list = my_parser.get('Tickers', 'TickerList')
        return tickers_list.replace(' ', '').replace(';', ',').split(',')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        return None


def get_soup(url):
    """Cooking the soup

    :param url: string
    :return: BeautifulSoup object
    """
    try:
        html_source = urllib2.urlopen(url)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        return None
    my_soup = BeautifulSoup(html_source, "html.parser")
    return my_soup


def get_headers(search_soup):
    """Scrape headers

    Given BeautifulSoup object
    :param search_soup: BeautifulSoup object
    :return: headers as list
    """

    div = search_soup.find('div', id='optionsCallsTable')
    if div:
        opt_table = div.find('table')
        if opt_table:
            headers = ['Date', 'Expire Date', 'Option Type']
            headers.extend([get_clean(th.text) for th in opt_table.find_all('th')])
            return headers


def get_quotes(search_soup, expire_date, options=None):
    """Scrape quotes row by row

    Given BeautifulSoup object, expire-date
    :param search_soup: BeautifulSoup object
    :param expire_date: datetime object
    :param options: list or tuple of string option types, e.g. ['call']. Default is None resulting in both Call and Put
    :return: list of lists of quotes data
    """

    all_quotes = []
    today_date = datetime.strftime(date.today(), '%d.%m.%Y')
    exp_date = datetime.strftime(expire_date, '%d.%m.%Y')
    if not options:
        options = ['Call', 'Put']
    for opt in options:
        div = search_soup.find('div', id='options{}sTable'.format(opt))
        if div:
            opt_table = div.find('table')
            if opt_table:
                tbody = opt_table.find('tbody')
                if tbody:
                    for tr in tbody.find_all('tr'):
                        row_quotes = [td.text.strip().replace(',', '') for td in tr.find_all('td')]
                        if row_quotes:
                            my_quotes = [today_date, exp_date, opt]
                            my_quotes.extend(row_quotes)
                            all_quotes.append(my_quotes)
                else:
                    print '\nUnable to find <tbody> tag for {} options for expire date {}\n'.format(opt, exp_date)
            else:
                print '\nUnable to find <table> for {} options for expire date {}\n'.format(opt, exp_date)
    return all_quotes


def get_clean(s):
    """Clean string from specific chars

    Clean headers from specific unicode chars, used as up/down arrows for sort
    :param s: string to clean
    :return: clean string
    """
    return s.replace(u'\n', '').replace(u'\ue004\ue002', '').replace(u'\u2235 Filter', '')


def main(ticker):
    soup = get_soup('http://finance.yahoo.com/q/op?s={}'.format(ticker))
    if soup:
        options_menu = soup.find('div', id='options_menu')
        if options_menu:
            select = options_menu.find('select')
            expire_dates = [[datetime.strptime(option.text, '%B %d, %Y'), option['data-selectbox-link']]
                            for option in select.find_all('option')]
            if expire_dates:
                headers = get_headers(soup)
                csv.register_dialect('yahoo', delimiter=',', quoting=csv.QUOTE_NONE, lineterminator='\n')
                if os.path.isfile('{}.csv'.format(ticker)):
                    with open('{}.csv'.format(ticker), 'r') as f:
                        current_headers = csv.DictReader(f).fieldnames
                else:
                    current_headers = None
                with open('{}.csv'.format(ticker), 'a') as f:
                    my_writer = csv.DictWriter(f, fieldnames=current_headers, dialect='yahoo')
                    # add headers if new file
                    if not my_writer.fieldnames:
                        my_writer.fieldnames = headers
                        my_writer.writeheader()
                    # loop trough all expire dates
                    for exp_date, link in expire_dates:
                        print 'Expire date and link: {}, {}'.format(datetime.strftime(exp_date,  '%d.%m.%Y'), link)
                        soup = get_soup('http://finance.yahoo.com{}'.format(link))
                        my_writer.writerows([dict(zip(headers, quotes)) for quotes in get_quotes(soup, exp_date)])
                        time.sleep(1)
                        # break
            else:
                print 'It looks like there are no options for ticker: {}'.format(ticker)
        else:
            print 'It looks like there is no such ticker: {}'.format(ticker)
    else:
        print 'Unable to retrieve html. Check the Internet connection and/or try again later.'


if __name__ == '__main__':
    # check if config.ini exists and if not found check if any command line arguments were supplied
    tickers = None
    if len(sys.argv) > 1:  # no config.ini, check for command line
        tickers = sys.argv[1:]
    elif os.path.exists('config.ini'):
        tickers = read_config()
    if not tickers:  # no config.ini or command line arguments
        tickers = raw_input('Enter ticker or tickers, separated by comma: ').replace(' ', '').split(',')  # ask user

    if tickers[0].lower() != 'quit':  # check if user decided to quit
        for tkr in tickers:  # loop trough tickers
            print '\nStart download for ticker {}'.format(tkr.upper())
            main(tkr)
        raw_input('Download complete. Press any key...')
