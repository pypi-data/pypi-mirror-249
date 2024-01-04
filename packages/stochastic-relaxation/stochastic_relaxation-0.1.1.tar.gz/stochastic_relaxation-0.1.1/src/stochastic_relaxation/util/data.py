'''
Store data in a format savable/loadable to/from disk
'''

import numpy as np
import xarray as xr
import time

#============#
# Data Class #
#============#
class Data:
    '''
    Stores all unprocessed data from a simulation.
    Note that all units are SI units
    '''
    
    def __init__(self, X, V, A):
        # Convert to xarray if not already
        if type(X) not in [xr.DataArray, xr.Dataset]:
            self.X = xr.DataArray(X, dims=['timestep', 'particle_index', 'dimension'])
            self.V = xr.DataArray(V, dims=['timestep', 'particle_index', 'dimension'])
            self.A = xr.DataArray(A, dims=['timestep', 'auxiliary_index', 'particle_index', 'dimension'])
        else:
            self.X = X
            self.V = V
            self.A = A
    
    def save(self, directory: str):
        '''
        Save the data to a file
        '''
        save_time = time.time()
        self.X.to_zarr(f'{directory}/r_{round(save_time)}/X.zarr', mode='w')
        self.V.to_zarr(f'{directory}/r_{round(save_time)}/V.zarr', mode='w')
        self.A.to_zarr(f'{directory}/r_{round(save_time)}/A.zarr', mode='w')

#==============#
# Data Loaders #
#==============#
def load_data(directory: str):
    '''
    Load data from a directory (directory should be named r_{save_time})
    '''
    X = xr.open_zarr(f'{directory}/X.zarr')
    V = xr.open_zarr(f'{directory}/V.zarr')
    A = xr.open_zarr(f'{directory}/A.zarr')
    return Data(X, V, A)
