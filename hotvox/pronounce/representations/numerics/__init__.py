'''
This module contains a list of classes in this module and submodules.
'''
from hotvox.pronounce.representations.numerics.decimal import DECIMAL
from hotvox.pronounce.representations.numerics.integer import Integer
from hotvox.pronounce.representations.numerics.roman import ROMAN

NUMERICS = [
    Integer
] + DECIMAL + ROMAN
