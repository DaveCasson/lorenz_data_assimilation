[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/DaveCasson/lorenz_data_assimilation/issues)

# Ensemble Data Assimilation with the Lorenz System

Data assimilation allows measurements of a system to be merged with models in order to improve simulations. While data assimilation can be applied to very complex systems, it can be demonstrated in more simple contexts. Synthetic test cases are often used to evaluate different methods.

This repository contains simple data assimilation examples coded in Python based on the [Lorenz system](https://en.wikipedia.org/wiki/Lorenz_system). Specifically ensemble data assimilation methods such as the Particle Filter.

## Lorenz Equations

The Lorenz equations are a system of three differential equations:

 ![lorenz equations](https://wikimedia.org/api/rest_v1/media/math/render/svg/7928004d58943529a7be774575a62ca436a82a7f)

This simplified mathematical model for atmospheric convection is sensitive to the equation parameters as well as the the initial conditions. The system solution can be generated and plotted in time by solving the differential equations, in this case using an explicit euler solution that step the equations through time.

## Test Case for Data assimilation

To test and implement the data assimilation algorithms, we first assume that there is a "perfect" model of the lorenz system by defining set model parameters and initial conditions. This "perfect" version provides the synthetic measurements for the data assimilation algorithm.

An "actual" model of the perfect system is then approximated by changing one of the model parameters. The actual model will deviate slightly from the perfect model. The measurements of the perfect model are used by data assimilation algorithms to improve the actual model estimate.

## Try it out for yourself

Open the Jupyter Notebook to test for yourself the implementation of the Lorenz equation and the effect of different data assimilation algorithms.
