===========================
Simple least square problem
===========================

This simplistic example is only meant to demonstrate the basic workflow of the
toolbox. Here we want to solve a least square problem, i.e. we want the
solution to converge to the original signal without any constraint. Lets
define this signal by :

>>> y = [4, 5, 6, 7]

The first function to minimize is the sum of squared distances between the
current signal `x` and the original `y`. For this purpose, we instantiate an
L2-norm object :

>>> import pyunlocbox
>>> f1 = pyunlocbox.functions.norm_l2(y=y)

This standard function object provides the :meth:`eval`, :meth:`grad` and
:meth:`prox` methods that will be useful to the solver. We can evaluate them
any given point :

>>> f1.eval([0, 0, 0, 0])
126
>>> f1.grad([0, 0, 0, 0])
array([ -8, -10, -12, -14])
>>> f1.prox([0, 0, 0, 0], 1)
array([ 2.66666667,  3.33333333,  4.        ,  4.66666667])

We need a second function to minimize, which usually describes a constraint. As
we have no constraint, we just define a dummy function object by hand. We have
to define the :meth:`eval` and :meth:`grad` methods as the solver we will use
requires it :

>>> f2 = pyunlocbox.functions.func()
>>> f2.eval = lambda x: 0
>>> f2.grad = lambda x: 0

We can now instantiate the solver object :

>>> solver = pyunlocbox.solvers.forward_backward()

And finally solve the problem :

>>> x0 = [0, 0, 0, 0]
>>> ret = pyunlocbox.solvers.solve([f1, f2], x0, solver, absTol=1e-5)
Solution found in 10 iterations :
    objective function f(sol) = 7.460428e-09
    last relative objective improvement : 1.624424e+03
    stopping criterion : ABS_TOL

The solving function returns several values, one is the found solution :

>>> ret['sol']
array([ 3.99996922,  4.99996153,  5.99995383,  6.99994614])

Another one is the value returned by each function objects at each iteration.
As we passed two function objects (L2-norm and dummy), the `objective` is a 2
by 11 (10 iterations plus the evaluation at `x0`) ``ndarray``. Lets plot a
convergence graph out of it :

>>> import numpy as np
>>> import matplotlib.pyplot as plt
>>> fig = plt.figure()
>>> objective = np.array(ret['objective'])
>>> _ = plt.semilogy(objective[:, 0], 'x', label='L2-norm')
>>> _ = plt.semilogy(objective[:, 1], label='Dummy')
>>> _ = plt.semilogy(np.sum(objective, axis=1), label='Global objective')
>>> _ = plt.grid(True)
>>> _ = plt.title('Convergence')
>>> _ = plt.legend(numpoints=1)
>>> _ = plt.xlabel('Iteration number')
>>> _ = plt.ylabel('Objective function value')
>>> fig.savefig('doc/tutorials/simple_convergence.pdf')
>>> fig.savefig('doc/tutorials/simple_convergence.png')

The below graph show an exponential convergence of the objective function. The
global objective is obviously only composed of the L2-norm as the dummy
function object was defined to always evaluate to 0 (``f2.eval = lambda x:
0``).

.. image:: simple_convergence.*