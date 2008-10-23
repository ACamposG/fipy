#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "mesh20x20.py"
 #
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
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
 # ###################################################################
 ##

r"""

This example solves a diffusion problem and demonstrates the use of
applying boundary condition patches.

.. raw:: latex

   \IndexClass{Grid2D}

..
    
    >>> from fipy import *

    >>> nx = 20
    >>> ny = nx
    >>> dx = 1.
    >>> dy = dx
    >>> L = dx * nx
    >>> mesh = Grid2D(dx=dx, dy=dy, nx=nx, ny=ny)

We create a `CellVariable` and initialize it to zero:
    
.. raw:: latex

   \IndexClass{CellVariable}

..

    >>> phi = CellVariable(name = "solution variable",
    ...                    mesh = mesh,
    ...                    value = 0.)

and then create a diffusion equation.  This is solved by default with an
iterative conjugate gradient solver.  

.. raw:: latex

   \IndexClass{TransientTerm}
   \IndexClass{ImplicitDiffusionTerm}

..

    >>> D = 1.
    >>> eq = TransientTerm() == ImplicitDiffusionTerm(coeff=D)

We apply Dirichlet boundary conditions

    >>> valueTopLeft = 0
    >>> valueBottomRight = 1

to the top-left and bottom-right corners.  Neumann boundary conditions
are automatically applied to the top-right and bottom-left corners.

.. raw:: latex

   \IndexClass{FixedValue}

..

    >>> x, y = mesh.getFaceCenters()
    >>> facesTopLeft = ((mesh.getFacesLeft() & (y > L / 2))
    ...                 | (mesh.getFacesTop() & (x < L / 2)))
    >>> facesBottomRight = ((mesh.getFacesRight() & (y < L / 2))
    ...                     | (mesh.getFacesBottom() & (x > L / 2)))

    >>> BCs = (FixedValue(faces=facesTopLeft, value=valueTopLeft),
    ...        FixedValue(faces=facesBottomRight, value=valueBottomRight))
    
We create a viewer to see the results

.. raw:: latex

   \IndexModule{viewers}

..

    >>> if __name__ == '__main__':
    ...     viewer = viewers.make(vars=phi,
    ...                           limits={'datamin': 0., 'datamax': 1.})
    ...     viewer.plot()

and solve the equation by repeatedly looping in time:

    >>> timeStepDuration = 10 * 0.9 * dx**2 / (2 * D)
    >>> steps = 10
    >>> for step in range(steps):
    ...     eq.solve(var=phi,
    ...              boundaryConditions=BCs,
    ...              dt=timeStepDuration)
    ...     if __name__ == '__main__':
    ...         viewer.plot()

.. image:: examples/diffusion/mesh20x20transient.pdf
   :scale: 50
   :align: center

..

We can test the value of the bottom-right corner cell.

    >>> print numerix.allclose(phi(((L,), (0,))), valueBottomRight, atol = 1e-2)
    1

    >>> if __name__ == '__main__':
    ...     raw_input("Implicit transient diffusion. Press <return> to proceed...")

-----

We can also solve the steady-state problem directly

    >>> ImplicitDiffusionTerm().solve(var=phi, 
    ...                               boundaryConditions = BCs)
    >>> if __name__ == '__main__':
    ...     viewer.plot()

.. image:: examples/diffusion/mesh20x20steadyState.pdf
   :scale: 50
   :align: center

and test the value of the bottom-right corner cell.

    >>> print numerix.allclose(phi(((L,), (0,))), valueBottomRight, atol = 1e-2)
    1
    
    >>> if __name__ == '__main__':
    ...     raw_input("Implicit steady-state diffusion. Press <return> to proceed...")

"""

__docformat__ = 'restructuredtext'

##from fipy.tools.profiler.profiler import Profiler
##from fipy.tools.profiler.profiler import calibrate_profiler

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())

