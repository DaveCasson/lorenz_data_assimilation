"""

Lorenz Data Assimilation

Utility Functions

Scripted by dave.casson@usask.ca

"""

import configparser
import logging
import ast
import numpy as np

def read_settings(settings_filename='settings.ini'):

    settings_reader = configparser.ConfigParser(allow_no_value=True)
    settings_reader.read(settings_filename)

    # Log the contents of the configuration file
    logging.info(f'The run configuration settings have been read from {settings_filename}')

    # Read all the configuration file elements into a dictionary
    settings_interim_dict = {sect: dict(settings_reader.items(sect)) for sect in settings_reader.sections()}
    # Remove the top level dict items, leaving only the key and value pairs
    settings = dict(ele for sub in settings_interim_dict.values() for ele in sub.items())

    #Convert numbers to floats
    for key, value in settings.items():
        try:
            settings[key] = int(value)
        except ValueError:
            try:
                settings[key] = float(value)
            except ValueError:
                try:
                    settings[key] = bool(value)
                except ValueError:
                    settings[key] = str(value)

    return settings


def outer_product_sum(A, B=None):

    """"Original Code Credit: https://github.com/rlabbe/filterpy/blob/master/filterpy/common/helpers.py"""
    """
    Computes the sum of the outer products of the rows in A and B
        P = \Sum {A[i] B[i].T} for i in 0..N
        Notionally:
        P = 0
        for y in A:
            P += np.outer(y, y)
    This is a standard computation for sigma points used in the UKF, ensemble
    Kalman filter, etc., where A would be the residual of the sigma points
    and the filter's state or measurement.
    The computation is vectorized, so it is much faster than the for loop
    for large A.
    Parameters
    ----------
    A : np.array, shape (M, N)
        rows of N-vectors to have the outer product summed
    B : np.array, shape (M, N)
        rows of N-vectors to have the outer product summed
        If it is `None`, it is set to A.
    Returns
    -------
    P : np.array, shape(N, N)
        sum of the outer product of the rows of A and B
    Examples
    --------
    Here sigmas is of shape (M, N), and x is of shape (N). The two sets of
    code compute the same thing.
    >>> P = outer_product_sum(sigmas - x)
    >>>
    >>> P = 0
    >>> for s in sigmas:
    >>>     y = s - x
    >>>     P += np.outer(y, y)
    """

    if B is None:
        B = A

    outer = np.einsum('ij,ik->ijk', A, B)
    return np.sum(outer, axis=0)
