# compare_factor.py
import time

try:
    from sympy import factorint
    HAS_SYMPY = True
except ImportError:
    factorint = None
    HAS_SYMPY = False
from dixon import dixon_factorization
from fermat import fermat_factorization
from polland_p_1 import polland_loop  # importa do outro arquivo
from snfs import snfs_factorization, SNFS_EXAMPLES


def print_result(name, factors, elapsed):
    print(f"\n[{name}] Result:")
    if factors and len(factors) == 2:
        a, b = factors
        print(f"  Factors: {a} and {b}")
    else:
        print("  Failed to find a non-trivial factor")
    print(f"  Time: {elapsed:.6f} seconds")

def run_all(n, run_snfs=False):
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

    # 4) SNFS (toy; opcional, didático, pode falhar rápido)
    if run_snfs:
        start = time.perf_counter()
        snfs_factors = snfs_factorization(n, bound=200_000, max_k=800, min_relations=20)
        t_snfs = time.perf_counter() - start
        print_result("SNFS (toy)", snfs_factors, t_snfs)

    # 5) Biblioteca: sympy.factorint
    print("\n[SymPy factorint] Result:")
    if HAS_SYMPY:
        start = time.perf_counter()
        fact_dict = factorint(n)   # {prime: exponent}
        t_sympy = time.perf_counter() - start
        print(f"  Factorization dict: {fact_dict}")
        print(f"  Time: {t_sympy:.6f} seconds")
    else:
        print("  sympy não instalado")


def main():
    # p e q (fatores próximos para permitir comparação entre métodos)
    snfs_ex = SNFS_EXAMPLES[0]
    tests = [
        ("Fácil", 97, 101),
        ("Intermediário", 983, 997),
        ("Difícil", 10007, 10009),
        ("Muito difícil (espalhado)", 104729, 1299709),
        ("SNFS exemplo", snfs_ex.known_factors[0], snfs_ex.known_factors[1]),
    ]

    run_snfs = True  # SNFS toy ativado (usa n pequenos da lista)

    for label, p, q in tests:
        N = p * q
        print("\n" + "=" * 70)
        print(f"{label} | p * q = {p} * {q} = {N}")
        print("=" * 70)
        run_all(N, run_snfs=run_snfs)


if __name__ == "__main__":
    main()
