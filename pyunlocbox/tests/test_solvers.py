#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test suite for the functions module of the pyunlocbox package.
"""

import unittest
import numpy as np
import numpy.testing as nptest
from pyunlocbox import functions, solvers


class FunctionsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_forward_backward_fista(self):
        """
        Test FISTA algorithm of forward-backward solver with L1-norm, L2-norm
        and dummy functions.
        """
        y = [4, 5, 6, 7]
        x0 = np.zeros(len(y))
        solver = solvers.forward_backward(method='FISTA')
        param = {'x0': x0, 'solver': solver}
        param['absTol'] = 1e-5
        param['verbosity'] = 'none'

        # L2-norm prox and dummy gradient.
        f1 = functions.norm_l2(y=y)
        f2 = functions.dummy()
        sol = [3.99996922, 4.99996153, 5.99995383, 6.99994614]
        ret = solvers.solve([f1, f2], **param)
        nptest.assert_allclose(ret['sol'], sol)
        self.assertEqual(ret['crit'], 'ABS_TOL')
        self.assertEqual(ret['niter'], 10)

        # Dummy prox and L2-norm gradient.
        f1 = functions.dummy()
        f2 = functions.norm_l2(y=y, lambda_=0.6)
        sol = [3.99867319, 4.99834148, 5.99800978, 6.99767808]
        ret = solvers.solve([f1, f2], **param)
        nptest.assert_allclose(ret['sol'], sol)
        self.assertEqual(ret['crit'], 'ABS_TOL')
        self.assertEqual(ret['niter'], 10)

        # L2-norm prox and L2-norm gradient.
        f1 = functions.norm_l2(y=y)
        f2 = functions.norm_l2(y=y)
        sol = [3.99904855, 4.99881069, 5.99857282, 6.99833496]
        ret = solvers.solve([f1, f2], **param)
        nptest.assert_allclose(ret['sol'], sol)
        self.assertEqual(ret['crit'], 'MAX_IT')

        # L1-norm prox and dummy gradient.
        f1 = functions.norm_l1(y=y)
        f2 = functions.dummy()
        sol = y
        ret = solvers.solve([f1, f2], **param)
        nptest.assert_allclose(ret['sol'], sol)
        self.assertEqual(ret['crit'], 'ABS_TOL')
        self.assertEqual(ret['niter'], 6)

        # Dummy prox and L1-norm gradient. As L1-norm possesses no gradient,
        # the algorithm exchanges the functions : exact same solution.
        f1 = functions.dummy()
        f2 = functions.norm_l1(y=y)
        sol = y
        ret = solvers.solve([f1, f2], **param)
        nptest.assert_allclose(ret['sol'], sol)
        self.assertEqual(ret['crit'], 'ABS_TOL')
        self.assertEqual(ret['niter'], 6)

        # L1-norm prox and L1-norm gradient. L1-norm possesses no gradient.
        f1 = functions.norm_l1(y=y)
        f2 = functions.norm_l1(y=y)
        self.assertRaises(ValueError, solvers.solve, [f1, f2], **param)

        # L1-norm prox and L2-norm gradient.
        f1 = functions.norm_l1(y=y, lambda_=1.0)
        f2 = functions.norm_l2(y=y, lambda_=0.8)
        sol = y
        ret = solvers.solve([f1, f2], **param)
        nptest.assert_allclose(ret['sol'], sol)
        self.assertEqual(ret['crit'], 'ABS_TOL')
        self.assertEqual(ret['niter'], 4)

    def test_forward_backward_ista(self):
        """
        Test ISTA algorithm of forward-backward solver with L1-norm, L2-norm
        and dummy functions. Test the effect of gamma and lambda parameters.
        """
        y = [4, 5, 6, 7]
        x0 = np.zeros(len(y))
        # Smaller step size and update rate --> slower convergence.
        solver = solvers.forward_backward(method='ISTA', gamma=.8, lambda_=.5)
        param = {'x0': x0, 'solver': solver}
        param['absTol'] = 1e-5
        param['verbosity'] = 'none'

        # L2-norm prox and dummy gradient.
        f1 = functions.norm_l2(y=y)
        f2 = functions.dummy()
        sol = [3.99915094, 4.99893867, 5.9987264, 6.99851414]
        ret = solvers.solve([f1, f2], **param)
        nptest.assert_allclose(ret['sol'], sol)
        self.assertEqual(ret['crit'], 'ABS_TOL')
        self.assertEqual(ret['niter'], 23)

        # L1-norm prox and L2-norm gradient.
        f1 = functions.norm_l1(y=y, lambda_=1.0)
        f2 = functions.norm_l2(y=y, lambda_=0.8)
        sol = [3.99999825, 4.9999979, 5.99999756, 6.99999723]
        ret = solvers.solve([f1, f2], **param)
        nptest.assert_allclose(ret['sol'], sol)
        self.assertEqual(ret['crit'], 'ABS_TOL')
        self.assertEqual(ret['niter'], 21)

suite = unittest.TestLoader().loadTestsFromTestCase(FunctionsTestCase)


def run():
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    run()