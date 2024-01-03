from .__init__ import *
from .functions import Func

class MyLittlePonyM():
  
  def __init__(self, n_epochs = 100, learning_rate = .001, neurons_layer = 2, layers = 2, momentum = 0.0001, act_func = 'ReLU', metric = 'lse'):
    
    self.ran_epochs = 0
    self.max_epochs = n_epochs
    self.eta = learning_rate
    self.alpha = momentum
    self.error = []; self.error_val = []

    self.hiddenLayers = layers
    self.neuronsPerHiddenLayer = neurons_layer
    self.Input = [0]*(layers+1); self.output = [0]*(layers+2)

    self.g = getattr(Func, act_func)
    self.der_g = getattr(Func, 'der_' + act_func)
    self.metric = getattr(Func, metric)

    self.es = False
    self.patience = 0
    self.startEpoch = 0

  def init_weights(self, x_shape):
    self.weights = []
    self.weights.append(np.squeeze(np.random.uniform(-1,1, size = [x_shape[1] + 1, self.neuronsPerHiddenLayer])).T)
    for i in range(self.hiddenLayers - 1):
      self.weights.append(np.squeeze(np.random.uniform(-1,1, size = [self.neuronsPerHiddenLayer + 1, self.neuronsPerHiddenLayer])).T)
    self.weights.append(np.random.uniform(-1,1, size = (self.neuronsPerHiddenLayer + 1,)).T)
    return

  def SetES(self, patience = 50, start = 0):
    self.es = True
    if patience <= 0 or start < 0:
      raise TypeError('Patience ou Start inválidos (Patience <= 0 ou Start < 0).')
    self.patience = patience
    self.startEpoch = start
    return

  def foward(self, X):
    self.output[0] = X
    for i, weights in enumerate(self.weights):
      self.Input[i] = np.dot(weights, np.append(-1, self.output[i]))
      if i != len(self.weights) - 1:
        self.output[i + 1] = self.g(self.Input[i])
      else:
        self.output[i + 1] = Func.sigmoid(self.Input[i])
    return


  def backward(self, X, y, prev):
    delta = (y - self.output[-1]) * Func.der_sigmoid(self.Input[-1])
    self.weights[-1] = self.weights[-1] + self.eta * delta * np.append(-1, self.output[-2])
    e_k = delta * self.weights[-1][1:]
    for L in range(2, self.hiddenLayers + 2):
      self.weights[-L] += np.dot((self.eta*e_k*self.der_g(self.Input[-L])).reshape(-1,1),
                                       np.append(-1, self.output[-L-1]).reshape(1,-1)) + self.alpha*(self.weights[-L] - prev[-L])
      e_k = np.dot(self.weights[-L].T[1:], e_k)
    return

  def train(self, X, y, x_val, y_val):
    self.init_weights(X.shape)
    prev_weights = [deepcopy(self.weights), deepcopy(self.weights)]
    best_metric = 0; patienceSpent = 0
    for i in range(self.max_epochs):
      error = 0; error_val = 0; metric = 0
      #training set
      for j, k in zip(X, y):
        self.foward(j)
        error += Func.lse(self.output[-1], k)
        self.backward(j, k, prev_weights[-1])
      self.ran_epochs += 1
      self.error.append(error)
      prev_weights.pop(); prev_weights.insert(0, deepcopy(self.weights))
      #validation set
      for m,n in zip(x_val, y_val):
        self.foward(m)
        error_val += Func.lse(self.output[-1], n)
        metric += self.metric(self.output[-1], n)
      self.error_val.append(error_val)
      #save best performing model
      if metric < best_metric or i == 0:
        best_metric = metric; best_weight = deepcopy(self.weights)
      #early stopping
      if self.es and self.startEpoch <= self.ran_epochs:
        if self.error_val[-1] <= min(self.error_val):
          patienceSpent = 0
        else:
          patienceSpent += 1
        if patienceSpent == self.patience:
          print('Early Stopping. Ran Epochs: ', self.ran_epochs)
          break
    #save best performing model
    self.weights = best_weight
    return

  def classifier(self, X):
    y = []
    for i in X:
        self.foward(i)
        y.append(self.output[-1])
    return (np.array(y) >= .5)*1

  def score(self, X, y):
    y_pred = self.classifier(X)
    return sum((y == y_pred))/len(y)*100

