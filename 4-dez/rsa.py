# Funções auxiliares
def mod_exp(base, expoente, modulo):
    """Expoenciação modular rápida (square-and-multiply)."""
    resultado = 1
    base = base % modulo

    while expoente > 0:
        if expoente % 2 == 1:      # se o expoente é ímpar
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        expoente //= 2

    return resultado

def egcd(a, b):
    """Algoritmo de Euclides estendido: retorna (g, x, y) tal que ax + by = g = mdc(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

def mod_inverse(a, m):
    """Calcula a inversa modular de a (mod m)."""
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("Inversa não existe (a e m não são coprimos)")
    return x % m

def text_to_number(text):
    """Converte uma string para inteiro usando base 256 (big-endian)."""
    byte_data = text.encode("utf-8")
    num = 0

    for b in byte_data:
        num = num * 256 + b   # ← ESSA é a linha chave da conversão

    return num

def number_to_text(num):
    """Converte um inteiro de volta para texto UTF-8."""
    if num < 0:
        raise ValueError("Número negativo não pode ser convertido em texto")

    if num == 0:
        return ""

    tamanho = (num.bit_length() + 7) // 8  # arredonda para múltiplos de 8 bits
    byte_data = num.to_bytes(tamanho, "big")
    return byte_data.decode("utf-8")

msg = "olá"
n = text_to_number(msg)
print(number_to_text(n))
assert number_to_text(n) == msg