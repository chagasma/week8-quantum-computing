#!/bin/bash

mkdir -p certs

echo "Generating legitimate certificate..."
openssl req -x509 -newkey rsa:2048 -keyout certs/legitimate_key.pem -out certs/legitimate_cert.pem -days 365 -nodes -subj "/CN=legitimate-bank.com"

echo "Generating fake certificate (MITM)..."
openssl req -x509 -newkey rsa:2048 -keyout certs/fake_key.pem -out certs/fake_cert.pem -days 365 -nodes -subj "/CN=legitimate-bank.com"

echo "Done. Certificates created in certs/ directory:"
echo "  - certs/legitimate_cert.pem / certs/legitimate_key.pem"
echo "  - certs/fake_cert.pem / certs/fake_key.pem"
