#!/usr/bin/env python3
import socket


def sniff_tls(port: int = 9443):
    """Listen for TLS packets on the given port and print encrypted payload bytes."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except PermissionError:
        print("Error: Run as root/sudo to capture packets")
        print("Usage: sudo python3 src/sniffer_https.py")
        return

    print(f"[TLS SNIFFER] Listening for HTTPS traffic on port {port}...")
    print("[TLS SNIFFER] Payloads will appear as encrypted bytes (unreadable without keys).\n")

    while True:
        packet, _ = sock.recvfrom(65565)

        ip_header = packet[0:20]
        iph_length = (ip_header[0] & 0xF) * 4

        tcp_header = packet[iph_length:iph_length + 20]
        tcph_length = ((tcp_header[12] >> 4) & 0xF) * 4

        src_port = int.from_bytes(tcp_header[0:2], "big")
        dst_port = int.from_bytes(tcp_header[2:4], "big")

        header_size = iph_length + tcph_length
        payload = packet[header_size:]

        if not payload:
            continue

        if port not in (src_port, dst_port):
            continue

        print("\n" + "=" * 60)
        print("[INTERCEPTED] TLS packet captured")
        print(f"Source port: {src_port} -> Dest port: {dst_port}")
        print(f"Payload length: {len(payload)} bytes")
        print("First 64 bytes (hex):")
        print(payload[:64].hex())
        print("[INFO] Content is encrypted; credentials are not readable from this capture.")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    sniff_tls()
