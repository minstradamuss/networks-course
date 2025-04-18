import socket
import time
from datetime import datetime

WINDOW_SIZE = 4
TIMEOUT = 3
PACKET_SIZE = 32

server_address = ('localhost', 12345)
log_file = open("C:\\Users\\User\\Source\\Repos\\networks-course\\lab10\\sender_log.txt", "w")

def log(msg):
    print(msg)
    log_file.write(f"{datetime.now()} - {msg}\n")

def print_sender_window(base, next_seq, total_packets):
    state = ""
    for i in range(total_packets):
        if i < base:
            state += f"[{i}:ACK] "
        elif base <= i < next_seq:
            state += f"[{i}:WAIT] "
        elif base <= i < base + WINDOW_SIZE:
            state += f"[{i}:READY] "
        else:
            state += f"[{i}] "
    log(f"Sender window: {state.strip()}")


def send_file(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT)

        with open(filename, 'rb') as f:
            data = f.read()

        total_packets = (len(data) + PACKET_SIZE - 1) // PACKET_SIZE
        base = 0
        next_seq = 0

        packets = []
        for i in range(total_packets):
            start = i * PACKET_SIZE
            end = start + PACKET_SIZE
            payload = data[start:end]
            packet = f"{i:04d}".encode() + payload
            packets.append(packet)

        while base < total_packets:
            while next_seq < base + WINDOW_SIZE and next_seq < total_packets:
                sock.sendto(packets[next_seq], server_address)
                log(f"Packet {next_seq} sent.")
                next_seq += 1

            print_sender_window(base, next_seq, total_packets)

            try:
                while True:
                    ack_data, _ = sock.recvfrom(1024)
                    ack_num = int(ack_data.decode())
                    log(f"ACK received for packet {ack_num}.")
                    if ack_num >= base:
                        base = ack_num + 1
                    if base == next_seq:
                        break
            except socket.timeout:
                log(f"Timeout occurred. Resending from packet {base}.")
                next_seq = base

        sock.sendto(b'DONE', server_address)
        log("File transfer complete.")
        log_file.close()

send_file('C:\\Users\\User\\Source\\Repos\\networks-course\\lab10\\data.txt')
