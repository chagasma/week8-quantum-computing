import math
import time
from sympy import prime

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

    # gerar primos com sympy.prime
    i = 1
    pri = prime(i)

    while pri <= B:
        # maior expoente e com pri**e <= B
        e = math.floor(math.log(B, pri))  # equivalente a log(B)/log(pri)
        a = pow(a, pri**e, N)

        # log "de vez em quando"
        if verbose and i % 50 == 0:
            print(f"[pollard] B={B} | prime index={i}, pri={pri}, e={e}, a={a}")

        i += 1
        pri = prime(i)

    g = math.gcd(a - 1, N)
    if 1 < g < N:
        return g
    return None


if __name__ == "__main__":
    # Escolhendo dois primos
    # p = 983
    # q = 997
    p = 97
    q = 101

    N = p * q
    print(f"N = {N} (p * q = {p} * {q})")

    result = polland_loop(N, verbose=True)

    if result is not None and 1 < result < N:
        print(f"\nFound factor: {result}")
        print(f"Other factor: {N // result}")
    else:
        print("\nNo factor found 😢")