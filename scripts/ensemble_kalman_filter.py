
"""

Ensemble Kalman Filter

Intended for solution of Lorenz System

Scripting by Dave Casson, dave.casson@usask.ca

"""



import numpy as np
from numpy import zeros, array, eye, dot
import logging

from .utilities import outer_product_sum
logging.basicConfig(level=logging.INFO)

def hx(x):
    """ Not currently used
    Observation Operator that converts modelled states to measurement space
        In the simplest case, this is an equivalency"""
    H   = np.array([1,0,0])
    x_h = np.multiply(x,H)

    return x_h

def update_enkf(settings, X_b_input, z):
    """

    X_b_input => Background matrix of states (nstate x nens)
    z   => Measurement array (nobs)

    X_b_mean => Background state mean (nstate)
    X_b_anol => Background anomalies (nstate x nens)

    P_b = Model Error Covariance

    H => Observation Operator (nstate)
    R => Observation Error Covariance Matrix (nobs, nobs)

    X_a = Updated state matrix (nstate x nens)
    """

    #Add run specific settings
    N = settings['num_ens']
    dim_z = 1
    R_array = np.eye(dim_z) * settings['measurement_var']
    H = np.array([1, 0, 0])
    H_T = np.transpose(H)

    X_b = np.transpose(X_b_input)
    X_b_anol = zeros(np.shape(X_b))
    X_a = zeros(np.shape(X_b))

    X_b_mean = np.mean(X_b, axis=0)

    for i in range(N):
        X_b_anol[i] = X_b[i] - X_b_mean

    P_b = outer_product_sum(X_b_anol)/(N-1)

    K = P_b * H_T / (H*P_b*H_T+R_array)

    for i in range(N):
        X_a[i] = X_b[i] + np.dot(K, z - H*X_b[i])

    X_a_mean = np.mean(X_a, axis=0)

    X_a_output = np.transpose(X_a)
    X_a_mean_output = np.transpose(X_a_mean)

    return X_a_output, X_a_mean_output


