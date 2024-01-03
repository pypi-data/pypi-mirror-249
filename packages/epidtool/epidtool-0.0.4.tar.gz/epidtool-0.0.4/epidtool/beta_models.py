import numpy as np

def polynom (t, **kargs):
   # Loli-2020, 0.0 < alpha < 1    

   if t < kargs['tl'] :
      beta_t = kargs['beta_0'] 
   else :
      beta_t = kargs['beta_0'] * (1.0 - kargs['alpha'] * kargs['mu'] * (t-kargs['tl'])/t)
   return beta_t

def power (t, **kargs):
   # https://doi.org/10.1038/s41598-020-78739-8   

   if t < kargs['tl'] :
      beta_t = kargs['beta_0'] 
   else :
      beta_t = kargs['beta_0'] * (1.0 - kargs['alpha'])** (kargs['mu'] *  (t- kargs['tl']))
   return beta_t
   
def exp(t, **kargs):
   # Fanelli-2020

   if t  < kargs['tl']  :
      beta_t = kargs['beta_0']
   else :
      beta_t = kargs['beta_0'] *  ((1.0 -  kargs['alpha']) \
         * np.exp (-kargs['mu'] * (t - kargs['tl']) ) \
         + kargs['alpha'])
   return beta_t


def tanh (t, **kargs):
   # Goswami-2020
   if t  < kargs['tl'] :
      beta_t = kargs['beta_0']
   else :
      beta_t = kargs['beta_0'] * (1.0 -  kargs['alpha'] \
         * np.tanh (kargs['mu'] *  (t- kargs['tl'])))
   return beta_t


