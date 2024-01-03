import datetime as dt
import logging
import sys
import time
import warnings
from ast import Return
import numpy as np
from scipy.optimize import minimize
from epidtool.compartmental_models import EpiDynamicsModel
from epidtool.beta_models import exp, tanh, power 

  
class Minimizer(object):

    """
    Class to fit the compartmemtal models to real-time
    data using the L-BFGS-B algorithm.
    
    epd_model (str) : User defined compartmental model from 
         available models (SIR, SIRD, SEIR, SEIRD).
    beta_model (str) : User defined time-dependent beta model 
         from available models (exp, tanh, power). 
    starting point (tuple) : initial guess for fitting parameters.
         Arguments are positional so you must follow the order: 
         gamma, beta_0, alpha, mu, alpha : FOR SIR      
         gamma, delta,  beta_0, alpha, mu, alpha : FOR SIRD 
         sigma, gamma, beta_0, alpha, mu, alpha : FOR SEIR
         sigma, gamma, delta,  beta_0, alpha, mu, alpha : FOR SEIRD        
    bounds (list of tuples) : [(p1_min,p1_max), (p2_min, p2_max) ...]
        must follow the order as is given in initial guess 
    kwargs = {'N': population, 'I0': I0, 'R0': R0}  for SIR 
        see example below.
    data (pandas data frame) : the columns must match with the initial conditions.
        For example, 
         in case of SIR model:
         Initial conditions : I0, R0
         So the data must have two columns, one for I(t) and another for R(t)
         For the SIRD case : Initial conditions : I0, R0, D0 
         and the data have three columns, for I(t), R(t) and D(t).
         in case of SEIR model:
         Initial conditions : E0, I0, R0
         So the data must have two columns, one for I(t) and another for R(t)
         For the SEIRD case : Initial conditions : E0, I0, R0, D0 
         and the data have three columns, for I(t), R(t) and D(t).
    We must provide the population of a country for which we want to fit the data.
    
    """
    def __init__(self, epd_model, beta_model = None):

        self.epd_model = epd_model 
        self.E = EpiDynamicsModel(epd_model,beta_model)  
        self.beta_model = beta_model
        if self.beta_model:
            self.mod = epd_model+"+"+beta_model
        else:
            self.mod = epd_model
        self.params = None  
        self.pm = {} 

    def initialize (self,starting_point,bounds=(), **kwargs):
 
        self.E.initilization(**kwargs)

        self.starting_point = starting_point 
        print(len(self.starting_point))
        if bounds:
            self.bounds = list(bounds)   
        else:
            if self.beta_model:
                self.bounds = bounds = [(1e-5, 1.0)] * (len(starting_point)-1)+[(0,100)]
            else:
                self.bounds = [(1e-5, 1.0)] * len(self.starting_point)
   
    def fit(self, data):
        """
        This is the fitting module and you must chose the parameters carefully. 
        """
        self.data = data
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        logging.info(f'L-BFGS-B optimization started: {dt.datetime.now()}')
        start_stopwatch = time.time()  
        options={'disp': None, 'maxcor': 10,\
                'ftol': 1.0e-09,\
                'gtol': 1e-06, 'eps': 1e-08,\
                'maxfun': 2500, 'maxiter': 2500,\
                'iprint': -1, 'maxls': 20}

        optimal = minimize(self.loss, self.starting_point,\
            method='L-BFGS-B', bounds=self.bounds,options=options)
        elapsed = time.time() - start_stopwatch
        logging.info(f'Elapsed time: {round(elapsed, 4)}s')
        self.params = list(optimal.x) 
        return optimal 
    def loss (self, point):
        params = list(point)
        solution = self.E.solve(self.data.shape[0], params)
        y_true = self.data.to_numpy()
        if (self.epd_model == 'SEIR' or self.epd_model == 'SEIRD'):
            y_pred = solution.y[2:,:].transpose()
        else:
            y_pred = solution.y[1:,:].transpose() 
        y_mean = y_true.mean (axis=0)
        weight = 1.0 - y_mean / np.sum(y_mean)

        res = weight *  (y_pred - y_true)

        rmsd = np.sqrt(np.mean(res**2)) 

        return rmsd 
        
    def simulate (self):

        """Simulate different compartments based on the fitted
        epidemiological parameters.
            
        Returns
        -------
        tuple
            simulated values of different epidomiological compartments.
        """
        sol = self.E.solve(self.data.shape[0], self.params)
        return sol
    

    def forecast (self, n_days):

        """Predict different compartments based on the fitted
        epidemiological parameters.
        
        Parameters
        ----------
        n_days : int
            Number of days to forecast different compartments in the future.

        Returns
        -------
        tuple
            predicted values of different compartments.
        """
        assert isinstance(n_days, (int, )), '`n_days` must be an integer.'
        return  self.E.solve(self.data.shape[0] + n_days, self.params)

    @property
    def get_params (self):
       if self.params is None:
            raise ValueError('No fitted parameters. Call `fit` method first.')
       param = ["%.6f" % x for x in self.params]
       param = [float(i) for i in param]
       start = 0
       if self.epd_model == 'SIR':
           self.pm['gamma'] = param[0]
           start += 1
       if self.epd_model == 'SIRD':
           self.pm['gamma'] = param[0]
           self.pm['delta'] = param[1]
           start += 2
       if self.epd_model == 'SEIR':
           self.pm['sigma'] = param[0]
           self.pm['gamma'] = param[1]
           start += 2
       if self.epd_model == 'SEIRD':
           self.pm['sigma'] = param[0]
           self.pm['gamma'] = param[1]
           self.pm['delta'] = param[2]
           start += 3
       if self.beta_model:
          [self.pm['beta_0'], self.pm['alpha'], self.pm['mu'], self.pm['tl']] = [param[i] for i in range(start, len(param))]
          self.beta = eval(self.beta_model) (len(self.data), beta_0=self.pm['beta_0'], alpha=self.pm['alpha'],mu=self.pm['mu'], tl=self.pm['tl'])
       else :
          self.pm['beta'] = param[start]
          self.beta = self.pm['beta']
       return self.Rt
    
    @property
    def Rt(self):
        if self.epd_model == 'SIR' or self.epd_model == 'SEIR':
            self.pm['Rt']  = self.beta/ self.pm['gamma'] 

        if self.epd_model == 'SIRD' or self.epd_model == 'SEIRD':
            self.pm['Rt']  = self.beta/ (self.pm['gamma'] + self.pm['delta']) 
        return self.fit_report

    @property
    def fit_report(self):
        print(f'{self.mod} model normalized parameters \n'
              f'------------------------------------ \n')
        fmt = '{:5s}\t{:11.5f}'.format
        print('Parameter\tValue')
        print('---------\t-----')
        for name, param in self.pm.items():
            print(fmt(name, param))
        print(f'------------------------------------ \n'
              f'Thank you for using epitools!'
            ) 
        return    
