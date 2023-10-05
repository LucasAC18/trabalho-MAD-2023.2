# Classes and functions created to help the simulation are defined here

from numpy.random import poisson, exponential
import math

# main class for implementing the event queue
# events are represented by a tuple => (type, event_time)
class Queue():

  def __init__(self):
    self.queue = []

  def __str__(self):
    return str(self.queue)

  def push(self, new_element):
    self.queue.append(new_element)
    self.queue.sort(key=lambda e: e[1])

  def pop(self):
    served = self.queue.pop(0)
    return served

  def is_empty(self):
    return len(self.queue) == 0

# class to store the metrics obtained from the simulation
class Statistics():

  def __init__(self, mcpr, mwtpr, mestpr, fthepr):
    self.mean_customers_per_round = mcpr
    self.mean_customers_in_system = sum(mcpr)/len(mcpr)
    self.mean_customers_interval = self.get_confidence_interval(self.mean_customers_per_round, self.mean_customers_in_system, len(mcpr))

    self.mean_wait_time_per_round = mwtpr
    self.mean_wait_time_in_system = sum(mwtpr)/len(mwtpr)
    self.mean_wait_time_interval = self.get_confidence_interval(self.mean_wait_time_per_round, self.mean_wait_time_in_system, len(mwtpr))

    self.mean_empty_state_time_per_round = mestpr
    self.mean_empty_state_time_in_system = sum(mestpr)/len(mestpr)
    self.mean_empty_state_interval = self.get_confidence_interval(self.mean_empty_state_time_per_round, self.mean_empty_state_time_in_system, len(mestpr))

    self.fraction_times_hit_empty_per_round = fthepr
    self.fraction_times_hit_empty_in_system = sum(fthepr)/len(fthepr)
    self.fraction_times_hit_empty_interval = self.get_confidence_interval(self.fraction_times_hit_empty_per_round, self.fraction_times_hit_empty_in_system, len(fthepr))

  def get_confidence_interval(self, metric_per_round, metric_mean, N):
    sd = [(val-metric_mean)**2 for val in metric_per_round]
    sd = sum(sd)/max((N-1),1)
    sd = math.sqrt(sd)

    return [metric_mean-1.96*sd/math.sqrt(N),metric_mean+1.96*sd/math.sqrt(N)]
  
  def __str__(self):
    return f'Mean customers in system    => {self.mean_customers_in_system}\nConfidence Interval         => {self.mean_customers_interval}\n\n' + \
           f'Mean wait time in system    => {self.mean_wait_time_in_system}\nConfidence Interval         => {self.mean_wait_time_interval}\n\n' + \
           f'Mean 0 state time in system => {self.mean_empty_state_time_in_system}\nConfidence Interval         => {self.mean_empty_state_interval}\n\n' + \
           f'Fraction of times 0 state   => {self.fraction_times_hit_empty_in_system}\nConfidence Interval         => {self.fraction_times_hit_empty_interval}\n'

# event types constants
TYPES = ["Arrival", "Departure"]

# distribution functions for arrival and departure events
def arrival_dist(_lambda):
  return exponential(1/_lambda)

def departure_dist(_mu):
  return exponential(1/_mu)

# Little's Law formula to calculate mean value of number of clients on the system analytically
def littles_law(_lambda, _mu):
  rho = _lambda/_mu

  return rho/(1-rho)