
"""

Particle Filter Class

Intended for solution of Lorenz System

Scripting by Dave Casson, dave.casson@usask.ca

"""



import matplotlib.pyplot as plt
import numpy as np

def calculate_likelihoods(settings,state_array,measurement):
    """Calculate likelihood of each particle based on error """

    errors = []
    likelihoods = []

    for ens in range(0, settings['num_ens']):

        #Extract particle from state array
        particle = state_array[0][ens]

        #Calculate errors
        error = abs(particle - measurement)

        # Calculate Likelihood
        likelihoods.append(np.exp(-0.5 * error * settings['measurement_var'] * error))

    return likelihoods

def calculate_weights(likelihoods):
    """Calculate weights based on likelihood"""
    weights = likelihoods / np.sum(likelihoods)
    return weights

def calculate_state_estimate(state_array,weights):

    """Calculate state estimate based on the weight of each particle"""
    u_est = np.average(state_array[0], weights=weights, axis=0)
    v_est = np.average(state_array[1], weights=weights, axis=0)
    w_est = np.average(state_array[2], weights=weights, axis=0)

    state_estimate = [u_est,v_est,w_est]

    return state_estimate

def calculate_neff(weights):
    """Calculate the effective weight of all particles"""
    return 1. / np.sum(np.square(weights))

def resample(settings,state_array,weights):
    """Resampling component of Sequential Importance Resampling algorithm """

    #Create empty array the size of the number of ensembles
    resample = np.empty((settings['num_ens']), dtype=int)

    #Calculate an array of the cumulative weights i.e. [0.02,0.06, .. ,1]
    zweightcumul = np.cumsum(weights)

    #Generate a random seed / value, and divide by the number of ensembles
    zrand = np.random.random() / settings['num_ens']

    #Loop through particles
    for ires in range(0, settings['num_ens']):
        #If the value is lower than the first weight, assign it to the first index.
        if zrand <= zweightcumul[0]:
            resample[ires] = 1

        #Check where the seed falls within the array of weights, then assign an index.
        for rk in range(1, settings['num_ens']):
            if (zweightcumul[rk - 1] < zrand) and (zrand <= zweightcumul[rk]):
                resample[ires] = rk + 1

        #Increment the random seed forward, by 1 / num_ens
        zrand += 1. / settings['num_ens']

    #Index correction needed due to python indexing
    resample_index = resample - 1

    # Resample according to re-sampling index
    for i, value in enumerate(resample_index):
        state_array[0][i] = state_array[0][value]
        state_array[1][i] = state_array[1][value]
        state_array[2][i] = state_array[2][value]

    return state_array


