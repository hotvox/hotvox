'''
pause.py
'''
from hotvox.pronounce.representation import Representation, CompressionError
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.representations.literal import Literal

class Pause(Representation):
    '''
    A Representation for pause punctuation (', ').
    '''

    def __init__(self, string: str) -> None:
        self.string = string

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        return [ Literal ]

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        '''
        Compression method for the Pause representation.
        '''
        new_sequence : Sequence = Sequence()
        for rep in sequence:
            if isinstance(rep, Literal):
                new_sequence.extend(_compress_literal(rep))
            else:
                new_sequence.append(rep)

        return new_sequence

    def is_space_before(self) -> bool:
        '''
        Return whether a space should be added before the representation.
        '''
        return False

    def pronounciation(self):
        return self.string

def _get_pause_string(string: str) -> bool:
    '''
    Return the terminal of the string.
    '''
    pauses = [',', ';']
    if string[-1] in pauses:
        return string[-1]
    return None

def _compress_literal(literal: Literal) -> list[Literal | Pause]:
    '''
    Compress a literal into a list of literals and pauses.
    '''
    if not isinstance(literal, Literal):
        raise CompressionError

    string = str(literal)
    if len(string) < 2:
        return [literal]

    pause_string = _get_pause_string(string)
    if pause_string is None:
        return [literal]

    return [Literal(string[:-1]), Pause(pause_string)]
