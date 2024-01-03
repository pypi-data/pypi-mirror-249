'''
Abstract class for integrators
    All integrators must implement the _step method
'''

import numpy as np
from stochastic_relaxation.util.options import Option
from stochastic_relaxation.util.data import Data

#==================#
# Integrator Class #
#==================#
class Integrator:
    def __init__(self, options: Option):
        self.options = options

        self.n = 0
        self.Nt = int(options.tfinal/options.dt)

        NP = self.options.NP
        ND = self.options.ND
        NA = self.options.NA
        self.X = np.zeros((NP, ND))
        self.V = np.zeros((NP, ND))
        self.A = np.zeros((NA, NP, ND))
        
        self.positions = np.zeros((self.Nt, NP, ND))
        self.velocities = np.zeros((self.Nt, NP, ND))
        self.auxiliaries = np.zeros((self.Nt, NA, NP, ND))
    
    def set_force(self, force):
        '''
        Sets the deterministic force function
        '''
        self.force = force
    
    def step(self):
        '''
        Compute one timestep of the simulation
        '''
        # skip 0th step (initialization)
        if self.n != 0:
            self._step()
        
        self.positions[self.n] = self.X
        self.velocities[self.n] = self.V
        self.auxiliaries[self.n] = self.A
        
        self.n += 1
    
    def reset(self):
        '''
        Reset the integrator
        '''
        self.n = 0
        self.X = np.zeros((self.options.NP, self.options.ND))
        self.V = np.zeros((self.options.NP, self.options.ND))
        self.A = np.zeros((self.options.NA, self.options.NP, self.options.ND))
    
    def update_dt(self, dt):
        '''
        Individual integrators must implement this method
        '''
        self.dt = dt
        self.Nt = int(np.floor(self.tfinal/dt))
        
        self.positions = np.zeros((self.Nt, self.NP, self.ND))
        self.velocities = np.zeros((self.Nt, self.NP, self.ND))
        self.auxiliaries = np.zeros((self.Nt, self.NA, self.NP, self.ND))

    
    def _step(self):
        '''
        Individual integrators must implement this method
        '''
        pass
        
    def getData(self):
        return Data(self.positions, self.velocities, self.auxiliaries)
