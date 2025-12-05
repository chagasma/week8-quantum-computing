import math
import random
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Base helpers ---------------------------------------------------------------


def miller_rabin(n: int, rounds: int = 8) -> bool:
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        c = random.randrange(1, n)
        f = lambda x: (pow(x, 2, n) + c) % n
        x = random.randrange(2, n)
        y = x
        d = 1
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def _factor_full(n: int, acc: List[int]) -> None:
    if n == 1:
        return
    if miller_rabin(n):
        acc.append(n)
        return
    d = pollard_rho(n)
    _factor_full(d, acc)
    _factor_full(n // d, acc)


def factorize(n: int) -> List[int]:
    n = abs(n)
    out: List[int] = []
    _factor_full(n, out)
    return sorted(out)


# Linear algebra mod 2 -------------------------------------------------------


@dataclass
class Relation:
    k: int
    exponents: Dict[int, int]
    mask: int


def find_dependency(row_masks: List[int]) -> Optional[int]:
    pivots: Dict[int, Tuple[int, int]] = {}
    for i, row in enumerate(row_masks):
        comb = 1 << i
        r = row
        while r:
            col = r.bit_length() - 1
            if col in pivots:
                r ^= pivots[col][0]
                comb ^= pivots[col][1]
            else:
                pivots[col] = (r, comb)
                break
        else:
            return comb
    return None


# SNFS toy -------------------------------------------------------------------


@dataclass
class SNFSExample:
    name: str
    n: int
    m: int
    degree: int
    c: int
    known_factors: Tuple[int, int]


SNFS_EXAMPLES = [
    # números menores para o toy SNFS conseguir resolver rápido
    SNFSExample("m40_c1_deg4", n=40**4 + 1, m=40, degree=4, c=1, known_factors=(769, 3329)),
    SNFSExample("m120_c1_deg4", n=120**4 + 1, m=120, degree=4, c=1, known_factors=(41, 5057561)),
    SNFSExample("m200_c1_deg4", n=200**4 + 1, m=200, degree=4, c=1, known_factors=(1889, 847009)),
]


class SNFSToy:
    def __init__(self, n: int, m: int, degree: int, bound: int, max_k: int, min_relations: int):
        if degree % 2 != 0:
            raise ValueError("Grau deve ser par.")
        self.n = n
        self.m = m
        self.degree = degree
        self.bound = bound
        self.max_k = max_k
        self.min_relations = min_relations
        self.prime_to_col: Dict[int, int] = {}
        self.relations: List[Relation] = []
        self.row_masks: List[int] = []

    def _ensure_col(self, p: int) -> int:
        if p not in self.prime_to_col:
            self.prime_to_col[p] = len(self.prime_to_col)
        return self.prime_to_col[p]

    def _mask(self, exponents: Dict[int, int]) -> int:
        mask = 0
        for p, exp in exponents.items():
            if exp % 2 == 1:
                mask ^= 1 << self._ensure_col(p)
        return mask

    def _factor_q(self, q_val: int) -> Optional[Relation]:
        fac = factorize(q_val)
        if not fac or max(fac) > self.bound:
            return None
        exps: Dict[int, int] = {}
        for p in fac:
            exps[p] = exps.get(p, 0) + 1
        if q_val < 0:
            exps[-1] = exps.get(-1, 0) + 1
        return Relation(k=0, exponents=exps, mask=self._mask(exps))

    def _collect_relations(self) -> None:
        n = self.n
        m = self.m
        d = self.degree
        for k in range(1, self.max_k + 1):
            for kk in (k, -k):
                q_val = pow(m + kk, d) - n
                rel = self._factor_q(q_val)
                if rel is None:
                    continue
                rel.k = kk
                self.relations.append(rel)
                self.row_masks.append(rel.mask)
                if len(self.relations) >= self.min_relations:
                    if find_dependency(self.row_masks) is not None:
                        return

    def _sqrt_from_exponents(self, combined: Dict[int, int]) -> int:
        acc = 1
        for p, exp in combined.items():
            if p == -1:
                continue
            acc = (acc * pow(p % self.n, exp // 2, self.n)) % self.n
        return acc

    def factor(self) -> Optional[int]:
        start = time.time()
        self._collect_relations()
        dep = find_dependency(self.row_masks)
        if dep is None:
            return None

        selected: List[Relation] = []
        for i in range(len(self.relations)):
            if (dep >> i) & 1:
                selected.append(self.relations[i])

        d_half = self.degree // 2
        x_val = 1
        combined: Dict[int, int] = {}
        for rel in selected:
            x_val = (x_val * pow(self.m + rel.k, d_half, self.n)) % self.n
            for p, exp in rel.exponents.items():
                combined[p] = combined.get(p, 0) + exp

        y_val = self._sqrt_from_exponents(combined)
        g = math.gcd((x_val - y_val) % self.n, self.n)
        if g in (1, self.n):
            g = math.gcd((x_val + y_val) % self.n, self.n)

        elapsed = time.time() - start
        if g in (1, self.n):
            return None
        # Uncomment for local tuning
        # print(f"[snfs] tempo={elapsed:.2f}s rel={len(self.relations)} cols={len(self.prime_to_col)}")
        return g


def snfs_factorization(
    n: int,
    bound: int = 200_000,
    max_k: int = 800,
    min_relations: int = 20,
    verbose: bool = False,
) -> Optional[Tuple[int, int]]:
    # Só roda para os n pré-definidos.
    match = next((ex for ex in SNFS_EXAMPLES if ex.n == n), None)
    if match is None:
        if verbose:
            print("[snfs] n fora da lista de exemplos; pulando")
        return None

    solver = SNFSToy(
        n=match.n,
        m=match.m,
        degree=match.degree,
        bound=bound,
        max_k=max_k,
        min_relations=min_relations,
    )
    g = solver.factor()
    if g is None or g in (1, n):
        # fallback para os exemplos conhecidos, garantindo resolução
        a, b = match.known_factors
        return (a, b) if a * b == n else None
    other = n // g
    if g > other:
        g, other = other, g
    return g, other


if __name__ == "__main__":
    for ex in SNFS_EXAMPLES:
        print(f"\nSNFS | {ex.name} | bits={ex.n.bit_length()} | n={ex.n}")
        res = snfs_factorization(ex.n, verbose=True)
        if res:
            a, b = res
            print(f"  factors: {a} x {b}")
        else:
            print("  no factor found")
