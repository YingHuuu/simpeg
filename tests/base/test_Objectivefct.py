from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import numpy as np
import scipy.sparse as sp
import unittest

from SimPEG import ObjectiveFunction
from SimPEG import Utils

np.random.seed(130)

class Empty_ObjFct(ObjectiveFunction.BaseObjectiveFunction):

    def __init__(self):
        super(Empty_ObjFct, self).__init__()


class TestBaseObjFct(unittest.TestCase):

    def test_derivs(self):
        objfct = ObjectiveFunction.L2ObjectiveFunction()
        self.assertTrue(objfct.test())

    def test_scalarmul(self):
        scalar = 10.
        nP = 100
        objfct_a = ObjectiveFunction.L2ObjectiveFunction(
            W=Utils.sdiag(np.random.randn(nP))
        )
        objfct_b = scalar * objfct_a
        m = np.random.rand(nP)

        objfct_c = objfct_a + objfct_b

        self.assertTrue(scalar * objfct_a(m) == objfct_b(m))
        self.assertTrue(objfct_b.test())
        self.assertTrue(objfct_c(m) == objfct_a(m) + objfct_b(m))

        self.assertTrue(len(objfct_c.objfcts) == 2)
        self.assertTrue(len(objfct_c.multipliers) == 2)
        self.assertTrue(len(objfct_c) == 2)

    def test_sum(self):
        scalar = 10.
        nP = 100.
        objfct = (
            ObjectiveFunction.L2ObjectiveFunction(W=sp.eye(nP)) +
            scalar * ObjectiveFunction.L2ObjectiveFunction(W=sp.eye(nP))
        )
        self.assertTrue(objfct.test())

        self.assertTrue(np.all(objfct.multipliers == np.r_[1., scalar]))

    def test_2sum(self):
        nP = 80
        alpha1 = 100
        alpha2 = 200

        phi1 = (
            ObjectiveFunction.L2ObjectiveFunction(W=Utils.sdiag(np.random.rand(nP))) +
            alpha1 * ObjectiveFunction.L2ObjectiveFunction()
        )
        phi2 = ObjectiveFunction.L2ObjectiveFunction() + alpha2 * phi1
        self.assertTrue(phi2.test())

        self.assertTrue(len(phi1.multipliers) == 2)
        self.assertTrue(len(phi2.multipliers) == 2)

        self.assertTrue(len(phi1.objfcts) == 2)
        self.assertTrue(len(phi2.objfcts) == 2)
        self.assertTrue(len(phi2) == 2)

        self.assertTrue(len(phi1) == 2)
        self.assertTrue(len(phi2) == 2)

        self.assertTrue(np.all(phi1.multipliers == np.r_[1., alpha1]))
        self.assertTrue(np.all(phi2.multipliers == np.r_[1., alpha2]))


    def test_3sum(self):
        nP = 90

        alpha1 = 0.3
        alpha2 = 0.6
        alpha3inv = 9

        phi1 = ObjectiveFunction.L2ObjectiveFunction(W=sp.eye(nP))
        phi2 = ObjectiveFunction.L2ObjectiveFunction(W=sp.eye(nP))
        phi3 = ObjectiveFunction.L2ObjectiveFunction(W=sp.eye(nP))

        phi = alpha1 * phi1 + alpha2 * phi2 + phi3 / alpha3inv

        m = np.random.rand(nP)

        self.assertTrue(
            np.all(phi.multipliers == np.r_[alpha1, alpha2, 1./alpha3inv])
        )

        self.assertTrue(
            alpha1*phi1(m) + alpha2*phi2(m) + phi3(m)/alpha3inv == phi(m)
        )

        self.assertTrue(len(phi.objfcts) == 3)

        self.assertTrue(phi.test())

    def test_sum_fail(self):
        nP1 = 10
        nP2 = 30

        phi1 = ObjectiveFunction.L2ObjectiveFunction(
                    W=Utils.sdiag(np.random.rand(nP1))
        )

        phi2 = ObjectiveFunction.L2ObjectiveFunction(
                    W=Utils.sdiag(np.random.rand(nP2))
                )

        with self.assertRaises(Exception):
            phi = phi1 + phi2

        with self.assertRaises(Exception):
            phi = phi1 + 100 * phi2

    def test_emptyObjFct(self):
        phi = Empty_ObjFct()
        x = np.random.rand(20)

        with self.assertRaises(NotImplementedError):
            phi(x)
            phi.deriv(x)
            phi.deriv2(x)

    def test_ZeroObjFct(self):
        # This is not a combo objective function, it will just give back an
        # L2 objective function. That might be ok? or should this be a combo
        # objective function?
        nP = 20
        alpha = 2.
        phi = alpha*(
            ObjectiveFunction.L2ObjectiveFunction(W = sp.eye(nP)) +
            Utils.Zero()*ObjectiveFunction.L2ObjectiveFunction()
        )


        self.assertTrue(len(phi.objfcts) == 1)
        self.assertTrue(phi.test())

    def test_updateMultipliers(self):
        nP = 10

        m = np.random.rand(nP)

        W1 = Utils.sdiag(np.random.rand(nP))
        W2 = Utils.sdiag(np.random.rand(nP))

        phi1 = ObjectiveFunction.L2ObjectiveFunction(W=W1)
        phi2 = ObjectiveFunction.L2ObjectiveFunction(W=W2)

        phi = phi1 + phi2

        self.assertTrue(phi(m) == phi1(m) + phi2(m))

        phi.multipliers[0] = Utils.Zero()
        self.assertTrue(phi(m) == phi2(m))

        phi.multipliers[0] = 1.
        phi.multipliers[1] = Utils.Zero()

        self.assertTrue(len(phi.objfcts) == 2)
        self.assertTrue(len(phi.multipliers) == 2)
        self.assertTrue(len(phi) == 2)

        self.assertTrue(phi(m) == phi1(m))

    def test_nP_unknownFail(self):
        alpha = 10.

        phi1 = alpha * ObjectiveFunction.L2ObjectiveFunction()

        self.assertTrue(phi1._test_deriv())

        # nP needs to be set in order to get the hessian for combo obj fcts
        with self.assertRaises(Exception):
            phi1._test_deriv2()


if __name__ == '__main__':
    unittest.main()

