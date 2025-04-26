import socket
import struct
import time
import select
import sys

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11

def calculate_checksum(source_string):
    count_to = (len(source_string) // 2) * 2
    checksum = 0
    for count in range(0, count_to, 2):
        this_val = source_string[count + 1] * 256 + source_string[count]
        checksum += this_val
        checksum &= 0xffffffff
    if count_to < len(source_string):
        checksum += source_string[len(source_string) - 1]
        checksum &= 0xffffffff
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    answer = ~checksum
    answer &= 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet(seq_number):
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, 0, 1, seq_number)
    data = struct.pack('d', time.time())
    my_checksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, my_checksum, 1, seq_number)
    return header + data

def send_and_receive(sock, dest_addr, ttl, timeout):
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    packet = build_packet(seq_number=ttl)
    start_time = time.time()
    sock.sendto(packet, (dest_addr, 1))

    ready = select.select([sock], [], [], timeout)
    if ready[0] == []:
        return None, None

    recv_packet, addr = sock.recvfrom(512)
    end_time = time.time()

    icmp_type, _, _, _, _ = struct.unpack('!BBHHH', recv_packet[20:28])

    if icmp_type == ICMP_TIME_EXCEEDED or icmp_type == ICMP_ECHO_REPLY:
        return addr[0], (end_time - start_time) * 1000
    else:
        return None, None

def traceroute(host, max_hops=30, probes_per_hop=3, timeout=1):
    try:
        dest_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Unable to resolve {host}")
        return

    print(f"Tracing route to {host} [{dest_ip}] with max {max_hops} hops:")

    for ttl in range(1, max_hops + 1):
        print(f"{ttl} ", end='')

        for probe in range(probes_per_hop):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            except socket.error as e:
                print(f"Socket error: {e}")
                return

            addr, rtt = send_and_receive(sock, dest_ip, ttl, timeout)
            sock.close()

            if addr:
                print(f"{addr} {rtt:.2f}ms", end=' ')
            else:
                print("*", end=' ')

        print()

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
