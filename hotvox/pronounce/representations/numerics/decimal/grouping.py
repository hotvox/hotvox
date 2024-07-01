'''
grouping.py
'''
from hotvox.pronounce.representation import Representation, CompressionError
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation import PUNCTUATION

class Grouping(Representation):
    '''
    Grouping representation.
    '''

    def __init__(self, polarity, integer_part, decimal_part) -> None:
        self.polarity = polarity
        self.integer_part = int(integer_part)
        self.decimal_part = None if decimal_part is None else int(decimal_part)

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

    def __str__(self) -> str:
        if self.decimal_part is not None:
            return f'{self.polarity}{self.integer_part:,}.{self.decimal_part}'

        return f'{self.polarity}{self.integer_part:,}'

def _compress_literal(literal: Literal) -> Literal | Grouping:
    if not isinstance(literal, Literal):
        raise CompressionError

    string = str(literal)
    without_polarity = _remove_polarity(string)
    without_decimal_part = _remove_decimal_part(without_polarity)
    valid_grouping_format = _is_valid_grouping_format(
        without_decimal_part
    )

    if not valid_grouping_format:
        return literal

    return Grouping(
        _get_polarity(string),
        _remove_delimiters(without_decimal_part),
        _get_decimal_part(without_polarity)
    )

def _get_polarity(string: str) -> str:
    '''
    Return the polarity of the string.
    '''
    if string[0] == '-':
        return '-'
    return ''

def _remove_polarity(string: str) -> str:
    '''
    Remove the polarity of the string.
    '''
    return string[1:] if _get_polarity(string) != '' else string

def _get_decimal_index(string: str) -> int:
    '''
    Return the index of the decimal point in the string.
    '''
    if '.' in string:
        return string.index('.')
    return None

def _get_decimal_part(string: str) -> str:
    '''
    Return the decimal part of the string.
    '''
    index = _get_decimal_index(string)
    if index is not None:
        # this will return the decimal part without the dot
        return string[index + 1:]
    return None

def _remove_decimal_part(string: str) -> str:
    '''
    Remove the decimal part of the string.
    '''
    index = _get_decimal_index(string)
    if index is not None:
        return string[:index]
    return string

def _remove_delimiters(string: str) -> str:
    '''
    Remove the delimiters from the string.
    '''
    return string.replace(',', '')

def _is_valid_grouping_format(string: str) -> bool:
    '''
    Check if the string is a valid grouping format.
    True:
        - 1,000
        - 10,000
        - 100,000
        - 1,000,000
    False:
        - 1,00
        - 10,00
        - 100,00
        - 1,0000
    '''
    if len(string) < 4:
        return False

    if string.count(',') == 0:
        return False

    if '.' in string:
        return False

    for i in range(len(string) - 1, -1, -1):
        r_index = len(string) - i - 1
        if string[i] == ',':
            if r_index % 4 != 3:
                return False
        elif not string[i].isdigit():
            return False

    return True
