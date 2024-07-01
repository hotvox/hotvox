'''
This file is used to test the pronounce function in the pronounce module.
'''
from hotvox.pronounce import pronounce

def test_pronounce():
    '''
    Test the pronounce function.
    '''
    assert pronounce('2') == 'Two'
