'''
Load options from an option file (.json) into an Option object
    Specify units for each physical parameter
'''

import json
from stochastic_relaxation.util.units import assert_pint_si_magnitude

#==============#
# Option Class #
#==============#
class Option:
    '''
    Stores simulation parameters and options
    
    Should be constructed from a JSON file, see 
    ```python
    import sri.util.options as options
    options.load_options()
    ``` 
    '''
    def __init__(self,
                 NP: int, ND: int, NA: int,
                 dt: str, tfinal: str,
                 Te: str, 
                 m: str, 
                 gamma: str,
                 initial_position,
                 **kwargs):
        '''
        NP number of particles
        ND number of dimensions
        NA number of auxiliary variables
        dt timestep
        tfinal final time
        Te equilibrium temperature
        m  mass of each particle, a scalar
        gamma gamma
        initial_position initial position of each particle (array of length ND)
        '''
        self.NP = NP
        self.ND = ND
        self.NA = NA
        
        self.dt = assert_pint_si_magnitude(dt, 's')
        self.tfinal = assert_pint_si_magnitude(tfinal, 's')
        self.Te = assert_pint_si_magnitude(Te, 'K')
        self.m = assert_pint_si_magnitude(m, 'kg')
        self.gamma = assert_pint_si_magnitude(gamma, '1/s')
        
        self.initial_position = [assert_pint_si_magnitude(x, 'm') for x in initial_position]
        
        # Add all other keyword arguments
        for key, val in kwargs.items():
            setattr(self, key, val)

#===============#
# Option Loader #
#===============#
def load_options(filename: str):
    '''
    Load options from a JSON file
    '''
    with open(filename, 'r') as f:
        options = json.load(f)
    return Option(**options)
