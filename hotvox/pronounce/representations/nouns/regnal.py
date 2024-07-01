'''
--- Wikipedia ---
https://en.wikipedia.org/wiki/Regnal_name  

A regnal name, regnant name, or reign name is the name used by monarchs and
popes during their reigns and subsequently, historically.

The regnal name is usually followed by a regnal number, written as a Roman 
numeral, to differentiate that monarch from others who have used the same
name while ruling the same realm. 
--- End of Wikipedia ---
'''
from hotvox.pronounce.representation import Representation
from hotvox.pronounce.representations.nouns.forename import Forename
from hotvox.pronounce.representations.numerics.roman.roman_numeral import RomanNumeral
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.utils.numbers import pronounce_ordinal

class Regnal(Representation):
    '''
    A Representation of a regnal name.
    '''

    def __init__(self, forename: Forename, roman_numeral: RomanNumeral) -> None:
        self.forename = forename
        self.roman_numeral = roman_numeral

    @staticmethod
    def defers_to() -> list[type]:
        '''
        Return the types that this representation defers to.
        '''
        return [ Forename, RomanNumeral ]

    @staticmethod
    def compress(sequence: Sequence) -> Sequence:
        new_sequence = Sequence()
        last_rep = None

        # loop through the sequence
        for rep in sequence:
            if  last_rep is not None and \
                isinstance(last_rep, Forename) and \
                isinstance(rep, RomanNumeral):

                # replace the last element (Forename) with a Regnal
                regnal = Regnal(last_rep, rep)
                new_sequence.pop()
                new_sequence.append(regnal)
                last_rep = regnal
            else:
                new_sequence.append(rep)
                last_rep = rep

        return new_sequence

    def pronounciation(self):
        '''
        Return the pronounciation of the roman numeral.
        '''
        return f'{self.forename.pronounciation()} the' + \
            f' {pronounce_ordinal(self.roman_numeral.integer).capitalize()}'
