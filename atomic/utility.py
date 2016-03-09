# -*- coding: utf-8 -*-
'''
Helper Functions
====================
Require internal imports.
'''
from operator import itemgetter
from exa.utility import mkpath
from exa.error import MissingColumns


def check(universe):
    '''
    '''
    rfc = ['rx', 'ry', 'rz', 'ox', 'oy', 'oz']    # Required columns in the Frame table for periodic calcs
    if 'periodic' in universe.frames.columns:
        if any(universe.frames['periodic'] == True):
            missing = set(rfc).difference(universe.frames.columns)
            if missing:
                raise MissingColumns(missing, universe.frames.__class__.__name__)
            return True
    return False


def formula_dict_to_string(fdict):
    '''
    '''
    return ''.join([k + '(' + str(fdict[k]) + ')' for k in sorted(fdict, key=itemgetter(0))])
