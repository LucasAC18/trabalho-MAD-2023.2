# The main simulation function is defined here, along with a main to test it

from helpers import *

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