'''
integer.py
'''
import itertools
import re

from hotvox.pronounce.representation import Representation
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation import PUNCTUATION
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.utils.chronometry import \
    MONTHS, MONTHS_SHORT, LIST_MONTHS_LONG_SHORT, DAY_ORDINAL_NUMERALS
from hotvox.pronounce.utils.numbers import pronounce_ordinal, pronounce_year

class CalendarDate(Representation):
    '''
    A Representation of a calendar date.
    '''

    def __init__(self, day: int, month: int, year: int | None) -> None:
        if not _is_valid_date(day, month, year):
            raise ValueError(f'Invalid date: {day}/{month}/{year}')

        self.day = int(day)
        self.month = int(month)
        self.year = int(year) if year is not None else None

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        return PUNCTUATION

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        new_sequence : Sequence = Sequence()
        # loop through the sequence
        iterator = iter(enumerate(sequence))
        for i, first_rep in iterator:
            second_rep = sequence[i + 1] if i + 1 < len(sequence) else None
            third_rep = sequence[i + 2] if i + 2 < len(sequence) else None

            rep_count = 0
            rep_count = 1 if rep_count == 0 and isinstance(first_rep,   Literal) else 0
            rep_count = 2 if rep_count == 1 and isinstance(second_rep,  Literal) else 1
            rep_count = 3 if rep_count == 2 and isinstance(third_rep,   Literal) else 2

            if 3 <= rep_count:
                calendar_date = _compress_literals([first_rep, second_rep, third_rep])
                if calendar_date:
                    new_sequence.append(calendar_date)
                    try:
                        next(itertools.islice(iterator, 2, 2))
                    except StopIteration:
                        pass
                    continue

            if 2 <= rep_count:
                calendar_date = _compress_literals([first_rep, second_rep])
                if calendar_date:
                    new_sequence.append(calendar_date)
                    try:
                        next(itertools.islice(iterator, 1, 1))
                    except StopIteration:
                        pass
                    continue

            if 1 <= rep_count:
                calendar_date = _compress_literals([first_rep])
                if calendar_date:
                    new_sequence.append(calendar_date)
                    continue

            new_sequence.append(first_rep)
        return new_sequence

    def pronounciation(self):
        '''
        Return the pronounciation of the calendar date.
        '''
        if self.year is None:
            return f'{MONTHS[self.month]} {pronounce_ordinal(self.day)}'
        return f'{MONTHS[self.month]} {pronounce_ordinal(self.day)}, {pronounce_year(self.year)}'

def _compress_literals(literals: list[Literal]) -> CalendarDate | None:
    '''
    Compress a list of literals into a CalendarDate if they form a valid date.
    '''
    if len(literals) == 1:
        return _compress_one_literal(literals)

    if len(literals) == 2:
        return _compress_two_literals(literals)

    if len(literals) == 3:
        return _compress_three_literals(literals)

    return None

def _compress_one_literal(literals: list[Literal]) -> CalendarDate | None:
    '''
    Compress a single literal into a CalendarDate if it is a valid date.
    Reference: https://en.wikipedia.org/wiki/Calendar_date
    '''
    string = ' '.join(str(literal) for literal in literals)
    r_day = r'(\d{1,2})'
    r_month =   r'(\d{1,2}|' + r'|'.join(LIST_MONTHS_LONG_SHORT) + r')'
    r_year = r'(\d{4})'

    # This little-endian sequence is used by a majority of the world and is the
    # preferred form by the United Nations when writing the full date format
    # in official documents.
    r_dmy = r'^' + r_day + r'[\/\-\.]' + r_month + r'[\/\-\.]' + r_year + r'$'
    r_dmy_match = re.match(r_dmy, string)
    if r_dmy_match:
        return _valid_date_or_none(*r_dmy_match.group(1, 2, 3))

    # In this format, the most significant data item is written before lesser
    # data items i.e. the year before the month before the day.
    ymd = r'^' + r_year + r'[\/\-\.]' + r_month + r'[\/\-\.]' + r_day + r'$'
    ymd_match = re.match(ymd, string)
    if ymd_match:
        return _valid_date_or_none(*ymd_match.group(3, 2, 1))

    return None

def _compress_two_literals(literals: list[Literal, Literal]) -> CalendarDate | None:
    '''
    Compress two literals into a CalendarDate if they form a valid date.
    This will look for a day and month in either order, using cardinal and ordinal numbers.
    Reference: https://en.wikipedia.org/wiki/Calendar_date
    '''
    string = ' '.join(str(literal) for literal in literals)
    r_day = r'(\d{1,2}|' + r'|'.join(DAY_ORDINAL_NUMERALS.values()) + r')'
    r_month = r'(' + r'|'.join(LIST_MONTHS_LONG_SHORT) + r')'

    # 17 Jan
    # 17 January
    # 17th Jan
    # 17th January
    r_dm = r'^' + r_day + r'\s' + r_month + r'$'
    r_dm_match = re.match(r_dm, string)
    if r_dm_match:
        return _valid_date_or_none(*r_dm_match.group(1, 2))

    # Jan 17
    # January 17
    # Jan 17th
    # January 17th
    r_md = r'^' + r_month + r'\s' + r_day + r'$'
    r_md_match = re.match(r_md, string)
    if r_md_match:
        return _valid_date_or_none(*r_md_match.group(2, 1))

    return None

def _compress_three_literals(literals: list[Literal, Literal, Literal]) -> CalendarDate | None:
    '''
    Compress two literals into a CalendarDate if they form a valid date.
    This will look for a day, month and year in DMY, MDY, and YDM order.
    Reference: https://en.wikipedia.org/wiki/Calendar_date
    '''

    string = ' '.join(str(literal) for literal in literals)
    r_day = r'(\d{1,2}|' + r'|'.join(DAY_ORDINAL_NUMERALS.values()) + r')'
    r_month = r'(' + r'|'.join(LIST_MONTHS_LONG_SHORT) + r')'
    r_year = r'(\d{4})'

    # 17 Jan 2022
    # 17th January 2022
    r_dmy = r'^' + r_day + r'\s' + r_month + r'\s' + r_year + r'$'
    r_dmy_match = re.match(r_dmy, string)
    if r_dmy_match:
        return _valid_date_or_none(*r_dmy_match.group(1, 2, 3))

    # Jan 17 2022
    # January 17th 2022
    r_mdy = r'^' + r_month + r'\s' + r_day + r'\s' + r_year + r'$'
    r_mdy_match = re.match(r_mdy, string)
    if r_mdy_match:
        return _valid_date_or_none(*r_mdy_match.group(2, 1, 3))

    # 2022 Jan 17
    # 2022 January 17th
    r_ydm = r'^' + r_year + r'\s' + r_month + r'\s' + r_day + r'$'
    r_ydm_match = re.match(r_ydm, string)
    if r_ydm_match:
        return _valid_date_or_none(*r_ydm_match.group(3, 2, 1))

    return None

def _is_valid_day(day: int) -> bool:
    return 1 <= day <= 31

def _is_valid_month(month: int) -> bool:
    return 1 <= month <= 12

def _is_valid_year(year: int | None) -> bool:
    if year is None:
        return True
    return -9999 <= year <= 9999

def _is_valid_date(day: int, month: int, year: int | None) -> bool:
    return _is_valid_day(day) and _is_valid_month(month) and _is_valid_year(year)

def _valid_date_or_none(
    day: int | str,
    month: int | str,
    year: int | str | None = None
) -> CalendarDate | None:
    if isinstance(day, str):
        if day in DAY_ORDINAL_NUMERALS.values():
            day = list(DAY_ORDINAL_NUMERALS.keys())[list(DAY_ORDINAL_NUMERALS.values()).index(day)]
        day = int(day)

    if isinstance(month, str):
        month = month.capitalize()
        if month in MONTHS_SHORT.values():
            month = list(MONTHS_SHORT.keys())[list(MONTHS_SHORT.values()).index(month)]

        if month in MONTHS.values():
            month = list(MONTHS.keys())[list(MONTHS.values()).index(month)]

        month = int(month)

    if isinstance(year, str):
        year = int(year)

    if _is_valid_date(day, month, year):
        return CalendarDate(day, month, year)
    return None
