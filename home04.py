#!/usr/bin/env python3

import re

# converter.py
from converter import nbrb_url, byn_default, rates_request, convert, to_table

MENU = {
    'Currency Converter': 0,
    'Deposit Helper': 1,
    'Deposit List': 2,
    'Exit': 3,
}

DEPOSITS = [
    {
        'Name': 'A',
        'Currency': 'BYN',
        'Term': 6,
        'Revocable': False,
        'Rate': 0.10
    },
    {
        'Name': 'B',
        'Currency': 'USD',
        'Term': 6,
        'Revocable': True,
        'Rate': 0.10
    },
    {
        'Name': 'C',
        'Currency': 'BYN',
        'Term': 1,
        'Revocable': True,
        'Rate': 0.03
    },
    {
        'Name': 'D',
        'Currency': 'BYN',
        'Term': 1,
        'Revocable': False,
        'Rate': 0.05
    },
    {
        'Name': 'E',
        'Currency': 'EUR',
        'Term': 3,
        'Revocable': True,
        'Rate': 0.05
    },
]


def main():
    '''
    Runs program
    '''

    user_input = validate_menu()  # parses MENU dict and reads input

    if user_input == 0:
        run_converter()  # runs currency converter (converter.py)
        exit(0)

    elif user_input == 1:
        curr, moneyz, term, revoc = validate_helper()
        deposit_helper(curr, moneyz, term, revoc)  # runs deposit helper
        exit(0)

    elif user_input == 2:
        key, reverse = validate_list()
        deposit_list(DEPOSITS, key, reverse)
        exit(0)

    elif user_input == 3:
        print('Quitting...')
        exit(0)


def deposit_helper(currency, amount, term, revocable):
    '''
    Accepts deposit helper menu input and calculates result.
    '''

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Я решил для выдачи депозита считать рейтинг предпочтительности вкладов.
    # Тут должна быть крутая математическая формула вычисления веса, но
    # моя формула запредельно тупая:
    # За попадание по валюте - +3,
    # за попадание по сроку - +2,
    # и за попадание в отзывность - +1.
    # Предпочтительным считается депозит с весом 5+. Если есть 4, то выдаю
    # его как возможный.
    # Если 4 нет, то честно говорю, что хороших нет, но показываю депозиты с
    # весом 3 как альтернативные.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    primary, secondary, alternative = [], [], []  # deposits to be offered to user
    standings = {}  # ratings for all deposits

    # calculates ratings and forms a dict with standings
    for d in DEPOSITS:
        rating = 0

        if currency.upper() == d['Currency']:  # currency rating
            rating += 3

        if term == d['Term']:  # term rating
            rating += 2
        elif 1 < term < 3 and d['Term'] == 1:
            rating += 2
        elif 2 <= term <= 4 and d['Term'] == 3:
            rating += 2
        elif 4 <= term <= 6 and d['Term'] == 6:
            rating += 2
        elif term > 6 and d['Term'] == 6:
            rating += 2
        else:
            pass

        if revocable == d['Revocable']:  # irrevocabile rating
            rating += 1

        standings[d['Name']] = rating  # e.g. {'A': 6}

    # tests
    # for k, v in standings.items():
    #     print(k,":", v)
    # print(revocable)

    # compares ratings and finds deposits to display
    for _id, rate in standings.items():
        for d in DEPOSITS:
            if _id in d.values() and rate >= 5:
                primary.append(d)

            if _id in d.values() and rate == 4:
                secondary.append(d)

            if _id in d.values() and rate == 3:
                alternative.append(d)

    # displays result
    if primary or secondary:
        display_helper_answer(primary, amount, 'best')
        display_helper_answer(secondary, amount, 'see_also')
    else:
        display_helper_answer(alternative, amount, 'try_another')


def display_helper_answer(deposits, moneyz, message):
    '''
    Args:
        deposits:  list of dicts with deposits
        moneyz:    user's amount of money to deposit
        message:   message to display on screen

    Displays answer with available deposits.
    '''
    message_string = {
        'best':         '\nYour best pick would be:\n',
        'try_another':  '\nSorry, we don\'t have a good option for you, but you may look into these:\n',
        'see_also':     '\nNot the best, but these may also suite you:\n',
    }

    if deposits:  # no message if empty
        print(message_string[message])
        for d in deposits:
            print('Deposit:', d['Name'])
            print('Currency:', d['Currency'])
            print('Term:', d['Term'], 'month(s)')
            print('Able to revoke:', 'Yes' if d['Revocable'] else 'No')
            print('Rate:', d['Rate'])
            print('Amount to deposit:', moneyz, '\n')
    else:
        # print('Sorry, no deposit variants available.')
        pass


def deposit_list(deposits, keyword='Name', reverse='False'):
    '''
    Accepts list of dicts with deposits and sorts them by given key
    with reverse option.
    Displays result.
    '''
    result = sorted(deposits,
                    key=lambda deposit: deposit[keyword.capitalize()],
                    reverse=reverse)

    display_list_answer(result)


def display_list_answer(deposits):
    '''
    Displays sorted deposits in a frame.
    '''
    frame = '*' * 20

    print('These are all available deposits:\n')
    print(frame)

    for d in deposits:
        print('Deposit:', d['Name'])
        print('Currency:', d['Currency'])
        print('Term:', d['Term'], 'month(s)')
        print('Able to revoke:', 'Yes' if d['Revocable'] else 'No')
        print('Rate:', d['Rate'])
        print(frame)

def validate_menu():
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
    revoc = False

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
        revoc_input = input('Is the deposit revocable? Enter YES or NO (Y/N):\n')

        if revoc_input.upper() not in ('Y', 'YES', 'N', 'NO'):
            print('Please enter correct input (Y, N, YES, NO)\n')
            continue
        else:
            break

    if revoc_input.upper() in ('Y', 'YES'):
        revoc = True
    elif revoc_input.upper() in ('N', 'NO'):
        revoc = False

    return curr, moneyz, term, revoc


def validate_list():
    '''
    Validates deposit list input.
    Returns key and reverse flag.
    '''
    while True:
        key = input('Enter sort key:\n'
                    'Name, Currency, Term, Revocable, Rate\n').lower()

        if key not in ('name', 'currency', 'term', 'revocable', 'rate'):
            print('Please enter correct key.\n')
            continue
        else:
            break

    while True:
        reverse_input = input('Reverse order? Enter YES or NO (Y/N):\n')

        if reverse_input.upper() not in ('Y', 'YES', 'N', 'NO'):
            print('Please enter correct input (Y, N, YES, NO)\n')
            continue
        else:
            break

    if reverse_input.upper() in ('Y', 'YES'):
        reverse = True
    elif reverse_input.upper() in ('N', 'NO'):
        reverse = False

    return key, reverse


def run_converter():
    '''
    Reads input and runs functions from converter.py
    '''
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Хочу попробовать регулярки, чтобы исключить ошибки с введением без пробелов,
    # или нескольких пробелов. Цифра обязательна (группа 1), валюта
    # опциональна (группа 2).
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while True:
        input_str = input("Enter amount and currency (BYN, EUR, USD, or RUB):\n")
        match = re.match(r'([0-9]+)\s*([a-zA-Z]{3})?', input_str)

        if match:
            moneyz = float(match.group(1))

            if match.group(2) and match.group(2).upper() in ('BYN', 'USD', 'EUR', 'RUB'):
                currency = match.group(2).upper()
                break
            else:
                print(
                    'No correct currency entered.\n'
                    'Showing results for BYN:\n'
                )
                currency = 'BYN'
                break

        else:
            print('Please correct amount and currency:\n')
            continue

    rates = rates_request(nbrb_url)
    to_table(convert(moneyz, rates, currency))


if __name__ == '__main__':
    main()
