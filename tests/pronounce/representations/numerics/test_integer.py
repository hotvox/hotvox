'''
Test the Integer representation
'''
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.numerics.decimal.grouping import Grouping
from hotvox.pronounce.representations.numerics.integer import Integer, \
    _compress_literal, _compress_grouping, _string_is_integer
from hotvox.pronounce.sequence import Sequence

def test__compress_literal():
    '''
    Test the _compress_literal function.
    '''
    assert _compress_literal(Literal('0')) == Integer('0')
    assert _compress_literal(Literal('123')) == Integer('123')
    assert _compress_literal(Literal('123.456')) == Literal('123.456')
    assert _compress_literal(Literal('-123.456')) == Literal('-123.456')
    assert _compress_literal(Literal('-123,456')) == Literal('-123,456')
    assert _compress_literal(Literal('123,456')) == Literal('123,456')
    assert _compress_literal(Literal('123456')) == Integer('123456')
    assert _compress_literal(Literal('8019876189')) == Integer('8019876189')

def test__compress_grouping():
    '''
    Test the _compress_grouping function.
    '''
    assert _compress_grouping(Grouping('', '0', None)) == Integer('0')
    assert _compress_grouping(Grouping('', '123', None)) == Integer('123')
    assert _compress_grouping(Grouping(None, '123', '456')) == Grouping(None, '123', '456')
    assert _compress_grouping(Grouping('-', '123', '456')) == Grouping('-', '123', '456')
    assert _compress_grouping(Grouping('', '123456', None)) == Integer('123456')
    assert _compress_grouping(Grouping('', '8019876189', None)) == Integer('8019876189')

def test__string_is_integer():
    '''
    Test the _string_is_integer function.
    '''
    assert _string_is_integer('0')
    assert _string_is_integer('123')
    assert not _string_is_integer('123.456')
    assert not _string_is_integer('-123.456')
    assert not _string_is_integer('-123,456')
    assert not _string_is_integer('123,456')
    assert _string_is_integer('123456')
    assert _string_is_integer('8019876189')

def test___compress__():
    '''
    Test the compression of literals and groupings into integers.
    '''
    string = "Here are 25 cookies, 3 cakes, and 1 pie. That is a lot in 2024. " + \
        "Canada's population of 39,103,912 would be happy for you to share."
    sequence = Sequence.from_string(string, represent_for=Integer)
    
    print('sequence: ', sequence)

    # ensure that exactly five Integers are in the sequence
    assert sum(1 for rep in sequence if isinstance(rep, Integer)) == 5

def test_pronounciation_cardinals():
    '''
    Test the pronounciation of cardinal numbers.
    '''
    cases = {
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

    for integer, pronounciation in cases.items():
        assert Integer(str(integer)).pronounciation() == pronounciation

def test_pronounciation_tens():
    '''
    Test the pronounciation of numbers < 100.
    '''
    cases = {
        21: 'twenty-one',
        25: 'twenty-five',
        32: 'thirty-two',
        58: 'fifty-eight',
        64: 'sixty-four',
        79: 'seventy-nine',
        83: 'eighty-three',
        99: 'ninety-nine'
    }

    for integer, pronounciation in cases.items():
        assert Integer(str(integer)).pronounciation() == pronounciation

def test_pronounciation_hundreds():
    '''
    Test the pronounciation of numbers < 1000.
    '''
    cases = {
        100: 'one hundred',
        200: 'two hundred',
        204: 'two hundred four',
        320: 'three hundred twenty',
        321: 'three hundred twenty-one',
        527: 'five hundred twenty-seven',
        765: 'seven hundred sixty-five',
    }

    for integer, pronounciation in cases.items():
        assert Integer(str(integer)).pronounciation() == pronounciation

def test_pronounciation_large_numbers():
    '''
    Test the pronounciation of numbers >= 1000.
    '''
    cases = {
        1000: 'one thousand',
        1004: 'one thousand four',
        1021: 'one thousand twenty-one',
        1100: 'one thousand one hundred',
        1107: 'one thousand one hundred seven',
        1873: 'one thousand eight hundred seventy-three',
        2024: 'two thousand twenty-four',
        5732: 'five thousand seven hundred thirty-two',
        10000: 'ten thousand',
        65535: 'sixty-five thousand five hundred thirty-five',
        100000: 'one hundred thousand',
        100123: 'one hundred thousand one hundred twenty-three',
        100999: 'one hundred thousand nine hundred ninety-nine',
        999999: 'nine hundred ninety-nine thousand nine hundred ninety-nine',
        1000000: 'one million',
        1000001: 'one million one',
        1000100: 'one million one hundred',
        1000999: 'one million nine hundred ninety-nine',
        1001000: 'one million one thousand',
        1001001: 'one million one thousand one',
        9999999: 'nine million nine hundred ninety-nine thousand nine hundred ninety-nine',
        1000000000: 'one billion',
        1000000001: 'one billion one',
        394234873200: 'three hundred ninety-four billion' + \
            ' two hundred thirty-four million' + \
            ' eight hundred seventy-three thousand' +
            ' two hundred',
        999999999999: 'nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999: 'nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999999: 'nine hundred ninety-nine quadrillion' + \
            ' nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999999999: 'nine hundred ninety-nine quintillion' + \
            ' nine hundred ninety-nine quadrillion' + \
            ' nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999999999999: 'nine hundred ninety-nine sextillion' + \
            ' nine hundred ninety-nine quintillion' + \
            ' nine hundred ninety-nine quadrillion' + \
            ' nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999999999999999: 'nine hundred ninety-nine septillion' + \
            ' nine hundred ninety-nine sextillion' + \
            ' nine hundred ninety-nine quintillion' + \
            ' nine hundred ninety-nine quadrillion' + \
            ' nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999999999999999999: 'nine hundred ninety-nine octillion' + \
            ' nine hundred ninety-nine septillion' + \
            ' nine hundred ninety-nine sextillion' + \
            ' nine hundred ninety-nine quintillion' + \
            ' nine hundred ninety-nine quadrillion' + \
            ' nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999999999999999999999: 'nine hundred ninety-nine nonillion' + \
            ' nine hundred ninety-nine octillion' + \
            ' nine hundred ninety-nine septillion' + \
            ' nine hundred ninety-nine sextillion' + \
            ' nine hundred ninety-nine quintillion' + \
            ' nine hundred ninety-nine quadrillion' + \
            ' nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999999999999999999999999: 'nine hundred ninety-nine decillion' + \
            ' nine hundred ninety-nine nonillion' + \
            ' nine hundred ninety-nine octillion' + \
            ' nine hundred ninety-nine septillion' + \
            ' nine hundred ninety-nine sextillion' + \
            ' nine hundred ninety-nine quintillion' + \
            ' nine hundred ninety-nine quadrillion' + \
            ' nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine',
        999999999999999999999999999999999999999: 'nine hundred ninety-nine undecillion' + \
            ' nine hundred ninety-nine decillion' + \
            ' nine hundred ninety-nine nonillion' + \
            ' nine hundred ninety-nine octillion' + \
            ' nine hundred ninety-nine septillion' + \
            ' nine hundred ninety-nine sextillion' + \
            ' nine hundred ninety-nine quintillion' + \
            ' nine hundred ninety-nine quadrillion' + \
            ' nine hundred ninety-nine trillion' + \
            ' nine hundred ninety-nine billion' + \
            ' nine hundred ninety-nine million' + \
            ' nine hundred ninety-nine thousand' + \
            ' nine hundred ninety-nine'
    }

    for integer, pronounciation in cases.items():
        assert Integer(str(integer)).pronounciation() == pronounciation
