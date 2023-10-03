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

  def __init__(self, mcpr, mwtpr, mestpr):
    self.mean_customers_per_round = mcpr
    self.mean_customers_in_system = sum(mcpr)/len(mcpr)
    self.mean_customers_interval = self.get_confidence_interval(self.mean_customers_per_round, self.mean_customers_in_system, len(mcpr))

    self.mean_wait_time_per_round = mwtpr
    self.mean_wait_time_in_system = sum(mwtpr)/len(mwtpr)
    self.mean_wait_time_interval = self.get_confidence_interval(self.mean_wait_time_per_round, self.mean_wait_time_in_system, len(mwtpr))

    self.mean_empty_state_time_per_round = mestpr
    self.mean_empty_state_time_in_system = sum(mestpr)/len(mestpr)
    self.mean_empty_state_interval = self.get_confidence_interval(self.mean_empty_state_time_per_round, self.mean_empty_state_time_in_system, len(mestpr))

  def get_confidence_interval(self, metric_per_round, metric_mean, N):
    sd = [(val-metric_mean)**2 for val in metric_per_round]
    sd = sum(sd)/max((N-1),1)
    sd = math.sqrt(sd)

    return [metric_mean-1.96*sd/math.sqrt(N),metric_mean+1.96*sd/math.sqrt(N)]

# event types
TYPES = ["Arrival", "Departure"]

# distribution functions for arrival and departure
def arrival_dist(_lambda):
  return exponential(1/_lambda)

def departure_dist(_mu):
  return exponential(1/_mu)

# Little Law formula to calculate mean value of number of clients on the system
def littles_law(_lambda, _mu):
  rho = _lambda/_mu

  return rho/(1-rho)

# function to properly simulate the queue
def simulate(_lambda, _mu, total_time = 10, total_rounds = 1):
  mean_customers_per_round = []
  mean_wait_time_per_round = []
  mean_empty_state_time_per_round = []

  # main loop
  for _ in range(total_rounds):
    simulation_queue = Queue()
    simulation_time = 0
    persons_counter = 0
    persons_arrived = 0

    arrival_time = arrival_dist(_lambda)
    service_end_time = total_time
    last_event_time = 0
    area_person_time = 0
    empty_state_time = 0

    simulation_queue.push((TYPES[0], arrival_time))

    while True:
      event = simulation_queue.pop()

      # run simulation until an event time exceeds the timeframe
      if event[1] > total_time:
        if persons_counter == 0:
          empty_state_time += total_time - last_event_time
        break

      if event[0] == TYPES[0]:          # if the event is an arrival
        simulation_time = event[1]
        area_person_time += persons_counter * (simulation_time - last_event_time)
        persons_counter += 1
        persons_arrived += 1

        if persons_counter == 1:  # if changed from state 0 to 1, push departure and update empty time
          empty_state_time += simulation_time - last_event_time
          service_end_time = simulation_time + departure_dist(_mu)
          simulation_queue.push((TYPES[1], service_end_time))

        last_event_time = simulation_time
        arrival_time = simulation_time + arrival_dist(_lambda)
        simulation_queue.push((TYPES[0], arrival_time))

      elif event[0] == TYPES[1]:       # if the event is a departure
        simulation_time = event[1]
        area_person_time += persons_counter * (simulation_time - last_event_time)
        persons_counter -= 1
        last_event_time = simulation_time

        if persons_counter > 0:
          service_end_time = simulation_time + departure_dist(_mu)
          simulation_queue.push((TYPES[1], service_end_time))

    # store the results of the round into lists
    mean_customers_per_round.append(area_person_time/total_time)
    mean_wait_time_per_round.append(area_person_time/persons_arrived)
    mean_empty_state_time_per_round.append(empty_state_time/total_time)

  return Statistics(mean_customers_per_round, mean_wait_time_per_round, mean_empty_state_time_per_round)

if __name__ == "__main__":
  l = 2
  m = 4

  stats = simulate(l,m,total_time=1000,total_rounds=10)
  print(f'Mean customers in system    => {stats.mean_customers_in_system}\nConfidence Interval         => {stats.mean_customers_interval}\n')
  print(f'Mean wait time in system    => {stats.mean_wait_time_in_system}\nConfidence Interval         => {stats.mean_wait_time_interval}\n')
  print(f'Mean 0 state time in system => {stats.mean_empty_state_time_in_system}\nConfidence Interval         => {stats.mean_empty_state_interval}\n')

  print(f'Analytic mean customers in system => {littles_law(l,m)}')
  print(f'Analytic mean wait time in system => {littles_law(l,m)/l}')