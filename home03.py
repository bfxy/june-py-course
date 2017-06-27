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

    user_input = validate_selector()  # parses MENU dict and reads input

    if user_input == 1:
        run_converter()  # runs currency converter
        exit(0)

    elif user_input == 2:
        curr, moneyz, term, irvc = validate_helper()  # runs deposit helper

    elif user_input == 3:
        print('Quitting...')
        exit(0)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Я решил для выдачи депозита считать рейтинг предпочтительности вкладов.
    # Тут должна быть крутая математическая формула вычисления приоритета, но
    # моя формула запредельно тупая:
    #
    # За попадание по валюте - +3 очка,
    # за попадание по сроку - +2 очка
    # и за попадание в отзывность - +1 очко.
    # Предпочтительным считается депозит с 5+ очками. Если есть 4, то выдаю
    # его как возможный.
    # Если 4 нет, то честно говорю, что хороших нет, но показываю 3-очковые,
    # как альтернативные.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    primary, secondary, alternative = [], [], []  # deposits to be offered to user
    standings = {}  # ratings for all deposits

    for d in DEPOSITS:  # calculates ratings and forms a dict with standings
        rating = 0

        if curr.upper() == d['Cur']:  # currency rating
            rating += 3

        if term == d['Term']:  # term rating
            rating += 2
        elif 1 < term < 3 and d['Term'] == 1:
            rating += 2
        elif 2 <= term <= 4 and d['Term'] == 3:
            rating += 2
        elif 4 <= term <= 6 and d['Term'] == 6:
            rating +=2
        elif term > 6 and d['Term'] == 6:
            rating += 2
        else:
            pass

        if irvc == d['Irrevocable']:  # irrevocabile rating
            rating += 1

        standings[d['Type']] = rating  # e.g. {'A': 6}

    for _id, rate in standings.items():  # compares ratings and adds deposits to display
        for d in DEPOSITS:
            if _id in d.values() and rate >= 5:
                primary.append(d)

            if _id in d.values() and rate == 4:
                secondary.append(d)

            if _id in d.values() and rate == 3:
                alternative.append(d)

    if primary or secondary:
        display_answer(primary, moneyz, 'best')
        display_answer(secondary, moneyz, 'see_also')
    else:
        display_answer(alternative, moneyz, 'try_another')


def validate_selector():
    '''
    Lets user choose between menu items from MENU dict
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


def validate_helper():
    '''
    Validates deposit helper input.
    Returns currency, deposit amount, period, and bool if deposit is irrevocable
    '''

    while True:
        curr = input('Enter currency: BYN, USD, or EUR\n').upper()
        if curr not in ('BYN', 'USD', 'EUR'):
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


def display_answer(deposits, moneyz, message):
    '''
    Args:
        list of dicts with deposits
        user's amount of money to deposit

    Displays answer with available deposits.
    '''

    message_string = {
        'best':         '\nYour best pick would be:\n',
        'try_another':  '\nSorry, we don\'t have a good option for you, but you may look into these:\n',
        'see_also':     '\nNot the best, but these will also suite you:\n',
    }

    if deposits:  # no message if empty
        print(message_string[message])
        for d in deposits:
            print('Deposit:', d['Type'])
            print('Currency:', d['Cur'])
            print('Term:', d['Term'], 'month(s)')
            print('Able to revoke:', 'No' if d['Irrevocable'] else 'Yes')
            print('Rate:', d['Rate'])
            print('Amount to deposit:', moneyz, '\n')
    else:
        # print('Sorry, no deposit variants available.')
        pass


def run_converter():
    '''
    Runs functions from converter.py
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