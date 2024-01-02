_symbol_map_ascii = {
    1: '{1}',
    2: '{2}',
    3: '{3}',
    4: '{4}',
    5: '{5}',
    6: '{6}',
    7: '{7}',
    8: '{8}',
    9: '{9}',
    10: '{10}',
    20: '{20}',
    30: '{30}',
    40: '{40}',
    50: '{50}',
    60: '{60}',
    70: '{70}',
    80: '{80}',
    90: '{90}',
    100: '{100}',
    10000: '{10,000}'
}

_symbol_map = {
    1: '፩',
    2: '፪',
    3: '፫',
    4: '፬',
    5: '፭',
    6: '፮',
    7: '፯',
    8: '፰',
    9: '፱',
    10: '፲',
    20: '፳',
    30: '፴',
    40: '፵',
    50: '፶',
    60: '፷',
    70: '፸',
    80: '፹',
    90: '፺',
    100: '፻',
    10000: '፼'
}

_reverse_symbol_map = {
    '፩': 1,
    '፪': 2,
    '፫': 3,
    '፬': 4,
    '፭': 5,
    '፮': 6,
    '፯': 7,
    '፰': 8,
    '፱': 9,
    '፲': 10,
    '፳': 20,
    '፴': 30,
    '፵': 40,
    '፶': 50,
    '፷': 60,
    '፸': 70,
    '፹': 80,
    '፺': 90,
    '፻': 100,
    '፼': 10000
}


def arabic_to_geez_ascii(numeral):
    assert (isinstance(numeral, int))
    assert (numeral > 0)

    return _arabic_to_geez(numeral, _symbol_map_ascii)


def arabic_to_geez(numeral):
    assert (isinstance(numeral, int))
    assert (numeral > 0)

    return _arabic_to_geez(numeral, _symbol_map)


def _arabic_to_geez(numeral, symbol_map):
    if numeral >= 20000:
        # numeral is in the range [20,000, infinity)
        num_ten_thousands = numeral // 10000
        remainder = numeral % 10000
        return _arabic_to_geez(num_ten_thousands, symbol_map) + symbol_map[10000] + _arabic_to_geez(remainder,
                                                                                                    symbol_map)

    elif numeral >= 10000:
        # numeral is in the range [10,000, 19,999]
        remainder = numeral % 10000
        return symbol_map[10000] + _arabic_to_geez(remainder, symbol_map)

    elif numeral >= 200:
        # numeral is in the range [200, 9,999]
        num_hundreds = numeral // 100
        remainder = numeral % 100
        return _arabic_to_geez(num_hundreds, symbol_map) + symbol_map[100] + _arabic_to_geez(remainder, symbol_map)

    elif numeral >= 100:
        # numeral is in the range [100, 199]
        remainder = numeral % 100
        return symbol_map[100] + _arabic_to_geez(remainder, symbol_map)

    elif numeral >= 10:
        # numeral is in the range [10, 99]
        num_tens = numeral // 10
        remainder = numeral % 10
        return symbol_map[num_tens * 10] + _arabic_to_geez(remainder, symbol_map)

    elif numeral >= 1:
        # numeral is in the range [1, 9]
        return symbol_map[numeral]

    else:
        # numeral is zero
        return ''


def geez_to_arabic(numeral):
    # todo: check the format of numeral
    assert (isinstance(numeral, str))

    return _geez_to_arabic_ten_thousands(numeral)


def _geez_to_arabic_ten_thousands(numeral):
    idx = numeral.rfind(_symbol_map[10000])
    if idx == -1:
        return _geez_to_arabic_hundreds(numeral)
    else:
        return max(_geez_to_arabic_ten_thousands(numeral[:idx]), 1) * 10000 + _geez_to_arabic_hundreds(
            numeral[idx + 1:])


def _geez_to_arabic_hundreds(numeral):
    idx = numeral.rfind(_symbol_map[100])
    if idx == -1:
        return _geez_to_arabic_tens_and_ones(numeral)
    else:
        return max(_geez_to_arabic_hundreds(numeral[:idx]), 1) * 100 + _geez_to_arabic_tens_and_ones(numeral[idx + 1:])


def _geez_to_arabic_tens_and_ones(numeral):
    return sum([_reverse_symbol_map.get(symbol, 0) for symbol in numeral])
