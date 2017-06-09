# python3

byn_ratio = {  # adding more currencies legitimately works
    'USD': 0.53,
    'EUR': 0.47,
    'RUR': 30.47,
    # 'XYZ': 13.37
}


def poschitai(amount):
    '''
    Returns dict with converted moneyz.
    '''
    global byn_ratio
    converted = {'BYN': amount}  # the dict starts with BYN according to task

    for key, value in byn_ratio.items():
        converted[key] = (value * amount).__round__(2)

    return converted


def krasivenko(currencies):
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
            print('*', k, '*', v, '*' )

        print(longest_line)


if __name__ == '__main__':
    amount = float(input("How much?\n"))
    krasivenko(poschitai(amount))