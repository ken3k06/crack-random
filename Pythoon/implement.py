from random import Random

class MT19937:
    def __init__(self, seed):
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908B0DF
        self.u, self.d = 11, 0xFFFFFFFF
        self.s, self.b = 7, 0x9D2C5680
        self.t, self.c = 15, 0xEFC60000
        self.l = 18
        self.f = 1812433253
        self.lower_mask = (1 << self.r) - 1  
        self.upper_mask = (~self.lower_mask) & 0xFFFFFFFF  
        self.mt = [0] * self.n 
        self.index = self.n 
        self.seed_mt(seed)

    def seed_mt(self, seed):
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, self.n):
            self.mt[i] = (self.f * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.w - 2))) + i) & 0xFFFFFFFF

    def extract(self):
        if self.index >= self.n:
            self.twist()
        y = self.mt[self.index]
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b 
        y ^= (y << self.t) & self.c 
        y ^= (y >> self.l)
        self.index += 1
        return y & 0xFFFFFFFF

    def twist(self):
        for i in range(self.n):
            x = (self.mt[i] & self.upper_mask) + (self.mt[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0: 
                xA ^= self.a
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA
        self.index = 0
class PythonMT19937(MT19937):
    def __init__(self, seed):
        MT19937.__init__(self, seed)
        if seed is not None:
            self.seed(seed)

    def seed(self, n):
        lower = 0xffffffff
        keys = []

        while n:
            keys.append(n & lower)
            n >>= 32

        if len(keys) == 0:
            keys.append(0)

        self.init_by_array(keys)

    def init_by_array(self, keys):
        MT19937.seed_mt(self, 0x12bd6aa)
        i, j = 1, 0
        for _ in range(max(624, len(keys))):
            self.mt[i] = ((self.mt[i] ^ ((self.mt[i-1] ^
                            (self.mt[i-1] >> 30)) * 0x19660d)) + keys[j] + j) & 0xffffffff
            i += 1
            j += 1
            if i >= 624:
                self.mt[0] = self.mt[623]
                i = 1
            j %= len(keys)

        for _ in range(623):
            self.mt[i] = ((self.mt[i] ^ ((self.mt[i-1] ^
                            (self.mt[i-1] >> 30)) * 0x5d588b65)) - i) & 0xffffffff
            i += 1
            if i >= 624:
                self.mt[0] = self.mt[623]
                i = 1

        self.mt[0] = 0x80000000

import random
seed = 2**32-33
print(seed.bit_length())
rng1 = random.Random(seed)
rng2 = PythonMT19937(seed)
rng3 = MT19937(seed)
r1 = rng1.getrandbits(32)
r2 = rng2.extract()
assert r1 == r2
