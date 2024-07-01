'''
Test cases for the TwentyFourHourClock representation.
'''
from hotvox.pronounce.representations.chronometry.twenty_four_hour_clock import TwentyFourHourClock
from hotvox.pronounce.sequence import Sequence

def test_convert():
    '''
    Test the conversion of a TwentyFourHourClock sequence to its pronounciation
    '''
    cases = {
        '00:00': 'midnight',
        '00:01': 'twelve oh one in the early morning',
        '01:00': 'one o\'clock in the early morning',
        '01:01': 'one oh one in the early morning',
        '11:11': 'eleven eleven in the morning',
        '12:00': 'noon',
        '12:01': 'twelve oh one in the afternoon',
        '13:00': 'one o\'clock in the afternoon',
        '13:01': 'one oh one in the afternoon',
        '23:59': 'eleven fifty-nine in the evening'
    }
    text_left = 'The time is '
    text_right = ', way past my bedtime!'
    for case, pronounciation in cases.items():
        sequence = Sequence.from_string(
            f'{text_left}{case}{text_right}',
            represent_for=TwentyFourHourClock
        )
        assert sequence.pronounciation() == f'{text_left}{pronounciation}{text_right}'
