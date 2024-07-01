'''
Test the Literal representation
'''
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.representations.literal import Literal

def test___init__():
    '''
    Test the __init__ method.
    '''
    string = "hello"

    instance = Literal(string)
    assert instance.string == string
    assert str(instance) == string

    compressed = Literal.compress(string)
    assert len(compressed) == 1
    assert str(compressed[0]) == str(instance)

def test_compression():
    '''
    Test the compression of string into literals.
    '''
    string = "hello world, how are you?"
    sequence = Sequence.from_string(string, represent_for=Literal)
    assert len(sequence) == len(string.split())
    for i, literal in enumerate(sequence):
        assert str(literal) == string.split()[i]
