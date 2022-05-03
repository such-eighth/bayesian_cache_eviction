from matplotlib.style import available
import numpy as np
from collections import deque
class markov_cache:
  def __init__(self, capacity, lookahead):
    self.cache = {} # the actual cache
    self.capacity = capacity # cache's capacity
    self.lookahead = lookahead # k
    self.key_counts = np.zeros(capacity) # 1d array for counts of each key in cache
    self.count_matrix = np.zeros((capacity,capacity)) #2d array of counts for transition matrix
    self.available_indices = deque() # queue of available indices, sorry there is prob a better way to do this
    for i in range(capacity):
      self.available_indices.append(i)
    self.key_to_index = {}
    self.index_to_key = {}
    self.last_key_index = -1

  def get(self, key):
    if key in self.cache:
      key_index = self.key_to_index[key]
      self.key_counts[key_index] += 1
      if(self.last_key_index != -1):
        self.count_matrix[self.last_key_index][key_index] += 1
      self.last_key_index = key_index
      return True, self.cache[key]
    else:
      return False
  
  def remove(self, key):
    if key in self.cache:
      key_index = self.key_to_index[key]
      print(key_index)
      self.available_indices.append(key_index)
      self.key_counts[key_index] = 0
      for i in range(self.capacity):
        self.count_matrix[i][key_index] = 0
        self.count_matrix[key_index][i] = 0
      self.key_to_index.pop(key)
      self.index_to_key.pop(key_index)
      self.cache.pop(key)
      if self.last_key_index == key_index:
        self.last_key_index = -1
      return True

    else:
      return False
  
  def set(self, key, val):
    if key in self.cache:
      key_index = self.key_to_index[key]
      self.cache[key] = val
      self.key_counts[key_index] += 1
      if(self.last_key_index != -1):
        self.count_matrix[self.last_key_index][key_index] += 1
      self.last_key_index = key_index
      return True
    else:
      while(len(self.available_indices) == 0):
        # don't think this should happen but just in case
        # if the last key has been removed just do LFU
        if(self.last_key_index == -1):
          min_key_index = self.key_counts.argmin()
          min_key = self.index_to_key(min_key_index)
          self.remove(min_key)
        else:
          # adjust key counts for the fact that the "next access" for the last access isn't accounted for in count_matrix
          temp_key_counts = self.key_counts
          temp_key_counts[self.last_key_index] -= 1

          key_freqs = temp_key_counts/np.sum(temp_key_counts)
          transition_matrix = np.multiply(key_freqs, self.count_matrix)
          total_probs = np.zeros((self.capacity,self.capacity))
          temp_matrix = transition_matrix
          for i in range(self.lookahead):
            temp_matrix = temp_matrix @ transition_matrix
            total_probs = total_probs + temp_matrix
          min_key_index = np.argmin(total_probs[self.last_key_index])
          min_key = self.index_to_key[min_key_index]
          self.remove(min_key)
          print(self.count_matrix)

      key_index = self.available_indices.popleft()
      self.key_to_index[key] = key_index
      self.index_to_key[key_index] = key
      self.key_counts[key_index] = 1
      if(self.last_key_index != -1):
        self.count_matrix[self.last_key_index][key_index] = 1
      self.last_key_index = key_index
      self.cache[key] = val
  
  def print_matrix(self):
    for key, val in self.key_to_index.items():
      print("key: ", key,": freq: ",self.key_counts[val])
      for k,v in self.key_to_index.items():
        print(k, " : ",self.count_matrix[val][v])

cache = markov_cache(2, 2)
cache.set("a", 0)
cache.get("a")
cache.set("b", 0)
cache.get("b")
cache.print_matrix()
cache.set("c", 0)
cache.print_matrix()



