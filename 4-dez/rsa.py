def mod_exp(base, expoente, modulo):
    resultado = 1
    base = base % modulo
    while expoente > 0:
        if expoente % 2 == 1:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        expoente //= 2
    return resultado


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError("Inversa não existe")
    return x % m


def text_to_number(text):
    byte_data = text.encode("utf-8")
    num = 0
    for b in byte_data:
        num = num * 256 + b
    return num


def number_to_text(num):
    if num < 0:
        raise ValueError("Número negativo não pode ser convertido")
    if num == 0:
        return ""
    tamanho = (num.bit_length() + 7) // 8
    byte_data = num.to_bytes(tamanho, "big")
    return byte_data.decode("utf-8")


def gerar_chaves_rsa(p, q, e=None):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    if e is None:
        if 65537 < phi_n and egcd(65537, phi_n)[0] == 1:
            e = 65537
        else:
            e = None
            for i in range(3, phi_n, 2):
                if egcd(i, phi_n)[0] == 1:
                    e = i
                    break
            if e is None:
                raise ValueError("Não foi possível encontrar e válido")
    
    if e >= phi_n or egcd(e, phi_n)[0] != 1:
        raise ValueError("e inválido")
    
    d = mod_inverse(e, phi_n)
    return n, e, d


def criptografar_rsa(mensagem, n, e):
    m = text_to_number(mensagem)
    
    if m >= n:
        raise ValueError(f"Mensagem muito grande: m={m}, n={n}")
    
    c = mod_exp(m, e, n)
    return c


def descriptografar_rsa(c, n, d):
    m = mod_exp(c, d, n)
    mensagem = number_to_text(m)
    return mensagem


if __name__ == "__main__":
    print("="*70)
    print("RSA - CRIPTOGRAFIA ASSIMÉTRICA")
    print("="*70)
    
    p = 999999937
    q = 1000000007
    
    print(f"\n1. Primos escolhidos:")
    print(f"   p = {p}")
    print(f"   q = {q}")
    
    n, e, d = gerar_chaves_rsa(p, q)
    phi_n = (p - 1) * (q - 1)
    
    print(f"\n2. Chaves geradas:")
    print(f"   n = {n}")
    print(f"   φ(n) = {phi_n}")
    print(f"   e = {e}")
    print(f"   d = {d}")
    
    print(f"\n3. Verificação: e·d mod φ(n) = {(e * d) % phi_n}")
    
    print("\n" + "="*70)
    print("TESTE 1: Mensagem curta")
    print("="*70)
    
    msg = "olá"
    print(f"\nMensagem original: '{msg}'")
    
    m_num = text_to_number(msg)
    print(f"Mensagem como número: {m_num}")
    
    c = criptografar_rsa(msg, n, e)
    print(f"\nCriptografada: {c}")
    
    msg_descriptografada = descriptografar_rsa(c, n, d)
    print(f"Descriptografada: '{msg_descriptografada}'")
    
    if msg == msg_descriptografada:
        print("\n✓ SUCESSO!")
    else:
        print("\n✗ ERRO!")
    
    print("\n" + "="*70)
    print("TESTE 2: Mensagem maior")
    print("="*70)
    
    msg2 = "RSA OK!"
    print(f"\nMensagem original: '{msg2}'")
    print(f"Mensagem como número: {text_to_number(msg2)}")
    
    c2 = criptografar_rsa(msg2, n, e)
    print(f"Criptografada: {c2}")
    
    msg2_desc = descriptografar_rsa(c2, n, d)
    print(f"Descriptografada: '{msg2_desc}'")
    print(f"✓ Sucesso: {msg2 == msg2_desc}")
    
    print("\n" + "="*70)
    print("TESTE 3: Múltiplas mensagens")
    print("="*70)
    
    mensagens_teste = ["A", "Hello!", "123", "OK"]
    
    for msg_teste in mensagens_teste:
        try:
            c_teste = criptografar_rsa(msg_teste, n, e)
            m_teste = descriptografar_rsa(c_teste, n, d)
            status = "✓" if msg_teste == m_teste else "✗"
            print(f"{status} '{msg_teste}' → {c_teste} → '{m_teste}'")
        except Exception as ex:
            print(f"✗ '{msg_teste}' → ERRO: {ex}")
    
    print("\n" + "="*70)
    