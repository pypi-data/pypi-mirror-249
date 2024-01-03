"""
General utilities.
"""

import os


def is_file(data: str = None) -> bool:
    """
    Check if it is a file or not.

    Parameter:
        data : str, file or string.

    Return:
        bool : if data is file or not.
    """
    if data is not None:
        if os.path.isfile(os.path.abspath(data)):
            return True
        else:
            return False
    else:
        return None


def prepare_string(string: str) -> list:
    """
    Prepare a string to a list.

    Parameter:
        string : str, data string.

    Return:
        List : list of strings.
    """
    lstring = string.split('\n')
    new_lstring = []
    for i in lstring:
        if i == '':
            new_lstring.append('\n')
        else:
            new_lstring.append(i + '\n')
    return new_lstring
