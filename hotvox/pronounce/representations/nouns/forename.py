'''
integer.py
'''
from hotvox.pronounce.representation import Representation, CompressionError
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation import PUNCTUATION
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.utils.nouns import get_forenames

class Forename(Representation):
    '''
    A Representation of a forename also known as a first name or given name.
    '''

    def __init__(self, string: str) -> None:
        self.string = string

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        return PUNCTUATION

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        # get the forenames here so that we don't have to do IO multiple times
        # map the forenames to uppercase
        forenames = list(map(str.upper, get_forenames()))

        # loop through the sequence
        for i, rep in enumerate(sequence):
            if isinstance(rep, Literal):
                sequence[i] = _compress_literal(rep, forenames)

        return sequence

    def pronounciation(self):
        '''
        Return the pronounciation of the roman numeral.
        '''
        return self.string.capitalize()

def _compress_literal(literal: Literal, forenames: list[str]) -> Literal | Forename:
    if not isinstance(literal, Literal):
        raise CompressionError

    string = str(literal)
    if  _string_is_forename(string, forenames):
        return Forename(string)

    return literal

def _string_is_forename(string: str, forenames: list[str]) -> bool:
    '''
    Return True if the string is a forename.
    '''
    if len(string) < 2 or not string.isalpha() or \
        not string[0].isupper() or not string[1:].islower():
        print(
            'string:', string,
            'len:', len(string),
            'isalpha:', string.isalpha(),
            'first_upper:', string[0].isupper(),
            'rest_lower:', string[1:].islower()
        )
        return False

    return string.upper() in forenames
