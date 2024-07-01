'''
A module for the Sequence class.
'''
from hotvox.pronounce.representation import Representation, is_ready as representer_is_ready, expand_defers_to

class Sequence(list[Representation]):
    '''
    A wrapper for a list of Representations.
    '''

    def count_type(self, representation: type) -> int:
        '''
        Return the number of representations of a given type in the Sequence.
        '''
        return sum(1 for rep in self if isinstance(rep, representation))

    def with_type(self, representation: type) -> list[Representation]:
        '''
        Return a list of representations of a given type in the Sequence.
        '''
        return [rep for rep in self if isinstance(rep, representation)]

    @ staticmethod
    def from_string(
            string: str,
            represent_with: list[type[Representation]] = None,
            represent_for: type[Representation] = None,
            sequence: 'Sequence' = None,
            represented_by: list[type[Representation]] = None
        ) -> 'Sequence':
        '''
        Create a Sequence from a string.
        '''
        if represent_with is None:
            if represent_for is None:
                raise SequenceRepresentationError("No representations are provided."\
                    + " try ALL from hotvox.pronounce.representations, or setting"\
                    + " represent_for to get the minimum requirements for the sequence.")
            represent_with = [represent_for] + expand_defers_to(represent_for)

        if represented_by is None:
            represented_by = []

        if sequence is None:
            sequence = string

        # queued_representers = represent_with - represented_by
        # TypeError: unsupported operand type(s) for -: 'list' and 'list'
        queued_representers = [rep for rep in represent_with if rep not in represented_by]

        ready_representers = []
        for representer in queued_representers:
            if representer_is_ready(representer, represented_by):
                ready_representers.append(representer)

        if len(ready_representers) == 0:
            raise SequenceRepresentationError("No representations are ready" \
                + " to compress the sequence." \
                + f" {queued_representers} are stuck.")

        for representer in ready_representers:
            sequence = representer.compress(sequence)
            represented_by.append(representer)

        # If the sequence is compressed by all compressors, return it
        if len(represent_with) == len(represented_by):
            return sequence

        return Sequence.from_string(
            string,
            represent_with=represent_with,
            represent_for=None,
            sequence=sequence,
            represented_by=represented_by
        )

    def pronounciation(self) -> str:
        '''
        Return the string representation of the Sequence.
        '''
        string = ''
        previous_rep = None
        for i, rep in enumerate(self):
            if i != 0 and rep.is_space_before():
                string += ' '

            if i == 0 or (previous_rep is not None and previous_rep.capitalize_next()):
                string += rep.pronounciation().capitalize()
            else:
                string += rep.pronounciation()

            previous_rep = rep

        return string


    def __str__(self) -> str:
        '''
        Return the string representation of the Sequence.
        '''
        string = ''
        for i, rep in enumerate(self):
            if i != 0 and rep.is_space_before():
                string += ' '
            string += str(rep)

        return string

class SequenceRepresentationError(Exception):
    '''
    An error that occurs when a sequence fails to compress.
    '''

    def __init__(self, message: str | None = None) -> None:
        '''
        Initialize the error with a message.
        '''
        super().__init__("Failed to represent sequence." if message is None else message)
