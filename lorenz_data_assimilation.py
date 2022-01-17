"""

Lorenz Data Assimilation

Simple solution of the Lorenz system in a deterministic and ensemble mode

Scripted by dave.casson@usask.ca

"""


import numpy as np
import logging
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.INFO)
from scripts import utilities as utils
from scripts import lorenz_plotting
from scripts import lorenz_array_prep
from scripts import particle_filter as pf
from scripts import ensemble_kalman_filter as enkf

def explicit_euler(quantity, flux, delta):
    """Use the explicit euler approximation to advance one timestep"""

    new_quantity = quantity + flux * delta

    return new_quantity

def predict(u_ini,v_ini,w_ini,du_dt,dv_dt,dw_dt,rho,psi,beta,delta_t):
    """Advance one timestep by applying explicit euler to the state and derivative"""

    #Explicit euler solution
    u = explicit_euler(u_ini,du_dt,delta_t)
    v = explicit_euler(v_ini, dv_dt, delta_t)
    w = explicit_euler(w_ini, dw_dt, delta_t)

    #Lorenz equations
    du_dt = rho * (v - u)
    dv_dt = u * (psi - w) - v
    dw_dt = u * v - beta * w

    return u,v,w,du_dt,dv_dt,dw_dt

def run_lorenz_deterministic(rho_array, psi_array, beta_array, u_ini,v_ini,w_ini,t_array,delta_t):
    """Run Lorenz using the predict function to move forward in time"""

    #Initialize variables and arrays
    u = u_ini
    v = v_ini
    w = w_ini
    du_dt = 0
    dv_dt = 0
    dw_dt = 0
    u_array = []
    v_array = []
    w_array = []

    #Loop through time, solving the lorenz equation
    for i, t in enumerate(t_array):

        #Each time through the loop, advance the model one timestep
        u, v, w, du_dt, dv_dt, dw_dt = predict(u,v,w,du_dt,dv_dt,dw_dt,rho_array[i],psi_array[i],beta_array[i],delta_t)

        u_array.append(u)
        v_array.append(v)
        w_array.append(w)

    state_array = np.vstack([u_array,v_array,w_array])

    return state_array


def run_lorenz_ensemble(settings, rho_ens_array, psi_ens_array, beta_ens_array, t_array, da_mode = None):
    """Run the Lorenz model (with options for data assimilation) using an ensemble of different parameter settings"""

    # Initialize values
    u = settings['u_ini_mod']
    v = settings['v_ini_mod']
    w = settings['w_ini_mod']
    du_dt = 0
    dv_dt = 0
    dw_dt = 0

    #Initialize result array
    state_estimate_array = []
    state_result_array = []

    # Initial loop iterates through the timesteps
    for i, t in enumerate(t_array):

        u_ens_array = []
        v_ens_array = []
        w_ens_array = []
        du_ens_array = []
        dv_ens_array = []
        dw_ens_array = []

        # Second loop iterates through ensemble members
        for ens in range(0, settings['num_ens']):

            # For every timestep, except the first,
            # the variables and derivative variables are updated from the previous timestep
            if i > 0:
                u = state_timestep_array[0][ens]
                v = state_timestep_array[1][ens]
                w = state_timestep_array[2][ens]
                du_dt = state_derivative_array[0][ens]
                dv_dt = state_derivative_array[1][ens]
                dw_dt = state_derivative_array[2][ens]

            # Use the predict function to move one timestep forward
            u_new, v_new, w_new, du_dt_new, dv_dt_new, dw_dt_new = predict(u, v, w, du_dt, dv_dt, dw_dt,
                                                                           rho_ens_array[ens], psi_ens_array[ens],
                                                                           beta_ens_array[ens],
                                                                           settings['delta_t'])

            # Append the state and derivative variables to create am array containing each ensemble member
            u_ens_array.append(u_new)
            v_ens_array.append(v_new)
            w_ens_array.append(w_new)
            du_ens_array.append(du_dt_new)
            dv_ens_array.append(dv_dt_new)
            dw_ens_array.append(dw_dt_new)

        # Append the ensemble results for each timestep
        state_timestep_array = np.vstack([u_ens_array, v_ens_array, w_ens_array])
        state_derivative_array = np.vstack([du_ens_array, dv_ens_array, dw_ens_array])



        if da_mode == 'pf':
            """Implement Particle Filter SIS or SIR algorithms. See the particle_filter.py for details"""
            if i == 0:
                logging.info('Running Particle Filter')

            likelihoods      = pf.calculate_likelihoods(settings, state_timestep_array,meas_array[i])
            weights          = pf.calculate_weights(likelihoods)
            state_estimate   = pf.calculate_state_estimate(state_timestep_array, weights)
            effective_weight = pf.calculate_neff(weights)
            n_eff            = settings['n_eff'] * settings['num_ens']

            if settings['resample_option'] == True and n_eff < effective_weight:
                if i == 0:
                    logging.info('Particle Filter with resampling')
                state_timestep_array = pf.resample(settings, state_timestep_array, weights)
                state_estimate = pf.calculate_state_estimate(state_timestep_array, weights)
                # Re-initialize weights for the next run
                weights.fill(1.0 / settings['num_ens'])

        if da_mode == 'enkf':
            """Implement Ensemble Kalman Filter. See ensemble_kalman_filter.py for details"""
            if i == 0:
                logging.info('Running EnKF')
            state_timestep_array, state_estimate = enkf.update_enkf(settings, state_timestep_array, meas_array[i])

        state_estimate_array.append(state_estimate)
        state_result_array.append(state_timestep_array)

    return state_result_array, state_estimate_array


if __name__ == '__main__':

    logging.info('Read settings from settings file.')
    settings = utils.read_settings()

    logging.info('Beginning perfect model run')
    t_array                                         = lorenz_array_prep.create_time_array(settings)
    rho_base_array, psi_base_array, beta_base_array = lorenz_array_prep.create_parameter_arrays(settings, 'base')
    rho_mod_array, psi_mod_array, beta_mod_array    = lorenz_array_prep.create_parameter_arrays(settings, 'mod')


    logging.info(f'First performing base model run.')
    state_array_base_run = run_lorenz_deterministic(rho_base_array, psi_base_array, beta_base_array,
                                      settings['u_ini_base'],settings['v_ini_base'],settings['w_ini_base'],
                                      t_array, settings['delta_t'])

    logging.info('Plot 3D result')
    #lorenz_plotting.plot_3D_lorenz(settings,state_array_base_run)

    logging.info('Plot variable comparison result')
    #lorenz_plotting.plot_lorenz_basis(state_array_base_run)

    logging.info('Second performing modified model run, to be used as pseudo-measurements')
    state_array_mod_run = run_lorenz_deterministic(rho_mod_array, psi_mod_array, beta_mod_array,
                                     settings['u_ini_mod'],settings['v_ini_mod'],settings['w_ini_mod'],
                                     t_array, settings['delta_t'])

    logging.info('Create ensemble of arrays, based on prescribed parameter variance')
    rho_ens_array, psi_ens_array, beta_ens_array = lorenz_array_prep.create_ens_arrays(settings)


    logging.info('Generating measurements at the desired frequency')
    meas_array = lorenz_array_prep.create_measurement_array(settings, state_array_base_run[0][:])

    if settings['run_pf'] == True:
        pf_ens_states, pf_est_states = run_lorenz_ensemble(settings, rho_ens_array, psi_ens_array, beta_ens_array,
                                                                       t_array, da_mode = 'pf')

        lorenz_plotting.plot_da_result(settings,state_array_base_run,state_array_mod_run,meas_array,
                                       pf_ens_states, pf_est_states,t_array,da_mode = 'pf')

    if settings['run_enkf'] == True:
        enkf_ens_states, enkf_est_states = run_lorenz_ensemble(settings, rho_ens_array, psi_ens_array, beta_ens_array,
                                                                       t_array, da_mode = 'enkf')

        lorenz_plotting.plot_da_result(settings,state_array_base_run,state_array_mod_run,meas_array,
                                       enkf_ens_states, enkf_est_states,t_array,da_mode = 'enkf')




