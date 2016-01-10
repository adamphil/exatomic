# -*- coding: utf-8 -*-

from linecache import getline
from atomic import _pd as pd
from atomic import _np as np
from atomic import _os as os
try:
    from atomic.algorithms.jitted import expand
except ImportError:
    from atomic.algorithms.nonjitted import expand

#Hacks?
from atomic.algorithms.nonjitted import generate_minimal_framedf_from_onedf as _gen_fdf
convert = 1.88973
columns = ['symbol', 'x', 'y', 'z']

def read_xyz(path, unit='A', metadata={}, **kwargs):
    '''
    Reads an xyz or xyz trajectory file

    Args
        path (str): file path
        unit (str): unit of atomic positions (optional - default 'A')
        metadata (dict): metadata as key, value pairs
        **kwargs: only if using with exa content management system

    Return
        unikws (dict): dataframes containing 'frame', 'one' body and 'meta' data

    See Also
        :class:`atomic.container.Universe`
    '''
    df = pd.read_csv(path, names=columns, delim_whitespace=True, skip_blank_lines=False)
    try:
        units = getline(path, 1).split()[1]
    except IndexError:
        units = unit
    frdxs = _index(df)
    comments = _comments(path, frdxs + 2)
    one = _parse_xyz(df, units, frdxs)
    frame = _gen_fdf(one)
    unikws = {
        'one': one,
        'frame': frame,
        'metadata': {'comments': comments, 'path': path}
    }
    unikws['metadata'].update(metadata)
    return unikws

def _index(df):
    vals = df['symbol'].values
    tot = len(vals)
    idxs = [0]
    cidx = int(vals[0]) + 2
    idxs.append(cidx)
    while cidx < tot:
        try:
            nidx = int(vals[cidx]) + 2
            cidx += nidx
            idxs.append(cidx)
        except ValueError:
            cidx += 1
    idxs.pop(-1)
    return np.array(idxs)

def _comments(path, cidxs):
    ret = ''
    for ln in cidxs:
        com = getline(path, ln)
        if com.strip():
            ret = ''.join([ret, str(ln), ':', com])
    return ret

def _parse_xyz(df, unit, frdxs):
    natdxs = np.array([int(df['symbol'].values[idx]) for idx in frdxs])
    frdx, odx, idxs = expand(frdxs + 2, natdxs)
    one = df.loc[df.index.isin(idxs), ['symbol', 'x', 'y', 'z']]
    one.loc[:, ['x', 'y', 'z']] = one.loc[:, ['x', 'y', 'z']].astype(float)
    if unit == 'A':
        one.loc[:, ['x', 'y', 'z']] *= convert
    one['frame'] = frdx
    one['one'] = odx
    one.set_index(['frame', 'one'], inplace=True)
    return one

def write_xyz(uni, path):
    pass
