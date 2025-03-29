import socket
import random
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 12345))

last_seq = 0
last_packet_time = time.time()
timeout_seconds = 5

print("UDP Heartbeat Server with simulated packet loss is running...")

try:
    while True:
        server_socket.settimeout(1.0)

        try:
            data, addr = server_socket.recvfrom(1024)
            recv_time = time.time()
            message = data.decode()
            seq_str, timestamp = message.split()
            seq = int(seq_str)

            if last_seq != 0 and seq > last_seq + 1:
                print(f'Warning: Lost {seq - last_seq - 1} packet(s)!')

            last_seq = seq
            last_packet_time = recv_time

            print(f'Received heartbeat seq={seq} sent at {timestamp}')

            if random.random() < 0.2:
                print("Simulated packet loss: not sending ACK")
                continue

            server_socket.sendto(f'ACK {seq}'.encode(), addr)

        except socket.timeout:
            if time.time() - last_packet_time > timeout_seconds:
                print("Client seems to be down! No heartbeat received.")
                last_packet_time = time.time()

except KeyboardInterrupt:
    print("Server stopped.")

finally:
    server_socket.close()
