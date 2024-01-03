import pandas as pd 
import numpy as np
from epidtool.table import tabulate
class tcoeff:
   """
     A class to estimate tranmission coefficients 
     beta, gamma and delta and reproduction number, 
     rt directly from the real-time data.

     - Souvik Manik, 2022
       For more details : souvik.manik@yahoo.com
   """
   def __init__(self, df):
      """ Constructor.
      
      Parameters
      ----------
      df : Dataframe,
       consist of Date, Confirmed(C), Recovered(R), 
       Death(D).
      """
      self.DF = pd.DataFrame()
      df.index = df['Date'].to_list() 
      self.i = df['Confirmed']
      self.r = df['Recovered']
      self.d = df['Death']

      self.i = self.i - (self.r + self.d)
      self.size = df.shape[0]
      self.dates = df['Date'].to_list()

   def get_tcoeff (self, epd_model, *args):
      """ 
      Estimate real-time transmission coefficients and
      effective reproduction numbers.

      Parameters
      ----------
      epd_model: str, 
          User defined compartmental model from available
            models (SIR, SIRD, SEIR, SEIRD).
      args : int, optional,
          Constant value of Incubation period only for SEIR
          and SEIRD model. 
          
      Returns
      -------
      Dataframe consist of time-dependent transmission
      coefficients and effective reproduction number.
      """ 
      I = self.i
      R = self.r
      D = self.d
      dfc = pd.DataFrame(columns=['Date','beta','gamma','Rt'])
      dI = I.diff(periods=1).iloc[1:]
      dR = R.diff(periods=1).iloc[1:]
      dD = D.diff(periods=1).iloc[1:]
      if (epd_model == 'SEIR' or epd_model == 'SEIRD'):
         sigma_in = args[0]
         sigma = 1.0/sigma_in
         E = ((dI+dR+dD)/sigma)
         dE = E.diff(periods=1).iloc[1:]

      if epd_model == 'SIR':
         dfc['beta']  = (dI + dR + dD ) / I
         dfc['gamma'] = (dR+dD) / I
         dfc['Rt'] = dfc['beta'] / dfc['gamma']

      if epd_model == 'SIRD':
         dfc['beta']  = (dI + dR + dD ) / I
         dfc['gamma'] = dR / I
         dfc['delta'] = dD / I
         dfc['Rt'] = dfc['beta'] / (dfc['gamma'] + dfc['delta'])
         
      if epd_model == 'SEIR':
         dfc['beta'] = (dE + dI + dR + dD ) / I
         dfc['gamma'] = (dR+dD) / I
         dfc['Rt'] = dfc['beta'] / dfc['gamma']
         
      if epd_model == 'SEIRD':
         dfc['beta'] = (dE + dI + dR + dD ) / I
         dfc['gamma'] = dR / I
         dfc['delta'] = dD / I
         dfc['Rt'] = dfc['beta'] / (dfc['gamma'] + dfc['delta'])
            
      dfc['Date'] = self.dates
      dfc.index = self.dates
      self.DF = self.DF._append(dfc,ignore_index=True)
      self.DF=self.DF[self.DF.replace([np.inf, -np.inf], np.nan).notnull().all(axis=1)]
      #print(self.DF)
      return self.DF
   def numstats(self):
      """
      Returns
      -------
      The numerical statistics of time-dependent transmission
      coefficients and effective reproduction number. 
      """
      if (int(self.DF.shape[1]) == 4):
          print("+----------------------------------------+")
          print("|Summary statistics of numerical columns:|")
      else:
          print("+---------------------------------------------------+")
          print("|    Summary statistics of all numerical columns:   |")
      print(tabulate(self.DF.describe().applymap(lambda x: str(int(x)) if abs(x - int(x)) < 1e-6 else str(round(x,4))), headers='keys', tablefmt='psql'))
      print(f'Thank you for using epitools! \n'
            f'-----------------------------'
            ) 


      
