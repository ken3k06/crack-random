from implement import *
from z3 import *

s = Solver()
vec = [BitVec(f'v_{i}', 64) for i in range(rngLen)]
cur = vec[:]
test_case = 700

tap = 0
feed = rngLen - rngTap
rng_real = RNGSource(v=None)
rng_real.seed(1234)
known = [rng_real.uint64() for _ in range(test_case)]

for i in range(test_case):
    tap = tap - 1 if tap - 1 >=0 else tap - 1 + rngLen
    feed = feed - 1 if feed - 1 >=0 else feed - 1 + rngLen
    x = (cur[feed] + cur[tap]) & ((1<<64) - 1)
    s.add(x == known[i])
    new_cur = cur[:]
    new_cur[feed] = x
    cur = new_cur
    

if s.check() == sat:
    m = s.model()
    arr = [m.evaluate(vec[i]).as_long() for i in range(rngLen)]

    rng_test = RNGSource(v=arr)
    for _ in range(test_case):
        rng_test.uint64()
    print("Test")
    for _ in range(10):
        print(rng_real.uint64(), rng_test.uint64())
else:
    print("unsat")
