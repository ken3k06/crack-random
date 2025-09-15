from implement import *
import random
def unshiftRight(x, shift):
    res = x
    for i in range(32):
        res = x ^ res >> shift
    return res

def unshiftLeft(x, shift, mask):
    res = x
    for i in range(32):
        res = x ^ (res << shift & mask)
    return res

def untemper(v):
    v = unshiftRight(v, 18)
    v = unshiftLeft(v, 15, 0xefc60000)
    v = unshiftLeft(v, 7, 0x9d2c5680)
    v = unshiftRight(v, 11)
    return v
rng = PythonMT19937(1234)
# You don't see some of the outputs
for _ in range(1234):
    rng.extract()

# you capture 624 consecutive outputs
state = [untemper(rng.extract()) for _ in range(624)]

print("Normal run :")

print(rng.extract())

print("\nPredicted run :")

# set RNG state from observed ouputs
random.setstate((3, tuple(state + [624]), None))

print(random.getrandbits(32))
