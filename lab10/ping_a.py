import socket
import struct
import time
import select


def checksum(source_string):
    sum = 0
    max_count = (len(source_string) // 2) * 2
    count = 0

    while count < max_count:
        val = source_string[count + 1] * 256 + source_string[count]
        sum += val
        sum &= 0xffffffff
        count += 2

    if max_count < len(source_string):
        sum += source_string[len(source_string) - 1]
        sum &= 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum & 0xffff
    return answer >> 8 | (answer << 8 & 0xff00)


def create_packet(packet_id):
    header = struct.pack("bbHHh", 8, 0, 0, packet_id, 1)
    data = struct.pack("d", time.time())
    packet_checksum = checksum(header + data)
    header = struct.pack("bbHHh", 8, 0, socket.htons(packet_checksum), packet_id, 1)
    return header + data


def ping(dest_addr, timeout=1, count=4):
    icmp = socket.getprotobyname("icmp")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except PermissionError:
        raise Exception("Root privileges are required to send ICMP packets.")

    print(f"\n--- Pinging {dest_addr} ---")
    packet_id = int((id(timeout) * time.time()) % 65535)

    for i in range(count):
        packet = create_packet(packet_id)
        sock.sendto(packet, (dest_addr, 1))
        print(f"[{i+1}] ICMP Echo Request sent...")

        start = time.time()
        ready = select.select([sock], [], [], timeout)

        if ready[0]:
            rec_packet, addr = sock.recvfrom(1024)
            time_received = time.time()
            rtt = (time_received - start) * 1000
            print(f"    Reply from {addr[0]}: time = {rtt:.2f} ms")
        else:
            print("    Request timed out.")

        time.sleep(1)

    sock.close()


if __name__ == "__main__":
    hosts = ["google.com", "baidu.com"]

    for host in hosts:
        try:
            ip = socket.gethostbyname(host)
            print(f"\nHost: {host} -> IP: {ip}")
            ping(ip)
        except socket.gaierror:
            print(f"Could not resolve {host}.")
