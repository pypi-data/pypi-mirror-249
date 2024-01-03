from .__init__ import *

class Func():
  
  def sigmoid(X):
    return (1/(1+np.exp(-X)))
  
  def der_sigmoid(X):
    sigma = Func.sigmoid(X)
    return (sigma*(1 - sigma))
  
  def der_tanh(X):
    return np.cosh(X)**-2
  
  def ReLU(X):
    return (X + abs(X))/2
  
  def der_ReLU(X):
    return (X > 0) * 1
  
  def sinc(X):
    return np.sin(X)/X
  
  def der_sinc(X):
    return (X*np.cos(X) - np.sin(X))/X**2
  
  def x_squared(X):
    return X**2
  
  def der_x_squared(X):
    return 2*X
  
  def lse(x, y):
    return (x - y)**2
  
  def acc(x, y):
    return ( (x >= .5)*1 != y)*1

    