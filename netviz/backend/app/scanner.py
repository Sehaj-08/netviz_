# backend/app/scanner.py

import os
import socket
import ipaddress
import time
import psutil
from ping3 import ping

# Try ARP scanning using scapy (requires npcap)
try:
    from scapy.all import ARP, Ether, srp, conf
    conf.verb = 0
    SCAPY_OK = True
except:
    SCAPY_OK = False


def detect_subnet():
    """Detect subnet like 192.168.1.0/24 or use NETVIZ_SUBNET env variable."""
    # If user manually specified subnet
    manual = os.environ.get("NETVIZ_SUBNET")
    if manual:
        return manual

    # Auto-detect from active interfaces
    addrs = psutil.net_if_addrs()
    for iface, info in addrs.items():
        for snic in info:
            if snic.family == socket.AF_INET:
                ip = snic.address
                mask = snic.netmask

                # ignore invalid or loopback
                if ip.startswith("127.") or ip.startswith("169.") or ip.startswith("0."):
                    continue

                try:
                    net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
                    return str(net)
                except:
                    pass

    return None


def ping_sweep(subnet):
    """Ping sweep fallback for Windows without npcap."""
    devices = []
    net = ipaddress.ip_network(subnet, strict=False)

    for ip in net.hosts():
        ip = str(ip)
        latency = ping(ip, timeout=1)
        if latency:
            devices.append({
                "ip": ip,
                "mac": None,
                "hostname": ip,
                "latency_ms": round(latency * 1000, 2),
                "last_seen": int(time.time())
            })
    return devices


def arp_scan(subnet):
    """Try ARP scan using scapy (if available)."""
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    pkt = ether / arp
    ans, _ = srp(pkt, timeout=2, inter=0.1)

    devices = []
    for _, r in ans:
        ip = r.psrc
        mac = r.hwsrc
        devices.append({
            "ip": ip,
            "mac": mac,
            "hostname": ip,
            "latency_ms": -1,
            "last_seen": int(time.time())
        })
    return devices


def scan_network():
    """Master function: detect subnet → ARP scan → fallback ping sweep."""
    subnet = detect_subnet()
    if not subnet:
        return []

    print(f"[Scanner] Scanning subnet: {subnet} (Scapy: {SCAPY_OK})")

    # If scapy is available (npcap installed), try ARP scan
    if SCAPY_OK:
        try:
            return arp_scan(subnet)
        except:
            pass

    # Otherwise fallback to ping sweep (always works)
    return ping_sweep(subnet)

if __name__ == "__main__":
    print(scan_network())
