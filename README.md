# cmpe273-assignment3
Q: What are the best k hashes and m bits values to store one million n keys (E.g. e52f43cd2c23bb2e6296153748382764) suppose we use the same MD5 hash key from pickle_hash.py and explain why?


Assuming there are one million keys and probability of desired false positive rate is 0.05<br/>
The best m bit values is -(n * math.log(p))/(math.log(2)**2) = 6235224<br/>
The best k hashes values is (m/n) * math.log(2) = 4
