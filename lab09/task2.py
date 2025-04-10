import socket
import sys

def check_ports(ip, start, end):
    open_ports = []
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 3:
        print(f"Provided {len(args)} arguments, but at least 3 are required (IP address, start port, end port).")
        sys.exit(1)

    ip_address = args[0]
    start_port = int(args[1])
    end_port = int(args[2])

    print(f"Scanning {ip_address} from port {start_port} to {end_port}...")

    ports = check_ports(ip_address, start_port, end_port)

    if ports:
        print("Open ports found:", ports)
    else:
        print("No open ports detected in the given range.")
