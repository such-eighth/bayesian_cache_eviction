from markov_cache import markov_cache

# Test various correctness operations for one key
def test_single_key():
  cache = markov_cache(32,2)
  cache.set("a","123")
  get_ok, get_val = cache.get("a")
  if(get_ok == False):
    return False
  if(get_val != "123"):
    return False
  cache.set("a","bcd")
  get_ok, get_val = cache.get("a")
  if(get_ok == False):
    return False
  if(get_val != "bcd"):
    return False
  return True

# test that cache allows empty string as a key
def test_empty_string_key():
  cache = markov_cache(32,2)
  cache.set("","123")
  get_ok, get_val = cache.get("")
  if(get_ok == False):
    return False
  if(get_val != "123"):
    return False
  return True


# test that cache allows empty value
def test_empty_value():
  cache = markov_cache(32,2)
  cache.set("a",[])
  get_ok, get_val = cache.get("a")
  if(get_ok == False):
    return False
  if(get_val != []):
    return False
  return True

# Test that the cache does not evict any elements if it hasn't reached capacity
def test_evict_before_capacity():
  cache = markov_cache(32,2)
  cache.set("a", "123456")
  cache.set("b", "123456")
  cache.set("a", "123")
  cache.set("c", "123456")
  cache.set("d", "123456")
  cache.set("e", "123456")
  # all elements should be in cache
  for key in ["a","b","c","d","e"]:
    in_cache = cache.get(key)
    if not in_cache:
      return False
  return True

# Test that the cache never allows more than its capacity
def test_going_above_capacity():
  # trying to add an element with too much capacity
  cache = markov_cache(32,2)
  cache.set("a", "123456")
  cache.set("b", "123456")
  cache.set("a", "123")
  cache.set("c", "123456")
  cache.set("d", "123456")
  cache.set("e", "12345678")
  found_notin = False
  for key in ["a","b","c","d","e"]:
    in_cache = cache.get(key)
    if not in_cache:
      found_notin = True
  if(found_notin == False):
    return False

  # trying to set a different val for an element already in cache
  cache = markov_cache(32,2)
  cache.set("a", "123456")
  cache.set("b", "123456")
  cache.set("c", "123456")
  cache.set("d", "123456")
  cache.set("a", "1234567891011")
  found_notin = False
  for key in ["a","b","c","d"]:
    in_cache = cache.get(key)
    if not in_cache:
      found_notin = True
  if(found_notin == False):
    return False
  return True

# test that overwriting key with set consumes the correct amount of space
def test_set_overwrite_space():
  cache = markov_cache(32,2)
  cache.set("a","123")
  cache.set("a", "123456")
  if(cache.available_capacity != 25):
    return False
  cache.set("a","1")
  if(cache.available_capacity != 30):
    return False
  return True


# test that remove prevents get from returning a value
def test_remove_correct():
  cache = markov_cache(32,2)
  cache.set("a","123")
  cache.remove("a")
  get_ok = cache.get("a")
  if get_ok:
    return False
  return True

# test that remove correctly updates the space avaialble in the cache
def test_remove_space():
  cache = markov_cache(32,2)
  cache.set("a","123")
  cache.remove("a")
  if(cache.available_capacity != 32):
    return False
  return True

# test that cache evicts the correct value on several small examples
def check_correct_evict():
  cache = markov_cache(4,2)
  cache.set("a","1")
  cache.set("a","0")
  cache.set("b","1")
  cache.set("a","1")
  # should evict b
  cache.set("c","3")
  get_b = cache.get("b")
  if(get_b == True):
    return False
  cache = markov_cache(4,2)
  cache.set("a","1")
  cache.set("a","0")
  cache.set("b","1")
  cache.set("b","1")
  cache.set("b","1")
  cache.set("b","1")
  cache.set("b","1")
  cache.set("b","1")
  cache.set("a","1")
  # should evict a
  cache.set("c","3")
  get_a = cache.get("a")
  if(get_a == True):
    return False
  return True

def run_all_tests():
  single_key_ok = test_single_key()
  if single_key_ok:
    print("Test various correctness operations for one key PASSED")
  else:
    print("Test various correctness operations for one key FAILED")

  empty_string_ok = test_empty_string_key()
  if empty_string_ok:
    print("test that cache allows empty string as a key PASSED")
  else:
    print("test that cache allows empty string as a key FAILED")

  empty_value_ok = test_empty_value()
  if empty_value_ok:
    print("test that cache allows empty value PASSED")
  else:
    print("test that cache allows empty value FAILED")
  
  evict_before_capacity_ok = test_evict_before_capacity()
  if evict_before_capacity_ok:
    print("Test that the cache does not evict any elements if it hasn't reached capacity PASSED")
  else:
    print("Test that the cache does not evict any elements if it hasn't reached capacity FAILED")
  
  above_capacity_ok = test_going_above_capacity()
  if above_capacity_ok:
    print("Test that the cache never allows more than its capacity PASSED")
  else:
    print("Test that the cache never allows more than its capacity FAILED")
  
  overwrite_space_ok = test_set_overwrite_space()
  if overwrite_space_ok:
    print("test that overwriting key with set consumes the correct amount of space PASSED")
  else:
    print("test that overwriting key with set consumes the correct amount of space FAILED")

  remove_correct_ok = test_remove_correct()
  if remove_correct_ok:
    print("test that remove prevents get from returning a value PASSED")
  else:
    print("test that remove prevents get from returning a value FAILED")
  
  remove_space_ok = test_remove_space()
  if remove_space_ok:
    print("test that remove correctly updates the space avaialble in the cache PASSED")
  else:
    print("test that remove correctly updates the space avaialble in the cache FAILED")
  
  correct_evict_ok = check_correct_evict()
  if correct_evict_ok:
    print("test that cache evicts the correct value on several small examples PASSED")
  else:
    print("test that cache evicts the correct value on several small examples FAILED")
run_all_tests()
  
  






