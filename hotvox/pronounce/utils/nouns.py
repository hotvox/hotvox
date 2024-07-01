'''
Utility functions for getting popular forenames.
Note: male refers to assigned male at birth,
      female refers to assigned female at birth.
'''

import os

# https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/Names/femalenames-usa-top1000.txt
FILE_FEMALE =  'femalenames-usa-top1000.txt'

# https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/Names/malenames-usa-top1000.txt
FILE_MALE = 'malenames-usa-top1000.txt'

def get_forenames() -> list[str]:
    '''
    Return a list of popular forenames.
    '''
    return list(set(_get_list(FILE_MALE) + _get_list(FILE_FEMALE)))

def _get_list(file_name: str) -> list[str]:
    '''
    Return a list of forenames from a file.
    '''
    file_path = os.path.join(os.path.dirname(__file__), 'lists', file_name)
    return [line.strip() for line in open(file_path, 'r', encoding='utf-8').readlines()]
