from matplotlib.style import available
import numpy as np
from collections import deque
import itertools
import random

class markov_cache:
  def __init__(self, capacity, lookahead):
    self.cache = {} # the actual cache
    self.capacity = capacity # cache's capacity
    self.available_capacity = capacity # capacity available in the cache
    self.lookahead = lookahead # number of elements to look ahead for markov computation
    self.key_counts = {} # counts for each key in cache
    self.count_matrix = {} # counts for transition matrix, will be dict of dicts
    self.last_key = "" # last key accessed
    self.is_empty = True # if cache is empty
    self.hits = 0 # number of cache hits
    self.misses = 0 # number of cache misses

  # If the key is in the cache, return True and the keys value. Otherwise return false
  def get(self, key):
    if key in self.cache:
      # Update frequency counts for this key
      self.key_counts[key] += 1
      if not self.is_empty:
        if key in self.count_matrix[self.last_key]:
          self.count_matrix[self.last_key][key] += 1
        else:
          self.count_matrix[self.last_key][key] = 1
      self.last_key = key
      self.hits += 1
      return True, self.cache[key]
    else:
      self.misses += 1
      return False
  
  # If the given key is in the cache, remove it and return true, otherwise return false
  def remove(self, key):
    if key in self.cache:
      # Adjust avaialble capacity and indices
      elem_size = len(key) + len(self.cache[key])
      self.available_capacity += elem_size
      # remove key from the cache
      self.cache.pop(key)
      return True

    else:
      return False

  
  # Associate the given value with the given key, evicting other keys and values if necessary
  # Return True if this succeeds, false otherwise
  def set(self, key, val):
    elem_size = len(key) + len(val)
    if(elem_size > self.capacity):
      return False
    if key in self.cache:
      needed_size = max(0,len(val) - len(self.cache[key]))
    else:
      needed_size = elem_size
    
    # compute Markov chain probabilities to find what to evict if necessary
    if(self.available_capacity < needed_size):
      # construct numpy arrays for key frequencies
      # have dict to map indices back to keys
      index_to_key = {}
      key_to_index = {}
      num_elem = len(self.key_counts)
      key_counts_arr = np.zeros(num_elem)
      count_matrix_arr = np.zeros((num_elem, num_elem))
      i = 0
      for k, counts in self.count_matrix.items():
        index_to_key[i] = k
        key_to_index[k] = i
        key_counts_arr[i] = self.key_counts[k]
        i += 1
      # construct 2d array for counts
      for k, counts in self.count_matrix.items():
        for next_key, v in counts.items():
          count_matrix_arr[key_to_index[k]][key_to_index[next_key]] = v

      # adjust key counts for the fact that the "next access" for the last access isn't accounted for in count_matrix
      temp_key_counts = key_counts_arr
      temp_key_counts[key_to_index[self.last_key]] -= 1

      # compute key frequencies instead of just counts
      key_freqs = temp_key_counts/np.sum(temp_key_counts)

      # compute Markov transition matrix
      transition_matrix = np.multiply(key_freqs, count_matrix_arr)

      # Store sum of all steps in markov chain
      total_probs = np.zeros((num_elem,num_elem))

      # Matrix after some number of multiplications of our Markov matrix
      # temp_matrix = transition_matrix

      # for i in range(self.lookahead):
      #   temp_matrix = temp_matrix @ transition_matrix
      #   total_probs = total_probs + temp_matrix

      
      all_matrices = [transition_matrix]
      for i in range(self.lookahead - 1):
        recent_matrix = all_matrices[-1]
        all_matrices.append(transition_matrix @ recent_matrix)
      
      for i in range(num_elem):
        for j in range(num_elem):
          total_val = 0
  
          for k in range(1, self.lookahead + 1):
            curr_val = 0
            for subset in itertools.combinations(range(0, self.lookahead), k):
              prod = 1
              for elem in subset:
                prod *= all_matrices[elem][i][j]
              curr_val += prod
            total_val += (-1)**(k+1) * curr_val
          total_probs[i][j] = total_val
      
      
      max_val = total_probs.max()
      last_key_index = key_to_index[self.last_key]
      # remove elements based on probabilities until we have enough space
      # If we're trying to update a key, set the matrix value to a high value so it doesn't get removed
      if key in key_to_index:
        total_probs[last_key_index][key_to_index[key]] = max_val + 1
      while(self.available_capacity < needed_size):
        min_key_index = np.argmin(total_probs[last_key_index])
        min_key = index_to_key[min_key_index]
        # set removed value to max so we don't remove it again
        total_probs[last_key_index][min_key_index] = max_val + 1
        self.remove(min_key)
    # update cache if key is there
    if key in self.cache:
      # change associated value in the cache and update capacity
      self.available_capacity += len(self.cache[key])
      self.available_capacity -= len(val)
      self.cache[key] = val
      # update counts for this key
      self.key_counts[key] += 1
      if not self.is_empty:
        if key in self.count_matrix[self.last_key]:
          self.count_matrix[self.last_key][key] += 1
        else:
          self.count_matrix[self.last_key][key] = 1
      self.last_key = key
      self.is_empty = False
    
    # add key to cache if it's not there
    else:
      self.available_capacity -= elem_size
      if key in self.key_counts:
        self.key_counts[key] += 1
      else:
        self.key_counts[key] = 1
        self.count_matrix[key] = {}
      if not self.is_empty:
        if key in self.count_matrix[self.last_key]:
          self.count_matrix[self.last_key][key] += 1
        else:
          self.count_matrix[self.last_key][key] = 1
      self.last_key = key
      self.cache[key] = val
      self.is_empty = False
    return True
    
  
  def print_matrix(self):
    print("key counts:", self.key_counts)
    print("matrix", self.count_matrix)


################################################################################
# STATS GENERATION                                                             #
################################################################################
def get_stats_random():
  print("Generate Data Randomly")
  cache = markov_cache(50, 2)
  keys = []

  for i in range(10):
    keys.append("file_" + str(i))
  for i in range(9, -1, -1):
    cache.set(keys[i], "val_" + str(i))
    
  for i in range(5000):
    r = random.randint(0, 9)
    cache.get(keys[r])
  
  print("cache hit rate = ", cache.hits / (cache.hits + cache.misses))

def get_stats_markov():
  print("Generate Data from a markov process")
  
  matrix = [[0.3,0,0.3,0,0,0,0.4,0,0,0], [0.1,0,0,0,0.3,0,0,0,0.6,0], 
  [0.9,0,0,0.04,0,0,0.06,0,0,0], [0.1,0,0,0.7,0,0,0.1,0,0.1,0], 
  [1,0,0,0,0,0,0,0,0,0], [0.5,0,0,0,0.3,0,0,0.2,0,0], [1,0,0,0,0,0,0,0,0,0], 
  [0.8,0,0,0,0.1,0,0,0,0.1,0], [1,0,0,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0,0,0]]

  cache = markov_cache(50, 2)
  keys = []

  for i in range(10):
    keys.append("file_" + str(i))
  for i in range(9, -1, -1):
    cache.set(keys[i], "val_" + str(i))
    
  cache.get(keys[3])
  prev_index = 0

  pop = range(0, 10)
  for i in range(4999):
    weights = matrix[prev_index]
    prev_index = random.choices(pop, weights)[0]
    cache.get(keys[prev_index])
  
  print("cache hit rate = ", cache.hits / (cache.hits + cache.misses))
    
get_stats_random()
get_stats_markov()
