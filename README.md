# Security Attack Demonstrations

Educational demos of network security attacks.

## Demo 1: HTTP Sniffing Attack

Demonstrates credential interception over plain HTTP.

### Setup

Terminal 1 - Start HTTP server:

```bash
python3 src/server.py
```

Terminal 2 - Start sniffer (requires root):

```bash
sudo python3 src/sniffer.py
```

Terminal 3 - Open browser:

```bash
xdg-open http://localhost:8080
```

### Test

1. Enter username and password
2. Click "Login"
3. Observe credentials in both terminals

## Demo 1B: HTTPS Sniffing (Encrypted Traffic)

Shows that you can still capture packets over HTTPS, but the payload is unreadable without the TLS keys.

### Setup

Generate certificates once (if not already created):

```bash
./scripts/generate_certs.sh
```

Terminal 1 - Start legitimate HTTPS server:

```bash
python3 src/legitimate_server.py
```

Terminal 2 - Start TLS sniffer (requires root):

```bash
sudo python3 src/sniffer_https.py
```

Terminal 3 - Open browser (accept the self-signed warning):

```bash
firefox --new-instance https://localhost:9443
```

### Test

1. Submit login form
2. TLS sniffer shows captured packets with hex bytes
3. Note that usernames/passwords are **not** visible because the traffic is encrypted

## Demo 2: CA Certificate Forgery Attack (MITM)

Demonstrates Man-in-the-Middle attack with fake certificate.

### Setup

Step 1 - Generate certificates:

```bash
./scripts/generate_certs.sh
```

Step 2 - Terminal 1 - Start legitimate HTTPS server:

```bash
python3 src/legitimate_server.py
```

Step 3 - Terminal 2 - Start MITM proxy with fake certificate:

```bash
python3 src/mitm_proxy.py
```

### Test Scenario A: Legitimate Server (Secure)

```bash
firefox --new-instance https://localhost:9443
```

Accept the self-signed certificate warning. This simulates a legitimate server.

### Test Scenario B: MITM Attack (Insecure)

```bash
firefox --new-instance https://localhost:8443
```

Accept the certificate warning. This simulates accepting a forged certificate.

The MITM proxy intercepts credentials even though the connection shows HTTPS.

## What This Demonstrates

**Attack 1 (HTTP)**: No encryption, credentials in plain text

**Attack 2 (MITM)**: HTTPS with fake certificate can decrypt traffic if user accepts invalid certificate

**Protection**: Always validate certificate authenticity, use certificate pinning, implement HSTS
