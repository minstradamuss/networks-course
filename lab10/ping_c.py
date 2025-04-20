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


def interpret_icmp_error(type_, code):
    if type_ == 3:
        if code == 0:
            return "Destination network unreachable"
        elif code == 1:
            return "Destination host unreachable"
        elif code == 2:
            return "Destination protocol unreachable"
        elif code == 3:
            return "Destination port unreachable"
        elif code == 6:
            return "Destination network unknown"
        elif code == 7:
            return "Destination host unknown"
        else:
            return f"Destination unreachable (code {code})"
    elif type_ == 11:
        return "Time exceeded"
    elif type_ == 12:
        return "Parameter problem"
    else:
        return f"ICMP error: type={type_}, code={code}"


def ping(dest_addr, timeout=1, count=4):
    icmp = socket.getprotobyname("icmp")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except PermissionError:
        raise Exception("Root privileges are required to send ICMP packets.")

    print(f"\nPING {dest_addr} ({dest_addr}): {count} packets")

    packet_id = int((id(timeout) * time.time()) % 65535)
    rtts = []
    packets_sent = 0
    packets_received = 0

    for i in range(count):
        packet = create_packet(packet_id)
        sock.sendto(packet, (dest_addr, 1))
        packets_sent += 1

        start = time.time()
        ready = select.select([sock], [], [], timeout)

        if ready[0]:
            rec_packet, addr = sock.recvfrom(1024)
            time_received = time.time()
            ip_header = rec_packet[:20]
            icmp_header = rec_packet[20:28]

            icmp_type, icmp_code, _, _, _ = struct.unpack("bbHHh", icmp_header)

            if icmp_type == 0:
                rtt = (time_received - start) * 1000
                rtts.append(rtt)
                packets_received += 1
                print(f"{len(rec_packet)} bytes from {addr[0]}: time={rtt:.2f} ms")
            else:
                error_msg = interpret_icmp_error(icmp_type, icmp_code)
                print(f"Error from {addr[0]}: {error_msg}")
        else:
            print("Request timed out.")

        time.sleep(1)

    sock.close()

    print("\n--- {} ping statistics ---".format(dest_addr))
    packet_loss = ((packets_sent - packets_received) / packets_sent) * 100

    if rtts:
        min_rtt = min(rtts)
        max_rtt = max(rtts)
        avg_rtt = sum(rtts) / len(rtts)
        print(f"{packets_sent} packets transmitted, {packets_received} received, {packet_loss:.1f}% packet loss")
        print(f"rtt min/avg/max = {min_rtt:.2f}/{avg_rtt:.2f}/{max_rtt:.2f} ms")
    else:
        print(f"{packets_sent} packets transmitted, 0 received, 100.0% packet loss")


if __name__ == "__main__":
    hosts = ["google.com", "baidu.com"]

    for host in hosts:
        try:
            ip = socket.gethostbyname(host)
            print(f"\nResolving {host}... IP: {ip}")
            ping(ip)
        except socket.gaierror:
            print(f"Could not resolve {host}.")
