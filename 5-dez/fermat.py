import math
from typing import Optional, Tuple


def fermat_factorization(n: int, max_iterations: int = 10_000) -> Optional[Tuple[int, int]]:
    """
    Factorize an odd integer using Fermat's method.

    Returns (p, q) or None if no factors are found within max_iterations.
    """
    if n <= 0:
        return None

    # Handle even numbers quickly
    if n % 2 == 0:
        return 2, n // 2

    a = math.isqrt(n)
    if a * a < n:
        a += 1  # ceil(sqrt(n))

    b2 = a * a - n

    for _ in range(max_iterations):
        b = math.isqrt(b2)
        if b * b == b2:
            f1 = a - b
            f2 = a + b

            if 1 < f1 < n:
                return f1, f2
            return None

        a += 1
        b2 = a * a - n

    return None


if __name__ == "__main__":
    n = int(input("Número a fatorar (Fermat): "))
    result = fermat_factorization(n)
    if result:
        p, q = result
        print(p, q)
    else:
        print("Fatores não encontrados dentro do limite de iterações.")
