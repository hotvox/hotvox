'''
integer.py
'''
from hotvox.pronounce.representation import Representation, CompressionError
from hotvox.pronounce.representations.chronometry import CHRONOMETRY
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation import PUNCTUATION
from hotvox.pronounce.representations.numerics.decimal.grouping import Grouping
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.utils.numbers import pronounce_number

class Integer(Representation):
    '''
    A Representation of an integer.
    '''

    def __init__(self, integer: str) -> None:
        self.integer = int(integer)

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        return PUNCTUATION + CHRONOMETRY + [ Grouping ]

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        # loop through the sequence
        for i, rep in enumerate(sequence):
            if isinstance(rep, Literal):
                sequence[i] = _compress_literal(rep)
            elif isinstance(rep, Grouping):
                sequence[i] = _compress_grouping(rep)

        return sequence

    def pronounciation(self):
        '''
        Return the pronounciation of the integer.
        '''
        return pronounce_number(self.integer)


def _compress_literal(literal: Literal) -> Literal | Integer:
    if not isinstance(literal, Literal):
        raise CompressionError

    string = str(literal)
    if _string_is_integer(string):
        return Integer(string)

    return literal

def _compress_grouping(grouping: Grouping) -> Grouping:
    if grouping.decimal_part is not None:
        return grouping

    return Integer(f'{grouping.polarity}{grouping.integer_part}')

def _string_is_integer(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False
