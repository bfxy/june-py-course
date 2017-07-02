#!/usr/bin/env python3
# converter.py

import urllib.request
from urllib.error import HTTPError, URLError
from socket import timeout
import json

nbrb_url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'

byn_default = {  # these are passed if API request fails
    'USD': 0.53,
    'EUR': 0.47,
    'RUB': 30.47,
    # 'XYZ': 13.37  # add more here
}


def rates_request(url):
    '''
    Sends URL request and expects a valid list of JSON objects.
    Returns dict with rates for BYN, USD, EUR, and RUB.
    '''
    rates = {}
    global byn_default

    try:
        with urllib.request.urlopen(url, timeout=5) as f:
            data = json.load(f)
            for cur in data:
                if cur['Cur_Abbreviation'] in ['USD', 'EUR', 'RUB']:  # add more here
                    # building dict with ratios
                    rates[cur['Cur_Abbreviation']] = (
                        # converting to 1 BYN = n XYZ
                        1 / (cur['Cur_OfficialRate'] / cur['Cur_Scale'])
                    )
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        print('Using default ratio.\n')
        rates = byn_default
    except URLError as e:
        print('Failed to reach a server.')
        print('Reason: ', e.reason)
        print('Using default ratio.\n')
        rates = byn_default
    except timeout:
        print('Request timeout. Using default ratio:\n')

    return rates


def convert(amount, rates, currency='BYN'):
    '''
    Returns dict with converted moneyz.
    '''
    if currency == 'BYN':
        converted = { 'BYN': amount }  # the dict starts with BYN according to task
    else:
        converted = { 'BYN': (amount / rates[currency]).__round__(2) }

    for key, value in rates.items():
        if not key == currency:
            # теперь используем получившееся количество BYN,
            # потому что таблица и API-запрос заточены под эту валюту.
            converted[key] = (value * converted['BYN']).__round__(2)
        else:
            converted[key] = amount.__round__(2)

    return converted


def to_table(rates):
    '''
    Writes krasivenky output.
    '''
    # finds the longest value to count how many stars we need
    longest_value = max([len(str(v)) for k, v in rates.items()])
    longest_line = (10*'*' + longest_value*'*')

    print(longest_line)  # start drawing

    for k, v in rates.items():
        # if value is short, the ending `*` should still be in place
        if len(str(v)) < longest_value:
            difference = longest_value - len(str(v))
            print('*', k, '*', v, ' '*difference + '*')
        else:
            print('*', k, '*', v, '*')

        print(longest_line)


if __name__ == '__main__':
    moneyz = float(input("How much?\n"))
    ratios = rates_request(nbrb_url)
    to_table(convert(moneyz, ratios))
