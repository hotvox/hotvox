'''
Test the Literal representation
'''
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.numerics.roman.roman_numeral import RomanNumeral, \
    _compress_literal, _string_is_roman_numeral
from hotvox.pronounce.sequence import Sequence

def test__compress_literal():
    '''
    Test the _compress_literal method.
    '''
    assert not  isinstance(_compress_literal(Literal('hello')), RomanNumeral)
    assert not  isinstance(_compress_literal(Literal('max')),   RomanNumeral)
    assert not  isinstance(_compress_literal(Literal('I')),     RomanNumeral)
    assert      isinstance(_compress_literal(Literal('V')),     RomanNumeral)
    assert      isinstance(_compress_literal(Literal('X')),     RomanNumeral)
    assert      isinstance(_compress_literal(Literal('XIV')),   RomanNumeral)

def test__string_is_roman_numeral():
    '''
    Test the _string_is_roman_numeral method.
    '''
    assert not _string_is_roman_numeral('hello')
    assert not _string_is_roman_numeral('max')
    assert not _string_is_roman_numeral('I')
    assert     _string_is_roman_numeral('V')
    assert     _string_is_roman_numeral('X')
    assert     _string_is_roman_numeral('XIV')

def test_compression():
    '''
    Test the compression of string into literals and roman numerals.
    '''
    string = "In MMXXIV, I had the pleasure of meeting V humans and XIV dogs."
    sequence = Sequence.from_string(string, represent_for=RomanNumeral)

    sequence_string = str(sequence)
    assert sequence_string == "In two thousand twenty-four," + \
        " I had the pleasure of meeting five humans and fourteen dogs."

    # Ensure exactly one RomanNumeral was created
    assert sequence.count_type(RomanNumeral) == 3

    # Ensure the RomanNumeral is 'II'
    assert sequence.with_type(RomanNumeral)[0].string == 'MMXXIV'
    assert sequence.with_type(RomanNumeral)[0].integer == 2024
    assert sequence.with_type(RomanNumeral)[1].string == 'V'
    assert sequence.with_type(RomanNumeral)[1].integer == 5
    assert sequence.with_type(RomanNumeral)[2].string == 'XIV'
    assert sequence.with_type(RomanNumeral)[2].integer == 14
