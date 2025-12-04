# Inversa Multiplicativa

## Definição

A **inversa multiplicativa** de um número $a$ é um número $b$ tal que:

$$a \times b = 1$$

Esse número $b$ é chamado de **inverso multiplicativo** de $a$, e é denotado por $a^{-1}$ ou $\frac{1}{a}$.

## Exemplo Simples

Para $a = 5$:

$$5 \times \frac{1}{5} = 1$$

Logo, $\frac{1}{5}$ é a inversa multiplicativa de $5$.

## Inversa Multiplicativa Modular

Em aritmética modular, a inversa multiplicativa de $a$ módulo $n$ é um número $x$ tal que:

$$a \times x \equiv 1 \pmod{n}$$

**Importante:** A inversa só existe se $a$ e $n$ são **coprimos** (ou seja, $\gcd(a, n) = 1$).

### Exemplo Modular

Encontrar a inversa de $3$ módulo $7$:

$$3 \times x \equiv 1 \pmod{7}$$

Testando valores:

- $3 \times 1 = 3 \equiv 3 \pmod{7}$
- $3 \times 2 = 6 \equiv 6 \pmod{7}$
- $3 \times 3 = 9 \equiv 2 \pmod{7}$
- $3 \times 4 = 12 \equiv 5 \pmod{7}$
- $3 \times 5 = 15 \equiv 1 \pmod{7}$

Logo, $3^{-1} \equiv 5 \pmod{7}$.

## Aplicação em Criptografia

A inversa multiplicativa modular é fundamental em algoritmos como **RSA**, onde é usada para calcular a chave privada $d$ a partir da chave pública $e$:

$$e \times d \equiv 1 \pmod{\phi(n)}$$

Onde $\phi(n)$ é a função totiente de Euler.
