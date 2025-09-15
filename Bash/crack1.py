M = 0x7fffffff
A = 16807
MASK15 = 0x7fff

def _map(x):
    return (((x >> 16) ^ (x & 0xffff)) & MASK15)

def recover_bash_seed(outputs):
    if not outputs:
        return []
    v0 = outputs[0] & MASK15
    cand = []
    for y in (v0, v0 | 0x8000):
        for high in range(1 << 15):
            low = high ^ y
            x = (high << 16) | low
            cand.append(x)
    invA = pow(A, -1, M)
    good = []
    for x0 in cand:
        x = x0
        ok = True
        for v in outputs:
            if _map(x) != (v & MASK15):
                ok = False
                break
            x = (A * x) % M
        if ok:
            seed = (invA * x0) % M
            good.append(seed)
    return sorted(set(good))

if __name__ == "__main__":
    outs = [5154, 3081, 27973]
    seeds = recover_bash_seed(outs)
    print(seeds)
