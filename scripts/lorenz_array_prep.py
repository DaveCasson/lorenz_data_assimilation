"""

Lorenz Data Assimilation

Simple of the Lorenz equations and the application of data assimilation methods.py

Scripted by dave.casson@usask.ca

"""

import numpy as np

def create_parameter_arrays(settings,mode):
    """ Create parameter arrays for the mode (base or modified) case """
    rho_array  = np.ones(settings['num_timesteps'])*settings[f'rho_{mode}']
    psi_array  = np.ones(settings['num_timesteps'])*settings[f'psi_{mode}']
    beta_array = np.ones(settings['num_timesteps'])*settings[f'beta_{mode}']

    return rho_array, psi_array, beta_array

def create_ens_arrays(settings):
    """Create ensemble arrays, by generating random numbers scaled by the variance, and
        applying to a multiplicative factor"""

    rho_var  = np.random.normal(loc=0, scale=settings['rho_var'], size=settings['num_ens'])
    psi_var  = np.random.normal(loc=0, scale=settings['psi_var'], size=settings['num_ens'])
    beta_var = np.random.normal(loc=0, scale=settings['beta_var'], size=settings['num_ens'])

    rho_ens_array  = settings['rho_mod'] * (1 + rho_var)
    psi_ens_array  = settings['psi_mod']  * (1 + psi_var)
    beta_ens_array = settings['beta_mod']  * (1 + beta_var)

    return rho_ens_array, psi_ens_array, beta_ens_array

def create_time_array(settings):
    """Create time array based on number of timesteps and increment"""
    return np.arange(0, settings['num_timesteps']*settings['delta_t'], settings['delta_t'])


def create_measurement_array(settings,base_run_array):
    """Create an array of measurements. This samples the base, or perfect, model run at a set frequency"""

    #Create array of nan values
    meas_array = np.empty(len(base_run_array))
    meas_array[:] = np.nan

    #If the index is exactly divisible by the measurement frequency, copy the measurement value.
    for i, value in enumerate(meas_array):
        int_check = i / settings['meas_freq']
        if int_check.is_integer():
            meas_array[i] = base_run_array[i]

    return meas_array
