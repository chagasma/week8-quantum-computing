<div align='justify'>

# Relatório de Demonstração: Vulnerabilidades HTTP

## Introdução

Este relatório documenta demonstrações práticas de vulnerabilidades de segurança em comunicações HTTP não criptografadas e ataques Man-in-the-Middle (MITM). O objetivo é evidenciar os riscos de segurança quando dados sensíveis são transmitidos sem proteção adequada.

---

## Ataque 1: Interceptação de Credenciais via HTTP

### Objetivo

Demonstrar como credenciais podem ser interceptadas quando transmitidas via HTTP (sem criptografia).

### Configuração do Ambiente

#### Passo 1: Iniciar o Servidor HTTP

O servidor HTTP foi iniciado na porta 8080 para simular um site inseguro:

![Servidor HTTP em execução](img/server.jpg)

O servidor está pronto para receber requisições HTTP sem qualquer tipo de criptografia.

#### Passo 2: Iniciar o Sniffer de Pacotes

Um sniffer de pacotes foi configurado para capturar todo o tráfego de rede na porta 8080:

![Sniffer capturando tráfego](img/server-02.jpg)

O sniffer monitora passivamente todas as comunicações, aguardando dados sensíveis.

### Execução do Ataque

#### Passo 3: Acesso à Página de Login e Submissão de Credenciais

O usuário acessa a página de login através do navegador e preenche suas credenciais:

![Página de login com credenciais](img/colecria-login.jpg)

A interface parece normal, mas toda comunicação está sendo transmitida em texto plano. As informações são enviadas via HTTP sem qualquer proteção.

### Resultado: Credenciais Interceptadas

O sniffer captura todo o tráfego HTTP, incluindo as credenciais em texto plano que foram enviadas pelo formulário:

![Credenciais interceptadas pelo sniffer](img/intercepted.jpg)

**Análise do Ataque:**

- **Credenciais expostas**: Username e password são claramente visíveis no tráfego capturado
- **Sem criptografia**: Todo o conteúdo é transmitido em texto legível
- **Fácil interceptação**: Qualquer pessoa na mesma rede pode capturar essas informações

### Impacto de Segurança

**Riscos Identificados:**

1. **Interceptação Passiva**: Atacantes podem capturar credenciais sem ser detectados
2. **Acesso Não Autorizado**: Com as credenciais, um atacante pode se passar pelo usuário
3. **Violação de Privacidade**: Dados pessoais e sensíveis ficam expostos

**Fator Crítico**: HTTP não oferece nenhuma proteção contra interceptação de dados.

---

## Ataque 2: Man-in-the-Middle (MITM) com Certificado Falsificado

### Objetivo

Demonstrar como um atacante pode interceptar comunicações HTTPS usando um certificado SSL/TLS falsificado.

### Configuração do Ambiente

#### Passo 1: Geração de Certificados

Foram gerados dois conjuntos de certificados:

- **Certificado Legítimo**: Para o servidor seguro
- **Certificado Falsificado**: Para o proxy MITM

```bash
./scripts/generate_certs.sh
```

#### Passo 2: Servidor HTTPS Legítimo

Um servidor HTTPS legítimo foi configurado na porta 9443:

```bash
python3 src/legitimate_server.py
```

Este servidor representa um ambiente seguro e confiável.

#### Passo 3: Proxy MITM com Certificado Falsificado

Um proxy MITM foi configurado na porta 8443 usando um certificado falsificado:

```bash
python3 src/mitm_proxy.py
```

Este proxy intercepta e descriptografa o tráfego HTTPS usando um certificado não confiável.

### Execução do Ataque

#### Cenário A: Servidor Legítimo (Seguro)

Quando o usuário acessa o servidor legítimo, o navegador alerta sobre o certificado auto-assinado, mas após aceitar, a comunicação é segura.

#### Cenário B: Ataque MITM (Inseguro)

O usuário acessa o proxy MITM que se faz passar pelo servidor legítimo:

![Página de login no servidor MITM](img/login.jpg)

O navegador mostra um aviso de certificado, mas se o usuário aceitar (comportamento comum em ambientes de teste), o atacante consegue interceptar todas as comunicações.

#### Passo 4: Submissão de Credenciais no MITM

Quando o usuário preenche e envia suas credenciais através do proxy MITM:

![Login sendo realizado no MITM](img/login-real.jpg)

As informações são enviadas via HTTPS, mas o proxy MITM consegue descriptografar o tráfego.

### Resultado: Interceptação de Tráfego HTTPS

O proxy MITM captura todo o tráfego HTTPS, incluindo as credenciais descriptografadas. Mesmo usando HTTPS, o proxy MITM consegue descriptografar e visualizar as credenciais.

**Análise do Ataque:**

- **HTTPS comprometido**: A conexão mostra o cadeado, mas está sendo interceptada
- **Certificado falsificado**: O atacante usa um certificado que parece legítimo
- **Usuário enganado**: O usuário aceita o certificado sem validar sua autenticidade

### Impacto de Segurança

**Riscos Identificados:**

1. **Falsa Sensação de Segurança**: O usuário vê HTTPS mas está sendo atacado
2. **Interceptação Ativa**: O atacante pode modificar ou registrar todo o tráfego
3. **Engenharia Social**: Ataques que exploram a confiança do usuário em certificados

**Fator Crítico**: HTTPS só é seguro se o certificado for validado corretamente. Certificados falsificados podem comprometer toda a segurança.

---

## Conclusões e Recomendações

### Principais Vulnerabilidades Demonstradas

1. **HTTP é Inseguro por Padrão**
   - Dados transmitidos em texto plano
   - Fácil interceptação passiva
   - Sem autenticação ou integridade

2. **HTTPS Pode Ser Comprometido**
   - Certificados falsificados podem enganar usuários
   - Validação de certificados é essencial
   - Usuários precisam estar atentos a avisos de segurança

### Medidas de Proteção

**Para Desenvolvedores:**

- Sempre usar HTTPS em produção
- Implementar HSTS (HTTP Strict Transport Security)
- Validar certificados corretamente
- Usar Certificate Pinning quando apropriado

**Para Usuários:**

- Nunca aceitar certificados não confiáveis
- Verificar a autenticidade de sites
- Estar atento a avisos de segurança do navegador
- Usar redes confiáveis (evitar Wi-Fi público para transações sensíveis)

### Importância da Segurança

Estas demonstrações evidenciam que:

- **Segurança não é opcional**: Dados sensíveis sempre devem ser protegidos
- **Criptografia é essencial**: Mas precisa ser implementada corretamente
- **Educação é fundamental**: Usuários e desenvolvedores precisam entender os riscos

---

## Considerações Finais

Este relatório demonstrou de forma prática como vulnerabilidades em comunicações HTTP podem ser exploradas. Os ataques mostrados são reais e podem ocorrer em ambientes de produção se as devidas precauções não forem tomadas.

A segurança da informação é uma responsabilidade compartilhada entre desenvolvedores, administradores de sistema e usuários finais. Todos devem estar cientes dos riscos e tomar as medidas apropriadas para proteger dados sensíveis.

</div>
