'''
representation.py
'''

class Representation:
    '''
    Base class for all representations in the project.
    '''

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        raise NotImplementedError

    @staticmethod
    def compress(sequence) -> list['Representation']:
        '''
        Compress a sequence of representations.
        '''
        raise NotImplementedError

    def is_space_before(self) -> bool:
        '''
        Return whether a space should be added after the representation.
        '''
        return True

    def capitalize_next(self) -> bool:
        '''
        Return whether the next representation should be capitalized.
        '''
        return False

    def pronounciation(self) -> str:
        '''
        Return the pronounciation of the representation.
        '''
        raise NotImplementedError

    def __str__(self) -> str:
        '''
        Return the representation as a string.
        '''
        return self.pronounciation()

    def __eq__(self, other: 'Representation') -> bool:
        '''
        Return whether the representation is equal to another.
        '''
        # return false if the types are different
        if self.__class__ != other.__class__:
            return False

        # return whether the string representations are equal
        # print("self: ", str(self))
        # print("other: ", str(other))
        # t_eq = str(self) == str(other)
        # print("t_eq: ", t_eq)
        return str(self) == str(other)

def is_ready(representer: type[Representation], represented_by: list[type]) -> bool:
    '''
    Return whether a representer is ready to compress a sequence.
    '''
    defers_to = representer.defers_to()
    for defer in defers_to:
        if defer not in represented_by:
            return False

    return True

def expand_defers_to(representer: type[Representation]) -> list[type]:
    '''
    Return the types that a representation defers to, including the types that
    those representations defer to.
    
    This is a recursive function.
    '''
    defers_to = representer.defers_to()
    expanded_defers_to = []
    for parent in defers_to:
        parent_defers_to = parent.defers_to()
        if parent_defers_to == []:
            expanded_defers_to.append(parent)
        else:
            expanded_defers_to += expand_defers_to(parent)
    # remove duplicates
    return list(set(defers_to + expanded_defers_to))

class CompressionError(Exception):
    '''
    An error that occurs when a representation fails to compress.
    '''

    def __init__(self, message: str | None = None) -> None:
        '''
        Initialize the error with a message.
        '''
        super().__init__("Failed to compress representation." if message is None else message)

class PronounciationError(Exception):
    '''
    An error that occurs when a representation fails to extract.
    '''

    def __init__(self, message: str | None = None) -> None:
        '''
        Initialize the error with a message.
        '''
        super().__init__("Failed to pronounce representation." if message is None else message)
