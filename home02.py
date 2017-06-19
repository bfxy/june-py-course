#!/usr/bin/env python3

import urllib.request
from urllib.error import HTTPError, URLError
import json

# converter.py
from converter import nbrb_url, api_request, convert, to_table

DEPOSITS = [
    {
        'Type':         'A',
        'Cur':          'BYN',
        'Term':          6,
        'Irrevocable':   True,  # irrevocable
        'Rate':          0.10
    },
    {
        'Type':          'B',
        'Cur':           'USD',
        'Term':          6,
        'Irrevocable':   False,  # revocable
        'Rate':          0.10
    },
    {
        'Type':          'C',
        'Cur':           'BYN',
        'Term':          1,
        'Irrevocable':   False,  # revocable
        'Rate':          0.03
    },
]

def main():
    '''
    Runs program
    '''

    user_input = validate_selector()

    if user_input == 1:
        # run currency converter
        run_converter()
        exit(0)
    else:
        # run deposit helper
        cur, moneyz, term, irvc = validate_helper()

    to_display = []  # deposits to be offered to user

    for d in DEPOSITS:

        if cur.upper() == d['Cur']:
            if ((d['Term'] == 1 and 1 <= term <= 5) or
                (d['Term'] == 6 and term >= 6)) or (
                d['Irrevocable'] == irvc):

                to_display.append(d)

    print('\nYou can make these deposits:\n')
    if to_display:
        for d in to_display:
            print('Deposit:', d['Type'])
            print('Currency:', d['Cur'])
            print('Term:', d['Term'], 'month(s)')
            print('Able to revoke:', 'No' if d['Irrevocable'] else 'Yes')
            print('Rate:', d['Rate'])
            print('Amount to deposit:', moneyz, '\n')
    else:
        print('Sorry, no deposit variants available.')

def validate_helper():
    '''
    Validates deposit helper input.
    Returns currency, deposit amount, period, and if deposit is irrevocable
    '''

    while True:
        cur = input('Enter currency: BYN or USD\n').upper()
        if cur not in ('BYN', 'USD'):
            print('Enter correct currency.\n')
            continue
        else:
            break

    while True:
        try:
            moneyz = float(input('Enter the amount of money:\n'))
        except ValueError:
            print('Incorrect input. Try numbers.\n')
        if moneyz < 0:
            print('Incorrect input. Please enter amount in number.\n')
            continue
        else:
            break

    while True:
        try:
            term = int(input('For how many months long?\n'))
        except ValueError:
            print('Incorrect input. Try numbers.\n')
            continue
        if term < 0:
            print('Incorrect input. Please enter term in months.\n')
            continue
        else:
            break

    while True:
        irvc = False
        user_input = input('Is the deposit revocable? Enter YES or no (Y/N):\n')

        if user_input.upper() not in ('Y', 'YES', 'N', 'NO'):
            print('Please enter correct input (Y, N, YES, NO)\n')
            continue
        else:
            break

        if user_input.upper() in ('Y', 'YES'):
            irvc = False
        elif user_input.upper() in ('N', 'NO'):
            irvc = True

    return cur, moneyz, term, irvc

def validate_selector():
    '''
    Lets user choose between currency converter and deposit helper
    Returns selection.
    '''

    while True:
        try:
            choice = int(input('Choose program:\n1 - Currency Converter\n2 - Deposit Helper\n'))
        except ValueError:
            print('Incorrect input. Try numbers.\n')
            continue

        if choice not in (1, 2):
            print('Please enter numbers between 1 or 2. Try again.\n')
            continue
        else:
            break

    return choice

def run_converter():
    '''
    Runs methods from converter.py
    '''

    while True:
        try:
            moneyz = float(input("How much?\n"))
        except ValueError:
            print('Please enter amount in number.\n')
            continue
        else:
            break
    ratios = api_request(nbrb_url)
    to_table(convert(moneyz, ratios))


if __name__ == '__main__':
    main()