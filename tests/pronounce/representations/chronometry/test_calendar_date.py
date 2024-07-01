'''
Test the CalendarDate representation.
'''
from hotvox.pronounce.representations.chronometry.calendar_date import \
    CalendarDate, _compress_one_literal, _compress_two_literals, _compress_three_literals
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.utils.chronometry import MONTHS, MONTHS_SHORT
from hotvox.pronounce.utils.numbers import get_ordinal_numeral

cases_dmy: dict[str, list[int, int, int]] = {
    'January first, nineteen hundred': [1, 1, 1900],
    'January first, nineteen hundred one': [1, 1, 1901],
    'February second, nineteen ten': [2, 2, 1910],
    'March third, nineteen twelve': [3, 3, 1912],
    'January first, two thousand': [1, 1, 2000],
    'January first, two thousand one': [1, 1, 2001],
    'February second, two thousand two': [2, 2, 2002],
    'March third, two thousand three': [3, 3, 2003],
    'April fourth, two thousand four': [4, 4, 2004],
    'May fifth, two thousand five': [5, 5, 2005],
    'June sixth, two thousand six': [6, 6, 2006],
    'July seventh, two thousand seven': [7, 7, 2007],
    'August eighth, two thousand eight': [8, 8, 2008],
    'September ninth, two thousand nine': [9, 9, 2009],
    'October tenth, twenty ten': [10, 10, 2010],
    'November eleventh, twenty eleven': [11, 11, 2011],
    'December twelfth, twenty twelve': [12, 12, 2012],
    'January thirteenth, twenty thirteen': [13, 1, 2013],
    'February fourteenth, twenty fourteen': [14, 2, 2014],
    'March fifteenth, twenty fifteen': [15, 3, 2015],
    'April sixteenth, twenty sixteen': [16, 4, 2016],
    'May seventeenth, twenty seventeen': [17, 5, 2017],
    'June eighteenth, twenty eighteen': [18, 6, 2018],
    'July nineteenth, twenty nineteen': [19, 7, 2019],
    'August twentieth, twenty twenty': [20, 8, 2020],
    'September twenty-first, twenty twenty-one': [21, 9, 2021],
    'October twenty-second, twenty twenty-two': [22, 10, 2022],
    'November twenty-third, twenty twenty-three': [23, 11, 2023],
    'December twenty-fourth, twenty twenty-four': [24, 12, 2024]
}

cases_dm = {
    'January first': [1, 1],
    'February second': [2, 2],
    'March third': [3, 3],
    'April fourth': [4, 4],
    'May fifth': [5, 5],
    'June sixth': [6, 6],
    'July seventh': [7, 7],
    'August eighth': [8, 8],
    'September ninth': [9, 9],
    'October tenth': [10, 10],
    'November eleventh': [11, 11],
    'December twelfth': [12, 12],
    'January thirteenth': [13, 1],
    'February fourteenth': [14, 2],
    'March fifteenth': [15, 3],
    'April sixteenth': [16, 4],
    'May seventeenth': [17, 5],
    'June eighteenth': [18, 6],
    'July nineteenth': [19, 7],
    'August twentieth': [20, 8],
    'September twenty-first': [21, 9],
    'October twenty-second': [22, 10],
    'November twenty-third': [23, 11],
    'December twenty-fourth': [24, 12]
}

date_formats_one_literal = [
    '%DCN/%MN/%Y',
    '%DCN-%MN-%Y',
    '%DCN.%MN.%Y'
]

date_formats_two_literals = [
    '%DCN %MS',
    '%DCN %ML',
    '%DON %MS',
    '%DON %ML',
    '%MS %DCN',
    '%MS %DON',
    '%ML %DCN',
    '%ML %DON',
]

date_formats_three_literals = [
    '%DCN %MS %Y',
    '%DON %MS %Y',
    '%DCN %ML %Y',
    '%DON %ML %Y',
    '%MS %DCN %Y',
    '%MS %DON %Y',
    '%ML %DCN %Y',
    '%ML %DON %Y',
    '%Y %MS %DCN',
    '%Y %MS %DON',
    '%Y %ML %DCN',
    '%Y %ML %DON',
]

def _format_date(day: int, month: int, year: int, date_format: str) -> str:
    '''
    Utility function to format a date.
    '''
    return date_format\
        .replace("%DCN", str(day))\
        .replace("%DON", get_ordinal_numeral(day))\
        .replace("%MN", str(month))\
        .replace("%MS", MONTHS_SHORT[month])\
        .replace("%ML", MONTHS[month])\
        .replace("%Y", str(year))

def test__compress_one_literal():
    '''
    Test the _compress_one_literal method of the CalendarDate representation.
    '''
    for date in cases_dmy.values():
        day, month, year = date
        for date_format in date_formats_one_literal:
            formatted_date = _format_date(day, month, year, date_format)
            literal = Literal(formatted_date)
            assert _compress_one_literal([literal]) == CalendarDate(day, month, year)

def test__compress_two_literals():
    '''
    Test the _compress_two_literals method of the CalendarDate representation.
    '''
    for date in cases_dm.values():
        day, month = date
        for date_format in date_formats_two_literals:
            formatted_date = _format_date(day, month, None, date_format)
            assert _compress_two_literals(
                [Literal(token) for token in formatted_date.split()]
            ) == CalendarDate(day, month, None)

def test__compress_three_literals():
    '''
    Test the _compress_three_literals method of the CalendarDate representation.
    '''
    for date in cases_dmy.values():
        day, month, year = date
        for date_format in date_formats_three_literals:
            formatted_date = _format_date(day, month, year, date_format)
            assert _compress_three_literals(
                [Literal(token) for token in formatted_date.split()]
            ) == CalendarDate(day, month, year)

def test_compress():
    '''
    Test the compress method of the CalendarDate representation.
    '''
    for pronounciation, date in cases_dmy.items():
        day, month, year = date
        for date_format in date_formats_one_literal + date_formats_three_literals:
            formatted_date = _format_date(day, month, year, date_format)
            assert Sequence.from_string(
                f'Yesterday was {formatted_date}. Today will be better.',
                represent_for=CalendarDate
            ).pronounciation() == f'Yesterday was {pronounciation}. Today will be better.'

    for pronounciation, date in cases_dm.items():
        day, month = date
        for date_format in date_formats_two_literals:
            formatted_date = _format_date(day, month, year, date_format)
            assert Sequence.from_string(
                f'I sit here every {formatted_date}. Greatness happens.',
                represent_for=CalendarDate
            ).pronounciation() == f'I sit here every {pronounciation}. Greatness happens.'

def test_pronounciation():
    '''
    Test the pronounciation method of the CalendarDate representation.
    '''
    for pronounciation, date in cases_dmy.items():
        assert CalendarDate(*date).pronounciation() == pronounciation
