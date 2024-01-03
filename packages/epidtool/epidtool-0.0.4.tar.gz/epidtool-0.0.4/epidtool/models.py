import numpy as np
from scipy.integrate import solve_ivp

def info():
    A = """
    +-------------------------------------------------------------------+
    |   This Module Contains Different Epidemiological Model Equations  |
    +-------------------------------------------------------------------+
    |  List of models:                                                  |
    |  1. Succeptable-Infected-Removed(SIR) model.                      |
    |  2. Succeptable-Infected-Recovered-Deceased(SIRD) model.          |
    |  3. Succeptable-Exposed-Infected-Removed(SEIR) model.             |
    |  4. Succeptable-Exposed-Infected-Recovered-Deceased(SEIRD) model. |
    +-------------------------------------------------------------------+
    """
    print(A)

def SIR (t, z, **kwargs):
   """
    Succeptable-Infected-Removed(SIR) model. For details check: 
    https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
    
    Parameters
    ----------
    t : numpy.ndarray
        Discrete time points.
    z : list or tuple
        Values of S, I and R.
    **kwargs : N, beta, sigma, gamma, delta
    N : int
        Total population
    beta : float
        Contact (infectious) rate controls the rate of spread. 
    gamma : float
        Recovery rate.   
    Returns
    -------
    list
        Values of the SIR compartmental model free parameters.
    """

   N, beta, gamma = \
      kwargs['N'], kwargs['beta'], kwargs['gamma']

   S, I, R  = z[0]/N, z[1], z[2]
   dSdt = -beta*S*I
   dIdt = beta*S*I-gamma*I
   dRdt = gamma*I
   return [dSdt, dIdt, dRdt]

def SIRD (t, z,  **kwargs):

   """
    Succeptable-Infected-Recovered-Deceased(SIRD) model. For details check: 
    https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
    
    Parameters
    ----------
    t : numpy.ndarray
        Discrete time points.
    z : list or tuple
        Values of S, I, R and D.
    **kwargs : N, beta, gamma, delta
    N : int
        Total population
    beta : float
        Contact (infectious) rate controls the rate of spread. 
    gamma : float
        Recovery rate.
    delta : float
        Recovery (or mortality) rate.
        
    Returns
    -------
    list
        Values of the SIRD compartmental model free parameters.
    """
   
   N, beta,  gamma, delta =\
       kwargs['N'], kwargs['beta'], kwargs['gamma'], kwargs['delta']

   S, I, R, D  = z[0]/N, z[1], z[2], z[3]

   dSdt = -beta*S*I
   dIdt = beta*S*I-(gamma+delta) * I
   dRdt = gamma*I
   dDdt = delta * I
   return [dSdt, dIdt, dRdt, dDdt]


def SEIR (t, z, **kwargs):
   
   """
    Succeptable-Exposed-Infected-Removed(SEIR) model. For details check: 
    https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
    
    Parameters
    ----------
    t : numpy.ndarray
        Discrete time points. 
    z : list or tuple
        Values of S, E, I and R.
    **kwargs : N, beta, sigma, gamma.
    N : int
        Total population.
    beta : float
        Contact (infectious) rate controls the rate of spread. 
    sigma : float
        Incubation rate, the reciprocal value of the incubation period. 
    gamma : float
        Removal or recovery rate.   
    Returns
    -------
    list
        Values of the SEIR compartmental model free parameters.
    """
   N, beta, gamma, sigma =\
       kwargs['N'], kwargs['beta'], kwargs['gamma'], kwargs['sigma']

   S, E, I, R  = z[0]/N, z[1], z[2], z[3]

   dSdt = -beta*S*I
   dEdt = beta*S*I-sigma*E
   dIdt = sigma*E-gamma*I
   dRdt = gamma*I
   return [dSdt, dEdt, dIdt, dRdt]

def SEIRD (t, z, **kwargs):
    """
    Succeptable-Exposed-Infected-Recovered-Deceased(SEIRD) model. For details 
    check: https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology
    
    Parameters
    ----------
    t : numpy.ndarray
        Discrete time points.
    z : list or tuple
        Values of S, E, I, R and D.
    **kwargs : N, beta, sigma, gamma, delta
    N : int
        Total population
    beta : float
        Contact (infectious) rate controls the rate of spread. 
    sigma : float
        Incubation rate, the reciprocal value of the incubation period. 
    gamma : float
        Recovery rate.
    delta : float
        Recovery (or mortality) rate.
        
    Returns
    -------
    list
        Values of the SEIRD compartmental model free parameters.
    """
    N, beta,  gamma, sigma, delta =\
       kwargs['N'], kwargs['beta'], kwargs['gamma'], kwargs['sigma'], kwargs['delta']
    S, E, I, R, D  = z[0]/N, z[1], z[2], z[3], z[4]
    dSdt = -beta*S*I
    dEdt = beta*S*I - sigma*E
    dIdt = sigma*E - (gamma+delta) * I
    dRdt = gamma*I
    dDdt = delta*I
    return [dSdt, dEdt, dIdt, dRdt, dDdt]
