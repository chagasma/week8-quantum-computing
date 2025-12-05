import math
import time


def primes_up_to(limit: int):
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            step = p
            sieve[p * p : limit + 1 : step] = [False] * (((limit - p * p) // step) + 1)
    return [i for i, flag in enumerate(sieve) if flag]


def polland_loop(N, verbose=False):
    B = 10

    while B < N:
        if verbose:
            print(f"\n[loop] Trying B = {B}")
            start_B = time.time()

        g = polland_p_minus_1(N, B, verbose=verbose)

        if verbose:
            dt = time.time() - start_B
            print(f"[loop] Finished B = {B} in {dt:.4f}s, g = {g}")

        if g is not None and 1 < g < N:
            return g

        B = B * 2

    return None


def polland_p_minus_1(N, B, verbose=False):
    a = 2
    g = math.gcd(a, N)
    if 1 < g < N:
        return g

    primes = primes_up_to(B)

    for idx, pri in enumerate(primes, start=1):
        e = math.floor(math.log(B, pri))
        a = pow(a, pri**e, N)

        if verbose and idx % 50 == 0:
            print(f"[pollard] B={B} | prime index={idx}, pri={pri}, e={e}, a={a}")

    g = math.gcd(a - 1, N)
    if 1 < g < N:
        return g
    return None


if __name__ == "__main__":
    p = 97
    q = 101

    N = p * q
    print(f"N = {N} (p * q = {p} * {q})")

    result = polland_loop(N, verbose=True)

    if result is not None and 1 < result < N:
        print(f"\nFound factor: {result}")
        print(f"Other factor: {N // result}")
    else:
        print("\nNo factor found")
