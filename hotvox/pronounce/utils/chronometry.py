'''
Utilities for dealing with dates and times.
'''
from hotvox.pronounce.utils.numbers import get_ordinal_numeral

MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

MONTHS_SHORT = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

DAY_ORDINAL_NUMERALS = dict((i, get_ordinal_numeral(i)) for i in range(1, 32))
LIST_MONTHS_LONG_SHORT = list(MONTHS.values()) + list(MONTHS_SHORT.values())
