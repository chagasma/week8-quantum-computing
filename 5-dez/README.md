# Algoritmos de Fatoracao

Este diretorio contem implementacoes de tres algoritmos classicos de fatoracao de inteiros, cada um com caracteristicas de complexidade distintas.

## Algoritmos Implementados

### Fermat

**Complexidade:** O(sqrt(n))

O metodo de Fermat busca representar um numero n como diferenca de dois quadrados perfeitos. Sua eficiencia depende fortemente da diferenca entre os fatores:

- Funciona melhor quando os fatores estao proximos a raiz quadrada de n
- Quando os fatores tem diferenca grande (delta), o tempo de execucao aumenta rapidamente
- Caso ideal: fatores proximos → rapido
- Caso pior: fatores distantes → lento

**Quando usar:** Numeros semi-primos com fatores proximos.

### Pollard p-1

**Complexidade:** O(B log B), onde B e o limite de suavidade

Este algoritmo detecta fatores primos p onde p-1 e um numero suave (composto apenas por primos pequenos).

- Complexidade exponencial em log B
- Probabilidade de sucesso depende da suavidade de p-1
- Com B = 2^32, encontra aproximadamente 25% dos fatores de 64 bits
- Se p-1 tem apenas fatores primos grandes, o algoritmo falha

**Quando usar:** Numeros cujos fatores primos p tem p-1 suave (composto por primos pequenos).

### Dixon

**Complexidade:** exp(sqrt(2 log n log log n)) - subexponencial

Metodo de base de fatores que busca relacoes lineares entre quadrados.

- Primeira complexidade subexponencial rigorosamente provada
- Mais rapido que trial division e Fermat para numeros grandes
- Precursor do Quadratic Sieve e Number Field Sieve
- Requer encontrar numeros suaves e resolver sistema linear mod 2

**Quando usar:** Fatoracao de numeros grandes onde Fermat e Pollard p-1 falham.

## Comparacao de Performance

```
Trial Division:     O(sqrt(n))              - exponencial
Fermat:             O(sqrt(n))              - exponencial, rapido se fatores proximos
Pollard p-1:        O(B log B)              - depende de p-1 suave
Dixon:              exp(sqrt(2 ln n ln ln n)) - subexponencial
Quadratic Sieve:    exp(sqrt(ln n ln ln n)) - subexponencial (mais rapido)
```

Para numeros grandes (>100 digitos), metodos modernos como Quadratic Sieve e General Number Field Sieve sao significativamente mais rapidos que os tres algoritmos implementados aqui.

## Arquivos

- `fermat.py` - Implementacao do metodo de Fermat
- `polland_p_1.py` - Implementacao do algoritmo de Pollard p-1
- `dixon.py` - Implementacao do metodo de Dixon
- `compare-algs.py` - Script para comparar performance dos algoritmos
