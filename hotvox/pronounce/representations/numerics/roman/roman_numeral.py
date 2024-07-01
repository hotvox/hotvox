'''
integer.py
'''
from hotvox.pronounce.representation import Representation, CompressionError
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation import PUNCTUATION
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.utils.numbers import pronounce_number

class RomanNumeral(Representation):
    '''
    A Representation of a roman numeral.
    '''

    def __init__(self, string: str) -> None:
        self.string = string
        self.integer = _roman_numeral_to_int(string)

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        return PUNCTUATION

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        # loop through the sequence
        for i, rep in enumerate(sequence):
            if isinstance(rep, Literal):
                sequence[i] = _compress_literal(rep)

        return sequence

    def pronounciation(self):
        '''
        Return the pronounciation of the roman numeral.
        '''
        return pronounce_number(self.integer)

def _compress_literal(literal: Literal) -> Literal | RomanNumeral:
    if not isinstance(literal, Literal):
        raise CompressionError

    string = str(literal)
    if _string_is_roman_numeral(string):
        return RomanNumeral(string)

    return literal

def _string_is_roman_numeral(string: str) -> bool:
    '''
    Determine if a one-word string is a roman numeral.
    '''
    # This is a common word that not often used in English
    # as a roman numeral. Usually these start at 2.
    if string == 'I':
        return False

    valid_letters = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
    for letter in string:
        if letter not in valid_letters:
            return False

    return True

def _roman_numeral_to_int(string: str) -> int:
    '''
    Convert a roman numeral to an integer.
    '''
    roman_numerals = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    # reverse the string
    string = string[::-1]

    total = 0
    last_value = 0
    for letter in string:
        value = roman_numerals[letter]
        if value < last_value:
            total -= value
        else:
            total += value
            last_value = value

    return total