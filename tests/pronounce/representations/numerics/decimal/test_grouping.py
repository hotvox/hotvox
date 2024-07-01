'''
Test the Grouping representation
'''
from hotvox.pronounce.representations.literal import Literal
from hotvox.pronounce.representations.punctuation.terminal import Terminal
from hotvox.pronounce.representations.punctuation.pause import Pause
from hotvox.pronounce.representations.numerics.decimal.grouping \
    import \
        Grouping, _compress_literal, _get_polarity, _remove_polarity, \
        _get_decimal_index, _get_decimal_part, _remove_decimal_part, \
        _remove_delimiters, _is_valid_grouping_format
from hotvox.pronounce.sequence import Sequence

def test__compress_literal():
    '''
    Test the _compress_literal function.
    '''
    assert _compress_literal(Literal('0')) == Literal('0')
    assert _compress_literal(Literal('123')) == Literal('123')
    assert _compress_literal(Literal('123.456')) == Literal('123.456')
    assert _compress_literal(Literal('-123.456')) == Literal('-123.456')
    assert _compress_literal(Literal('-123,456')) == Grouping('-', '123456', None)
    assert _compress_literal(Literal('123,456')) == Grouping('', '123456', None)
    assert _compress_literal(Literal('123,456.789')) == Grouping('', '123456', '789')
    assert _compress_literal(Literal('-123,456.789')) == Grouping('-', '123456', '789')
    assert _compress_literal(Literal('8,019,876,189')) == Grouping('', '8019876189', None)

def test__get_polarity():
    '''
    Test the _get_polarity function.
    '''
    assert _get_polarity('0') == ''
    assert _get_polarity('-0') == '-'
    assert _get_polarity('123') == ''
    assert _get_polarity('-123') == '-'
    assert _get_polarity('123-') == ''
    assert _get_polarity('+123') == ''
    assert _get_polarity('123+') == ''

def test__remove_polarity():
    '''
    Test the _remove_polarity function.
    '''
    assert _remove_polarity('0') == '0'
    assert _remove_polarity('-0') == '0'
    assert _remove_polarity('123') == '123'
    assert _remove_polarity('-123') == '123'
    assert _remove_polarity('123-') == '123-'
    assert _remove_polarity('+123') == '+123'
    assert _remove_polarity('123+') == '123+'

def test__get_decimal_index():
    '''
    Test the _get_decimal_index function.
    '''
    assert _get_decimal_index('0') is None
    assert _get_decimal_index('-0') is None
    assert _get_decimal_index('123') is None
    assert _get_decimal_index('-123') is None
    assert _get_decimal_index('123-') is None
    assert _get_decimal_index('+123') is None
    assert _get_decimal_index('123+') is None
    assert _get_decimal_index('123.456') == 3
    assert _get_decimal_index('-123.456') == 4
    assert _get_decimal_index('123,456') is None
    assert _get_decimal_index('-123,456') is None
    assert _get_decimal_index('123,456.789') == 7
    assert _get_decimal_index('-123,456.789') == 8

def test__get_decimal_part():
    '''
    Test the _get_decimal_part function.
    '''
    assert _get_decimal_part('0') is None
    assert _get_decimal_part('-0') is None
    assert _get_decimal_part('123') is None
    assert _get_decimal_part('-123') is None
    assert _get_decimal_part('123-') is None
    assert _get_decimal_part('+123') is None
    assert _get_decimal_part('123+') is None
    assert _get_decimal_part('123.456') == '456'
    assert _get_decimal_part('-123.456') == '456'
    assert _get_decimal_part('123,456') is None
    assert _get_decimal_part('-123,456') is None
    assert _get_decimal_part('123,456.789') == '789'
    assert _get_decimal_part('-123,456.789') == '789'

def test__remove_decimal_part():
    '''
    Test the _remove_decimal_part function.
    '''
    assert _remove_decimal_part('0') == '0'
    assert _remove_decimal_part('-0') == '-0'
    assert _remove_decimal_part('123') == '123'
    assert _remove_decimal_part('-123') == '-123'
    assert _remove_decimal_part('123-') == '123-'
    assert _remove_decimal_part('+123') == '+123'
    assert _remove_decimal_part('123+') == '123+'
    assert _remove_decimal_part('123.456') == '123'
    assert _remove_decimal_part('-123.456') == '-123'
    assert _remove_decimal_part('123,456') == '123,456'
    assert _remove_decimal_part('-123,456') == '-123,456'
    assert _remove_decimal_part('123,456.789') == '123,456'
    assert _remove_decimal_part('-123,456.789') == '-123,456'

def test__remove_delimiters():
    '''
    Test the _remove_delimiters function.
    '''
    assert _remove_delimiters('0') == '0'
    assert _remove_delimiters('-0') == '-0'
    assert _remove_delimiters('123') == '123'
    assert _remove_delimiters('-123') == '-123'
    assert _remove_delimiters('123-') == '123-'
    assert _remove_delimiters('+123') == '+123'
    assert _remove_delimiters('123+') == '123+'
    assert _remove_delimiters('123.456') == '123.456'
    assert _remove_delimiters('-123.456') == '-123.456'
    assert _remove_delimiters('123,456') == '123456'
    assert _remove_delimiters('-123,456') == '-123456'
    assert _remove_delimiters('123,456.789') == '123456.789'
    assert _remove_delimiters('-123,456.789') == '-123456.789'

def test__is_valid_grouping_format():
    '''
    Test the _is_valid_grouping_format function.
    '''
    assert not _is_valid_grouping_format('0')
    assert not _is_valid_grouping_format('-0')
    assert not _is_valid_grouping_format('123')
    assert not _is_valid_grouping_format('-123')
    assert not _is_valid_grouping_format('123-')
    assert not _is_valid_grouping_format('+123')
    assert not _is_valid_grouping_format('123+')
    assert not _is_valid_grouping_format('123.456')
    assert not _is_valid_grouping_format('-123.456')
    assert _is_valid_grouping_format('1,234')
    assert not _is_valid_grouping_format('-1,234')
    assert _is_valid_grouping_format('12,345')
    assert not _is_valid_grouping_format('12,3456')
    assert _is_valid_grouping_format('123,456')
    assert not _is_valid_grouping_format('123,4567')
    assert _is_valid_grouping_format('1,234,567')
    assert not _is_valid_grouping_format('1,2,34567')

def test_compression():
    '''
    Test the compression of literals into groupings.
    '''
    string = "The population of Earth on Jan. 1, 2024 was 8,019,876,189 humans. "\
        + "While Canada only has 39,103,912, it is still a lot."
    sequence = Sequence.from_string(
        string,
        represent_for=Grouping
    )

    sequence_string = str(sequence)
    assert sequence_string == string

    # ensure that exactly two Groupings are in the sequence
    assert sum(1 for rep in sequence if isinstance(rep, Grouping)) == 2

def test___str__():
    '''
    Test the __str__ method.
    '''
    assert str(Grouping('', '0', None)) == '0'
    assert str(Grouping('-', '0', None)) == '-0'
    assert str(Grouping('', '0', '123')) == '0.123'
    assert str(Grouping('-', '0', '123')) == '-0.123'
    assert str(Grouping('', '123', None)) == '123'
    assert str(Grouping('-', '123', None)) == '-123'
    assert str(Grouping('', '123', '123')) == '123.123'
    assert str(Grouping('-', '123', '123')) == '-123.123'
    assert str(Grouping('', '123456', None)) == '123,456'
    assert str(Grouping('-', '123456', None)) == '-123,456'
    assert str(Grouping('', '123456', '123')) == '123,456.123'
    assert str(Grouping('-', '123456', '123')) == '-123,456.123'
    assert str(Grouping('', '123456789', None)) == '123,456,789'
    assert str(Grouping('-', '123456789', None)) == '-123,456,789'
    assert str(Grouping('', '123456789', '123')) == '123,456,789.123'
    assert str(Grouping('-', '123456789', '123')) == '-123,456,789.123'
