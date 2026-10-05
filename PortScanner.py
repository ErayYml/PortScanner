#!/usr/bin/env python3
"""
Basit Port Tarayıcı (TCP Connect Scan)
---------------------------------------
Eğitim amaçlı geliştirilmiştir. Sadece sahibi olduğunuz veya
tarama izniniz olan sistemler üzerinde kullanın.
"""

import socket
import threading
import queue
import argparse
import sys
import json
from datetime import datetime

# Yaygın portlar ve servis isimleri (basit bir eşleme)
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Alt",
}

print_lock = threading.Lock()
results = []


def grab_banner(sock):
    """Bağlantıdan basit bir banner (servis bilgisi) okumayı dener."""
    try:
        sock.settimeout(1)
        banner = sock.recv(1024).decode(errors="ignore").strip()
        return banner if banner else None
    except Exception:
        return None


def scan_port(target, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((target, port))
        if result == 0:
            service = COMMON_PORTS.get(port, "Bilinmiyor")
            banner = grab_banner(sock)
            entry = {
                "port": port,
                "service": service,
                "banner": banner,
            }
            with print_lock:
                banner_text = f" | Banner: {banner}" if banner else ""
                print(f"[+] Port {port:<6} AÇIK  | Servis: {service:<10}{banner_text}")
            results.append(entry)
    except Exception:
        pass
    finally:
        sock.close()


def worker(target, timeout, q):
    while not q.empty():
        try:
            port = q.get_nowait()
        except queue.Empty:
            return
        scan_port(target, port, timeout)
        q.task_done()


def parse_ports(port_arg):
    """'1-1000' veya '22,80,443' gibi girdileri port listesine çevirir."""
    ports = set()
    for part in port_arg.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Hedef çözümlenemedi: {target}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Basit Çok İş Parçacıklı Port Tarayıcı")
    parser.add_argument("target", help="Hedef IP adresi veya domain (örn: 192.168.1.1)")
    parser.add_argument(
        "-p", "--ports", default="1-1024",
        help="Taranacak portlar (örn: 1-1000 veya 22,80,443). Varsayılan: 1-1024"
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=100,
        help="Eş zamanlı thread sayısı (varsayılan: 100)"
    )
    parser.add_argument(
        "--timeout", type=float, default=0.5,
        help="Bağlantı zaman aşımı, saniye (varsayılan: 0.5)"
    )
    parser.add_argument(
        "-o", "--output", help="Sonuçları JSON dosyasına kaydet (örn: sonuc.json)"
    )
    args = parser.parse_args()

    ip = resolve_target(args.target)
    ports = parse_ports(args.ports)

    print(f"\nHedef: {args.target} ({ip})")
    print(f"Taranacak port sayısı: {len(ports)}")
    print(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("-" * 50)

    q = queue.Queue()
    for port in ports:
        q.put(port)

    threads = []
    for _ in range(min(args.threads, len(ports) or 1)):
        t = threading.Thread(target=worker, args=(ip, args.timeout, q))
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("-" * 50)
    print(f"Tarama tamamlandı. {len(results)} açık port bulundu.\n")

    if args.output:
        results_sorted = sorted(results, key=lambda r: r["port"])
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(
                {"target": args.target, "ip": ip, "open_ports": results_sorted},
                f, ensure_ascii=False, indent=2
            )
        print(f"Sonuçlar kaydedildi: {args.output}")


if __name__ == "__main__":
    main()
