'''
Helper functions for random number generation
'''

import numpy as np
from numpy import random

from stochastic_relaxation.util.constants import kB

#===========#
# RNG State #
#===========#
def get_state_for_json():
    r0, r1, r2, r3, r4 = random.get_state()
    r1 = [int(i) for i in r1]
    return [r0, r1, r2, r3, r4]
    
def set_state_from_json(arr):
    r0, r1, r2, r3, r4 = arr
    random.set_state((r0, np.array(r1, dtype=np.uint32), r2, r3, r4))

#===============================#
# Maxwell Boltzmann equilibrium #
#===============================#
def init_maxwell_boltzmann(Te, m, NP, ND):
    '''
    Returns the velocities of NP particles in ND dimensions, with
    equilibrium temperature Te, and masses m, using the 
    Maxwell-Boltzmann equilibrium distribution
    '''
    assert(NP > 0)
    assert(ND > 0)
    rnd = random.normal(size=(NP, ND))
    vth = np.sqrt(kB * Te / m)  # thermal speed
    return rnd * vth * 2**0.5
