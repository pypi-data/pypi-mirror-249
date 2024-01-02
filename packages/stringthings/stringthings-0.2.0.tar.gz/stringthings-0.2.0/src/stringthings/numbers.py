# -*-coding: utf-8 -*-
"""
Created on Mon Jan 01 13:53:33 2024

@author: Martín Araya
"""

__all__ = ['is_numeric', 'get_number']


def is_numeric(string):
    """
    returns True if the string is a number
    """
    # assert type(string) is str
    try:
        float(string)
        return True
    except:
        return False


def get_number(string):
    """
    returns the number, as integer or float, contained in a string
    """
    if is_numeric(string):
        try:
            return int(string)
        except:
            return float(string)
