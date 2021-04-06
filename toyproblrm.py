
from collections import OrderedDict
 
class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
 

    def get(self, key: int) -> int:
        if key not in self.cache:
            print ("-1")
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]
 
 
    def put(self, key: int, value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)
 
cache = LRUCache(3) 

cache.put(1, 1)
print(cache.cache)
cache.put(2, 2)
print(cache.cache)
# cache.get(3)
# print(cache.cache)
cache.put(3, 3)
print(cache.cache)
cache.get(2)
print(cache.cache)
# cache.put(4, 4)
# print(cache.cache)
cache.get(1)
print(cache.cache)
cache.get(3)
print(cache.cache)
cache.get(4)
print(cache.cache)
# cache.put(2,2)
# print(cache.cache)
cache.put(5,5)
print(cache.cache)
cache.put(6,6)
print(cache.cache)
cache.get(5)
print(cache.cache)
cache.get(7)
print(cache.cache)
