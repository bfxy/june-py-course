#!/usr/bin/env python3
# converter.py

import urllib.request
from urllib.error import HTTPError, URLError
import json

nbrb_url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'

byn_default = {  # these are passed if API request fails
    'USD': 0.53,
    'EUR': 0.47,
    'RUB': 30.47,
    # 'XYZ': 13.37  # add more here
}


def api_request(url):
    '''
    Sends URL request and expects a valid list of JSON objects
    '''
    currencies = {}
    global byn_default

    try:
        with urllib.request.urlopen(url) as f:
            data = json.load(f)
            for cur in data:
                if cur['Cur_Abbreviation'] in ['USD', 'EUR', 'RUB']:  # add more here
                    # building dict with ratios
                    currencies[cur['Cur_Abbreviation']] = (
                        # converting to 1 BYN = n XYZ
                        1 / (cur['Cur_OfficialRate'] / cur['Cur_Scale'])
                    )
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        print('Using default ratio.')
        currencies = byn_default
    except URLError as e:
        print('Failed to reach a server.')
        print('Reason: ', e.reason)
        print('Using default ratio.')
        currencies = byn_default

    return currencies


def convert(amount, currencies):
    '''
    Returns dict with converted moneyz.
    '''
    converted = {'BYN': amount}  # the dict starts with BYN according to task

    for key, value in currencies.items():
        converted[key] = (value * amount).__round__(2)

    return converted


def to_table(currencies):
    '''
    Writes krasivenky output.
    '''
    # finds the longest value to count how many stars we need
    longest_value = max([len(str(v)) for k, v in currencies.items()])
    longest_line = (10*'*' + longest_value*'*')

    print(longest_line)  # start drawing

    for k, v in currencies.items():
        # if value is short, the ending `*` should still be in place
        if len(str(v)) < longest_value:
            difference = longest_value - len(str(v))
            print('*', k, '*', v, ' '*difference + '*')
        else:
            print('*', k, '*', v, '*')

        print(longest_line)


if __name__ == '__main__':
    moneyz = float(input("How much?\n"))
    ratios = api_request(nbrb_url)
    to_table(convert(moneyz, ratios))
