import socket
import struct
import time
import select
import sys

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11

def calculate_checksum(source_string):
    if len(source_string) % 2:
        source_string += b'\x00'
    checksum = sum(struct.unpack('!%dH' % (len(source_string) // 2), source_string))
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += checksum >> 16
    return (~checksum) & 0xffff

def create_packet(seq_number):
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, 0, seq_number)
    data = struct.pack('d', time.time())
    chksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, chksum, 0, seq_number)
    return header + data

def send_probe(sock, addr, ttl, timeout):
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    packet = create_packet(seq_number=ttl)
    sock.sendto(packet, (addr, 0))
    start = time.time()

    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        recv_packet, src_addr = sock.recvfrom(512)
        end = time.time()

        icmp_header = recv_packet[20:28]
        icmp_type, _, _, _, _ = struct.unpack('!BBHHH', icmp_header)

        if icmp_type in [ICMP_TIME_EXCEEDED, ICMP_ECHO_REPLY]:
            return src_addr[0], (end - start) * 1000
    return None, None

def traceroute(host, max_hops=30, probes_per_hop=3, timeout=1):
    try:
        dest_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Failed to resolve {host}")
        return

    print(f"Tracing route to {host} [{dest_ip}]:")

    for ttl in range(1, max_hops + 1):
        print(f"{ttl} ", end='')

        current_host = None
        rtts = []

        for _ in range(probes_per_hop):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            except socket.error as err:
                print(f"Error creating socket: {err}")
                return

            addr, rtt = send_probe(sock, dest_ip, ttl, timeout)
            sock.close()

            if addr:
                if not current_host:
                    try:
                        hostname = socket.gethostbyaddr(addr)[0]
                    except socket.herror:
                        hostname = addr
                    current_host = f"{hostname} [{addr}]"

                rtts.append(f"{rtt:.2f}ms")
            else:
                rtts.append("*")

        if current_host:
            print(f"{current_host} ", end='')

        print(' '.join(rtts))

        if addr == dest_ip:
            break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <host> [max_hops] [probes_per_hop] [timeout]")
        sys.exit(1)

    host = sys.argv[1]
    max_hops = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    probes = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 1

    traceroute(host, max_hops, probes, timeout)
