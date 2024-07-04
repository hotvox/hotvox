'''
This module provides a function to transform a string into a form
easily pronounced by a voice assistant.
'''
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.representations import ALL_REPRESENTATIONS

def pronounce(string: str) -> str:
    '''
    Transform a string into a sequence of representations.
    '''
    sequence = Sequence.from_string(string, represent_with=ALL_REPRESENTATIONS)
    return sequence.pronounciation()
