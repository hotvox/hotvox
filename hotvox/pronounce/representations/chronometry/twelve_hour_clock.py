'''
civil_time.py
'''
import itertools
import re

from hotvox.pronounce.representation import Representation
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation.pause import Pause
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.utils.numbers import pronounce_number

class TwelveHourClock(Representation):
    '''
    --- Wikipedia ---
    The 12-hour clock is a time convention in which the 24 hours of the day
    are divided into two periods: a.m. (from Latin ante meridiem, translating
    to "before midday") and p.m. (from Latin post meridiem, translating to
    "after midday").
    Each period consists of 12 hours numbered: 12 (acting as 0),
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10 and 11.
    Reference: https://en.wikipedia.org/wiki/12-hour_clock
    --- End of Wikipedia ---
    '''
    def __init__(self, hour: int, minute: int | None = 0) -> None:
        '''
        Initialize the TwelveHourClock Representation.
        The hour must be between 0 and 23.
        '''
        self.hour = hour
        self.minute = minute

    @staticmethod
    def defers_to() -> list[type]:
        return [Literal, Pause]

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        '''
        Compress the sequence into a TwelveHourClock representation.
        '''
        new_sequence = Sequence()

        iterator = iter(enumerate(sequence))
        for i, first_rep in iterator:
            second_rep = sequence[i + 1] if i + 1 < len(sequence) else None
            if not isinstance(first_rep, Literal) or not isinstance(second_rep, Literal):
                new_sequence.append(first_rep)
                continue

            r_hour = r'([0-9]|0[0-9]|1[0-2])'
            r_minute = r'([0-5][0-9])'
            r_hour_minute = r'^' + r_hour + r'(:' + r_minute + r')?$'
            r_am = r'^([Aa]\.?[Mm]\.?)$'
            r_pm = r'^([Pp]\.?[Mm]\.?)$'

            r_hour_minute_match = re.match(r_hour_minute, str(first_rep))
            if not r_hour_minute_match:
                new_sequence.append(first_rep)
                continue

            hour = int(r_hour_minute_match.group(1))
            minute = int(r_hour_minute_match.group(3)) if r_hour_minute_match.group(3) else 0

            if re.match(r_pm, str(second_rep)):
                hour += 12 if hour != 12 else 0
            elif re.match(r_am, str(second_rep)):
                if hour == 12:
                    hour = 0
            else:
                new_sequence.append(first_rep)
                continue

            new_sequence.append(TwelveHourClock(hour, minute))
            # Skip the next representation (a.m. or p.m.)
            try:
                next(itertools.islice(iterator, 1, 1))
            except StopIteration:
                pass

        return new_sequence

    def pronounciation(self) -> str:
        '''
        Return the pronounciation of the TwelveHourClock.
        '''
        if self.minute == 0 and self.hour == 0:
            return 'midnight'

        if self.minute == 0 and self.hour == 12:
            return 'noon'

        if self.minute == 0:
            return f'{_pronounce_hour(self.hour)} o\'clock {_pronounce_period(self.hour)}'

        return  f'{_pronounce_hour(self.hour)}' + \
                f' {_pronounce_minute(self.minute)}' + \
                f' {_pronounce_period(self.hour)}'

def _pronounce_hour(hour: int) -> str:
    '''
    Return the pronounciation of the hour.
    '''
    if hour in (0, 12):
        return pronounce_number(12)
    return f'{pronounce_number(hour % 12)}'

def _pronounce_minute(minute: int) -> str:
    '''
    Return the pronounciation of the minute.
    '''
    if minute == 0:
        return ''
    if 1 <= minute <= 9:
        return f'oh {pronounce_number(minute)}'
    return f'{pronounce_number(minute)}'

def _pronounce_period(hour: int) -> str:
    '''
    Return the pronounciation of the period.
    '''
    if hour < 6:
        return 'in the early morning'
    if hour < 12:
        return 'in the morning'
    if hour < 18:
        return 'in the afternoon'
    return 'in the evening'
