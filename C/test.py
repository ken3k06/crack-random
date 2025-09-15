from implement import *
from crack import *
RNG = GlibcRandom(seed = 1234)
outputs = RNG.next_many(128)
print(outputs)
seed = recover_seed(outputs)
print(f"{seed = }")
