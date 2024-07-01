'''
terminal.py
'''
from hotvox.pronounce.representation import Representation, CompressionError
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.representations.chronometry.twelve_hour_clock import TwelveHourClock
from hotvox.pronounce.representations.literal import Literal

class Terminal(Representation):
    '''
    A Representation for terminal punctuation ('. ', '! ', '? ').
    '''

    def __init__(self, string: str) -> None:
        self.string = string

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        return [ Literal, TwelveHourClock ]

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        '''
        Compression method for the Terminal representation.
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

    def capitalize_next(self) -> bool:
        '''
        Return whether the next representation should be capitalized.
        '''
        return True

    def pronounciation(self):
        return self.string

def _get_terminal_string(string: str) -> bool:
    '''
    Return the terminal of the string.
    '''
    terminals = ['.', '!', '?' ]
    if string[-1] in terminals:
        return string[-1]
    return None

def _compress_literal(literal: Literal) -> list[Literal | Terminal]:
    '''
    Compress a literal into a list of literals and terminals.
    '''
    if not isinstance(literal, Literal):
        raise CompressionError

    string = str(literal)
    if len(string) < 2:
        return [literal]

    terminal_string = _get_terminal_string(string)
    if terminal_string is None:
        return [literal]

    return [Literal(string[:-1]), Terminal(terminal_string)]
