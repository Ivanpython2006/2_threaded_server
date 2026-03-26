#!/usr/bin/env python3
"""
Многопоточный сканер портов
"""

import socket
import threading
import sys
import time
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port, timeout=1):
    """Сканирует один порт"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return port, True
    except:
        pass
    return port, False

def scan_host(host, ports, threads=100):
    """Сканирует хост на указанные порты"""
    print(f"Сканирование {host}...")
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, host, port) for port in ports]
        
        for future in futures:
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"Порт {port}: открыт")
    
    return open_ports

def main():
    if len(sys.argv) < 2:
        print("Использование: python scanner.py <хост> [порты]")
        print("Пример: python scanner.py localhost 1-1024")
        print("Пример: python scanner.py 192.168.1.1 80,443,8080")
        sys.exit(1)
    
    host = sys.argv[1]
    ports = []
    
    if len(sys.argv) >= 3:
        port_arg = sys.argv[2]
        if '-' in port_arg:
            start, end = map(int, port_arg.split('-'))
            ports = range(start, end + 1)
        elif ',' in port_arg:
            ports = [int(p) for p in port_arg.split(',')]
        else:
            ports = [int(port_arg)]
    else:
        ports = range(1, 1025)
    
    start_time = time.time()
    open_ports = scan_host(host, ports)
    end_time = time.time()
    
    print(f"\nОткрытые порты на {host}: {open_ports}")
    print(f"Время сканирования: {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    main()