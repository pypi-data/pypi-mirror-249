'''
Collection of deterministic force terms

To implement additional forces, create a new class that inherits from Force and
implement the `__call__` and `U` methods.

Note that force constructors should take in pint strings as inputs, and convert
them to pint quantities, convert them to base units, and then to magnitudes.
See `assert_pint_si_magnitude` in `src/util/units.py`.
'''

from stochastic_relaxation.util.units import assert_pint_si_magnitude

class Force:
    def __call__(self, X):
        pass
    
    def U(self, X):
        pass

class HarmonicForce(Force):
    def __init__(self, k: str):
        self.k = assert_pint_si_magnitude(k, 'kg/s^2')
    
    def __call__(self, X):
        return -self.k * X
    
    def U(self, X):
        return 0.5 * self.k * X**2

class UniformForce(Force):
    '''
    Note this is not technically correct, as the input 
    `U0` is a scalar not a vector, and represents the
    vector with each component as `U0`
    '''
    
    def __init__(self, U0: str):
        self.U0 = assert_pint_si_magnitude(U0, 'kg m/s^2')
    
    def __call__(self, X):
        return self.U0
    
    def U(self, X):
        return -self.U0 * X

class FreeForce(Force):
    def __call__(self, X):
        return 0
    
    def U(self, X):
        return 0
