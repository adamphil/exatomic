# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Interpolation
################################
Hidden wrapper function that makes it convenient to choose
an interpolation scheme available in scipy.
"""

from scipy.interpolate import (interp1d, interp2d, griddata,
                               pchip_interpolate, krogh_interpolate,
                               barycentric_interpolate, Akima1DInterpolator,
                               CloughTocher2DInterpolator, RectBivariateSpline,
                               RegularGridInterpolator)
from scipy.signal import savgol_filter

def _interpolate(df, x, y, z, method, kind, yfirst, dim, minimum):
    # Check that columns are in df
    if len(set([x, y, z]) & set(df.columns)) != 3:
        raise Exception('{!r}, {!r} and {!r} must be in df.columns'.format(x, y, z))
    # Map the method to the function or class in scipy
    convenience = {'cloughtocher': CloughTocher2DInterpolator,
                    'barycentric': barycentric_interpolate,
                    'regulargrid': RegularGridInterpolator,
                      'bivariate': RectBivariateSpline,
                          'akima': Akima1DInterpolator,
                          'krogh': krogh_interpolate,
                          'pchip': pchip_interpolate,
                       'interp1d': interp1d,
                       'interp2d': interp2d,
                       'griddata': griddata}
    # Check that the interpolation method is supported
    if method not in convenience.keys():
        raise Exception('method must be in {}'.format(convenience.keys()))
    # Shape the data in df
    pivot = df.pivot(x, y, z)
    xdat = pivot.index.values
    ydat = pivot.columns.values
    zdat = pivot.values
    # New (x, y) values
    newx = np.linspace(xdat.min(), xdat.max(), dim)
    newy = np.linspace(ydat.min(), ydat.max(), dim)
    # Details of the implementation in scipy
    # First 5 are explicitly 2D interpolation
    if method == 'bivariate':
        interpz = convenience[method](xdat, ydat, zdat)
        newz = interpz(newx, newy).T
    elif method == 'interp2d':
        interpz = convenience[mehtod](xdat, ydat, zdat.T, kind=kind)
        newz = interpz(newx, newy)
    elif method in ['griddata', 'cloughtocher', 'regulargrid']:
        meshx, meshy = np.meshgrid(xdat, ydat)
        newmeshx, newmeshy = np.meshgrid(newx, newy)
        points = np.array([meshx.flatten(order='F'),
                           meshy.flatten(order='F')]).T
        newpoints = np.array([newmeshx.flatten(order='F'),
                              newmeshy.flatten(order='F')]).T
        if method == 'cloughtocher':
            interpz = convenience[method](points, zdat.flatten())
            newz = interpz(newpoints)
            newz = newz.reshape((dim, dim), order='F')
        elif method == 'regulargrid':
            interpz = convenience[method]((xdat, ydat), zdat)
            newz = interpz(newpoints)
            newz = newz.reshape((dim, dim), order='F')
        else:
            newz = convenience[method](points, zdat.flatten(), newpoints)
            newz = newz.reshape((dim, dim), order='F')
    # 1D interpolation applied across both x and y
else:
    # Not sure if we need this complexity but interesting to see if
    # the order of interpolation matters (based on method)
    newz = np.empty((dim, dim), dtype=np.float64)
    kwargs = {'kind': kind} if method == 'interp1d' else {}
    if yfirst:
        partz = np.empty((xdat.shape[0], dim), dtype=np.float64)
        if method in ['interp1d', 'akima']:
            for i in range(xdat.shape[0]):
                zfunc = convenience[method](ydat, zdat[i,:], **kwargs)
                partz[i] = zfunc(newy)
            for i in range(dim):
                zfunc = convenience[method](xdat, partz[:,i], **kwargs)
                newz[i,:] = zfunc(newy)
            newz = newz[::-1,::-1]
        else:
            for i in range(xdat.shape[0]):
                partz[i] = convenience[method](ydat, zdat[i,:], newy)
            for i in range(dim):
                newz[i,:] = convenience[method](xdat, partz[:,i], newx)
    else:
        partz = np.empty((ydat.shape[0], dim), dtype=np.float64)
        if method in ['interp1d', 'akima']:
            for i in range(ydat.shape[0]):
                zfunc = convenience[method](xdat, zdat[:,i], **kwargs)
                partz[i] = zfunc(newx)
            for i in range(dim):
                zfunc = convenience[method](ydat, partz[:,i], **kwargs)
                newz[:,i] = zfunc(newy)
        else:
            for i in range(ydat.shape[0]):
                partz[i] = convenience[method](xdat, zdat[:,i], newx)
            for i in range(dim):
                newz[:,i] = convenience[method](ydat, partz[:,i], newy)
    # Find minimum values for the interpolated data set
    minima = None
    if minimum:
        minima = np.empty((dim, 3), dtype=np.float64)
        window = dim - (1 - dim % 2)
        # Smooth this out as it can be quite jagged
        minima[1] = savgol_filter(minima[1], window, 3)
    return {'x': newx, 'y': newy, 'z': newz, 'min': minima}


# Sample of a wrapper around the hidden function for public API
def interpolate_j2(df, method='interp2d', kind='cubic', yfirst=False,
                   dim=21, minimum=False):
    """
    Given a dataframe containing alpha, gamma, j2 columns,
    return a dictionary for plotting.
    """
    interped = _interpolate(df, 'alpha', 'gamma', 'j2',
                            method, kind, yfirst, dim, minimum)
    for key, cart in [('alpha', 'x'), ('gamma', 'y'), ('j2', 'z')]:
        interped[key] = interped.pop(cart)
    return interped
