#!/usr/bin/env python

## 
 # ###################################################################
 #  PyFiVol - Python-based finite volume PDE solver
 # 
 #  FILE: "test.py"
 #                                    created: 11/10/03 {3:23:47 PM}
 #                                last update: 1/16/04 {11:45:32 AM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

"""Test steady-state diffusion solutions
"""
 
import unittest
from fivol.examples.phase.theta.modularVariable import ModularVariable
from Numeric import pi
from Numeric import array
from fivol.meshes.grid2D import Grid2D
from fivol.tests.testBase import TestBase
from fivol.examples.phase.theta.noModularVariable import NoModularVariable

class TestMod(TestBase):
    def setUp(self, value, dx = 1., dy = 1.):
        mesh = Grid2D(dx, dy, 2, 1)
        self.theta = ModularVariable(
            mesh = mesh,
            value = value)

    def testResult(self):
        self.assertArrayWithinTolerance(self.result, self.answer, 1e-10)

class TestModSubtract(TestMod):
    def setUp(self):
        TestMod.setUp(self, -2 * pi / 3.)
        self.thetaOther = ModularVariable(
            mesh = self.theta.getMesh(),
            value = 2. * pi / 3.)
        self.result = (self.thetaOther - self.theta).getNumericValue()
        self.answer = self.theta.getNumericValue()

class TestModCellToFace(TestMod):
    def setUp(self):
        TestMod.setUp(self, array((2. * pi / 3., -2. * pi / 3.)))
        self.answer = array((-pi, 2. * pi / 3., -2. * pi / 3., 2. * pi / 3., -2. * pi / 3., 2. * pi / 3., -2. * pi / 3.))
        self.result = self.theta.getFaceValue().getNumericValue()

class TestModCellGrad(TestMod):
    def setUp(self):
        dx = 0.5
        TestMod.setUp(self, array((2. * pi / 3., -2. * pi / 3.)), dx = dx, dy = 0.5)
        self.answer = array(((pi / 3., 0.), (pi / 3., 0.))) / dx
        self.result = self.theta.getGrad().getNumericValue()

class TestModNoMod(TestMod):
    def setUp(self):
        TestMod.setUp(self, 1., dx = 1., dy = 1.)
        thetaNoMod = NoModularVariable(self.theta)
        self.answer = array((0. , 0.))
        self.theta[:] = self.answer
        self.result = thetaNoMod.getNumericValue()

class TestModFaceGrad(TestMod):
    def setUp(self):
        dx = 0.5
        dy = 0.5
        TestMod.setUp(self, array((2. * pi / 3., -2. * pi / 3.)) , dx = dx, dy = dy)
        self.answer = array(((2. * pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (0., 0.), (0., 0.))) / dx
        self.result = self.theta.getFaceGrad().getNumericValue()

class TestModFaceGradNoMod(TestMod):
    def setUp(self):
        dx = 0.5
        dy = 0.5
        TestMod.setUp(self, array((2. * pi / 3., -2. * pi / 3.)) , dx = dx, dy = dy)
        thetaNoMod = NoModularVariable(self.theta)
        self.answer = array(((2. * pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (pi / 3., 0.), (0., 0.), (0., 0.))) / dx - array(((-4. * pi / 3., 0.), (-2. * pi / 3., 0.), (-2. * pi / 3., 0.), (-2. * pi / 3., 0.), (-2. * pi / 3., 0.), (0., 0.), (0., 0.))) / dx
        self.diff = self.theta.getFaceGrad() - thetaNoMod.getFaceGrad()
        self.result = self.diff.getNumericValue()
        
def suite():
    theSuite = unittest.TestSuite()
    theSuite.addTest(unittest.makeSuite(TestModSubtract))
    theSuite.addTest(unittest.makeSuite(TestModCellToFace))
    theSuite.addTest(unittest.makeSuite(TestModCellGrad))
    theSuite.addTest(unittest.makeSuite(TestModNoMod))
    theSuite.addTest(unittest.makeSuite(TestModFaceGrad))
    theSuite.addTest(unittest.makeSuite(TestModFaceGradNoMod))
    return theSuite
    
if __name__ == '__main__':
    theSuite = suite()
    unittest.TextTestRunner(verbosity=2).run(theSuite)

            
            
