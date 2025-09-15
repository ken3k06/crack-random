from rng_cooked import rng_cooked
# const: 
rngLen = 607
rngTap = 273
rngMax = 1 << 63
rngMask = rngMax - 1
int32max = (1 << 31) - 1

def seedrand(x):
    A = 48271
    Q = 44488
    R = 3399
    hi = x  // Q
    lo = x % Q
    x = A*lo - R*hi
    if x < 0:
        x += int32max
    return x
class RNGSource:
    def __init__(self, v):
        self.tap = 0 
        self.feed = rngLen - rngTap
        if v is None:
            self.vec = [0] * rngLen
        else:
            self.vec = v 
    def seed(self,seed):
        self.tap = 0 
        self.feed = rngLen - rngTap
        
        seed = seed % int32max
        if seed < 0:
            seed += int32max
        if seed == 0:
            seed = 89482311
        x = int(seed)
        for i in range(-20,rngLen):
            x = seedrand(x)
            if i >=0 :
                u = (int(x) << 40) & 0xFFFFFFFFFFFFFFFF
                x = seedrand(x)
                u ^= (int(x) << 20) & 0xFFFFFFFFFFFFFFFF
                x = seedrand(x)
                u ^= (int(x) & 0xFFFFFFFFFFFFFFFF)
                u ^= rng_cooked[i]
                self.vec[i] = u
    def int63(self):
        return self.uint64() & rngMask
    def uint64(self):
        self.tap -= 1
        if self.tap < 0:
            self.tap += rngLen
        self.feed -= 1
        if self.feed < 0:
            self.feed += rngLen
        x = self.vec[self.feed] + self.vec[self.tap]
        self.vec[self.feed] = x
        return int(x) & 0xFFFFFFFFFFFFFFFF
