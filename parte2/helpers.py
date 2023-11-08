# Classes and functions created to help the simulation are defined here

from numpy.random import exponential

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

# class for representing the nodes of the tree 
class Node():

  def __init__(self, value):
    self.value = value
    self.childs = []

  def append_child(self, child):
    self.childs.append(child)

  def get_childs(self):
    return self.childs

# class for representing the tree 
class Tree():

  def __init__(self):
    self.num_nodes = 0
    self.current_time = 0
    self.root = Node(self.num_nodes)
    self.order = []
    self.current = self.root

  def create_node(self):
    self.num_nodes += 1
    return Node(self.num_nodes)
  
  def arrive_client(self):
    current = self.current
    new = self.create_node()
    current.append_child(new)
    self.order.append(new)

  def next_server(self):
    if len(self.order) == 0:
      self.current = None
    else:
      self.current = self.order.pop(0)


# event types constants
TYPES = ["Arrival", "Departure"]

# distribution functions for arrival and departure events
def arrival_dist(_lambda):
  return exponential(1/_lambda)

def departure_dist(_mu):
  return exponential(1/_mu)