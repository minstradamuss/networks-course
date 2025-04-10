import socket
import psutil

def get_ip_address():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def get_netmask(ip):
    for interface in psutil.net_if_addrs().values():
        for addr in interface:
            if addr.family == socket.AF_INET and addr.address == ip:
                return addr.netmask
    return None

if __name__ == "__main__":
    ip = get_ip_address()
    netmask = get_netmask(ip)

    if ip and netmask:
        print(f"IP Address: {ip}")
        print(f"Subnet Mask: {netmask}")
    else:
        print("can't get information")