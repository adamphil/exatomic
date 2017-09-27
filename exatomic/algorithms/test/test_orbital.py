## -*- coding: utf-8 -*-
## Copyright (c) 2015-2016, Exa Analytics Development Team
## Distributed under the terms of the Apache License 2.0
##"""
##Tests for building molecular orbitals
##"""
##<<<<<<< HEAD
##import numpy as np
##import pandas as pd
##
##from exa.test import UnitTester
##from exatomic.algorithms.orbital import (make_fps, solid_harmonics, clean_sh,
##                                         Nucpos, _sphr_prefac, _cart_prefac,
##                                         gen_basfn)
##
##class TestNucpos(UnitTester):
##    def setUp(self):
##        self.zeros = Nucpos(0, 0, 0)
##        self.nonzs = Nucpos(1, 2, 3)
##
##    def test_zero(self):
##        self.assertEqual(self.zeros.x, 'x')
##        self.assertEqual(self.zeros.y, 'y')
##        self.assertEqual(self.zeros.z, 'z')
##        self.assertEqual(self.zeros.r2, '(x**2+y**2+z**2)')
##
##    def  test_nonz(self):
##        self.assertEqual(self.nonzs.x, '(x-1.0000000000)')
##        self.assertEqual(self.nonzs.y, '(y-2.0000000000)')
##        self.assertEqual(self.nonzs.z, '(z-3.0000000000)')
##        self.assertEqual(self.nonzs.r2, '((x-1.0000000000)**2+(y-2.0000000000)**2+(z-3.0000000000)**2)')
##
##
##class TestMakeFps(UnitTester):
##    def setUp(self):
##        self.min = make_fps(-8, 8, 50)
##        self.all = make_fps(-8, 8, 50, nrfps=5,
##                            xmin=-4,  xmax=4,  nx=75,
##                            ymin=-6,  ymax=6,  ny=100,
##                            zmin=-10, zmax=10, nz=150)
##
##    def test_min(self):
##        self.assertEqual(self.min.nx[0], 50)
##        self.assertEqual(self.min.ny[0], 50)
##        self.assertEqual(self.min.nz[0], 50)
##        self.assertEqual(self.min.ox[0], -8)
##        self.assertEqual(self.min.oy[0], -8)
##        self.assertEqual(self.min.oz[0], -8)
##        self.assertEqual(self.min.dxi[0], 0.32)
##        self.assertEqual(self.min.dyj[0], 0.32)
##        self.assertEqual(self.min.dzk[0], 0.32)
##        self.assertEqual(self.min.dxj[0], 0)
##        self.assertEqual(self.min.dyk[0], 0)
##        self.assertEqual(self.min.dzi[0], 0)
##        self.assertEqual(self.min.dxk[0], 0)
##        self.assertEqual(self.min.dyi[0], 0)
##        self.assertEqual(self.min.dzj[0], 0)
##
##    def test_all(self):
##        self.assertEqual(self.all.shape, (5, 18))
##        self.assertEqual(self.all.nx[0], 75)
##        self.assertEqual(self.all.ny[0], 100)
##        self.assertEqual(self.all.nz[0], 150)
##        self.assertEqual(self.all.ox[0], -4)
##        self.assertEqual(self.all.oy[0], -6)
##        self.assertEqual(self.all.oz[0], -10)
##        self.assertTrue(np.isclose(self.all.dxi[0], 0.106667))
##        self.assertEqual(self.all.dyj[0], 0.12)
##        self.assertTrue(np.isclose(self.all.dzk[0], 0.133333))
##        self.assertEqual(self.all.dxj[0], 0)
##        self.assertEqual(self.all.dyk[0], 0)
##        self.assertEqual(self.all.dzi[0], 0)
##        self.assertEqual(self.all.dxk[0], 0)
##        self.assertEqual(self.all.dyi[0], 0)
##        self.assertEqual(self.all.dzj[0], 0)
##
##
##class TestCleanSH(UnitTester):
##    def setUp(self):
##        self.sh = clean_sh(solid_harmonics(3))
##
##    def test_clean(self):
##        self.assertEqual(self.sh[(0,  0)], [''])
##        self.assertEqual(self.sh[(1, -1)], ['{nuc.y}*'])
##        self.assertEqual(self.sh[(1,  0)], ['{nuc.z}*'])
##        self.assertEqual(self.sh[(1,  1)], ['{nuc.x}*'])
##        self.assertEqual(self.sh[(2, -2)], ['1.7320508076*{nuc.x}*{nuc.y}*'])
##        self.assertEqual(self.sh[(2, -1)], ['1.7320508076*{nuc.y}*{nuc.z}*'])
##        self.assertEqual(self.sh[(2,  1)], ['1.7320508076*{nuc.x}*{nuc.z}*'])
##        self.assertEqual(self.sh[(3, -2)], ['3.8729833462*{nuc.x}*{nuc.y}*{nuc.z}*'])
##
##
##class TestSphrPrefac(UnitTester):
##    def setUp(self):
##        self.csh = clean_sh(solid_harmonics(3))
##        self.nuc = Nucpos(0, 0, 0)
##
##    def test_sphr_prefac(self):
##        self.assertEqual(_sphr_prefac(self.csh, 0,  0, self.nuc), [''])
##        self.assertEqual(_sphr_prefac(self.csh, 1, -1, self.nuc), ['y*'])
##        self.assertEqual(_sphr_prefac(self.csh, 1,  0, self.nuc), ['z*'])
##        self.assertEqual(_sphr_prefac(self.csh, 1,  1, self.nuc), ['x*'])
##        self.assertEqual(_sphr_prefac(self.csh, 2, -2, self.nuc), ['1.7320508076*x*y*'])
##        self.assertEqual(_sphr_prefac(self.csh, 2, -1, self.nuc), ['1.7320508076*y*z*'])
##        self.assertEqual(_sphr_prefac(self.csh, 2,  1, self.nuc), ['1.7320508076*x*z*'])
##        self.assertEqual(_sphr_prefac(self.csh, 3, -2, self.nuc), ['3.8729833462*x*y*z*'])
##
##
##class TestCartPrefac(UnitTester):
##    def setUp(self):
##        self.org = Nucpos(0, 0, 0)
##        self.nor = Nucpos(0.5,0.5,0.5)
##
##    def test_cart_prefac(self):
##        self.assertEqual(_cart_prefac(0, 0, 0, 0, self.org), [''])
##        self.assertEqual(_cart_prefac(1, 1, 0, 0, self.org), ['x*'])
##        self.assertEqual(_cart_prefac(1, 0, 1, 0, self.org), ['y*'])
##        self.assertEqual(_cart_prefac(1, 0, 0, 1, self.org), ['z*'])
##        self.assertEqual(_cart_prefac(2, 2, 0, 0, self.org), ['x**2*'])
##        self.assertEqual(_cart_prefac(2, 1, 1, 0, self.org), ['x*y*'])
##        self.assertEqual(_cart_prefac(2, 1, 0, 1, self.org), ['x*z*'])
##        self.assertEqual(_cart_prefac(2, 0, 1, 1, self.org), ['y*z*'])
##        self.assertEqual(_cart_prefac(2, 0, 2, 0, self.org), ['y**2*'])
##        self.assertEqual(_cart_prefac(2, 0, 0, 2, self.org), ['z**2*'])
##        self.assertEqual(_cart_prefac(1, 1, 0, 0, self.nor), ['(x-0.5000000000)*'])
##        self.assertEqual(_cart_prefac(1, 0, 1, 0, self.nor), ['(y-0.5000000000)*'])
##        self.assertEqual(_cart_prefac(1, 0, 0, 1, self.nor), ['(z-0.5000000000)*'])
##        self.assertEqual(_cart_prefac(2, 2, 0, 0, self.nor), ['(x-0.5000000000)**2*'])
##        self.assertEqual(_cart_prefac(2, 1, 1, 0, self.nor), ['(x-0.5000000000)*(y-0.5000000000)*'])
##
##
##class TestGenBsfn(UnitTester):
##    def setUp(self):
##        self.uncontdf = pd.DataFrame.from_dict({'N': [1], 'd': [1], 'alpha': [1]})
##        self.contdf = pd.DataFrame.from_dict({'N': [1, 2], 'd': [1, 2], 'alpha': [1, 2]})
##        self.r2str = Nucpos(0,0,0).r2
##
##    def test_gen_basfn(self):
##        self.assertEqual(gen_basfn([''], self.uncontdf, self.r2str),
##                         '(1.00000000*1.00000000*np.exp(-1.00000000*(x**2+y**2+z**2)))')
##        self.assertEqual(gen_basfn([''], self.contdf, self.r2str),
##                         '(1.00000000*1.00000000*np.exp(-1.00000000*(x**2+y**2+z**2))+'
##                         '2.00000000*2.00000000*np.exp(-2.00000000*(x**2+y**2+z**2)))')
#=======
#import numpy as np
#import pandas as pd
#
#from exa.test import UnitTester
#from exatomic.algorithms.basis import clean_sh, solid_harmonics
#from exatomic.algorithms.orbital import (make_fps, _atompos, _sphr_prefac,
#                                         _cart_prefac, gen_basfn)
#
#class Testatompos(UnitTester):
#    def setUp(self):
#        self.zeros = _atompos(0,  0, 0)
#        self.nonzs = _atompos(1, -2, 3)
#        self.precs = _atompos(1, -2.1111111, 3, precision=4)
#
#    def test_zero(self):
#        self.assertEqual(self.zeros['x'], 'x')
#        self.assertEqual(self.zeros['y'], 'y')
#        self.assertEqual(self.zeros['z'], 'z')
#        self.assertEqual(self.zeros['r2'], '(x**2+y**2+z**2)')
#        self.assertEqual(self.zeros['r'], '(x**2+y**2+z**2)**0.5')
#
#    def  test_nonz(self):
#        self.assertEqual(self.nonzs['x'], '(x-1.)')
#        self.assertEqual(self.nonzs['y'], '(y+2.)')
#        self.assertEqual(self.nonzs['z'], '(z-3.)')
#        self.assertEqual(self.nonzs['r2'], '((x-1.)**2+(y+2.)**2+(z-3.)**2)')
#        self.assertEqual(self.nonzs['r'], '((x-1.)**2+(y+2.)**2+(z-3.)**2)**0.5')
#
#    def test_precs(self):
#        self.assertEqual(self.precs['y'], '(y+2.1111)')
#        self.assertEqual(self.precs['r2'], '((x-1.)**2+(y+2.1111)**2+(z-3.)**2)')
#
#
#class TestMakeFps(UnitTester):
#    def setUp(self):
#        self.min = make_fps(-8, 8, 50)
#        self.all = make_fps(-8, 8, 50, nrfps=5,
#                            xmin=-4,  xmax=4,  nx=75,
#                            ymin=-6,  ymax=6,  ny=100,
#                            zmin=-10, zmax=10, nz=150)
#
#    def test_min(self):
#        self.assertEqual(self.min.nx[0], 50)
#        self.assertEqual(self.min.ny[0], 50)
#        self.assertEqual(self.min.nz[0], 50)
#        self.assertEqual(self.min.ox[0], -8)
#        self.assertEqual(self.min.oy[0], -8)
#        self.assertEqual(self.min.oz[0], -8)
#        self.assertEqual(self.min.dxi[0], 0.32)
#        self.assertEqual(self.min.dyj[0], 0.32)
#        self.assertEqual(self.min.dzk[0], 0.32)
#        self.assertEqual(self.min.dxj[0], 0)
#        self.assertEqual(self.min.dyk[0], 0)
#        self.assertEqual(self.min.dzi[0], 0)
#        self.assertEqual(self.min.dxk[0], 0)
#        self.assertEqual(self.min.dyi[0], 0)
#        self.assertEqual(self.min.dzj[0], 0)
#
#    def test_all(self):
#        self.assertEqual(self.all.shape, (5, 18))
#        self.assertEqual(self.all.nx[0], 75)
#        self.assertEqual(self.all.ny[0], 100)
#        self.assertEqual(self.all.nz[0], 150)
#        self.assertEqual(self.all.ox[0], -4)
#        self.assertEqual(self.all.oy[0], -6)
#        self.assertEqual(self.all.oz[0], -10)
#        self.assertTrue(np.isclose(self.all.dxi[0], 0.106667))
#        self.assertEqual(self.all.dyj[0], 0.12)
#        self.assertTrue(np.isclose(self.all.dzk[0], 0.133333))
#        self.assertEqual(self.all.dxj[0], 0)
#        self.assertEqual(self.all.dyk[0], 0)
#        self.assertEqual(self.all.dzi[0], 0)
#        self.assertEqual(self.all.dxk[0], 0)
#        self.assertEqual(self.all.dyi[0], 0)
#        self.assertEqual(self.all.dzj[0], 0)
#
#
#class TestCleanSH(UnitTester):
#    def setUp(self):
#        self.sh = clean_sh(solid_harmonics(3))
#
#    def test_clean(self):
#        self.assertEqual(self.sh[(0,  0)], [''])
#        self.assertEqual(self.sh[(1, -1)], ['1.0*{y}*'])
#        self.assertEqual(self.sh[(1,  0)], ['1.0*{z}*'])
#        self.assertEqual(self.sh[(1,  1)], ['1.0*{x}*'])
#        self.assertEqual(self.sh[(2, -2)], ['1.73205080756888*{x}*{y}*'])
#        self.assertEqual(self.sh[(2, -1)], ['1.73205080756888*{y}*{z}*'])
#        self.assertEqual(self.sh[(2,  1)], ['1.73205080756888*{x}*{z}*'])
#        self.assertEqual(self.sh[(3, -2)], ['3.87298334620742*{x}*{y}*{z}*'])
#
#
#class TestSphrPrefac(UnitTester):
#    def setUp(self):
#        self.csh = clean_sh(solid_harmonics(3))
#        self.nuc = _atompos(0, 0.5, 0)
#
#    def test_sphr_prefac(self):
#        self.assertEqual(_sphr_prefac(self.nuc, self.csh, 0,  0), [''])
#        self.assertEqual(_sphr_prefac(self.nuc, self.csh, 1, -1), ['1.0*(y-0.5)*'])
#        self.assertEqual(_sphr_prefac(self.nuc, self.csh, 1,  0), ['1.0*z*'])
#        self.assertEqual(_sphr_prefac(self.nuc, self.csh, 1,  1), ['1.0*x*'])
#        self.assertEqual(_sphr_prefac(self.nuc, self.csh, 2, -2), ['1.73205080756888*x*(y-0.5)*'])
#        self.assertEqual(_sphr_prefac(self.nuc, self.csh, 2, -1), ['1.73205080756888*(y-0.5)*z*'])
#        self.assertEqual(_sphr_prefac(self.nuc, self.csh, 2,  1), ['1.73205080756888*x*z*'])
#        self.assertEqual(_sphr_prefac(self.nuc, self.csh, 3, -2), ['3.87298334620742*x*(y-0.5)*z*'])
#
#
#class TestCartPrefac(UnitTester):
#    def setUp(self):
#        self.org = _atompos(0, 0, 0)
#        self.nor = _atompos(0.5,0.5,0.5)
#
#    def test_cart_prefac(self):
#        self.assertEqual(_cart_prefac(self.org, '', 0, 0, 0, 0,), [''])
#        self.assertEqual(_cart_prefac(self.org, '', 1, 1, 0, 0,), ['x*'])
#        self.assertEqual(_cart_prefac(self.org, '', 1, 0, 1, 0,), ['y*'])
#        self.assertEqual(_cart_prefac(self.org, '', 1, 0, 0, 1,), ['z*'])
#        self.assertEqual(_cart_prefac(self.org, '', 2, 2, 0, 0,), ['x**2*'])
#        self.assertEqual(_cart_prefac(self.org, '', 2, 1, 1, 0,), ['x*y*'])
#        self.assertEqual(_cart_prefac(self.org, '', 2, 1, 0, 1,), ['x*z*'])
#        self.assertEqual(_cart_prefac(self.org, '', 2, 0, 1, 1,), ['y*z*'])
#        self.assertEqual(_cart_prefac(self.org, '', 2, 0, 2, 0,), ['y**2*'])
#        self.assertEqual(_cart_prefac(self.org, '', 2, 0, 0, 2,), ['z**2*'])
#        self.assertEqual(_cart_prefac(self.nor, '', 1, 1, 0, 0,), ['(x-0.5)*'])
#        self.assertEqual(_cart_prefac(self.nor, '', 1, 0, 1, 0,), ['(y-0.5)*'])
#        self.assertEqual(_cart_prefac(self.nor, '', 1, 0, 0, 1,), ['(z-0.5)*'])
#        self.assertEqual(_cart_prefac(self.nor, '', 2, 2, 0, 0,), ['(x-0.5)**2*'])
#        self.assertEqual(_cart_prefac(self.nor, '', 2, 1, 1, 0,), ['(x-0.5)*(y-0.5)*'])
#        self.assertEqual(_cart_prefac(self.nor, '1.0', 2, 1, 1, 0,), ['1.0*(x-0.5)*(y-0.5)*'])
#
#
#class TestGenBsfn(UnitTester):
#    def setUp(self):
#        self.uncontdf = pd.DataFrame.from_dict({'N': [1], 'd': [1], 'alpha': [1]})
#        self.contdf = pd.DataFrame.from_dict({'N': [1, 2], 'd': [1, 2], 'alpha': [1, 2]})
#        self.uncontdf['Nd'] = self.uncontdf['N'] * self.uncontdf['d']
#        self.contdf['Nd'] = self.contdf['N'] * self.contdf['d']
#        self.atom = _atompos(0,0,0)
#
#    def test_gen_basfn(self):
#        self.assertEqual(gen_basfn([''], self.uncontdf, self.atom['r2'], precision=0),
#                         '(1*exp(-1*(x**2+y**2+z**2)))')
#        self.assertEqual(gen_basfn([''], self.uncontdf, self.atom['r'], precision=1),
#                         '(1.0*exp(-1.0*(x**2+y**2+z**2)**0.5))')
#        self.assertEqual(gen_basfn([''], self.contdf, self.atom['r2'], precision=2),
#                         '(1.00*exp(-1.00*(x**2+y**2+z**2))+'
#                          '4.00*exp(-2.00*(x**2+y**2+z**2)))')
#>>>>>>> org/master
