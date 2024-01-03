import numpy as np
from scipy.integrate import solve_ivp
from epidtool.beta_models import exp, tanh, power 
from epidtool.models import SIR, SIRD, SEIR, SEIRD

class EpiDynamicsModel:

   """
   Class to initialize and solve the model equations.
   for time varying contact rate beta, parameterized
   by a set of four parameters - beta_0, alpha, mu and tl.
   
   Example : 
   for SIR model,
     E = Epidemology ('SIR','exp')

     E.initilization (N=1000,I0=10,R0=0)
     #s = E.evolve (size,[gamma,beta_0,alpha,mu,tl])
     s = E.evolve (160,[0.1,0.24,0.1,0.0,1000])


     outputs: 
        s.t = t 
        s.y[0] = S(t)
        s.y[1] = I(t)
        s.y[2] = R(t)
   """

   def __init__(self, epd_model, beta_model=None):
      """
      Constractor.
      epd_model (str) : User defined compartmental model from 
         available models (SIR, SIRD, SEIR, SEIRD).
      beta_model (str) : User defined time-dependent beta model 
         from available models (exp, tanh, power).
      """
      self.epd_model = epd_model
      self.model = eval (epd_model)
      self.beta_model = beta_model 


   def initilization (self, **kwargs):

      try:
         self.N = kwargs['N']
         I0 = kwargs['I0']
         R0 = kwargs['R0']
 
         if self.epd_model == 'SIR':
             S0 = self.N - I0 -  R0
             self.Y0 = [S0, I0, R0]

         if self.epd_model == 'SIRD':
             D0 = kwargs['D0']
             S0 = self.N - D0 - I0 - R0
             self.Y0 = [S0, I0, R0, D0]
 
         if self.epd_model == 'SEIR':
             E0 = kwargs['E0']
             S0 =  self.N - I0 - R0 - E0  
             self.Y0 = [S0, E0, I0, R0]
             
         if self.epd_model == 'SEIRD':
             E0 = kwargs['E0']
             D0 = kwargs['D0']
             S0 =  self.N - I0 - R0 - E0 -D0 
             self.Y0 = [S0, E0, I0, R0, D0]
    
      except:
         print("You must give valid initial conditions")  
         print(kwargs)
         return 

   def func (self, t, y, *args):

       P = {'N': self.N}
       start = 0
       if self.epd_model == 'SIR':
           P ['gamma'] = args[0]
           start += 1
       if self.epd_model == 'SIRD':
           P['gamma'] = args[0]
           P ['delta'] = args[1]
           start += 2
       if self.epd_model == 'SEIR':
           P['sigma'] = args[0]
           P['gamma'] = args[1]
           start += 2
       if self.epd_model == 'SEIRD':
           P['sigma'] = args[0]
           P['gamma'] = args[1]
           P['delta'] = args[2]
           start += 3
       if self.beta_model:
          [beta_0, alpha, mu, tl] = [args[i] for i in range(start, len(args))]
          P['beta'] = eval(self.beta_model) (t, beta_0=beta_0, alpha=alpha,mu=mu, tl=tl)
       else :
          P['beta'] = args[start]
  
       return self.model (t, y, **P)


   def solve (self, size, args):
    
      """Solve epidomiological equations to simulate different 
      model compartments.

        Returns
        -------
        tuple
            Simulated values of diffent compartments.
      """
      assert isinstance(size, (int, )), '`n_days` must be an integer.'
      self.t = np.arange(0, size, 1)
      
      sol = solve_ivp(self.func,  [0, size], tuple(self.Y0),\
         t_eval = self.t,vectorized=True, args=args)
 
      return sol 
 
