# -*-coding: utf-8 -*-
"""
Created on Mon Jan 01 13:53:33 2024

@author: Martín Araya
"""

__version__ = "0.2.0"
__release__ = 20240101

from .dates import date, is_date
from .numbers import is_numeric, get_number
from .splits import multisplit, split_dmmmy
from .compression import expand, compress
from .filenames import extension

__all__ = ['multisplit',
           'split_dmmmy', 'date', 'is_date',
           'is_numeric', 'get_number',
           'expand', 'compress',
           'extension']
