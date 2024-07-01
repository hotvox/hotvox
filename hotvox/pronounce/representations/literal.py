'''
literal.py
'''
from hotvox.pronounce.representation import Representation
from hotvox.pronounce.sequence import Sequence

class Literal(Representation):
    '''
    A Representation wrapper for a string.
    '''

    def __init__(self, string: str) -> None:
        self.string = string

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        return [ ]

    @staticmethod
    def compress(sequence: str) -> Sequence:
        '''
        Compress a string into a Sequence of literals.
        '''
        if not isinstance(sequence, str):
            raise ValueError("Sequence must be a single string")

        return Sequence([Literal(token) for token in sequence.split()])

    def pronounciation(self):
        return self.string
