'''
This module contains a list of classes in this module and submodules
'''
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.chronometry import CHRONOMETRY
from hotvox.pronounce.representations.punctuation import PUNCTUATION
from hotvox.pronounce.representations.nouns import NOUNS
from hotvox.pronounce.representations.numerics import NUMERICS

ALL_REPRESENTATIONS = [
    Literal,
] \
    + CHRONOMETRY \
    + NOUNS \
    + NUMERICS \
    + PUNCTUATION
