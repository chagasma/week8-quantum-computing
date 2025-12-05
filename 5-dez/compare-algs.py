# compare_factor.py
import time
from sympy import factorint
from dixon import dixon_factorization
from fermat import fermat_factorization
from polland_p_1 import polland_loop  # importa do outro arquivo


def print_result(name, factors, elapsed):
    print(f"\n[{name}] Result:")
    if factors and len(factors) == 2:
        a, b = factors
        print(f"  Factors: {a} and {b}")
    else:
        print("  Failed to find a non-trivial factor")
    print(f"  Time: {elapsed:.6f} seconds")

def run_all(n):
    print(f"N = {n}")

    # 1) Seu algoritmo: Pollard p-1
    start = time.perf_counter()
    factor = polland_loop(n, verbose=False)
    t_pollard = time.perf_counter() - start
    pollard_factors = (factor, n // factor) if factor and 1 < factor < n else None
    print_result("Pollard p-1", pollard_factors, t_pollard)

    # 2) Fermat
    start = time.perf_counter()
    fermat_factors = fermat_factorization(n)
    t_fermat = time.perf_counter() - start
    print_result("Fermat", fermat_factors, t_fermat)

    # 3) Dixon
    start = time.perf_counter()
    dixon_factors = dixon_factorization(n, verbose=False)
    t_dixon = time.perf_counter() - start
    print_result("Dixon", dixon_factors, t_dixon)

    # 4) Biblioteca: sympy.factorint
    start = time.perf_counter()
    fact_dict = factorint(n)   # {prime: exponent}
    t_sympy = time.perf_counter() - start

    print("\n[SymPy factorint] Result:")
    print(f"  Factorization dict: {fact_dict}")
    print(f"  Time: {t_sympy:.6f} seconds")


def main():
    # p e q (fatores próximos para permitir comparação entre métodos)
    tests = [
        ("Fácil", 97, 101),
        ("Intermediário", 983, 997),
        ("Difícil", 10007, 10009),
        ("Muito difícil (espalhado)", 104729, 1299709),
    ]

    for label, p, q in tests:
        N = p * q
        print("\n" + "=" * 70)
        print(f"{label} | p * q = {p} * {q} = {N}")
        print("=" * 70)
        run_all(N)


if __name__ == "__main__":
    main()
