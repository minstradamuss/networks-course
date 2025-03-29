import socket
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 12345))

print("Server is running...")

while True:
    data, addr = server_socket.recvfrom(1024)
    if random.random() < 0.2:
        continue
    data = data.decode().upper()
    server_socket.sendto(data.encode(), addr)
