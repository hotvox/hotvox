'''
Pronounce numbers.
'''

from hotvox.pronounce.representation import PronounciationError

CARDINAL_BASE = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety'
}

ORDINAL_BASE = {
    0: 'zeroth',
    1: 'first',
    2: 'second',
    3: 'third',
    4: 'fourth',
    5: 'fifth',
    6: 'sixth',
    7: 'seventh',
    8: 'eighth',
    9: 'ninth',
    10: 'tenth',
    11: 'eleventh',
    12: 'twelfth',
    13: 'thirteenth',
    14: 'fourteenth',
    15: 'fifteenth',
    16: 'sixteenth',
    17: 'seventeenth',
    18: 'eighteenth',
    19: 'nineteenth',
    20: 'twentieth',
    30: 'thirtieth',
    40: 'fortieth',
    50: 'fiftieth',
    60: 'sixtieth',
    70: 'seventieth',
    80: 'eightieth',
    90: 'ninetieth'
}

ORDINAL_NUMERAL_UNITS = {
    0: 'th',
    1: 'st',
    2: 'nd',
    3: 'rd',
    4: 'th',
    5: 'th',
    6: 'th',
    7: 'th',
    8: 'th',
    9: 'th',
    10: 'th',
    11: 'th',
    12: 'th',
    13: 'th',
}

large_number_groups = {
    3: 'thousand',
    6: 'million',
    9: 'billion',
    12: 'trillion',
    15: 'quadrillion',
    18: 'quintillion',
    21: 'sextillion',
    24: 'septillion',
    27: 'octillion',
    30: 'nonillion',
    33: 'decillion',
    36: 'undecillion',
}

def get_ordinal_numeral(cardinal: int) -> str:
    '''
    Get the ordinal numeral of a cardinal number.
    e.g. 1 -> 1st, 2 -> 2nd, 3 -> 3rd, etc.
    '''
    if cardinal in ORDINAL_NUMERAL_UNITS:
        return f'{cardinal}{ORDINAL_NUMERAL_UNITS[cardinal]}'
    return f'{cardinal}{ORDINAL_NUMERAL_UNITS[cardinal % 10]}'

def pronounce_number(number: int) -> str:
    '''
    Alias for pronounce_cardinal.
    '''
    return _pronounce_number_recursive(number, CARDINAL_BASE)

def pronounce_cardinal(number: int) -> str:
    '''
    Pronounce a number in cardinal form.
    '''
    return _pronounce_number_recursive(number, CARDINAL_BASE)

def pronounce_ordinal(number: int) -> str:
    '''
    Pronounce a number in ordinal form.
    '''
    return _pronounce_number_recursive(number, ORDINAL_BASE)

def pronounce_year(number: int) -> str:
    '''
    Pronounce a number as a year.
    '''
    era = '' if number > 0 else ' BC'
    digits = str(abs(number))
    if len(digits) == 4:
        # 2008 -> two thousand eight
        if digits[:3] == '200':
            if digits[3] == '0':
                return 'two thousand'
            return  'two thousand' + \
                    f' {_pronounce_number_recursive(int(digits[3:]), CARDINAL_BASE)}{era}'
        # 1900 -> nineteen hundred
        # 1904 -> nineteen hundred four
        elif digits[2] == '0':
            if digits[3] == '0':
                return f'{_pronounce_number_recursive(int(digits[:2]), CARDINAL_BASE)} hundred'
            return  f'{_pronounce_number_recursive(int(digits[:2]), CARDINAL_BASE)}' + \
                    f' hundred {CARDINAL_BASE[int(digits[3:])]}{era}'
        # 1912 -> nineteen twelve
        # 2012 -> twenty twelve
        return f'{_pronounce_number_recursive(int(digits[:2]), CARDINAL_BASE)} ' + \
            f'{_pronounce_number_recursive(int(digits[2:]), CARDINAL_BASE)}{era}'
    return _pronounce_number_recursive(number, CARDINAL_BASE)

def _pronounce_number_recursive(number: int, numeral_base: dict[int, str]) -> str:
    '''
    Pronounce a number in cardinal form.
    '''
    digits = str(number)
    digits_length = len(digits)

    if digits_length < 3 and number in numeral_base:
        return numeral_base[number]

    if digits_length == 2:
        return _pronounce_tens(digits, numeral_base)

    if digits_length == 3:
        return _pronounce_hundreds(digits, numeral_base)

    if digits_length >= 3:
        return _pronounce_large_numbers(digits, numeral_base)

    raise PronounciationError(f'Failed to pronounce number: {number}')

def _pronounce_tens(digits: str, numeral_base: dict[int, str]) -> str:
    return f'{CARDINAL_BASE[int(digits[0] + "0")]}-{numeral_base[int(digits[1])]}'

def _pronounce_hundreds(digits: str, numeral_base: dict[int, str]) -> str:
    hundreds_place = int(digits[:-2])
    if digits[-2:] == '00':
        return f'{_pronounce_number_recursive(hundreds_place, numeral_base)} hundred'
    return f'{_pronounce_number_recursive(hundreds_place, numeral_base)} hundred' + \
        f' {_pronounce_number_recursive(int(digits[-2:]), numeral_base)}'

def _pronounce_large_numbers(digits: str, numeral_base: dict[int, str]) -> str:
    '''
    Handles thousands and up.
    '''
    length = len(digits)
    grouping_length = (length - 1) // 3 * 3
    group_name = large_number_groups[grouping_length]
    group_value = int(digits[:-grouping_length])
    remainder_value = int(digits[-grouping_length:])
    if remainder_value == 0:
        return f'{_pronounce_number_recursive(group_value, numeral_base)} {group_name}'
    return f'{_pronounce_number_recursive(group_value, numeral_base)} {group_name}' + \
        f' {_pronounce_number_recursive(remainder_value, numeral_base)}'
