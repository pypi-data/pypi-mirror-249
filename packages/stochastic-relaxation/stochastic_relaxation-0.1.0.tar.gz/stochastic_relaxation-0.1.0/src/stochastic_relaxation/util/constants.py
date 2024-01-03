'''
Collection of useful constants
'''

import numpy as np
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity

u_kB = Q_(1.380649e-23, 'J/K')

kB = 1.380649e-23
PI = np.pi
