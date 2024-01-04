'''
OVRVO Integrator

Time Step Rescaling Recovers Continuous-Time Dynamical
Properties for Discrete-Time Langevin Integration of
Nonequilibrium Systems
Sivak et. al, 2014
'''

import numpy as np

from stochastic_relaxation.util.integrator import Integrator
from stochastic_relaxation.util.random import init_maxwell_boltzmann
from stochastic_relaxation.util.constants import kB

#=======#
# OVRVO #
#=======#
class OVRVO(Integrator):
    def __init__(self, options, use_tanh=True):
        '''
        use_tanh whether to use the tanh rescaling function, otherwise does not rescale
        '''
        super().__init__(options)

        # initialize position and velocity
        self.X = np.zeros((options.NP, options.ND))
        self.V = init_maxwell_boltzmann(options.Te, options.m, options.NP, options.ND)

        # computed variables
        self.a = np.exp(-options.gamma * options.dt)
        self.sqrt_a = np.sqrt(self.a)
        self.beta = 1 / (kB * options.Te)
        self.sqrt_1a_betam = np.sqrt((1 - self.a) / (self.beta * options.m))
        self.gaussian = np.random.normal(size=(options.NP,options.ND))

        # timestep rescaling parameter
        self.b = 1
        if use_tanh:
            self.b = np.sqrt((2 / (options.gamma * options.dt)) * np.tanh(options.gamma * options.dt / 2))

        self.bdt = self.b * options.dt
        self.bdto2m = 0.5 * self.b * options.dt / options.m
    
    def _step(self):
        # O [Ornstein-Uhlenbeck]
        v_14 = self.sqrt_a * self.V + self.sqrt_1a_betam * self.gaussian

        # V [Velocity update]
        v_12 = v_14 + self.bdto2m * self.force(self.X)

        # R [Position update]
        self.X = self.X + self.bdt * v_12

        # V [Velocity update]
        v_34 = v_12 + self.bdto2m * self.force(self.X)

        # O [Ornstein-Uhlenbeck]
        self.gaussian = np.random.normal(size=(self.options.NP, self.options.ND))
        self.V = self.sqrt_a * v_34 + self.sqrt_1a_betam * self.gaussian
    
    def reset(self):
        '''
        Reset the integrator
        '''
        super().reset()
        self.X = np.zeros((self.options.NP, self.options.ND))
        self.V = init_maxwell_boltzmann(self.options.Te, self.options.m, self.options.NP, self.options.ND)
        self.gaussian = np.random.normal(size=(self.options.NP,self.options.ND))

    def update_dt(self, dt: float):
        '''
        Update the timestep. Note that this is a scalar, not a pint quantity (i.e. must already be in SI units)
        '''
        super().update_dt(dt)
        self.a = np.exp(-self.options.gamma * dt)
        self.sqrt_a = np.sqrt(self.a)
        self.sqrt_1a_betam = np.sqrt((1 - self.a) / (self.beta * self.options.m))
        
        self.b = np.sqrt((2 / (self.options.gamma * dt)) * np.tanh(self.options.gamma * dt / 2))
        self.bdt = self.b * dt
        self.bdto2m = 0.5 * self.b * self.dt / self.options.m
