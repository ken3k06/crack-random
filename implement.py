import subprocess

BASH_RAND_MAX = 0x7fff 

class BashRandom:
    def __init__(self, seed: int, shell_compatibility_level: int = 51):
        self.rseed = seed & 0xffffffff
        self.shell_compat = int(shell_compatibility_level)
    @staticmethod
    def _intrand32(last: int) -> int:
        if last == 0:
            last = 123459876
        q = 127773
        r = 2836
        a = 16807
        m = 0x7fffffff  

        h = last // q
        l = last - (q * h)
        t = a * l - r * h
        ret = t + m if t < 0 else t
        return ret

    def _brand_(self) -> int:
        self.rseed = self._intrand32(self.rseed)

        if self.shell_compat > 50:
            v = ((self.rseed >> 16) ^ (self.rseed & 0xffff))
        else:
            v = self.rseed

        return v & BASH_RAND_MAX
    def next(self) -> int:
        return self._brand_()
    def next_n(self, n: int) -> list:
        return [self._brand_() for _ in range(n)]
# GNU bash, version 5.1.16
def bash_random(seed):
    if seed is None:
        cmd = ["bash", "-c", "echo $RANDOM"]
    else:
        cmd = ["bash", "-c", f"RANDOM={int(seed)}; echo $RANDOM"]
    proc = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, check=True)
    return int(proc.stdout.strip())
def bash_random_n(seed, count):
    if count < 1:
        return []
    if seed is None:
        cmd = f"for i in $(seq {count}); doecho $RANDOM; done"
    else:
        cmd = f"RANDOM={int(seed)}; for i in $(seq {count}); do echo $RANDOM; done"
    proc = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, check=True)
    lines = [ln for ln in proc.stdout.splitlines() if ln.strip() != ""]
    return [int(x) for x in lines]
print(bash_random_n(seed = 1337, count = 10))
rng = BashRandom(seed= 1337, shell_compatibility_level=51)
print(rng.next_n(10))
'''
[24697, 15233, 8710, 4659, 20253, 16480, 30033, 24872, 17510, 11420]
[24697, 15233, 8710, 4659, 20253, 16480, 30033, 24872, 17510, 11420]
'''
