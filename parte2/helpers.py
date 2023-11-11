# Classes and functions created to help the simulation are defined here

from numpy.random import exponential
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

# class for representing the nodes of the tree 
class Node():

  def __init__(self, value):
    self.value = value
    self.childs = []

  def append_child(self, child):
    self.childs.append(child)

  def get_children(self):
    return self.childs

# class for representing the tree 
class Tree():

  def __init__(self):
    self.num_nodes = 0
    self.current_time = 0
    self.root = Node(self.num_nodes)
    self.order = []
    self.current = self.root
    self.is_finite = False

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

  def child_count_per_node(self, node):
    child_count = [len(node.get_children())]

    for child in node.get_children():
      child_count += self.child_count_per_node(child)

    return child_count
  
  def get_child_count(self):
    return self.child_count_per_node(self.root)
  
  def node_height(self, node):
    if len(node.get_children()) == 0:
      return 0

    height = max([self.node_height(child) for child in node.get_children()])
    return height + 1
  
  def height_per_node(self, node):
    height_count = [self.node_height(node)]

    for child in node.get_children():
      height_count += self.height_per_node(child)

    return height_count

  def get_height(self):
    return self.height_per_node(self.root)
  
  def get_root_outdegree(self):
    return self.get_child_count()[0]
  
  def get_max_outdegree(self):
    return max(self.get_child_count())
  
def get_confidence_interval(metric_per_round, N):
    metric_mean = sum(metric_per_round)/max(N,1)
    sd = [(val-metric_mean)**2 for val in metric_per_round]
    sd = sum(sd)/max((N-1),1)
    sd = math.sqrt(sd)

    return [metric_mean-1.96*sd/math.sqrt(N),metric_mean+1.96*sd/math.sqrt(N)]

# event types constants
TYPES = ["Arrival", "Departure"]

# distribution functions for arrival and departure events
def arrival_dist(_lambda):
  return exponential(1/_lambda)

def departure_dist(_mu, deterministic=False):
  return _mu if deterministic else exponential(1/_mu)