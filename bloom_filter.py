import math 
import mmh3 
from bitarray import bitarray 


# m = bit array size
# n = number of expected keys to be stored
# p = Probability of desired false positive rate
class BloomFilter():
    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.m = self.get_size(n, p)
        self.hash_count = self.get_hash_count(self.m, n) 
        self.bit_array = bitarray(self.m) 
        self.bit_array.setall(0) 


    def get_size(self, n, p):
        m = -(n * math.log(p))/(math.log(2)**2) 
        return int(m) 

    
    def get_hash_count(self, m, n):
        k = (m/n) * math.log(2) 
        return int(k) 

    # add an item in bloom filter
    def add(self, item): 
        digests = [] 
        for i in range(self.hash_count): 
            digest = mmh3.hash(item, i) % self.m 
            digests.append(digest) 
  
            self.bit_array[digest] = True

    
    # Check for existence of an item in filter 
    def is_member(self, item): 
        for i in range(self.hash_count): 
            digest = mmh3.hash(item, i) % self.m 
            if self.bit_array[digest] == False: 
                return False

        return True

