"""

Lorenz Data Assimilation

Plotting Functions

Scripted by dave.casson@usask.ca

"""

import configparser
import ast
import matplotlib.pyplot as plt
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)


def plot_3D_lorenz(settings,state_array):
    """Create 3D plot of Lorenz equations"""
    logging.info('Log test')
    fig = plt.figure(figsize=(20, 10))
    ax = fig.gca(projection="3d")
    ax.plot(state_array[0][:], state_array[1][:], state_array[1][:])
    ax.set_xlabel('u')
    ax.set_ylabel('y')
    ax.set_zlabel('w')
    ax.set_title(f"Lorenz System \n "
                 f"{settings['num_timesteps']} Timesteps")
    plt.savefig('./figures/3DFigure.png')

    return

def plot_lorenz_basis(state_array_base_run):
    """Create comparison plots of the u, v, and w variables"""
    plt.figure(figsize=(20, 10))

    plt.subplot(131)
    plt.title('u vs v')
    plt.ylabel('v')
    plt.xlabel('u')
    plt.plot(state_array_base_run[:][0],state_array_base_run[:][1])

    plt.subplot(132)
    plt.title('u vs w')
    plt.ylabel('w')
    plt.xlabel('u')
    plt.plot(state_array_base_run[:][0], state_array_base_run[:][2])

    plt.subplot(133)
    plt.title('v vs w')
    plt.ylabel('w')
    plt.xlabel('v')
    plt.plot(state_array_base_run[:][1], state_array_base_run[:][2])
    plt.savefig('figures/BasisRun.png')


def plot_ensembles(u_df,v_df,w_df):

    for i in range(0, num_ens):
        plt.figure(figsize=(20, 10))

        plt.subplot(131)
        plt.title('u vs v')
        plt.ylabel('v')
        plt.xlabel('u')
        plt.plot(u_df[i],v_df[i])

        plt.subplot(132)
        plt.title('u vs w')
        plt.ylabel('w')
        plt.xlabel('u')
        plt.plot(u_df[i],w_df[i])

        plt.subplot(133)
        plt.title('v vs w')
        plt.ylabel('w')
        plt.xlabel('v')
        plt.plot(v_df[i], w_df[i])

    plt.savefig(f'EnsembleRun.png')

def plot_da_result(settings,state_array_base_run,state_array_mod_run,meas_array,
                   state_array_ens_run, state_estimate_ens_run,t_array,da_mode):

    u_final_ens = []
    v_final_ens = []
    w_final_ens = []
    u_estimate  = []
    v_estimate  = []
    w_estimate  = []

    length_t = settings['delta_t'] * settings['num_timesteps']

    if da_mode == 'pf':
        plot_colour = 'red'
    else:
        plot_colour = 'green'

    for i,val in enumerate(state_array_ens_run):
        u_final_ens.append(state_array_ens_run[i][0])
        v_final_ens.append(state_array_ens_run[i][1])
        w_final_ens.append(state_array_ens_run[i][2])

    for i,val in enumerate(state_estimate_ens_run):
        u_estimate.append(state_estimate_ens_run[i][0])
        v_estimate.append(state_estimate_ens_run[i][1])
        w_estimate.append(state_estimate_ens_run[i][2])

    u_df = pd.DataFrame(u_final_ens)
    v_df = pd.DataFrame(v_final_ens)
    w_df = pd.DataFrame(w_final_ens)
    u_quantiles = u_df.quantile([.05, .95], axis=1)
    v_quantiles = v_df.quantile([.05, .95], axis=1)
    w_quantiles = w_df.quantile([.05, .95], axis=1)

    '''Plotting Function'''
    plt.figure(figsize=(15,10))
    plt.suptitle(f'{da_mode} result')
    plt.subplot(311)
    plt.title('Basis Run')
    plt.title('u vs time')
    plt.ylabel('u')
    plt.xlabel('time')
    plt.fill_between(t_array,u_quantiles.iloc[1].values, u_quantiles.iloc[0].values,alpha=0.3, color=plot_colour,label='5%-95%')
    plt.scatter(t_array, meas_array, marker='+', color='k', label='Measurements')
    plt.plot(t_array, state_array_mod_run[:][0], color='blue',label='Model')
    plt.scatter(t_array, u_estimate, color=plot_colour, label='State Mean Estimate')
    plt.legend()

    plt.subplot(312)
    plt.title('Basis Run')
    plt.title('v vs time')
    plt.ylabel('v')
    plt.xlabel('time')
    plt.fill_between(t_array,v_quantiles.iloc[1].values, v_quantiles.iloc[0].values,alpha=0.3, color=plot_colour,label='5%-95%')
    plt.plot(t_array, state_array_base_run[:][1], color='black', label='Truth')
    plt.plot(t_array, state_array_mod_run[:][1], color='blue', label='Model')
    plt.scatter(t_array, v_estimate, color=plot_colour, label="State Mean Estimate")
    plt.legend()

    plt.subplot(313)
    plt.title('Basis Run')
    plt.title('w vs time')
    plt.ylabel('w')
    plt.xlabel('time')
    plt.fill_between(t_array,w_quantiles.iloc[1].values, w_quantiles.iloc[0].values,alpha=0.3, color=plot_colour,label='5%-95%')
    plt.plot(t_array, state_array_base_run[:][2], color='black', label='Truth')
    plt.plot(t_array, state_array_mod_run[:][2], color='blue', label='Model')
    plt.scatter(t_array, w_estimate, color=plot_colour, label='State Mean Estimate')
    plt.legend()
    plt.legend()
    plt.xlim(0,length_t)
    plt.tight_layout()
    plt.savefig(f'{da_mode}_result.png')
    plt.show()

def plot_da_result_test(settings,state_array_base_run,state_array_mod_run,meas_array,
                   state_array_ens_run, state_estimate_ens_run,t_array,axs):



    u_final_ens = []
    v_final_ens = []
    w_final_ens = []
    u_estimate  = []
    v_estimate  = []
    w_estimate  = []

    length_t = settings['delta_t'] * settings['num_timesteps']

    for i,val in enumerate(state_array_ens_run):
        u_final_ens.append(state_array_ens_run[i][0])
        v_final_ens.append(state_array_ens_run[i][1])
        w_final_ens.append(state_array_ens_run[i][2])

    for i,val in enumerate(state_estimate_ens_run):
        u_estimate.append(state_estimate_ens_run[i][0])
        v_estimate.append(state_estimate_ens_run[i][1])
        w_estimate.append(state_estimate_ens_run[i][2])

    u_df = pd.DataFrame(u_final_ens)
    v_df = pd.DataFrame(v_final_ens)
    w_df = pd.DataFrame(w_final_ens)
    u_quantiles = u_df.quantile([.05, .95], axis=1)
    v_quantiles = v_df.quantile([.05, .95], axis=1)
    w_quantiles = w_df.quantile([.05, .95], axis=1)

    axs[0].set_title('u vs time')
    axs[0].set(xlabel='time', ylabel='v')
    axs[0].fill_between(t_array,u_quantiles.iloc[1].values, u_quantiles.iloc[0].values,alpha=0.3, color='r',label='5%-95%')
    axs[0].scatter(t_array, meas_array, marker='+', color='k', label='Measurements')
    axs[0].plot(t_array, state_array_mod_run[:][0], color='blue',label='Model')
    axs[0].scatter(t_array, u_estimate, color='red', label='State Mean Estimate')
    axs[0].legend()

    axs[1].set_title('v vs time')
    axs[1].set(xlabel = 'time',ylabel='v')
    axs[1].fill_between(t_array,v_quantiles.iloc[1].values, v_quantiles.iloc[0].values,alpha=0.3, color='r',label='5%-95%')
    axs[1].plot(t_array, state_array_base_run[:][1], color='black', label='Truth')
    axs[1].plot(t_array, state_array_mod_run[:][1], color='blue', label='Model')
    axs[1].scatter(t_array, v_estimate, color='red', label="State Mean Estimate")
    axs[1].legend()

    axs[2].set_title('w vs time')
    axs[2].set(xlabel = 'time',ylabel='w')
    axs[2].fill_between(t_array,w_quantiles.iloc[1].values, w_quantiles.iloc[0].values,alpha=0.3, color='r',label='5%-95%')
    axs[2].plot(t_array, state_array_base_run[:][2], color='black', label='Truth')
    axs[2].plot(t_array, state_array_mod_run[:][2], color='blue', label='Model')
    axs[2].scatter(t_array, w_estimate, color='red', label='State Mean Estimate')
    axs[2].legend()
    axs[2].legend()
    axs[2].set_xlim(0,length_t)

    return axs
