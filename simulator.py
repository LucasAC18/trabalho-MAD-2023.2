# The main simulation function is defined here, along with a main to test it

from helpers import *

# function to properly simulate the queue
def simulate(_lambda, _mu, total_time = 10, total_rounds = 1):
  mean_customers_per_round = [] # mean number of customers in the system per round
  mean_wait_time_per_round = [] # mean wait time in the system per round
  mean_empty_state_time_per_round = [] # mean time in which the system was empty per round
  fraction_times_hit_empty_per_round = [] # fraction of times the system hit 0 customers per round

  # main loop
  for _ in range(total_rounds):
    simulation_queue = Queue() # event queue
    simulation_time = 0 # current time in the simulation
    persons_counter = 0 # number of persons currently in the system
    persons_arrived = 0 # number of persons that arrived in the system
    times_system_empty = 0 # number of times the system hit 0 persons
    events_counter = 0 # number of events treated

    arrival_time = arrival_dist(_lambda) # time of the next arrival
    service_end_time = total_time # time of the next departure
    last_event_time = 0 # time of the last event treated
    area_person_time = 0 # area of the number of persons in the system over time, used to calculate some metrics
    empty_state_time = 0 # amount of time in which the system was empty

    simulation_queue.push((TYPES[0], arrival_time))

    while True:
      event = simulation_queue.pop() # takes the next event from the queue

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
        arrival_time = simulation_time + arrival_dist(_lambda)
        simulation_queue.push((TYPES[0], arrival_time))

        if persons_counter == 1:  # if changed from state 0 to 1, push departure and update empty time
          empty_state_time += simulation_time - last_event_time
          service_end_time = simulation_time + departure_dist(_mu)
          simulation_queue.push((TYPES[1], service_end_time))

      elif event[0] == TYPES[1]:       # if the event is a departure
        simulation_time = event[1]
        area_person_time += persons_counter * (simulation_time - last_event_time)
        persons_counter -= 1

        if persons_counter > 0: # if there are still people in the system, push next departure
          service_end_time = simulation_time + departure_dist(_mu)
          simulation_queue.push((TYPES[1], service_end_time))
        else:                  # if the system became empty, update the number of times it became empty
          times_system_empty += 1

      last_event_time = simulation_time # after treating the event, update last event time
      events_counter += 1 # update the number of events treated

    # store the results of the round into lists
    mean_customers_per_round.append(area_person_time/total_time)
    mean_wait_time_per_round.append(area_person_time/persons_arrived)
    mean_empty_state_time_per_round.append(empty_state_time/total_time)
    fraction_times_hit_empty_per_round.append(times_system_empty/events_counter)

  return Statistics(mean_customers_per_round, mean_wait_time_per_round, mean_empty_state_time_per_round, fraction_times_hit_empty_per_round)

if __name__ == "__main__":
  l = 1
  m = 2

  stats = simulate(l,m,total_time=1000,total_rounds=10)
  
  print(stats)
  print(f'Analytic mean customers in system => {littles_law(l,m)}')
  print(f'Analytic mean wait time in system => {littles_law(l,m)/l}')