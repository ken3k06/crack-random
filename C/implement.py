M31 = 2147483647  
M32 = 2**32     
def to_int32_signed(x: int) -> int:
    x &= 0xFFFFFFFF
    if x & 0x80000000:
        return x - 0x100000000
    return x

class GlibcRandom:
    def __init__(self, seed: int):

        r = [0] * 344
        r[0] = seed & 0xFFFFFFFF
        for i in range(1, 31):
            prev_signed = to_int32_signed(r[i-1])
            r[i] = (16807 * prev_signed) % M31
            if r[i] < 0:
                r[i] += M31 
        for i in range(31, 34):
            r[i] = r[i-31]
        for i in range(34, 344):
            r[i] = (r[i-31] + r[i-3]) & 0xFFFFFFFF

        self.r = r  
    
    def random(self) -> int:
        val = (self.r[-31] + self.r[-3]) & 0xFFFFFFFF
        self.r.append(val)
        return (val >> 1) & 0x7FFFFFFF  
    def next_many(self, n: int):
        return [self.random() for _ in range(n)]


check = [
    1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335,
    719885386, 1649760492, 596516649, 1189641421, 1025202362, 1350490027,
    783368690, 1102520059, 2044897763, 1967513926, 1365180540, 1540383426,
    304089172, 1303455736, 35005211, 521595368, 294702567, 1726956429,
    336465782, 861021530, 278722862, 233665123, 2145174067, 468703135,
    1101513929, 1801979802, 1315634022, 635723058, 1369133069, 1125898167,
    1059961393, 2089018456, 628175011, 1656478042, 1131176229, 1653377373,
    859484421, 1914544919, 608413784, 756898537, 1734575198, 1973594324,
    149798315, 2038664370, 1129566413, 184803526, 412776091, 1424268980,
    1911759956, 749241873, 137806862, 42999170, 982906996, 135497281
]
rng = GlibcRandom(seed=1)
generated = rng.next_many(60)
test = (generated == check)
print(test)
