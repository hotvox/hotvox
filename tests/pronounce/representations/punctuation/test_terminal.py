'''
Test the Terminal representation
'''
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation.terminal import Terminal, \
    _compress_literal, _get_terminal_string

def test__compress_literal():
    '''
    Test the _compress_literal function.
    '''
    assert _compress_literal(Literal('0')) == [Literal('0')]
    assert _compress_literal(Literal('Hello')) == [Literal('Hello')]
    for terminal_string in ['.', '!', '?']:
        assert _compress_literal(Literal(terminal_string + 'Hello')) == \
            [Literal(terminal_string +'Hello')]
        representations = _compress_literal(Literal('Hello' + terminal_string))
        assert representations == [Literal('Hello'), Terminal(terminal_string)]
        assert representations[1].string == terminal_string

def test__get_terminal_string():
    '''
    Test the _get_terminal_string function.
    '''
    assert _get_terminal_string('Hello') is None
    for terminal_string in ['.', '!', '?']:
        assert _get_terminal_string('Hello' + terminal_string) == terminal_string
        assert _get_terminal_string(terminal_string + 'Hello') is None

def test___compress__():
    '''
    Test the compression of literals into terminals.
    '''
    string = "Here are a few sentences. They are separated by terminal punctuation! How exciting?"
    sequence = Sequence.from_string(string, represent_for=Terminal)

    assert str(sequence) == string

    # Test that three Terminal objects are in the sequence
    assert len([rep for rep in sequence if isinstance(rep, Terminal)]) == 3
