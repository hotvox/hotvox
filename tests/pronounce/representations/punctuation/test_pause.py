'''
Test the Pause representation
'''
from hotvox.pronounce.sequence import Sequence
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation.pause import Pause, \
    _compress_literal, _get_pause_string

def test__compress_literal():
    '''
    Test the _compress_literal function.
    '''
    assert _compress_literal(Literal('0')) == [Literal('0')]
    assert _compress_literal(Literal('Hello')) == [Literal('Hello')]
    for pause_string in [',']:
        assert _compress_literal(Literal(pause_string + 'Hello')) == \
            [Literal(pause_string +'Hello')]
        representations = _compress_literal(Literal('Hello' + pause_string))
        assert representations == [Literal('Hello'), Pause(pause_string)]
        assert representations[1].string == pause_string

def test__get_terminal_string():
    '''
    Test the _get_terminal_string function.
    '''
    assert _get_pause_string('Hello') is None
    for pause_string in [',']:
        assert _get_pause_string('Hello' + pause_string) == pause_string
        assert _get_pause_string(pause_string + 'Hello') is None

def test___compress__():
    '''
    Test the compression of literals into terminals.
    '''
    string = "Sometimes there is one problem, sometimes there are two, those give me pause."
    sequence = Sequence.from_string(string, represent_for=Pause)

    assert str(sequence) == string

    # Test that two Pause objects are in the sequence
    assert len([rep for rep in sequence if isinstance(rep, Pause)]) == 2
