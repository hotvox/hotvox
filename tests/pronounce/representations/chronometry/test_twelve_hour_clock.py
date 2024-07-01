'''
Test cases for the twelve_hour_clock module and its TwelveHourClock class.
'''
from hotvox.pronounce.representations.chronometry.twelve_hour_clock import TwelveHourClock, \
    _pronounce_hour, _pronounce_minute, _pronounce_period
from hotvox.pronounce.sequence import Sequence

def test__pronounce_hour():
    '''
    Test the _pronounce_hour function.
    '''
    assert _pronounce_hour(0) == 'twelve'
    assert _pronounce_hour(1) == 'one'
    assert _pronounce_hour(11) == 'eleven'
    assert _pronounce_hour(12) == 'twelve'
    assert _pronounce_hour(19) == 'seven'
    assert _pronounce_hour(23) == 'eleven'

def test__pronounce_minute():
    '''
    Test the _pronounce_minute function
    '''
    assert _pronounce_minute(0) == ''
    assert _pronounce_minute(1) == 'oh one'
    assert _pronounce_minute(9) == 'oh nine'
    assert _pronounce_minute(10) == 'ten'
    assert _pronounce_minute(59) == 'fifty-nine'

def test__pronounce_period():
    '''
    Test the _pronounce_period function.
    '''
    assert _pronounce_period(0) == 'in the early morning'
    assert _pronounce_period(5) == 'in the early morning'
    assert _pronounce_period(6) == 'in the morning'
    assert _pronounce_period(11) == 'in the morning'
    assert _pronounce_period(12) == 'in the afternoon'
    assert _pronounce_period(17) == 'in the afternoon'
    assert _pronounce_period(18) == 'in the evening'
    assert _pronounce_period(23) == 'in the evening'

def test_convert():
    '''
    Test the conversion of a TwelveHourClock sequence to its pronounciation.
    '''
    cases = {
        '12:00 AM': 'midnight',
        '12:04 A.M.': 'twelve oh four in the early morning',
        '12:59 am': 'twelve fifty-nine in the early morning',
        '1:24 a.m.': 'one twenty-four in the early morning',
        '7:30 AM': 'seven thirty in the morning',
        '11:59 AM': 'eleven fifty-nine in the morning',
        '12:00 PM': 'noon',
        '12:04 P.M.': 'twelve oh four in the afternoon',
        '12:59 pm': 'twelve fifty-nine in the afternoon',
        '1:24 p.m.': 'one twenty-four in the afternoon',
        '7:30 PM': 'seven thirty in the evening',
        '11:59 PM': 'eleven fifty-nine in the evening'
    }
    text_left = 'The time is '
    text_right = ', way past my bedtime!'
    for case, pronounciation in cases.items():
        sequence = Sequence.from_string(
            f'{text_left}{case}{text_right}',
            represent_for=TwelveHourClock
        )
        assert sequence.pronounciation() == f'{text_left}{pronounciation}{text_right}'
