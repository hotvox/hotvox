'''
Test the Forename class and its associated functions.
'''
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.nouns.forename import Forename, \
    _compress_literal, _string_is_forename
from hotvox.pronounce.sequence import Sequence

forenames = list(map(str.upper, ['JACK', 'JAMES', 'JANE', 'JAKE', 'JILL', 'JOHN']))
other_nouns = ['dog', 'Dog', 'DOG', 'frankfurt', 'Frankfurt', 'FRANKFURT']
incorrect_case = ['jack', 'jAck', 'jACK', 'JACK']
correct_case = ['Jack', 'James', 'Jane', 'Jake', 'Jill', 'John']

def test__compress_literal():
    '''
    Test the _compress_literal function.
    '''
    for string in other_nouns:
        assert _compress_literal(Literal(string), forenames) == Literal(string)
    for string in incorrect_case:
        assert _compress_literal(Literal(string), forenames) == Literal(string)
    for string in correct_case:
        assert _compress_literal(Literal(string), forenames) == Forename(string)

def test__string_is_forename():
    '''
    Test the _string_is_forename function.
    '''
    for string in other_nouns:
        assert not _string_is_forename(string, forenames)
    for string in incorrect_case:
        assert not _string_is_forename(string, forenames)
    for string in correct_case:
        assert _string_is_forename(string, forenames)

def test_pronounciation():
    '''
    Test the pronounciation method.
    '''
    for string in correct_case:
        assert Forename(string).pronounciation() == string.capitalize()

def test_compress():
    '''
    Test the compress method.
    '''
    sequence = Sequence.from_string(
        'Jack and Jill climbed the Algonquin Park hill.',
        represent_for=Forename
    )

    # ensure that there are two Forename objects
    assert sequence.count_type(Forename) == 2

    # ensure the first Forename object is 'Jack'
    assert sequence.with_type(Forename)[0].string == 'Jack'

    # ensure the second Forename object is 'Jill'
    assert sequence.with_type(Forename)[1].string == 'Jill'
