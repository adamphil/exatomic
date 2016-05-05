# -*- coding: utf-8 -*-
'''
Field
============
'''
import numpy as np
from exa.numerical import Field


class AtomicField(Field):
    '''
    Class for storing atomic cube data (scalar field of 3D space). Note that
    this class follows the pattern established by the `cube file format`_.

    Note:
        Supports any shape "cube".

    .. _cube file format: http://paulbourke.net/dataformats/cube/
    '''
    _precision = 6
    _groupbys = ['frame']
    _categories = {'frame': np.int64, 'label': str, 'field_type': str}
    _traits = ['nx', 'ny', 'nz', 'ox', 'oy', 'oz', 'dxi', 'dxj', 'dxk',
               'dyi', 'dyj', 'dyk', 'dzi', 'dzj', 'dzk']
    _columns = ['nx', 'ny', 'nz', 'ox', 'oy', 'oz', 'dxi', 'dxj', 'dxk',
                'dyi', 'dyj', 'dyk', 'dzi', 'dzj', 'dzk', 'frame', 'label']

    def compute_dv(self):
        '''
        Compute the volume element for each field.

        Volume of a parallelpiped whose dimensions are :math:`\mathbf{a}`,
        :math:`\mathbf{b}`, :math:`\mathbf{c}` is given by:

        .. math::

            v = \\left|\\mathbf{a}\\cdot\\left(\\mathbf{b}\\times\\mathbf{c}\\right)\\right|

        Warning:
            Assumes parallelpiped (only type of field supported).
        '''
        def _dv(row):
            '''
            Helper function that performs the operation above.
            '''
            a = row[['dxi', 'dxj', 'dxk']].values.astype(np.float64)
            b = row[['dyi', 'dyj', 'dyk']].values.astype(np.float64)
            c = row[['dzi', 'dzj', 'dzk']].values.astype(np.float64)
            return np.dot(a, np.cross(b, c))
        self['dv'] = self.apply(_dv, axis=1)

    def integration(self):
        '''
        Check that field values are normalized.

        Computes the integral of the field values. For normalized fields (e.g
        orbitals), the result should be 1.

        .. math::

            \\int\\left|phi_{i}\\right|^{2}dV
        '''
        if 'dv' not in self:
            self.compute_dv()
        self['sums'] = [np.sum(fv**2) for fv in self.field_values]
        norm = self['dv'] * self['sums']
        del self['sums']
        return norm

    def rotate(self, a, b, angle):
        '''
        Unitary transformation of the discrete field.

        .. code-block:: Python

            newfield = myfield.rotate(0, 1, np.pi / 2)

        Args:
            a (int): Index of first field
            b (int): Index of second field
            angle (float): Angle of rotation

        Return:
            newfield (:class:`~atomic.field.AtomicField`): Rotated field values and data
        '''
        d0 = self.ix[a]
        d1 = self.ix[b]
        f0 = self.field_values[a]
        f1 = self.field_values[b]
        f = exa.Series(np.cos(angle) * f0 + np.sin(angle) * f1)
        return self.__class__(f, d0)
