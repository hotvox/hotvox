'''
Test the Regnal class.
'''
from hotvox.pronounce.representations.nouns.forename import Forename
from hotvox.pronounce.representations.nouns.regnal import Regnal
from hotvox.pronounce.representations.numerics.roman.roman_numeral import RomanNumeral
from hotvox.pronounce.sequence import Sequence

def test_compress():
    '''
    Test the _compress_literal function.
    '''
    sequence = Sequence.from_string(
        'Today is the first day of the MMXXIV century.' + \
        ' I will be meeting with the ghost of King George VI.' + \
        ' He was the father of Queen Elizabeth II.' + \
        ' George Washington probably would not have liked him.' + \
        ' The funny thing is, I played both yesteday in' + \
        ' Civiliation IV Beyond the Sword.',
        represent_for=Regnal
    )

    # ensure that there are two Regnal objects
    assert sequence.count_type(Regnal) == 2

    # ensure the first Regnal object is 'George VI'
    assert sequence.with_type(Regnal)[0].forename.string == 'George'

    # ensure the second Regnal object is 'Elizabeth II'
    assert sequence.with_type(Regnal)[1].forename.string == 'Elizabeth'

def test_pronounciation():
    '''
    Test the pronounciation method.
    '''
    assert Regnal(
        Forename('George'), RomanNumeral('VI')
    ).pronounciation() == 'George the Sixth'

    assert Regnal(
        Forename('Elizabeth'), RomanNumeral('II')
    ).pronounciation() == 'Elizabeth the Second'
