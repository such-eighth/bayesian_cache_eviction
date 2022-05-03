from matplotlib.style import available
import numpy as np
from collections import deque
class markov_cache:
  def __init__(self, capacity, min_element_size, lookahead):
    self.cache = {} # the actual cache
    self.capacity = capacity # cache's capacity
    self.available_capacity = capacity # capacity available in the cache
    self.lookahead = lookahead # number of elements to look ahead for markov computation
    self.array_length = capacity//min_element_size + 1 # array lengths to start with
    self.key_counts = np.zeros(self.array_length) # 1d array for counts of each key in cache
    self.count_matrix = np.zeros((self.array_length, self.array_length)) #2d array of counts for transition matrix
    self.available_indices = deque() # queue of available indices, sorry there is prob a better way to do this
    for i in range(self.array_length):
      self.available_indices.append(i)
    self.key_to_index = {} # dict to map keys to indices
    self.index_to_key = {} # dict to map indices to keys
    self.last_key_index = -1 # index of last key

  # If the key is in the cache, return True and the keys value. Otherwise return false
  def get(self, key):
    if key in self.cache:
      key_index = self.key_to_index[key]

      # Update frequency counts for this key
      self.key_counts[key_index] += 1
      if(self.last_key_index != -1):
        self.count_matrix[self.last_key_index][key_index] += 1
      self.last_key_index = key_index
      return True, self.cache[key]
    else:
      return False
  
  # If the given key is in the cache, remove it and return true, otherwise return false
  def remove(self, key):
    if key in self.cache:
      key_index = self.key_to_index[key]
      # Adjust avaialble capacity and indices
      elem_size = len(key) + len(self.cache[key])
      self.available_capacity += elem_size
      self.available_indices.append(key_index)
      # set all counts for key's index to 0
      self.key_counts[key_index] = 0
      for i in range(self.capacity):
        self.count_matrix[i][key_index] = 0
        self.count_matrix[key_index][i] = 0
      # remove key from dictionaries and from the cache
      self.key_to_index.pop(key)
      self.index_to_key.pop(key_index)
      self.cache.pop(key)
      # avoid errors if the last key accessed is the one we just removed
      if self.last_key_index == key_index:
        self.last_key_index = -1
      return True

    else:
      return False
  # NEED TO DO
  # Needs to maybe resize arrays because number of elements is not constant
  def check_and_resize_arrays():
    return True
  
  # Associate the given value with the given key, evicting other keys and values if necessary
  # Return True if this succeeds, false otherwise
  def set(self, key, val):
    elem_size = len(key) + len(val)

    # NEED TO FIX FOR DIFFERENT VALUE SIZES
    if key in self.cache:
      key_index = self.key_to_index[key]
      # change associated value in the cache
      self.cache[key] = val
      # update counts for this key
      self.key_counts[key_index] += 1
      if(self.last_key_index != -1):
        self.count_matrix[self.last_key_index][key_index] += 1
      self.last_key_index = key_index
      return True
    else:
      while(elem_size > self.available_capacity):
        # If the last key has been removed or there is no last key, use LFU
        if(self.last_key_index == -1):
          min_key_index = self.key_counts.argmin()
          min_key = self.index_to_key(min_key_index)
          self.remove(min_key)
        else:
          # adjust key counts for the fact that the "next access" for the last access isn't accounted for in count_matrix
          temp_key_counts = self.key_counts
          temp_key_counts[self.last_key_index] -= 1

          # compute key frequencies instead of just counts
          key_freqs = temp_key_counts/np.sum(temp_key_counts)

          # compute Markov transition matrix
          transition_matrix = np.multiply(key_freqs, self.count_matrix)

          # Store sum of all steps in markov chain
          total_probs = np.zeros((self.capacity,self.capacity))

          # Matrix after some number of multiplications of our Markov matrix
          temp_matrix = transition_matrix
          for i in range(self.lookahead):
            temp_matrix = temp_matrix @ transition_matrix
            total_probs = total_probs + temp_matrix
          # Find which key to remove
          # NEED TO CHANGE TO ONLY DO THE MARKOV STUFF ONCE AND THEN JUST REMOVE SEVERAL BASED ON IT
          min_key_index = np.argmin(total_probs[self.last_key_index])
          min_key = self.index_to_key[min_key_index]
          self.remove(min_key)
      
      # add key to cache and update dicts and maps
      key_index = self.available_indices.popleft()
      self.available_capacity -= elem_size
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

# Test that the cache does not evict any elements if it hasn't reached capacity
def test_evict_before_capacity():

# Test that the cache never allows more elements than its capacity
def test_going_above_capacity():

# Test various correctness operations for one key
def test_single_key():

cache = markov_cache(2, 2)
cache.set("a", 0)
cache.get("a")
cache.set("b", 0)
cache.get("b")
cache.print_matrix()
cache.set("c", 0)
cache.print_matrix()



