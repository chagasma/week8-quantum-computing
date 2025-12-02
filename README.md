# HTTP Insecure Demo

Demonstração de interceptação de credenciais em HTTP sem SSL.

## Execução

### Terminal 1: Iniciar o servidor

```bash
python3 server.py
```

### Terminal 2: Iniciar o sniffer (requer root)

```bash
sudo python3 sniffer.py
```

### Terminal 3: Abrir o navegador

```bash
xdg-open http://localhost:8080
```

Ou acesse manualmente: `http://localhost:8080`

## Teste

1. Preencha username e password no formulário
2. Clique em "Login"
3. Observe:
   - **Terminal 1**: servidor recebe e loga as credenciais
   - **Terminal 2**: sniffer intercepta e exibe em texto plano

## O que isso demonstra

HTTP transmite dados em texto plano. Qualquer pessoa na mesma rede pode interceptar:

- Credenciais
- Tokens de sessão
- Dados pessoais
- Informações sensíveis

**Solução**: Use HTTPS (HTTP + TLS/SSL) para criptografar a comunicação.

## Requisitos

- Python 3.x (biblioteca padrão)
- Permissões de root para o sniffer
- Navegador web
