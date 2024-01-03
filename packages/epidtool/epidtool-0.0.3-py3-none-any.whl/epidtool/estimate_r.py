import os
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import scipy
import warnings

class Rt:
   """
     A class to estimate effective reproduction number 
     using Kalman filtering techniques directly from 
     the real-time data.

     - Souvik Manik, 2022
       For more details : souvik.manik@yahoo.com
   """
   def __init__(self, df):
      """ Constructor.
      
      Parameters
      ----------
      df : Dataframe,
       consist of "Date" and "Infected" column. 
      """
      self.DF = pd.DataFrame()
      df.index = df['Date'].to_list() 
      self.i = df['Infected']
      self.rate = self.i.pct_change()
      self.size = df.shape[0]
      self.dates = df['Date'].to_list()
   
   @staticmethod
   def estimate_R(y, gamma, n_start_values_grid = 0, maxiter = 200):
        """Estimate basic reproduction number using
        Kalman filtering techniques
        
        Args:
            y (np array): Time series of growth rate in infections
            gamma (double): Rate of recoveries (gamma)
            n_start_values_grid (int, optional): Number of starting values used in the optimization;
                the effective number of starting values is (n_start_values_grid ** 2)
            maxiter (int, optional): Maximum number of iterations
        
        Returns:
            dict: Dictionary containing the results
            R (np array): Estimated series for R
            se_R (np array): Estimated standard error for R
            flag (int): Optimization flag (0 if successful)
            sigma2_irregular (float): Estimated variance of the irregular component
            sigma2_level (float): Estimated variance of the level component
            gamma (float): Value of gamma used in the estimation

        """
        assert isinstance(n_start_values_grid, int), \
        "n_start_values_grid must be an integer"

        assert isinstance(maxiter, int), \
        "maxiter must be an integer"

        assert n_start_values_grid >= 0 and maxiter > 0, \
        "n_start_values_grid and max_iter must be positive"

        assert isinstance(y, np.ndarray), \
        "y must be a numpy array"

        assert y.ndim == 1, \
        "y must be a vector"

        # Setup model instance
        mod_ll = sm.tsa.UnobservedComponents(y, 'local level')
        
        # Estimate model
        if n_start_values_grid > 0:
            # If requested, use multiple starting
            # values for more robust optimization results
            start_vals_grid = np.linspace(0.01, 2.0, n_start_values_grid) * pd.Series(y).var()
            opt_res = []
            for start_val_1 in start_vals_grid:
                for start_val_2 in start_vals_grid:
                    res_ll = mod_ll.fit(start_params = np.array([start_val_1, start_val_2]),
                                        disp = False, maxiter = maxiter)
                    opt_res.append({'obj_value': res_ll.mle_retvals['fopt'],
                                    'start_val_1': start_val_1,
                                    'start_val_2': start_val_2,
                                    'flag': res_ll.mle_retvals['warnflag']})
            # The optimizer minimizes the negative of
            # the likelihood, so find the minimum value
            opt_res = pd.DataFrame(opt_res)
            opt_res.sort_values(by = 'obj_value', ascending = True, inplace = True)
            res_ll = mod_ll.fit(start_params = np.array([opt_res['start_val_1'][0], 
                                                        opt_res['start_val_2'][0]]),
                                maxiter = maxiter, disp = False)
        else:
            res_ll = mod_ll.fit(maxiter = maxiter, disp = False)
        R = 1 + 1 / (gamma) * res_ll.smoothed_state[0]
        se_R = (1 / gamma * (res_ll.smoothed_state_cov[0] ** 0.5))[0]
        return {'R': R,
                'se_R': se_R,
                'flag': res_ll.mle_retvals['warnflag'],
                'sigma2_irregular': res_ll.params[0],
                'sigma2_level': res_ll.params[1],
                'signal_to_noise': res_ll.params[1] / res_ll.params[0],
                'gamma': gamma}

   def estimate (self, gamma_i, n_start_values_grid = 0, maxiter = 200):
      """ 
        Estimate basic reproduction number using
        Kalman filtering techniques
        
        Args:
            y (np array): Time series of growth rate in infections
            gamma_i (int): Rate of recoveries (gamma)
            n_start_values_grid (int, optional): Number of starting values used in the optimization;
                the effective number of starting values is (n_start_values_grid ** 2)
            maxiter (int, optional): Maximum number of iterations
        
        Returns:
            Dataframe consist of time-dependent effective reproduction number(R) 
            and estimated standard error for R

      """
      gamma = 1/gamma_i
      y = self.rate.values
      Res = self.estimate_R(y, gamma = gamma, n_start_values_grid = 0, maxiter = 200)
      dfc = pd.DataFrame(columns=['Date', 'R', 'se_R'])
      dfc["R"]=Res["R"]
      dfc["se_R"]=Res["se_R"]
      dfc['Date'] = self.dates
      dfc.index = self.dates
      self.DF = self.DF.append(dfc)
      return self.DF
