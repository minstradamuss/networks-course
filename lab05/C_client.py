# -*- coding: utf-8 -*-

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

port = 12345
client.bind(("", port))

print(f"UDP Client слушает широковещательные сообщения на порту {port}...")

while True:
    data, addr = client.recvfrom(1024)
    print(f"Получено время от {addr}: {data.decode()}")
