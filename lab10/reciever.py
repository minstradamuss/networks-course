import socket
import random
from datetime import datetime

EXPECTED_PACKET = 0
PACKET_LOSS_PROB = 0.3

log_file = open("C:\\Users\\User\\Source\\Repos\\networks-course\\lab10\\receiver_log.txt", "w")

def log(msg):
    print(msg)
    log_file.write(f"{datetime.now()} - {msg}\n")

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(('localhost', 12345))
log("[Receiver] Waiting for incoming packets...")

with open('C:\\Users\\User\\Source\\Repos\\networks-course\\lab10\\received_output.txt', 'wb') as f:
    while True:
        packet, addr = receiver_socket.recvfrom(1024)
        if packet == b'DONE':
            log("[Receiver] File transfer complete.")
            break

        seq_num = int(packet[:4])
        data = packet[4:]

        if random.random() < PACKET_LOSS_PROB:
            log(f"[Receiver] Packet {seq_num} lost (simulated).")
            continue

        if seq_num == EXPECTED_PACKET:
            f.write(data)
            log(f"[Receiver] Received expected packet {seq_num}. Sending ACK {seq_num}.")
            EXPECTED_PACKET += 1
        else:
            log(f"[Receiver] Out-of-order packet {seq_num} received. Expected {EXPECTED_PACKET}. Sending ACK {EXPECTED_PACKET - 1}.")

        ack = str(EXPECTED_PACKET - 1).encode()
        receiver_socket.sendto(ack, addr)

log_file.close()
