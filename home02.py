#!/usr/bin/env python3

import urllib.request
from urllib.error import HTTPError, URLError
import json

# converter.py
from converter import nbrb_url, byn_default, api_request, convert, to_table

MENU = {
    'Currency Converter':   1,
    'Deposit Helper':       2,
    'Exit':                 3,
}

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
    {
        'Type':          'D',
        'Cur':           'BYN',
        'Term':          1,
        'Irrevocable':   True,  # irrevocable
        'Rate':          0.05
    },
        {
        'Type':          'E',
        'Cur':           'EUR',
        'Term':          3,
        'Irrevocable':   False,  # revocable
        'Rate':          0.05
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
    elif user_input == 2:
        # run deposit helper
        curr, moneyz, term, irvc = validate_helper()
    elif user_input == 3:
        print('Quitting...')
        exit(0)

    to_display = []  # deposits to be offered to user

    for d in DEPOSITS:

        if curr.upper() == d['Cur']:
            if term >= d['Term']:
                to_display.append(d)
            elif irvc == d['Irrevocable']:
                to_display.append(d)
            else:
                pass

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
        curr = input('Enter currency: BYN or USD\n').upper()
        if curr not in ('BYN', 'USD'):
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
        user_input = input('Is the deposit revocable? Enter YES or NO (Y/N):\n')

        if user_input.upper() not in ('Y', 'YES', 'N', 'NO'):
            print('Please enter correct input (Y, N, YES, NO)\n')
            continue
        else:
            break

        if user_input.upper() in ('Y', 'YES'):
            irvc = False
        elif user_input.upper() in ('N', 'NO'):
            irvc = True

    return curr, moneyz, term, irvc

def validate_selector():
    '''
    Lets user choose between currency converter and deposit helper
    Returns selection.
    '''
    menu_string = 'Choose program:\n'

    for name, number in MENU.items():
        menu_string += '{} — {}\n'.format(number, name)

    while True:
        try:
            choice = int(input(menu_string))
        except ValueError:
            print('Incorrect input. Try numbers.\n')
            continue

        if choice not in MENU.values():
            print('Please enter valid choice.\n')
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