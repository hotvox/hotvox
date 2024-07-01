'''
civil_time.py
'''
import re

from hotvox.pronounce.representations.chronometry.twelve_hour_clock import TwelveHourClock
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.sequence import Sequence

class TwentyFourHourClock(TwelveHourClock):
    '''
    --- Wikipedia ---
    The modern 24-hour clock is the convention of timekeeping in which the
    day runs from midnight to midnight and is divided into 24 hours. This
    is indicated by the hours (and minutes) passed since midnight, from 00(:00)
    to 23(:59).
    Reference: https://en.wikipedia.org/wiki/24-hour_clock
    --- End of Wikipedia ---
    '''

    @staticmethod
    def defers_to() -> list[type]:
        return [TwelveHourClock]

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        '''
        Compress the sequence into a TwelveHourClock representation.
        '''
        for i, rep in enumerate(sequence):
            if not isinstance(rep, Literal):
                continue

            r_hour = r'([0-9]|0[0-9]||1[0-9]|2[0-3])'
            r_minute = r'([0-5][0-9])'
            # minutes are mandatory
            r_hour_minute = r'^' + r_hour + r':' + r_minute + r'$'

            r_match = re.match(r_hour_minute, str(rep))
            if not r_match:
                continue

            hour, minute = map(int, r_match.groups())
            sequence[i] = TwentyFourHourClock(hour, minute)

        return sequence
